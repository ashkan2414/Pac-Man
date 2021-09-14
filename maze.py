import pickle
import random
from copy import deepcopy

from game_component import *
from managers import *


class Maze(GameComponent):
    """
    A pacman maze generated random from scratch

    Attributes:
    -----------
    maze (list): The 2 dimensional list of blocks making up the maze
    block_size (int): The size of the blocks in pixels
    wall_surface (Surface): The surface the walls are drawn on
    n (int): List iterator counter

    Methods:
    --------
    def point(self, point):
        Returns the block at the point

    def draw_walls(self):
        Draws the walls on the wall surface

    def generate_maze(self):
        Generates and returns a pac-man maze

    Static Methods:
    ---------------
    def generate_pieces(width, height):
        Generates and returns maze pieces that fit together

    def generate_piece_presets():
        Generates and returns a list of maze piece presets

    Parent (GameComponent):
    """
    __doc__ += GameComponent.__doc__

    def __init__(self, parent, bounds):
        super().__init__(parent, bounds)
        self.maze = []
        self.aspect_ratio = MAZE_WIDTH / MAZE_HEIGHT
        self.block_size = 0
        self.wall_surface = None
        self.n = 0

        globals.wall_images = {}
        for wall_type in BlockWallType:
            for r in range(4):
                globals.maze_wall_images[(wall_type, r * 90)] = pygame.transform.rotate(
                    pygame.image.load(os.path.join(MAZE_FILE_PATH, BLOCK_WALL_IMAGES.get(wall_type))), r * 90)

        globals.scaled_maze_wall_images = globals.maze_wall_images.copy()

        globals.maze_barrier_image = pygame.image.load(os.path.join(MAZE_FILE_PATH, BLOCK_BARRIER_IMAGE))
        globals.scaled_maze_barrier_image = globals.maze_barrier_image.copy()

        globals.fruit_image = pygame.image.load(os.path.join(MAZE_FILE_PATH, FRUIT_IMAGE))
        globals.scaled_fruit_image = globals.fruit_image.copy()

    def __iter__(self):
        """
        Sets up object for iteration
        """
        self.n = 0
        return self

    def __next__(self):
        """
        Returns the next block in iteration

        Returns:
            MazeBlock: The next block in iteration
        """
        # If the maze is defined and iterator counter is less than the number of blocks
        if self.maze and self.n < len(self.maze) * len(self.maze[0]):
            # Calculate x and y position based on the value of iterator
            y = self.n // len(self.maze)
            x = self.n % len(self.maze)
            # Increment iterator
            self.n += 1
            # Return the block at point
            return self.point((Point(x, y)))
        else:
            raise StopIteration

    def __getitem__(self, x):
        """
        Returns the column at x value

        Parameter:
            x (int): The x coordinate

        Returns:
            list: The column at x
        """
        return self.maze[x]

    def start(self):
        globals.fruit_spawnable = False
        self.generate_maze()
        self.draw_walls()
        super().start()

    def process_event(self, event):
        if event.type == GAME_START:
            globals.fruit_spawnable = False
            TimedEventManager.add_timed_event(pygame.event.Event(FRUIT_SPAWN_READY), FRUIT_COOLDOWN_DURATION)
        elif event.type == LEVEL_FINISH or event.type == LEVEL_RESET:
            globals.fruit_spawnable = False
        elif event.type == FRUIT_SPAWN_READY:
            globals.fruit_spawnable = True
        super().process_event(event)

    def draw(self):
        # Clear surface
        self.surface.fill(EMPTY)
        # Draw the walls
        self.surface.blit(self.wall_surface, (0, 0))

        # Draw path blocks and count the number of unconsumed points
        globals.points_left = 0
        for block in self:
            if block.block_type == MazeBlockType.PATH:
                block.draw(self.surface, self.block_size)
                if not block.pickup_consumed:
                    globals.points_left += 1
                else:
                    if globals.fruit_spawnable and random.randrange(1, 100 // FRUIT_SPAWN_CHANCE) == 1:
                        block.pickup_type = BlockPickupType.FRUIT
                        block.pickup_consumed = False
                        globals.fruit_spawnable = False

        if DISPLAY_MAZE_GRIDLINES:
            # Draw maze grid lines
            for x in range(MAZE_WIDTH + 1):
                pygame.draw.line(self.surface, WHITE, (x * self.block_size, 0),
                                 (x * self.block_size, MAZE_HEIGHT * self.block_size))
            for y in range(MAZE_HEIGHT + 1):
                pygame.draw.line(self.surface, WHITE, (0, y * self.block_size),
                                 (MAZE_WIDTH * self.block_size, y * self.block_size))

        super().draw()

    def on_scale(self, container_bounds):
        super().on_scale(container_bounds)
        # Determine block pixel size
        self.block_size = int(self.as_bounds.width / MAZE_WIDTH)

        # Deal with gaps left when scaling maze
        bound_position_offset = (self.as_bounds.width - MAZE_WIDTH * self.block_size) / 2
        self.as_bounds.x += bound_position_offset
        self.as_bounds.y += bound_position_offset
        self.as_bounds.width -= bound_position_offset * 2
        self.as_bounds.height -= bound_position_offset * 2
        self.surface = pygame.Surface(self.as_bounds.size(), flags=pygame.SRCALPHA)

        # Scale wall images using the raw original images
        globals.scaled_maze_wall_images.clear()
        block_size = (self.block_size, self.block_size)
        for walL_type, image in globals.maze_wall_images.items():
            globals.scaled_maze_wall_images[walL_type] = pygame.transform.smoothscale(image, block_size)

        globals.scaled_maze_barrier_image = pygame.transform.smoothscale(globals.maze_barrier_image, block_size)
        globals.scaled_fruit_image = pygame.transform.smoothscale(globals.fruit_image, block_size)

        # Draw the maze walls
        self.draw_walls()

    def point(self, point):
        """
        Returns the block at the point

        Parameters:
            point (Point): The location of the block to return

        Returns:
            MazeBlock: The block at the point
        """
        if 0 <= point.x < len(self.maze) and 0 <= point.y < len(self.maze[0]):
            return self[point.x][point.y]
        else:
            return MazeBlock(point)

    def draw_walls(self):
        """
        Draws the walls on the wall surface
        """
        # Setup wall drawing surface
        self.wall_surface = pygame.surface.Surface(self.surface.get_size())
        # Draw the walls on the surface
        for block in self:
            if block.block_type != MazeBlockType.PATH:
                block.draw(self.wall_surface, self.block_size)

    def generate_maze(self):
        """
        Generates and returns a pac-man maze

        Returns:
            list: A generated maze
        """
        # Create empty 2D list to store maze
        self.maze = [[MazeBlock(Point(x, y)) for y in range(MAZE_HEIGHT)] for x in
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
            piece.fill_maze(self.maze)

        # Remove last column to make it symmetrical for mirroring
        self.maze.pop()

        # Set barrier block
        self.maze[-1][MAZE_BARRIER_Y_POSITION] = BarrierBlock(Point(len(self.maze) - 1, MAZE_BARRIER_Y_POSITION))

        # Add power pellets
        # Find all path blocks to the left of the power pellet max x setting
        path_blocks = [block for block in self if block.block_type == MazeBlockType.PATH and
                       block.position.x <= POWER_PELLET_MAX_X]
        # For the number of power pellets, choose random path blocks set their pickup type to power pellet
        for i in range(POWER_PELLET_QUANTITY // 2):
            random_block = random.choice(path_blocks)
            random_block.pickup_type = BlockPickupType.POWER_PELLET
            path_blocks.remove(random_block)

        # Mirror the maze
        for x in range(len(self.maze) - 1, -1, -1):
            self.maze.append([])
            for y in range(len(self.maze[0])):
                new_block = self.maze[x][y].copy()
                new_block.position = Point(len(self.maze) - 1, y)
                self.maze[-1].append(new_block)

        # Setup wall blocks and add point path blocks
        for block in self:
            if block.block_type == MazeBlockType.WALL:
                block.setup(self)
            elif block.block_type == MazeBlockType.PATH:
                if block.pickup_type == BlockPickupType.NONE:
                    block.pickup_type = BlockPickupType.POINT
                    globals.points_left += 1

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

        piece_presets_path = os.path.join(SAVE_FILE_PATH, PIECE_PRESETS_FILE)

        if os.path.exists(piece_presets_path):
            file = open(piece_presets_path, "rb")
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

            file = open(piece_presets_path, "wb")
            pickle.dump(piece_presets, file)
            file.close()

        # Return all the piece presets
        return piece_presets


class MazePiece:
    """
    A maze piece is a collection of tiles which create a piece of the maze

    ...

    Attributes:
    -----------
    center_points (list): The list of tile center points
    scaled_center_points (list): The list of block center points
    vertices (list): The list of path vertices
    empty_edge_piece (bool): Whether the piece is an empty edge piece type

    Methods:
    --------
    def rotate(self, angle, axis):
        Rotates the maze piece and its point around an axis point

    def translate(self, displacement):
        Translates the maze piece and its point by a displacement

    def calculate_vertices(self):
        Calculates the edge vertex points of the piece in order

    def fill_maze(self, maze):
        Fills maze with blocks

    def is_edge_piece(self, edge_density):
        Returns whether this maze piece is an edge piece
    """

    def __init__(self, points):
        """
        Returns a maze piece object

        Parameters:
            points (list): The list of tile center points

        Returns:
            MazePiece: A new maze piece object
        """
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
                        angle = (vertex - current_vertex).vector().angular_position()
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

    def fill_maze(self, maze):
        """
        Fills maze with blocks

        Parameters:
            maze (list): The maze to fill
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
    """
    A maze block is a the simplest form of object that makes up a maze

    ...

    Attributes:
    -----------
    position (Point): The position of the block


    Static Attributes:
    ------------------
    block_type (MazeBlockType): The type of block

    Methods:
    --------
    def draw(self, surface, block_size):
        Draws the block on the surface

    def copy(self):
        Returns a copy object
    """

    block_type = MazeBlockType.EMPTY

    def __init__(self, position):
        """
        Returns a new maze block object

        Parameters:
            position (Point): The location of the block

        Returns:
            MazeBlock: A new maze block object
        """
        self.position = position

    def __str__(self):
        """
        Returns the string representation of the maze block

        Returns:
            string: The string representation of the maze block
        """
        return self.block_type.name + str(self.position)

    def __repr__(self):
        """
        Returns the string representation of the maze block

        Returns:
            string: The string representation of the maze block
        """
        return self.__str__()

    def __eq__(self, other):
        """
        Returns whether this block equals another block in terms of block type

        Parameters:
            other: The other block to compare to

        Returns:
            bool: Whether this block equals another block in terms of block type
        """
        return self.block_type == other

    def draw(self, surface, block_size):
        """
        Draws the block on the surface

        Parameters:
            surface (Surface): The surface to draw on
            block_size (int): The size of each block in pixels

        """
        pygame.draw.rect(surface, MAZE_EMPTY_COLOR,
                         (self.position.x * block_size, self.position.y * block_size,
                          block_size, block_size))

    def copy(self):
        """
        Returns a copy object

        Returns:
            MazeBlock: A copy object
        """
        return self.__class__(self.position)


class PathBlock(MazeBlock):
    """
    A maze block representation path blocks

    Attributes:
    -----------
    pickup_type (BlockPickupType): The type of pickup available at this path block
    pickup_consumed (bool): Whether the pickup has been consumed

    Parent (MazeBlock):
    """
    __doc__ += MazeBlock.__doc__

    block_type = MazeBlockType.PATH

    def __init__(self, position):
        super().__init__(position)
        self.pickup_type = BlockPickupType.NONE
        self.pickup_consumed = False

    def draw(self, surface, block_size):
        # Draw black square on block as background
        pygame.draw.rect(surface, MAZE_PATH_COLOR,
                         (self.position.x * block_size, self.position.y * block_size,
                          block_size, block_size))

        # If the pickup has still not been consumed, draw it
        if not self.pickup_consumed:
            # If its a point pickup, draw a circle the size of a point pickup
            if self.pickup_type == BlockPickupType.POINT:
                pygame.draw.circle(surface, MAZE_POINT_COLOR,
                                   ((self.position.x + 0.5) * block_size,
                                    (self.position.y + 0.5) * block_size),
                                   MAZE_POINT_RADIUS_FACTOR * block_size // 2)

            # If its a power pellet pickup, draw a circle the size of a power pellet
            elif self.pickup_type == BlockPickupType.POWER_PELLET:
                pygame.draw.circle(surface, MAZE_POINT_COLOR,
                                   ((self.position.x + 0.5) * block_size,
                                    (self.position.y + 0.5) * block_size),
                                   MAZE_POWER_PELLET_RADIUS_FACTOR * block_size // 2)

            elif self.pickup_type == BlockPickupType.FRUIT:
                surface.blit(globals.scaled_fruit_image, (self.position.x * block_size, self.position.y * block_size))

    def copy(self):
        new_block = super().copy()
        new_block.pickup_type = self.pickup_type
        new_block.pickup_consumed = self.pickup_consumed
        return new_block


class WallBlock(MazeBlock):
    """
    A maze block representation wall blocks

    Attributes:
    -----------
    wall_type (BlockWallType): The type of wall
    orientation (int): The rotation of the wall
    mirror_x (bool): Whether the block image should be mirrored in the x
    mirror_y (bool): Whether the block image should be mirrored in the y

    Methods:
    --------
    def setup(self, maze):
        Sets up the wall type, orientation and mirror settings for drawing the wall

    Parent (MazeBlock):
    """
    block_type = MazeBlockType.WALL

    def __init__(self, position):
        super().__init__(position)
        self.wall_type = BlockWallType.CENTER
        self.orientation = 0
        self.mirror_x = False
        self.mirror_y = False

    def setup(self, maze):
        """
        Sets up the wall type, orientation and mirror settings for drawing the wall

        Parameters:
            maze (Maze): The maze object to get information from
        """

        # Get neighbours
        neighbours = {"TL": maze.point(self.position + Point(-1, -1)), "L": maze.point(self.position + Point(-1, 0)),
                      "BL": maze.point(self.position + Point(-1, 1)), "B": maze.point(self.position + Point(0, 1)),
                      "BR": maze.point(self.position + Point(1, 1)), "R": maze.point(self.position + Point(1, 0)),
                      "TR": maze.point(self.position + Point(1, -1)), "T": maze.point(self.position + Point(0, -1))}

        side_neighbours = {"L": neighbours.get("L"),
                           "B": neighbours.get("B"),
                           "R": neighbours.get("R"),
                           "T": neighbours.get("T")}

        # If beside barrier
        if neighbours.get("R") == MazeBlockType.BARRIER or neighbours.get("L") == MazeBlockType.BARRIER:
            self.wall_type = BlockWallType.EDGE_BARRIER_SIDE
            if neighbours.get("R") == MazeBlockType.BARRIER:
                self.mirror_x = True
            return

        # Get block count of surrounding blocks
        wall_count = list(neighbours.values()).count(MazeBlockType.WALL)
        path_count = list(neighbours.values()).count(MazeBlockType.PATH)
        empty_count = list(neighbours.values()).count(MazeBlockType.EMPTY)

        # Determine indicating block count and type
        outer_edge = empty_count > 0
        block_count = empty_count if outer_edge else path_count
        indicating_block_type = MazeBlockType.EMPTY if outer_edge else MazeBlockType.PATH

        # Depending on the surrounding block type, determine the orientation, type and mirror settings
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
    """
    A maze block representation barrier blocks

    Parent (MazeBlock):
    """
    block_type = MazeBlockType.BARRIER

    def draw(self, surface, block_size):
        surface.blit(globals.scaled_maze_barrier_image,
                     (self.position.x * block_size, self.position.y * block_size))
