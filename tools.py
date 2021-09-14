import math
import os

import pygame


def draw_image(surface, image, bounds):
    surface.blit(pygame.transform.smoothscale(image, bounds.size()), bounds.position())


def draw_ellipse(surface, color, center, x_radius, y_radius):
    ellipse_rect = (center.x - x_radius, center.y - y_radius, x_radius * 2, y_radius * 2)
    pygame.draw.ellipse(surface, color, ellipse_rect)


def load_animation(animation_path):

    def frame_num(file_name):
        frame_num = int("".join(filter(str.isdigit, file_name)))
        return frame_num

    file_path = animation_path[0]
    file_name = animation_path[1]

    files = []

    with os.scandir(file_path) as entries:
        for file in entries:
            if file_name in file.name:
                files.append(file.name)

    files.sort(key=frame_num)

    frames = []
    for file in files:
        frames.append(pygame.image.load(os.path.join(file_path, file)))
    return frames


def add_text_digit_padding(text, padding):
    if len(text) < padding:
        text = "0" * (padding - len(text)) + text
    return text


class CartesianObject:
    """
    Holds information about a geometric object on a cartesian grid and provides methods to interact with them

    ...

    Attributes:
    -----------
    x (int, float): The x coordinate of the cartesian object
    y (int, float): The y coordinate of the cartesian object

    Methods:
    --------
    def rotate(self, angle, axis):
        Rotates this cartesian object around an axis cartesian object

    def round(self):
        Rounds the coordinates of the cartesian object

    def translate(self, displacement):
        Translates the cartesian object with a displacement

    Static Methods:
    ---------------
    def distance(object1, object2):
        Returns the distance between two cartesian objects

    def rounded(point):
        Returns a rounded version of the cartesian object

    def rotated(cartesian_object, angle, axis):
        Returns a resultant cartesian object rotated around another cartesian object axis
    """

    def __init__(self, x, y):
        """
        Returns a cartesian object
        """
        self.x = x
        self.y = y

    def __str__(self):
        """
        Returns the string representation of the cartesian object

        Returns:
            string: The string representation
        """
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __repr__(self):
        """
        Returns the string representation of the coordinates

        Returns:
            string: The string representation
        """
        return self.__str__()

    def __hash__(self):
        """
        Returns the hash of the cartesian object

        Returns:
            int: The hash of the cartesian object
        """
        return hash((self.x, self.y))

    def __add__(self, other):
        """
        Returns the addition of this cartesian object and another cartesian object

        Parameters:
            other (CartesianObject): The other cartesian object

        Returns:
            CartesianObject: The addition of this cartesian object and another cartesian object
        """
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """
        Returns the subtraction of this cartesian object and another cartesian object

        Parameters:
            other (CartesianObject): The other cartesian object

        Returns:
            CartesianObject: The subtraction of this cartesian object and another cartesian object
        """
        return self.__class__(self.x - other.x, self.y - other.y)

    def __truediv__(self, value):
        """
        Returns this cartesian object divided by a scalar value

        Parameters:
            value (int, float): The scalar value to divide by

        Returns:
            Point: The cartesian object divided by a scalar value
        """
        return self.__class__(self.x / value, self.y / value)

    def __mul__(self, value):
        """
        Returns this cartesian object multiplied by a scalar value

        Parameters:
            value (int, float): The scalar value to multiply by

        Returns:
            Point: The cartesian object multiplied by a scalar value
        """
        return self.__class__(self.x * value, self.y * value)

    def __eq__(self, other):
        """
        Returns whether this cartesian object is equal to another cartesian object

        Parameters:
            other (CartesianObject): The other cartesian object to compare to

        Returns:
            bool: Whether this cartesian object is equal to another cartesian object
        """
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        """
        Returns whether this cartesian object is not equal to another one

        Parameters:
            other (CartesianObject): The other to cartesian object to compare to

        Returns:
            bool: Whether this cartesian object is not equal to another cartesian object
        """
        return not (self == other)

    def copy(self):
        return self.__class__(self.x, self.y)

    def rotate(self, angle, axis):
        """
        Rotates this cartesian object around an axis cartesian object

        Parameters:
            angle (int, float): The angle to rotate in degrees
            axis (CartesianObject): The cartesian object to rotate around
        """
        # Get rotated cartesian object
        result = CartesianObject.rotated(self, angle, axis)
        # Modify attributes to the result
        self.x = result.x
        self.y = result.y

    def round(self):
        """
        Rounds the coordinates of the cartesian object
        """
        self.x = int(round(self.x))
        self.y = int(round(self.y))

    def translate(self, displacement):
        """
        Translates the cartesian object with a displacement

        Parameters:
            displacement (CartesianObject): The displacement to translate the cartesian object with
        """
        self.x += displacement.x
        self.y += displacement.y

    @staticmethod
    def distance(object1, object2):
        """
        Returns the distance between two cartesian objects

        Parameters:
            object1 (CartesianObject): The first cartesian object
            object2 (CartesianObject): The second cartesian object

        Returns:
            int, float: The distance between the cartesian objects
        """
        return ((object2.x - object1.x) ** 2 + (object2.y - object1.y) ** 2) ** 0.5

    @staticmethod
    def rounded(point):
        """
        Returns a rounded version of the cartesian object

        Parameters:
            cartesian object (Point): The cartesian object to round

        Returns:
            Point: A rounded version of the cartesian object
        """
        return Point(int(round(point.x)), int(round(point.y)))

    @staticmethod
    def rotated(cartesian_object, angle, axis):
        """
        Returns a resultant cartesian object rotated around another cartesian object axis

        Parameters:
            cartesian_object (CartesianObject): The cartesian object to rotate
            angle (int, float): The angle to rotate in degrees
            axis (CartesianObject): The cartesian object to rotate around

        Returns:
            CartesianObject: The rotated cartesian object
        """
        # Calculate current angle
        current_angle = math.atan2(cartesian_object.x - axis.x, cartesian_object.y - axis.y)
        # Calculate target angle
        target_angle = math.radians(angle) + current_angle
        # Get the distance between axis and the cartesian object
        distance = CartesianObject.distance(cartesian_object, axis)
        # Create a cartesian object at target angle with distance from axis and return it
        return cartesian_object.__class__(math.sin(target_angle), math.cos(target_angle)) * distance + axis


