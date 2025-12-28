import math

"""
This is my personal library for vector and matrix maths to 
allow 3d graphics to be processed. 

Version 0.1

By Kalinda Y


Directions are as follows:
x is forwards
y is left
z is up
"""

class Vector:
    def __init__(self, position_vector: tuple[float, float, float]):
        self.x, self.y, self.z = position_vector
        self.rotation_x = 0
        self.rotation_y = 0
        self.rotation_z = 0
        self.magnitude = math.hypot(self.x, self.y, self.z)

    def __add__(self, other: Vector) -> Vector:
        return Vector((
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        ))

    def __sub__(self, other: Vector) -> Vector:
        return Vector((
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        ))

    def get_pos(self):
        return self.x, self.y, self.z

    def matrix_multiply(self, other: Matrix) -> Vector:
        return Vector((
            math.sumprod(self.get_pos(), other.contents[0]),
            math.sumprod(self.get_pos(), other.contents[1]),
            math.sumprod(self.get_pos(), other.contents[2]),
        ))


class Matrix:
    def __init__(self, contents: tuple[tuple[float, float, float],
                                       tuple[float, float, float],
                                       tuple[float, float, float]]):
        self.contents = contents
        self.determinant = (contents[0][0]*(contents[1][1]*contents[2][2]-contents[2][1]*contents[1][2]) -
                            contents[1][0]*(contents[0][1]*contents[2][2]-contents[2][1]*contents[0][2]) +
                            contents[2][0]*(contents[0][1]*contents[1][2]-contents[1][1]*contents[0][2]))

    # noinspection PyTypeChecker
    def __mul__(self, other: float) -> Matrix:
        return Matrix(tuple([tuple([self.contents[row][column]*other for column in range(3)]) for row in range(3)]))

    def __str__(self):
        return (f"| {self.contents[0][0]:.3f} {self.contents[0][1]:.3f} {self.contents[0][2]:.3f} |\n"
                f"| {self.contents[1][0]:.3f} {self.contents[1][1]:.3f} {self.contents[1][2]:.3f} |\n"
                f"| {self.contents[2][0]:.3f} {self.contents[2][1]:.3f} {self.contents[2][2]:.3f} |")

    # noinspection PyTypeChecker
    def left_multiply(self, other: Matrix) -> Matrix:
        # new matrix is on the left
        return Matrix(tuple([tuple([
            math.sumprod(other.contents[k], [self.contents[j][i] for j in range(3)])
            for i in range(3)]) for k in range(3)]))

class Camera:
    def __init__(self, position: Vector, yaw: float, pitch: float, fov: float):
        self.position = position
        self.yaw = yaw
        self.pitch = pitch
        self.fov = fov
        self.facing = Vector((1, 0, 0))
        self.upwards = Vector((0, 0, 1))

        self.turn_vertical(pitch)
        self.turn_horizonal(yaw)

    def turn_horizonal(self, degrees):
        self.facing.matrix_multiply(rotation_matrix_z(degrees))
        self.upwards.matrix_multiply(rotation_matrix_z(degrees))
        self.yaw += degrees

    def turn_vertical(self, degrees):
        self.facing.matrix_multiply(rotation_matrix_z(-self.yaw))
        self.facing.matrix_multiply(rotation_matrix_y(degrees))
        self.facing.matrix_multiply(rotation_matrix_z(self.yaw))
        self.upwards.matrix_multiply(rotation_matrix_z(-self.yaw))
        self.upwards.matrix_multiply(rotation_matrix_y(degrees))
        self.upwards.matrix_multiply(rotation_matrix_z(self.yaw))
        self.pitch += degrees

    def add_position(self, vector: Vector):
        self.position += vector

    def zoom(self, num: float):
        self.fov += num


class Segment(Vector):
    def __init__(self, point1: Vector, point2: Vector):
        super().__init__((point1-point2).get_pos())
        self.points = (point1, point2)

    def project(self, cam: Camera):
        solution = []
        for point in self.points:
            difference_vector = point - cam.position
            distance_to_cam = dot(cam.facing, difference_vector)
            projection_distance = math.hypot(difference_vector.magnitude, distance_to_cam) * cam.fov / distance_to_cam
            projection_angle = math.atan2(dot(cam.facing, cross(cam.upwards, difference_vector)), dot(cam.upwards, difference_vector))
            projection_x = projection_distance*math.sin(projection_angle)
            projection_y = projection_distance*math.cos(projection_angle)
            solution.append((projection_x, projection_y))

        return tuple(solution)


def dot(vct1: Vector, vct2: Vector) -> float:
    return math.sumprod(vct1.get_pos(), vct2.get_pos())

def cross(vct1: Vector, vct2: Vector) -> Vector:
    return Vector((
        vct1.y * vct2.z - vct2.y * vct1.z,
        vct2.x * vct1.z - vct1.x * vct2.z,
        vct1.x * vct2.y - vct2.x * vct1.y
    ))

def rotation_matrix_x(degrees):
    return Matrix((
        (1, 0, 0),
        (0, math.cos(degrees), -math.sin(degrees)),
        (0, math.sin(degrees), math.cos(degrees))
    ))

def rotation_matrix_y(degrees):
    return Matrix((
        (math.cos(degrees), 0, math.sin(degrees)),
        (0, 1, 0),
        (-math.sin(degrees), 0, math.cos(degrees))
    ))

def rotation_matrix_z(degrees):
    return Matrix((
        (math.cos(degrees), -math.sin(degrees), 0),
        (math.sin(degrees), math.cos(degrees), 0),
        (0, 0, 1)
    ))

