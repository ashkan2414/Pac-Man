import random, os, pickle
from copy import deepcopy
from settings import *
from tools import *


def generate_maze():
    """
    Generates and returns a pac-man maze

    Returns:
        list: A generated maze
    """
    # Create empty 2D list to store maze
    maze = [[MazeBlockType.EMPTY for y in range((HEIGHT_TILE_COUNT + 1) * BLOCK_DIVISION)] for x in
            range(int((WIDTH_TILE_COUNT // 2 + 1.5) * BLOCK_DIVISION))]

    # Get the maze pieces
    pieces = generate_pieces(WIDTH_TILE_COUNT // 2 + 1, HEIGHT_TILE_COUNT)

    for piece in pieces:
        if piece.is_edge_piece():
            piece.outer_wall = True
            break

    # Insert each piece into maze
    for piece in pieces:
        piece.generate_map(maze)

    # Mirror the maze
    for x in range(len(maze) - 1, -1, -1):
        maze.append(maze[x])

    # Return the generated maze
    return maze


def generate_pieces(width, height):
    """
    Generates and returns maze pieces that fit together

    Parameters:
        width (int): The width of the maze in tiles
        height (int): The height of the maze in tiles

    Returns:
        list: The list of maze pieces
    """

    # Create a list of points for each tile
    unoccupied_tiles = [Point(x, y) for x in range(width) for y in range(height)]
    # Empty list to hold the maze pieces
    maze_pieces = []

    center_piece = MazePiece([Point(3, 3), Point(3, 4), Point(4, 3), Point(4, 4)])
    for point in center_piece.center_points:
        unoccupied_tiles.remove(point)

    # Generate a list of all possible piece presets
    piece_presets = generate_piece_presets()

    # Shuffle the presets and put the default 1 square preset shape at the end to reduce frequency
    default_preset = piece_presets[0]
    piece_presets.remove(default_preset)
    random.shuffle(piece_presets)
    piece_presets.append(default_preset)

    # While there are still unoccupied_tiles
    while unoccupied_tiles:

        # Choose a random tile
        current_tile_point = random.choice(unoccupied_tiles)
        # For every preset
        for preset in piece_presets:
            fits = True
            # Try putting the preset on the current tile with every single tile in the preset
            for center_point in preset.center_points:
                # Calculate displacement from selected point to current tile point
                displacement = current_tile_point - center_point
                # Deep copy the preset so it doesn't get modified when we translate it
                copied_preset = deepcopy(preset)
                # Translate the preset to the start point
                copied_preset.translate(displacement)

                fits = True
                # For each point in the center points
                for point in copied_preset.center_points:
                    # If the point is out of bounds or is not occupied
                    if point.x > width - 1 or point.x < 0 or point.y > height - 1 or point.y < 0 or point not in unoccupied_tiles:
                        # Set fits to false and break
                        fits = False
                        break

                # If the preset fits
                if fits:
                    # Add the preset to list of pieces and remove the occupied tiles from unoccupied list
                    for point in copied_preset.center_points:
                        if point in unoccupied_tiles:
                            unoccupied_tiles.remove(point)
                    maze_pieces.append(copied_preset)
                    break

            # If the preset fits, choose another random tile
            if fits:
                break

    # Return the generated pieces
    return maze_pieces


def generate_piece_presets():
    """
    Generates and returns a list of maze piece presets

    Returns:
        list: The list of maze piece presets
    """
    # Direction to vector translate dictionary
    direction_vector_map = {"L": Vector(-1, 0), "R": Vector(1, 0), "U": Vector(0, 1), "D": Vector(0, -1)}

    # Empty list to store the resulting presets
    piece_presets = []

    if os.path.exists(PIECE_PRESETS_FILE_PATH):
        file = open(PIECE_PRESETS_FILE_PATH, "rb")
        piece_presets = pickle.load(file)

    else:
        # For all the point paths in the shape presets
        for paths in maze_piece_shape_presets:
            points = {Point(0, 0)}  # List stores all the points for this piece shape preset
            # For every path in the paths
            for path in paths:
                # Start at origin
                point = Point(0, 0)
                # For each direction in the path
                for direction in path:
                    # Add on the vector representation of the direction to the current point
                    point += direction_vector_map.get(direction)
                # Add the point to the list of points for this piece shape preset
                points.add(point)

            # Cycle through each rotation and generate all possible pieces for the shape preset
            # i represents the number of 90 degree rotations applied
            for i in range(4):
                # Create a MazePiece object with the points
                # Use deepcopy so that the pieces don't modify each others' points
                piece_preset = MazePiece(deepcopy(list(points)))
                # Rotate it around the current point with the current angle
                piece_preset.rotate(i * 90, Point(0, 0))
                # Add it to the list of piece presets if its not already in the list
                if piece_preset not in piece_presets:
                    piece_presets.append(piece_preset)

        file = open(PIECE_PRESETS_FILE_PATH, "wb")
        pickle.dump(piece_presets, file)
        file.close()

    # Return all the piece presets
    return piece_presets


def get_surrounding_blocks(point):
    """
    Returns the surrounding blocks of a point

    Parameters:
        point (Point): The point to get surroundings of

    Returns:
        list: The list of surrounding blocks
    """
    points = []

    for x in range(3):
        for y in range(3):
            points.append(point + Point(x - 1, y - 1))
    return points


class MazeBlockType:
    EMPTY = 0
    WALL = 1
    PATH = 2


class MazePiece:

    def __init__(self, points):
        self.center_points = points
        self.divided_center_points = []
        self.vertices = []
        self.outer_wall = False

    def __str__(self):
        return str(self.center_points)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.center_points == other.center_points

    def __hash__(self):
        return hash(tuple(self.center_points))

    def rotate(self, angle, axis):

        for point in self.center_points:
            point.rotate(angle, axis)
            point.round()

    def translate(self, displacement):

        for point in self.center_points:
            point.translate(displacement)
            point.round()

    def calculate_vertices(self):

        unsorted_vertices = []
        for point in self.center_points:
            half_block = BLOCK_DIVISION // 2
            divided_point = point * BLOCK_DIVISION + Point(half_block, half_block)
            self.divided_center_points.append(divided_point)
            unsorted_vertices.append(divided_point + Point(half_block + 1, half_block + 1))
            unsorted_vertices.append(divided_point + Point(half_block + 1, -half_block))
            unsorted_vertices.append(divided_point + Point(-half_block, half_block + 1))
            unsorted_vertices.append(divided_point + Point(-half_block, -half_block))

        for vertex in unsorted_vertices.copy():

            count = unsorted_vertices.count(vertex)
            if count == 4:
                num_to_remove = 4
            else:
                num_to_remove = count - 1
            for i in range(num_to_remove):
                unsorted_vertices.remove(vertex)

        current_vertex = Point.left_most(unsorted_vertices)
        unsorted_vertices.remove(current_vertex)
        self.vertices = [current_vertex]

        while unsorted_vertices:
            next_vertex = [Point(1000, 1000), -1000]
            for vertex in unsorted_vertices:
                angle = Vector.angle(current_vertex.vector(), vertex.vector())
                if current_vertex.is_grid_collinear(vertex):
                    if len(self.vertices) < 2 or not (vertex - current_vertex).vector().intersects_points(
                            self.vertices[:-1], current_vertex):
                        if angle > next_vertex[1]:
                            next_vertex = [vertex, angle]
                        elif angle == next_vertex[1]:
                            if Point.distance(current_vertex, vertex) < Point.distance(current_vertex, next_vertex[0]):
                                next_vertex = [vertex, angle]

            current_vertex = next_vertex[0]
            unsorted_vertices.remove(next_vertex[0])
            self.vertices.append(next_vertex[0])

    def generate_map(self, maze):

        self.calculate_vertices()

        if not self.outer_wall:
            for center_point in self.divided_center_points:
                for x in range(BLOCK_DIVISION):
                    for y in range(BLOCK_DIVISION):
                        point = center_point + Point(x, y)
                        maze[point.x][point.y] = MazeBlockType.WALL

            current_point = self.vertices[0]
            for point in self.vertices[1:] + [current_point]:
                direction = (point - current_point).vector().normalised()
                while current_point != point:
                    x = int(current_point.x) + BLOCK_DIVISION // 2
                    y = int(current_point.y) + BLOCK_DIVISION // 2
                    if x < len(maze):
                        maze[x][y] = MazeBlockType.PATH
                        for block in get_surrounding_blocks(Point(x, y)):
                            if 0 <= block.x < len(maze) and 0 <= block.y < len(maze[0]) and maze[block.x][
                                block.y] == MazeBlockType.EMPTY:
                                maze[block.x][block.y] = MazeBlockType.WALL

                    current_point += direction

    def is_edge_piece(self):

        edge_tiles = 0
        for point in self.center_points:
            if point.x == 0:
                edge_tiles += 1

        return edge_tiles > 2
