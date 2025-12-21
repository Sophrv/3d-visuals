import math


class Vector:
    def __init__(self, pos_vector: tuple[float, float, float]):
        self.x, self.y, self.z = pos_vector
        self.magnitude = math.hypot(self.x, self.y, self.z)
        # z goes up, y is to the left of +x, yaw going clockwise from +x, pitch from x-y plane to z
        # form of (yaw, pitch)
        self.direction = (
            math.degrees(math.atan2(self.y, self.x)),
            math.degrees(math.atan2(self.z, math.hypot(self.y, self.x)))
        )

    def return_pos(self):
        return self.x, self.y, self.z

    def __mul__(self, other: float):
        return Vector((self.x*other, self.y*other, self.z*other))

    def __add__(self, other: Vector):
        ox, oy, oz = other.x, other.y, other.z
        return Vector((self.x + ox, self.y + oy, self.z + oz))

    def __sub__(self, other: Vector):
        ox, oy, oz = other.x, other.y, other.z
        return Vector((self.x - ox, self.y - oy, self.z - oz))

    def get_angle(self, other: Vector):
        return -math.acos(math.sumprod(self.return_pos(), other.return_pos()) / (self.magnitude * other.magnitude))


class Camera:
    def __init__(self, position: Vector, looking_direction: Vector, fov: float):
        self.position = position
        self.looking_direction = looking_direction * (1/looking_direction.magnitude)
        self.upwards_angle = 0
        self.fov = fov
        horizonal_magnitude = math.hypot(looking_direction.x, looking_direction.y)
        self.upwards_vector = Vector((
            -1 * looking_direction.x * looking_direction.z / horizonal_magnitude,
            -1 * looking_direction.y * looking_direction.z / horizonal_magnitude,
            horizonal_magnitude
        ))

    def add_position(self, add_position: Vector):
        self.position += add_position

    def zoom(self, change_in_fov: float):
        self.fov += change_in_fov





class Segment:
    def __init__(self, point1: Vector, point2: Vector):
        self.points = (point1, point2)
        self.direction = Vector((
            point1.x - point2.x,
            point1.y - point2.y,
            point1.z - point2.z,
        ))

    def intersect_plane(self, equation: tuple[float, float, float, float]) -> Vector:
        # equation in form ax + by + cz = d
        a, b, c, d = equation
        numerator = d - math.sumprod(equation[:3], self.points[0].return_pos())
        denominator = math.sumprod(equation[:3], self.direction.return_pos())
        try:
            line_multiple = numerator / denominator
        except ZeroDivisionError:
            line_multiple = 0
        return self.points[0] + (self.direction * line_multiple)


    def project(self, camera: Camera) -> tuple[tuple[float, float], tuple[float, float]]:
        new_segments = (
            Segment(self.points[0], camera.position),
            Segment(self.points[1], camera.position)
        )
        center_of_view = camera.position + camera.looking_direction * camera.fov
        a, b, c = camera.looking_direction.return_pos()
        d = math.sumprod(camera.looking_direction.return_pos(), center_of_view.return_pos())
        points_to_be_viewed = [segment.intersect_plane((a, b, c, d)) for segment in new_segments]
        plane_vectors = [center_of_view - points_to_be_viewed[i] for i in range(2)]
        angles_to_up = [camera.upwards_vector.get_angle(vector) for vector in plane_vectors]
        solutions = (
            (plane_vectors[0].magnitude * math.sin(angles_to_up[0]),
             plane_vectors[0].magnitude * math.cos(angles_to_up[0])),
            (plane_vectors[1].magnitude * math.sin(angles_to_up[1]),
             plane_vectors[1].magnitude * math.cos(angles_to_up[1])),
        )
        return solutions








