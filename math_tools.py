import math


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __truediv__(self, value):
        return Point(self.x / value, self.y / value)

    def __mul__(self, value):
        return Point(self.x * value, self.y * value)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not (self == other)

    def is_collinear(self, other_point):
        return self.x == other_point.x or self.y == other_point.y

    def angle(self, other_point):
        return math.degrees(math.atan2(other_point.x - self.x, other_point.y - self.y))

    def distance(self, other_point):
        return ((other_point.x - self.x) ** 2 + (other_point.y - self.y) ** 2) ** 0.5

    @staticmethod
    def left_most(points):

        left_most_points = [points[0]]
        for point in points:
            if point.x < left_most_points[0].x:
                left_most_points.clear()
                left_most_points.append(point)
            elif point.x == left_most_points[0].x and point not in left_most_points:
                left_most_points.append(point)

        if len(left_most_points) > 1:
            result = left_most_points[0]
            for point in left_most_points:
                if point.y < result.y:
                    result = point
        else:
            result = left_most_points[0]

        return result


class Vector2(Point):

    def __init__(self, point):
        super().__init__(point.x, point.y)

    def __truediv__(self, value):
        return Vector2(super().__truediv__(value))

    def __mul__(self, value):
        return Vector2(super().__mul__(value))

    def magnitude(self):
        return self.distance(Point(0, 0))

    def normalised(self):
        return self / self.magnitude()

    def intersects_points(self, points, start=Point(0, 0)):

        for point in points:
            point -= start
            if 0 <= point.x <= self.x and 0 <= point.y <= self.y:
                if Vector2(point).normalised == self.normalised:
                    return True
