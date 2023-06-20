from utils.collision import _3d_utils
import numpy as np
import math

class Vector3D:
    __slots__ = ["x", "y", "z"]

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"Vector3D(X={self.x}, Y={self.y}, Z={self.z})"

    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def to_numpy_array(self):
        return np.array([self.x, self.y, self.z])

    def distance(self, _vector_3d):
        return math.sqrt((self.x - _vector_3d.x)**2 + (self.y - _vector_3d.y)**2 + (self.z - _vector_3d.z)**2)

    def rotate(self, rotation):
        vector = self.to_numpy_array()
        rotation = rotation.to_numpy_array()
        rotated_vector = _3d_utils.rotate_numpy_vectors([vector], rotation)[0]

        self.x = rotated_vector[0]
        self.y = rotated_vector[1]
        self.z = rotated_vector[2]
