from panda3d.core import Vec3

from utils import panda_math

class CollisionPlane:
    __slots__ = ["width", "length", "position", "rotation"]

    def __init__(self, width, length, position, rotation):
        self.width = width / 2
        self.length = length / 2
        self.position = position
        self.rotation = Vec3(rotation.x, rotation.y, rotation.z)

    def generate_index_and_vertex_list(self):
        up_left_vertex = panda_math.rotate_vec3(Vec3(-self.width, self.length, 0), self.rotation) + self.position
        up_right_vertex = panda_math.rotate_vec3(Vec3(self.width, self.length, 0), self.rotation) + self.position
        down_right_vertex = panda_math.rotate_vec3(Vec3(self.width, -self.length, 0), self.rotation) + self.position
        down_left_vertex = panda_math.rotate_vec3(Vec3(-self.width, -self.length, 0), self.rotation) + self.position

        index_list = [
            3, 2, 0,
            2, 1, 0
        ]

        vertex_list = [
            up_left_vertex,
            up_right_vertex,
            down_right_vertex,
            down_left_vertex
        ]

        return index_list, vertex_list
