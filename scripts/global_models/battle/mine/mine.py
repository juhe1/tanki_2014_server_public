from panda3d.core import Vec3

class Mine:
    def __init__(self):
        self.activated = False
        self.mine_id = 0
        self.owner_id = 0
        self.position = Vec3()
