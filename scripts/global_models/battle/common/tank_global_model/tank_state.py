from panda3d.core import Vec3
import enum

class TankState:
    def __init__(self):
        self.angular_velocity = Vec3()
        self.chassis_control = 0
        self.linear_velocity = Vec3()
        self.orientation = Vec3()
        self.position = Vec3(0,10000,-1000)
        self.turret_angle = 0.0
        self.turret_control = 0


class LogicStateEnum(enum.Enum):
    OUT_OF_GAME = 1
    ACTIVATING = 2
    ACTIVE = 3
    DEAD = 4


class LogicState:
    def __init__(self):
        self.state = LogicStateEnum.OUT_OF_GAME
