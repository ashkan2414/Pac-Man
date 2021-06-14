import os
import pickle
import random
from copy import deepcopy

from game_component import *
from tools import *
from globals import MazeBlockType, BlockPickupType, BlockWallType
import globals


class Maze(GameComponent):

    def __init__(self, parent, bounds):
        super().__init__(parent, bounds)
        self.maze = []
        self.width = WIDTH_TILE_COUNT * TILE_SCALE_FACTOR + 3
        self.height = HEIGHT_TILE_COUNT * TILE_SCALE_FACTOR + 3
        self.aspect_ratio = self.width / self.height
        self.block_pixel_size = 0
        self.respawn_point = Point(0, 0)
        self.n = 0

        self.wall_images = {}
        for wall_type in BlockWallType:
            for r in range(4):
                self.wall_images[(wall_type, r * 90)] = pygame.transform.rotate(
                    pygame.image.load(BLOCK_WALL_IMAGE_FILES.get(wall_type)), r * 90)

        globals.scaled_maze_wall_images = self.wall_images.copy()

        self.barrier_image = pygame.image.load(BLOCK_BARRIER_IMAGE_FILE)
        globals.scaled_maze_barrier_image = self.barrier_image.copy()

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.maze and self.n < len(self.maze) * len(self.maze[0]):
            x = self.n // len(self.maze)
            y = self.n % len(self.maze)
            self.n += 1
            return self.point((Point(x, y)))
        else:
            raise StopIteration

    def __getitem__(self, key):
        return self.maze[key]

    def start(self):
        self.generate_maze()
        self.block_pixel_size = round(self.as_bounds.width / self.width)
        super().start()

    def draw(self):
        self.surface.fill(EMPTY)

        for block in self:
            block.draw(self.surface, self.block_pixel_size)

        if DISPLAY_MAZE_GRIDLINES:
            for x in range(self.width + 1):
                pygame.draw.line(self.surface, WHITE, (x * self.block_pixel_size, 0),
                                 (x * self.block_pixel_size, self.height * self.block_pixel_size))
            for y in range(self.height + 1):
                pygame.draw.line(self.surface, WHITE, (0, y * self.block_pixel_size),
                                 (self.width * self.block_pixel_size, y * self.block_pixel_size))

        super().draw()

    def on_scale(self, container_bounds):
        super().on_scale(container_bounds)
        self.block_pixel_size = round(self.as_bounds.width / self.width)

        globals.scaled_maze_wall_images.clear()
        block_size = (self.block_pixel_size, self.block_pixel_size)
        for walL_type, image in self.wall_images.items():
            globals.scaled_maze_wall_images[walL_type] = pygame.transform.smoothscale(image, block_size)

        globals.scaled_maze_barrier_image = pygame.transform.smoothscale(self.barrier_image, block_size)

    def point(self, point):
        if 0 <= point.x < len(self.maze) and 0 <= point.y < len(self.maze[0]):
            return self[point.x][point.y]
        else:
            return MazeBlock(point)

    def generate_maze(self):
        """
        Generates and returns a pac-man maze

        Returns:
            list: A generated maze
        """
        # Create empty 2D list to store maze
        self.maze = [[MazeBlock(Point(x, y)) for y in range(self.height)] for x in
                     range(int((WIDTH_TILE_COUNT // 2 + 1) * TILE_SCALE_FACTOR + 1))]

        # Get the maze pieces
        pieces = Maze.generate_pieces(WIDTH_TILE_COUNT // 2 + 1, HEIGHT_TILE_COUNT)

        # Set the first edge piece in the pieces list to an empty edge piece
        for piece in pieces:
            if piece.is_edge_piece(2):
                piece.empty_edge_piece = True
                break

        # Insert each piece into maze
        for piece in pieces:
            piece.draw(self.maze)

        # Remove last column to make it symmetrical for mirroring
        self.maze.pop()

        self.maze[-1][MAZE_BARRIER_Y_POSITION] = BarrierBlock(Point(len(self.maze) - 1, MAZE_BARRIER_Y_POSITION))

        # Mirror the maze
        for x in range(len(self.maze) - 1, -1, -1):
            self.maze.append([])
            for y in range(len(self.maze[0])):
                new_block = self.maze[x][y].copy()
                new_block.position = Point(len(self.maze) - 1, y)
                self.maze[-1].append(new_block)

        for block in self:
            if block.block_type == MazeBlockType.WALL:
                block.setup(self)
            elif block.block_type == MazeBlockType.PATH:
                block.pickup_type = BlockPickupType.POINT

        self.respawn_point = Point(self.width // 2, self.height // 2)

    @staticmethod
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
        piece_presets = Maze.generate_piece_presets()

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

    @staticmethod
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


class MazePiece:
    def __init__(self, points):
        self.center_points = points
        self.scaled_center_points = []
        self.vertices = []
        self.empty_edge_piece = False

    def __str__(self):
        """
        Returns the string representation of the maze piece

        Returns:
            string: The string representation of the maze piece
        """
        return str(self.center_points)

    def __repr__(self):
        """
        Returns the string representation of the maze piece

        Returns:
            string: The string representation of the maze piece
        """
        return self.__str__()

    def __eq__(self, other):
        """
        Returns whether this maze piece is equal to another maze piece

        Returns:
            bool: Whether this maze piece is equal to another maze piece
        """
        return self.center_points == other.center_points

    def __hash__(self):
        """
        Returns the hash of the maze piece

        Returns:
            int: The hash of the maze piece
        """
        return hash(tuple(self.center_points))

    def rotate(self, angle, axis):
        """
        Rotates the maze piece and its point around an axis point

        Parameters:
            angle (int, float): The angle to rotate
            axis (Point): The point to rotate around
        """

        for point in self.center_points:
            point.rotate(angle, axis)
            point.round()

    def translate(self, displacement):
        """
        Translates the maze piece and its point by a displacement

        Parameters:
            displacement (Point, Vector): The amount and direction to translate
        """

        for point in self.center_points:
            point.translate(displacement)
            point.round()

    def calculate_vertices(self):
        """
        Calculates the edge vertex points of the piece in order
        """
        # Get the unsorted vertices by taking the scaling the tiles with the tile scale factor and getting the corner
        # blocks of the scaled tiles
        unsorted_vertices = []
        for point in self.center_points:
            scaled_center_point = point * TILE_SCALE_FACTOR + Point(TILE_SCALE_FACTOR // 2, TILE_SCALE_FACTOR // 2)
            half_tile = TILE_SCALE_FACTOR // 2
            self.scaled_center_points.append(scaled_center_point)
            unsorted_vertices.append(scaled_center_point + Point(half_tile + 1, half_tile + 1))
            unsorted_vertices.append(scaled_center_point + Point(half_tile + 1, -half_tile))
            unsorted_vertices.append(scaled_center_point + Point(-half_tile, half_tile + 1))
            unsorted_vertices.append(scaled_center_point + Point(-half_tile, -half_tile))

        # Get rid of overlapping vertices and vertices which lie in the middle of the piece
        # For each vertex
        for vertex in unsorted_vertices.copy():
            # Get the number of identical vertices
            frequency = unsorted_vertices.count(vertex)
            # If there are 4 identical vertices, then the vertex lies in the center of the piece
            if frequency == 4:
                # Remove all 4 vertices
                num_to_remove = 4
            # Otherwise
            else:
                # Remove all but one
                num_to_remove = frequency - 1
            # Remove the vertices
            for i in range(num_to_remove):
                unsorted_vertices.remove(vertex)

        # Start at the left most vertex
        current_vertex = Point.left_most(unsorted_vertices)
        # Remove it from unsorted vertices list and add it to the vertices
        unsorted_vertices.remove(current_vertex)
        self.vertices = [current_vertex]

        # While not all vertices have been ordered
        while unsorted_vertices:
            # Holds the best candidate vertex along with the angle it makes with the current vertex
            next_vertex = [Point(1000, 1000), -1000]
            # For each vertex in the unsorted list
            for vertex in unsorted_vertices:
                # If the vertices are lined up directly on the grid
                if current_vertex.is_grid_collinear(vertex):
                    # If the vector from current vertex to the vertex doesn't intersect any of the ordered vertices
                    if len(self.vertices) < 2 or not (vertex - current_vertex).vector().intersects_points(
                            self.vertices[:-1], current_vertex):
                        # Get the angle from the vertex and the current vertex
                        angle = Vector.angle(current_vertex.vector(), vertex.vector())
                        # If the angle is bigger than the best vertex so far, set the best vertex to this vertex
                        if angle > next_vertex[1]:
                            next_vertex = [vertex, angle]
                        # If the angle is the same as best vertex so far, only set the best vertex to this vertex if
                        # its closer to the current vertex
                        elif angle == next_vertex[1]:
                            if Point.distance(current_vertex, vertex) < Point.distance(current_vertex, next_vertex[0]):
                                next_vertex = [vertex, angle]

            # Set the current vertex to the new vertex
            current_vertex = next_vertex[0]
            # Remove the new vertex from unsorted list and add it to the vertices list
            unsorted_vertices.remove(next_vertex[0])
            self.vertices.append(next_vertex[0])

    def draw(self, maze):
        """
        Draws the piece on the maze

        Parameters:
            maze (list): The maze to draw on
        """
        # Calculate the vertices
        self.calculate_vertices()

        # If the piece isn't a empty edge piece type, start by filling all the piece tile blocks with walls
        if not self.empty_edge_piece:
            # For each block around each scaled center point
            for center_point in self.scaled_center_points:
                for x in range(TILE_SCALE_FACTOR):
                    for y in range(TILE_SCALE_FACTOR):
                        point = center_point + Point(x, y)
                        # Set the block to wall
                        maze[point.x][point.y] = WallBlock(point)

        # Set the current point the first vertex in the vertices list
        current_point = self.vertices[0]
        # Cycle through vertices starting from the second vertices
        for point in self.vertices[1:] + [current_point]:
            # Get the direction going from the current point to current vertex
            direction = (point - current_point).vector().normalised()
            # While we still haven't arrived at the current vertex
            while current_point != point:
                # Move the point down and right by half the scale factor to make room for the outer walls
                x = int(current_point.x) + TILE_SCALE_FACTOR // 2
                y = int(current_point.y) + TILE_SCALE_FACTOR // 2
                # If the x value is within the map width
                if x < len(maze):
                    # If not an empty edge piece, set current point to path otherwise, only make it a path if the point
                    # doesn't lie on the edge of the maze
                    if not self.empty_edge_piece or (x > TILE_SCALE_FACTOR // 2 and TILE_SCALE_FACTOR // 2 < y < len(
                            maze[0]) - TILE_SCALE_FACTOR // 2 - 1):
                        maze[x][y] = PathBlock(Point(x, y))
                        # Set all the empty blocks around this current path block to walls
                        for block in Point.get_neighbour_points(Point(x, y)):
                            if 0 <= block.x < len(maze) and 0 <= block.y < len(maze[0]):
                                if maze[block.x][block.y] == MazeBlockType.EMPTY:
                                    maze[block.x][block.y] = WallBlock(block)
                # Move to the next point by going towards the vertex by one block
                current_point += direction

    def is_edge_piece(self, edge_density):
        """
        Returns whether this maze piece is an edge piece

        Parameters:
            edge_density (int): The number of tiles on the edge required for this to be considered an edge piece

        Returns:
            bool: Whether this maze piece is an edge piece
        """
        edge_tiles = 0
        # For every unscaled center point
        for point in self.center_points:
            # If the point is on the left edge
            if point.x == 0:
                # Increment the number of edge tiles
                edge_tiles += 1

        # If the number of edge tiles is equal to or greater than the required edge density, return true
        return edge_tiles >= edge_density


class MazeBlock:
    block_type = MazeBlockType.EMPTY

    def __init__(self, position):
        self.position = position

    def __str__(self):
        return self.block_type.name

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.block_type == other

    def draw(self, surface, block_size):
        pygame.draw.rect(surface, MAZE_EMPTY_COLOR,
                         (self.position.x * block_size, self.position.y * block_size,
                          block_size, block_size))

    def copy(self):
        return self.__class__(self.position)


class PathBlock(MazeBlock):
    block_type = MazeBlockType.PATH

    def __init__(self, position):
        super().__init__(position)
        self.pickup_type = BlockPickupType.NONE
        self.pickup_consumed = False

    def draw(self, surface, block_size):
        pygame.draw.rect(surface, MAZE_PATH_COLOR,
                         (self.position.x * block_size, self.position.y * block_size,
                          block_size, block_size))

        if not self.pickup_consumed:
            if self.pickup_type == BlockPickupType.POINT:
                pygame.draw.circle(surface, MAZE_POINT_COLOR,
                                   ((self.position.x + 0.5) * block_size,
                                    (self.position.y + 0.5) * block_size),
                                   MAZE_POINT_RADIUS_FACTOR * block_size // 2)
            if self.pickup_type == BlockPickupType.POWER_PELLET:
                pygame.draw.circle(surface, MAZE_POINT_COLOR,
                                   ((self.position.x + 0.5) * block_size,
                                    (self.position.y + 0.5) * block_size),
                                   MAZE_POWER_PELLET_RADIUS_FACTOR * block_size // 2)

    def copy(self):
        new_block = super().copy()
        new_block.pickup_type = self.pickup_type
        new_block.pickup_consumed = self.pickup_consumed
        return new_block


class WallBlock(MazeBlock):
    block_type = MazeBlockType.WALL

    def __init__(self, position):
        super().__init__(position)
        self.wall_type = BlockWallType.CENTER
        self.orientation = 0
        self.mirror_x = False
        self.mirror_y = False

    def setup(self, maze):
        neighbours = {"TL": maze.point(self.position + Point(-1, -1)), "L": maze.point(self.position + Point(-1, 0)),
                      "BL": maze.point(self.position + Point(-1, 1)), "B": maze.point(self.position + Point(0, 1)),
                      "BR": maze.point(self.position + Point(1, 1)), "R": maze.point(self.position + Point(1, 0)),
                      "TR": maze.point(self.position + Point(1, -1)), "T": maze.point(self.position + Point(0, -1))}

        side_neighbours = {"L": maze.point(self.position + Point(-1, 0)),
                           "B": maze.point(self.position + Point(0, 1)),
                           "R": maze.point(self.position + Point(1, 0)),
                           "T": maze.point(self.position + Point(0, -1))}

        if neighbours.get("R") == MazeBlockType.BARRIER:
            self.wall_type = BlockWallType.EDGE_BARRIER_SIDE
            self.mirror_x = True
            return
        elif neighbours.get("L") == MazeBlockType.BARRIER:
            self.wall_type = BlockWallType.EDGE_BARRIER_SIDE
            return

        wall_count = list(neighbours.values()).count(MazeBlockType.WALL)
        path_count = list(neighbours.values()).count(MazeBlockType.PATH)
        empty_count = list(neighbours.values()).count(MazeBlockType.EMPTY)

        outer_edge = empty_count > 0
        block_count = empty_count if outer_edge else path_count
        indicating_block_type = MazeBlockType.EMPTY if outer_edge else MazeBlockType.PATH

        if block_count == 2 or block_count == 3:
            if outer_edge and list(side_neighbours.values()).count(MazeBlockType.WALL) == 3:
                self.wall_type = BlockWallType.EDGE_CONNECTOR_SIDE
                if neighbours.get("L") == indicating_block_type:
                    self.orientation = 90
                    self.mirror_y = neighbours.get("BR") == MazeBlockType.PATH
                elif neighbours.get("R") == indicating_block_type:
                    self.orientation = 270
                    self.mirror_y = neighbours.get("TL") == MazeBlockType.PATH
            else:
                self.wall_type = BlockWallType.EDGE_SIDE if outer_edge else BlockWallType.SIDE
                if neighbours.get("L") == indicating_block_type:
                    self.orientation = 90
                elif neighbours.get("R") == indicating_block_type:
                    self.orientation = 270
                elif neighbours.get("T") == indicating_block_type:
                    self.orientation = 0
                elif neighbours.get("B") == indicating_block_type:
                    self.orientation = 180

        elif block_count == 1:
            if wall_count == 4 and outer_edge:
                self.wall_type = BlockWallType.EDGE_CONNECTOR_CORNER
            else:
                self.wall_type = BlockWallType.EDGE_INNER_CORNER if outer_edge else BlockWallType.CORNER

            if neighbours.get("TL") == indicating_block_type:
                self.orientation = 180
            elif neighbours.get("BL") == indicating_block_type:
                self.orientation = 0 if self.wall_type == BlockWallType.EDGE_CONNECTOR_CORNER else 270
                self.mirror_x = self.wall_type == BlockWallType.EDGE_CONNECTOR_CORNER
            elif neighbours.get("BR") == indicating_block_type:
                self.orientation = 0
            elif neighbours.get("TR") == indicating_block_type:
                self.orientation = 180 if self.wall_type == BlockWallType.EDGE_CONNECTOR_CORNER else 90
                self.mirror_x = self.wall_type == BlockWallType.EDGE_CONNECTOR_CORNER

        elif block_count == 4 or block_count == 5 or block_count == 6:
            self.wall_type = BlockWallType.EDGE_OUTER_CORNER if outer_edge else BlockWallType.CORNER
            if neighbours.get("L") == indicating_block_type and neighbours.get("T") == indicating_block_type:
                self.orientation = 0
            elif neighbours.get("L") == indicating_block_type and neighbours.get("B") == indicating_block_type:
                self.orientation = 90
            elif neighbours.get("R") == indicating_block_type and neighbours.get("B") == indicating_block_type:
                self.orientation = 180
            elif neighbours.get("R") == indicating_block_type and neighbours.get("T") == indicating_block_type:
                self.orientation = 270

    def draw(self, surface, block_size):
        image = pygame.transform.flip(globals.scaled_maze_wall_images.get((self.wall_type, self.orientation)),
                                      self.mirror_x, self.mirror_y)
        surface.blit(image, (self.position.x * block_size, self.position.y * block_size))

    def copy(self):
        new_block = super().copy()
        new_block.wall_type = self.wall_type
        new_block.orientation = self.orientation
        return new_block


class BarrierBlock(MazeBlock):
    block_type = MazeBlockType.BARRIER

    def __init__(self, position):
        super().__init__(position)

    def draw(self, surface, block_size):
        surface.blit(globals.scaled_maze_barrier_image,
                     (self.position.x * block_size, self.position.y * block_size))
