import pygame
import math


class GUITools:

    @staticmethod
    def draw_text(text, screen, pos, font, size, colour):
        font = pygame.font.SysFont(font, size)

        text = font.render(text, False, colour)
        text_size = text.get_size()

        pos[0] = pos[0] - text_size[0] // 2
        pos[1] = pos[1] - text_size[1] // 2

        screen.blit(text, pos)


class Point:
    """
    Holds information about a point on a cartesian grid and provides methods to interact with points
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        """
        Returns the string representation of the point as coordinates

        Returns:
            string: The string representation of the point
        """
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __repr__(self):
        """
        Returns the string representation of the point as coordinates

        Returns:
            string: The string representation of the point
        """
        return self.__str__()

    def __hash__(self):
        """
        Returns the hash of the point

        Returns:
            int: The hash of the point
        """
        return hash((self.x, self.y))

    def __add__(self, other):
        """
        Returns the addition of this point and another point

        Parameters:
            other (Point): The other point

        Returns:
            Point: The addition of this point and another point
        """
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """
        Returns the subtraction of this point and another point

        Parameters:
            other (Point): The other point

        Returns:
            Point: The subtraction of this point and another point
        """
        return Point(self.x - other.x, self.y - other.y)

    def __truediv__(self, value):
        """
        Returns this point divided by a scalar value

        Parameters:
            value (int, float): The scalar value to divide by

        Returns:
            Point: The point divided by a scalar value
        """
        return Point(self.x / value, self.y / value)

    def __mul__(self, value):
        """
        Returns this point multiplied by a scalar value

        Parameters:
            value (int, float): The scalar value to multiply by

        Returns:
            Point: The point multiplied by a scalar value
        """
        return Point(self.x * value, self.y * value)

    def __eq__(self, other):
        """
        Returns whether this point is equal to another point

        Parameters:
            other (Point): The other to point to compare to

        Returns:
            bool: Whether this point is equal to another point
        """
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        """
        Returns whether this point is not equal to another point

        Parameters:
            other (Point): The other to point to compare to

        Returns:
            bool: Whether this point is not equal to another point
        """
        return not (self == other)

    def is_grid_collinear(self, other):
        """
        Returns whether this point is collinear with another point on the cartesian grid lines

        Parameters:
            other (Point): The other point to check

        Returns:
            bool: Whether this point is collinear with another point on the cartesian grid lines
        """
        return self.x == other.x or self.y == other.y

    @staticmethod
    def distance(point1, point2):
        """
        Returns the distance between two points

        Parameters:
            point1 (Point): The first point
            point2 (Point): The second point

        Returns:
            int, float: The distance between the points
        """
        return ((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2) ** 0.5

    def rotate(self, angle, axis):
        """
        Rotates this point around an axis point

        Parameters:
            angle (int, float): The angle to rotate in degrees
            axis (Point): The point to rotate around
        """
        # Get rotated point
        result = Point.rotate_point(self, angle, axis)
        # Modify attributes to the result
        self.x = result.x
        self.y = result.y

    def round(self):
        """
        Rounds the coordinates of the point
        """
        self.x = int(round(self.x))
        self.y = int(round(self.y))

    def translate(self, displacement):
        """
        Translates the point with a displacement

        Parameters:
            displacement (Point, Vector): The displacement to translate the point with
        """
        self.x += displacement.x
        self.y += displacement.y

    def vector(self):
        """
        Returns this point as a vector

        Returns:
            Vector: The point as a vector object
        """
        return Vector(self.x, self.y)

    @staticmethod
    def rotate_point(point, angle, axis):
        """
        Returns a resultant point rotated around another point axis

        Parameters:
            point (Point): The point to rotate
            angle (int, float): The angle to rotate in degrees
            axis (Point): The point to rotate around

        Returns:
            Point: The rotated point
        """
        # Calculate current angle
        current_angle = math.atan2(point.x - axis.x, point.y - axis.y)
        # Calculate target angle
        target_angle = math.radians(angle) + current_angle
        # Get the distance between axis and the point
        distance = Point.distance(point, axis)
        # Create a point at target angle with distance from axis and return it
        return Point(math.sin(target_angle), math.cos(target_angle)) * distance + axis

    @staticmethod
    def left_most(points):

        """
        Returns the left most lowest point in a set of points

        Parameters:
            points (list): The set of points to search through

        Returns:
            Point: The left most lowest point in the set of points
        """

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


class Vector(Point):

    """
    Stores information about a vector and provides methods to interact with vectors

    ...

    Methods:
    --------
    def magnitude(self):
        Returns the magnitude of the vector

    def normalised(self):
        Returns a normalized vector in the same direction

    def intersects_points(self, points, start=Point(0, 0)):
        Returns whether the vector intersects any point

    @staticmethod
    def angle(vector1, vector2):
        Returns the angle between two vectors

    Parent (Point):
    """

    __doc__ += Point.__doc__

    def __add__(self, other):
        """
        Returns the addition of this vector and another vector

        Parameters:
            other (Vector): The other vector

        Returns:
            Vector: The addition of this vector and another vector
        """
        return super().__add__(other).vector()

    def __sub__(self, other):
        """
        Returns the subtraction of this vector and another vector

        Parameters:
            other (Vector): The other vector

        Returns:
            Vector: The subtraction of this vector and another vector
        """
        return super().__add__(other).vector()

    def __truediv__(self, value):
        """
        Returns this vector divided by a scalar value

        Parameters:
            value (int, float): The scalar value to divide by

        Returns:
            Vector: The vector divided by a scalar value
        """
        return super().__truediv__(value).vector()

    def __mul__(self, value):
        """
        Returns this vector multiplied by a scalar value

        Parameters:
            value (int, float): The scalar value to multiply by

        Returns:
            Vector: The vector multiplied by a scalar value
        """
        return super().__mul__(value).vector()

    def magnitude(self):
        """
        Returns the magnitude of the vector

        Returns:
            int, float: The magnitude of the vector
        """
        return self.distance(Point(0, 0), self)

    def normalised(self):
        """
        Returns a normalized vector in the same direction

        Returns:
            Vector: The normalized vector in the same direction
        """
        return self / self.magnitude()

    def intersects_points(self, points, start=Point(0, 0)):
        """
        Returns whether the vector intersects any point

        Parameters:
            points (list): The set of points to check
            start (Point): The base point coordinate of the vector (Default: Point(0,0))
        """
        # For all the points
        for point in points:
            # Move them relative to vector by subtracting the start coordinate
            point -= start
            # If the point is within the vector bounds
            if 0 <= point.x <= self.x and 0 <= point.y <= self.y:
                # If both the vector normalised and the point vector normalized equal each other
                if point.vector().normalised == self.normalised:
                    # Then the vector intersects the point so return True
                    return True
        # If not returned by here, then no intersections were detected so return False
        return False

    @staticmethod
    def angle(vector1, vector2):
        """
        Returns the angle between two vectors

        parameters:
            vector1 (Vector): The first vector
            vector2 (Vector): The second vector

        Returns:
            int, float: The angle between the vectors
        """
        return math.degrees(math.atan2(vector2.x - vector1.x, vector2.y - vector1.y))
