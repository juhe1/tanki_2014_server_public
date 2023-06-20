from panda3d.core import Mat3, Vec3, LMatrix3f, LVector3f
import math

def rotate_vector_with_node(vector, np):
    mat3 = Mat3()
    np.getQuat().extractToMatrix(mat3)
    return mat3.xform(vector)

def inverse_rotate_vector_with_node(vector, np):
    mat3 = Mat3()
    np.getQuat().extractToMatrix(mat3)
    mat3.invertInPlace()
    return mat3.xform(vector)

def extract_direction_from_vector(vector, normal):
    return vector.project(normal)

def remove_direction_from_vector(vector, normal):
    return vector - extract_direction_from_vector(vector, normal)

def rotate_vec3(position, rotation, radian=True):
    if radian:
        rotation = rotation * 180 / math.pi

    x_angle, y_angle, z_angle = rotation.getX(), rotation.getY(), rotation.getZ()
    x_rot = Mat3().rotateMat(x_angle, Vec3(1, 0, 0))
    y_rot = Mat3().rotateMat(y_angle, Vec3(0, 1, 0))
    z_rot = Mat3().rotateMat(z_angle, Vec3(0, 0, 1))
    rotation_matrix = x_rot * y_rot * z_rot
    rotated_position = rotation_matrix.xform(position)
    return rotated_position
