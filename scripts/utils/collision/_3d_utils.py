import numpy as np
from utils import panda_math
from game import game
from panda3d.core import Vec3

def point_inside_box_check(box_rotation, box_position, half_box_size, point_pos):
    point_pos = point_pos - box_position
    point_pos_rotated = panda_math.rotate_vec3(point_pos, -box_rotation)

    return point_pos_rotated.x < half_box_size.x and point_pos_rotated.x > -half_box_size.x and point_pos_rotated.y < half_box_size.y and point_pos_rotated.y > -half_box_size.y and point_pos_rotated.z < half_box_size.z and point_pos_rotated.z > -half_box_size.z