class Point(CartesianObject):
    """
    Holds information about a geometric point on a cartesian grid and provides methods to interact with them

    ...

    Methods:
    --------
    def is_grid_collinear(self, other):
        Returns whether this point is collinear with another point on the cartesian grid lines

    def vector(self):
        Returns this point as a vector

    Static Methods:
    ---------------
    def left_most(points):
        Returns the left most lowest point in a set of points

    def get_neighbour_points(point):
        Returns the surrounding points of a point

    Parent (CartesianObject):
    """

    __doc__ += CartesianObject.__doc__

    def is_grid_collinear(self, other):
        """
        Returns whether this point is collinear with another point on the cartesian grid lines

        Parameters:
            other (Point): The other point to check

        Returns:
            bool: Whether this point is collinear with another point on the cartesian grid lines
        """
        return self.x == other.x or self.y == other.y

    def vector(self):
        """
        Returns this point as a vector

        Returns:
            Vector: The point as a vector object
        """
        return Vector(self.x, self.y)

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

    @staticmethod
    def get_neighbour_points(point):
        """
        Returns the surrounding points of a point

        Parameters:
            point (Point): The point to get surroundings of

        Returns:
            list: The list of surrounding point
        """
        points = []

        for x in range(3):
            for y in range(3):
                points.append(point + Point(x - 1, y - 1))
        points.remove(point)
        return points


class Vector(CartesianObject):
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

    def angular_position(self):
        Returns the angular position of the vector on a cartesian grid

    Static Methods:
    ---------------
    def angle(vector1, vector2):
        Returns the angle between two vectors

    CartesianObject (Point):
    """

    __doc__ += CartesianObject.__doc__

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
        magnitude = self.magnitude()
        if magnitude == 0:
            return Vector(0, 0)
        else:
            return self / magnitude

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

    def angular_position(self):
        """
        Returns the angular position of the vector on a cartesian grid

        Returns:
            float: The angular position of the vector
        """
        return math.degrees(math.atan2(self.x, self.y))

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
        return math.degrees(
            math.acos((vector1.x * vector2.x + vector1.y * vector2.y) / (vector1.magnitude() * vector2.magnitude())))


class Bounds(pygame.Rect):

    def size(self):
        return self.width, self.height

    def position(self):
        return self.x, self.y

    def point(self):
        return Point(self.x, self.y)

    def is_within(self, x, y):
        return self.left <= x <= self.right and self.top <= y <= self.bottom

    def aspect_ratio(self):
        return self.width / self.height


class BoundScale:

    def __init__(self, x_scale, y_scale, width_scale, height_scale):
        self.x = x_scale
        self.y = y_scale
        self.width = width_scale
        self.height = height_scale
