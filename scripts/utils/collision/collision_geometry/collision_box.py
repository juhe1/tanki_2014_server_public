from panda3d.core import Vec3

from utils import panda_math

class CollisionBox:
    __slots__ = ["size", "position", "rotation"]

    def __init__(self, size, position, rotation):
        self.size = size / 2
        self.position = position
        self.rotation = rotation

    def generate_index_and_vertex_list(self):
        up_back_left_vertex = panda_math.rotate_vec3( Vec3(-self.size.x, self.size.y, -self.size.z), self.rotation) + self.position
        up_back_right_vertex = panda_math.rotate_vec3( Vec3(self.size.x, self.size.y, -self.size.z), self.rotation) + self.position
        down_back_left_vertex = panda_math.rotate_vec3( Vec3(-self.size.x, -self.size.y, -self.size.z), self.rotation) + self.position
        down_back_right_vertex = panda_math.rotate_vec3( Vec3(self.size.x, -self.size.y, -self.size.z), self.rotation) + self.position

        up_front_left_vertex = panda_math.rotate_vec3( Vec3(-self.size.x, self.size.y, self.size.z), self.rotation ) + self.position
        down_front_left_vertex = panda_math.rotate_vec3( Vec3(-self.size.x, -self.size.y, self.size.z), self.rotation) + self.position
        up_front_right_vertex = panda_math.rotate_vec3( Vec3(self.size.x, self.size.y, self.size.z), self.rotation) + self.position
        down_front_right_vertex = panda_math.rotate_vec3( Vec3(self.size.x, -self.size.y, self.size.z), self.rotation) + self.position

        index_list = [
            2,0,1,1,3,2,
            5,4,0,0,2,5,
            5,2,3,3,7,5,
            6,4,5,5,7,6,
            3,1,6,6,7,3,
            0,4,6,6,1,0
        ]

        vertex_list = [
            up_back_left_vertex,
            up_back_right_vertex,
            down_back_left_vertex,
            down_back_right_vertex,

            up_front_left_vertex,
            down_front_left_vertex,
            up_front_right_vertex,
            down_front_right_vertex
        ]

        return index_list, vertex_list
