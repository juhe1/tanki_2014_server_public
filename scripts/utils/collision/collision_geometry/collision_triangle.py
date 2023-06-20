from utils import panda_math

class CollisionTriangle:
    __slots__ = ["vertices", "position", "rotation"]

    def __init__(self, vertices, position, rotation):
        self.vertices = vertices
        self.position = position
        self.rotation = rotation

    def generate_index_and_vertex_list(self):
        vertex0 = panda_math.rotate_vec3(self.vertices[0], self.rotation) + self.position
        vertex1 = panda_math.rotate_vec3(self.vertices[1], self.rotation) + self.position
        vertex2 = panda_math.rotate_vec3(self.vertices[2], self.rotation) + self.position

        index_list = [0,1,2]
        vertex_list = [vertex0, vertex1, vertex2]

        return index_list, vertex_list
