import server_properties
import sys

if server_properties.DEBUG_ENABLED:
    import direct.directbase.DirectStart

from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState
from direct.showbase.ShowBase import NodePath

from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import Point3
from panda3d.core import TransformState
from panda3d.core import BitMask32
from panda3d.core import WindowProperties
from panda3d.core import LineSegs
from panda3d.core import NodePath

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletConeShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import ZUp
from pandac.PandaModules import PStatClient

from utils import color

#PStatClient.connect()

CAMERA_MOVE_SPEED = 25

class FreeCameraController:
    def __init__(self, camera, game):
        self.camera = camera
        self.camera.setPos(0,0,20000)

        # disable original camera control
        base.disableMouse()

        # lock mouse
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)
        self.mouse_lock = False
        game.accept('x', self.togle_mouse_lock)

        self.mouse_x = 0
        self.mouse_y = 0

        self.register_watch_modifiers()
        base.taskMgr.add(self.mouse_look_task, "MouseLookTask")
        base.taskMgr.add(self.camera_movement, "camera_movement_task")

    def togle_mouse_lock(self):
        self.mouse_lock = not self.mouse_lock

    def register_watch_modifiers(self):
        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('left', 'a')
        inputState.watchWithModifiers('reverse', 's')
        inputState.watchWithModifiers('right', 'd')
        inputState.watchWithModifiers('turnLeft', 'q')
        inputState.watchWithModifiers('turnRight', 'e')

    def mouse_look_task(self, task):
        if not self.mouse_lock: return task.cont

        if(base.mouseWatcherNode.hasMouse() == True):
            mpos = base.mouseWatcherNode.getMouse()
            self.camera.setH((self.mouse_x + mpos.getX()) * -50)
            self.camera.setP((self.mouse_y + mpos.getY()) * 50)

            if abs(mpos.getX()) > 0.3 or abs(mpos.getY()) > 0.3:
                self.mouse_x += mpos.getX()
                self.mouse_y += mpos.getY()

                # move to center
                mouse_x = base.win.get_x_size() / 2
                mouse_y = base.win.get_y_size() / 2
                base.win.move_pointer(0, int(mouse_x), int(mouse_y))

        return task.cont

    def camera_movement(self, task):
        # Get the camera position
        cam_pos = self.camera.getPos()

        # Move the camera based on the key status
        if inputState.isSet('forward'):
            direction = Vec3(0, CAMERA_MOVE_SPEED, 0)
            cam_pos += self.camera.getMat().xformVec(direction)
        if inputState.isSet('left'):
            direction = Vec3(-CAMERA_MOVE_SPEED, 0, 0)
            cam_pos += self.camera.getMat().xformVec(direction)
        if inputState.isSet('reverse'):
            direction = Vec3(0, -CAMERA_MOVE_SPEED, 0)
            cam_pos += self.camera.getMat().xformVec(direction)
        if inputState.isSet('right'):
            direction = Vec3(CAMERA_MOVE_SPEED, 0, 0)
            cam_pos += self.camera.getMat().xformVec(direction)

        # Set the camera position
        self.camera.setPos(cam_pos)

        return task.cont


class Game(DirectObject):

    def __init__(self):
        global update_registry
        update_registry = UpdateRegistry()

        if server_properties.DEBUG_ENABLED:
            taskMgr.add(update_registry.update, 'updateWorld')

            base.setBackgroundColor(*color.hex_color_to_rgb(0xe7feff))
            base.setFrameRateMeter(True)

            # create free camera controller
            base.cam.setPos(0, 0, 100)
            base.cam.lookAt(0, 0, -1)
            FreeCameraController(base.cam, self)

            # Light
            alight = AmbientLight('ambientLight')
            alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
            alightNP = render.attachNewNode(alight)

            dlight = DirectionalLight('directionalLight')
            dlight.setDirection(Vec3(1, 1, -1))
            dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
            dlightNP = render.attachNewNode(dlight)

            render.clearLight()
            render.setLight(alightNP)
            render.setLight(dlightNP)

            self.toggleWireframe()

            # Physics
            self.setup()

            self.line = None
            self.create_debug_line()
        else:
            self.worldNP = NodePath("word_np")

        # Input
        self.accept('escape', self.doExit)
        self.accept('r', self.doReset)
        self.accept('f1', self.toggleWireframe)
        self.accept('f2', self.toggleTexture)
        self.accept('f3', self.toggleDebug)
        self.accept('f5', self.doScreenshot)

        update_registry.add_listenner(self.update)

        self.physics_worlds = []

    def create_debug_line(self):
        self.line = LineSegs()

        # Set the color of the line
        self.line.setColor(0, 0, 1, 1)

        # Add a segment to the line
        pos = Vec3(0,0,0)
        to = Vec3(0, 0, 0)
        self.line.moveTo(pos.x, pos.y, pos.z)
        self.line.drawTo(to.x, to.y, to.z)

        # Convert the line to a node
        node = self.line.create()

        self.line_node = NodePath(node)

        # Attach the node to the scene
        self.line_node.reparentTo(render)

    def move_debug_line(self, pos, to):
        if not server_properties.DEBUG_ENABLED: return

        self.line.moveTo(pos.x, pos.y, pos.z)
        self.line.drawTo(to.x, to.y, to.z)

        self.line_node.remove_node()
        node = self.line.create()
        self.line_node = NodePath(node)
        self.line_node.reparent_to(render)

    def add_physics_world(self, physics_world):
        self.physics_worlds.append(physics_world)

    def doExit(self):
        self.cleanup()
        sys.exit(1)

    def doReset(self):
        self.cleanup()
        self.setup()

    def toggleWireframe(self):
        base.toggleWireframe()

    def toggleTexture(self):
        base.toggleTexture()

    def toggleDebug(self):
        if self.debugNP.isHidden():
            self.debugNP.show()
        else:
            self.debugNP.hide()

    def doScreenshot(self):
        base.screenshot('Bullet')

    def update(self, dt):
        for physics_world in self.physics_worlds:
            physics_world.doPhysics(dt)

    def cleanup(self):
        self.world = None
        self.worldNP.removeNode()

    def setup(self):
        self.worldNP = render.attachNewNode('World')

        # World
        self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
        #self.debugNP.show()

class UpdateRegistry:
    def __init__(self):
        self.listenner_functions = []

    def add_listenner(self, function):
        self.listenner_functions.append(function)

    def remove_listenner(self, function):
        self.listenner_functions.remove(function)

    def update(self, task):
        dt = globalClock.getDt()

        for listenner_function in self.listenner_functions:
            listenner_function(dt)

        return task.cont


update_registry = None
game = Game()
