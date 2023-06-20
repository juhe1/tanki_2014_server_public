from panda3d.core import Geom, GeomTriangles, GeomVertexData, GeomVertexFormat, InternalName
from panda3d.core import GeomVertexWriter
from panda3d.bullet import BulletTriangleMesh, BulletTriangleMeshShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletWorld
from panda3d.core import Vec3, GeomNode, NodePath
from game import game
import gc

class CollisionGeometry:
    def __init__(self):
        self.collision_boxes = None
        self.collision_planes = None
        self.collision_triangles = None

        self.map = map
        self.physics_world = None

    def create_new_physics_word(self):
        self.physics_world = BulletWorld()
        self.physics_world.setGravity(Vec3(0, 0, -9.81))

        geometry = self.generate_geometry()
        self.create_map_rigidbody(geometry)
        self.create_collision_mesh_visualizer(geometry)
        game.add_physics_world(self.physics_world)

    def create_collision_mesh_visualizer(self, geometry):
        # Create a NodePath for the geometry
        node = GeomNode('triangle')
        node.addGeom(geometry)
        np = NodePath(node)
        np.reparentTo(game.worldNP)

    def create_map_rigidbody(self, geometry):
        bt = BulletTriangleMesh()
        bt.addGeom(geometry)

        rb = BulletRigidBodyNode('rb')
        rb.addShape(BulletTriangleMeshShape(bt, dynamic=True))
        np = NodePath(rb)
        np.reparentTo(game.worldNP)

        self.physics_world.attachRigidBody(np.node())

    def create_index_and_vertex_list(self):
        index_offset = 0
        index_list = []
        vertex_list = []

        def append_index_and_vertex_list(index_list_in, vertex_list_in):
            nonlocal vertex_list, index_list, index_offset
            vertex_list += vertex_list_in

            for index in index_list_in:
                index_list.append(index + index_offset)

            index_offset += len(vertex_list_in)

        for collision_box in self.collision_boxes:
            append_index_and_vertex_list(*collision_box.generate_index_and_vertex_list())

        for collision_plane in self.collision_planes:
            append_index_and_vertex_list(*collision_plane.generate_index_and_vertex_list())

        for collision_triangle in self.collision_triangles:
            append_index_and_vertex_list(*collision_triangle.generate_index_and_vertex_list())

        return index_list, vertex_list

    def generate_geometry(self):
        index_list, vertex_list = self.create_index_and_vertex_list()

        # Create the format of the vertex data
        format = GeomVertexFormat.getV3n3cpt2()

        # Create the vertex data
        vertexData = GeomVertexData("triangle", format, Geom.UHDynamic)

        vertexWriter = GeomVertexWriter(vertexData, 'vertex')
        for vertex in vertex_list:
            vertexWriter.addData3f(vertex)

        # Add the indices to the vertex data
        triangles = GeomTriangles(Geom.UHDynamic)
        for index in index_list:
            triangles.addVertex(index)

        # Create the geometry
        geometry = Geom(vertexData)
        geometry.addPrimitive(triangles)

        self.collision_boxes = None
        self.collision_planes = None
        self.collision_triangles = None
        gc.collect()

        return geometry
