import pygame, random, copy
from enum import Enum

import globals
from settings import *
from tools import *


class GameStateType(Enum):
    START_MENU = 0
    SETTING_MENU = 1
    GAME_MENU = 2


class GameState:

    def __init__(self, state_type):
        self.type = state_type

    def start(self):
        pass

    def update(self):
        self.events()
        self.draw()

    def events(self):
        pass

    def draw(self):
        globals.game.screen.fill((255, 255, 255))

    def end(self):
        pass

    @staticmethod
    def default_events(event):
        if event.type == pygame.QUIT:
            globals.game.running = False
        if event.type == pygame.VIDEORESIZE:
            new_size = list(event.dict['size'])

            if new_size[0] < MIN_SIZE[0]:
                new_size[0] = MIN_SIZE[0]
            if new_size[1] < MIN_SIZE[1]:
                new_size[1] = MIN_SIZE[1]

            size_change = (abs(new_size[0] - globals.size[0]), abs(new_size[1] - globals.size[1]))
            if size_change[0] > size_change[1]:
                new_size[1] = int(new_size[0] // ASPECT_RATIO)
            else:
                new_size[0] = int(new_size[1] * ASPECT_RATIO)

            globals.game.screen = pygame.display.set_mode(new_size, pygame.RESIZABLE)
            globals.size = tuple(new_size)


class StartMenu(GameState):

    def __init__(self):
        super().__init__(GameStateType.START_MENU)

    def update(self):
        for event in pygame.event.get():
            GameState.default_events(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    globals.game.set_game_state(GameStateType.GAME_MENU)

        GUITools.draw_text("PAC-MAN", globals.game.screen, [globals.size[0] // 2, 100],
                           FONT, HEADER_SIZE, (170, 130, 60))


class SettingMenu(GameState):

    def __init__(self):
        super().__init__(GameStateType.SETTING_MENU)

    def update(self):
        for event in pygame.event.get():
            GameState.default_events(event)


class GameMenu(GameState):

    def __init__(self):
        super().__init__(GameStateType.GAME_MENU)

        self.maze = [[True for y in range((HEIGHT_TILE_COUNT + 1) * BLOCK_DIVISION)] for x in
                     range((WIDTH_TILE_COUNT + 1) * BLOCK_DIVISION)]
        pieces = MazePiece.generate_pieces(WIDTH_TILE_COUNT // 2 + 1, HEIGHT_TILE_COUNT)

        for piece in pieces:

            piece.calculate_vertices()
            points = copy.deepcopy(piece.vertices + [piece.vertices[0]])
            current_point = points[0]
            for point in points[1:]:
                direction = (point - current_point).vector().normalised()
                while current_point != point:
                    x = int(current_point.x) + BLOCK_DIVISION // 2
                    y = int(current_point.y) + BLOCK_DIVISION // 2

                    if x < len(self.maze) // 2:
                        self.maze[x][y] = False
                        self.maze[len(self.maze) - 1 - x][y] = False

                    current_point += direction

    def events(self):
        for event in pygame.event.get():
            GameState.default_events(event)

    def draw(self):

        super().draw()

        for x in range(len(self.maze)):
            for y in range(len(self.maze[x])):

                wall = self.maze[x][y]
                if wall:
                    color = (10, 10, 10)
                else:
                    color = (65, 65, 65)

                pygame.draw.rect(globals.game.screen, color,
                                 (x * BLOCK_SIZE + BLOCK_SIZE, y * BLOCK_SIZE + BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        color = (100, 100, 100)
        for x in range(len(self.maze) + 1):
            pygame.draw.line(globals.game.screen, color, (x * BLOCK_SIZE + BLOCK_SIZE, BLOCK_SIZE),
                             (x * BLOCK_SIZE + BLOCK_SIZE, (len(self.maze[0]) + 1) * BLOCK_SIZE))

        for y in range(len(self.maze[0]) + 1):
            pygame.draw.line(globals.game.screen, color, (BLOCK_SIZE, y * BLOCK_SIZE + BLOCK_SIZE),
                             ((len(self.maze) + 1) * BLOCK_SIZE, y * BLOCK_SIZE + BLOCK_SIZE))


class MazePiece:

    def __init__(self, points):
        self.center_points = points
        self.vertices = []

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
            x = point.x * BLOCK_DIVISION + half_block
            y = point.y * BLOCK_DIVISION + half_block
            divided_point = Point(x, y)
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

    @staticmethod
    def generate_pieces(width, height):

        # Create a list of points for each tile
        unoccupied_tiles = [Point(x, y) for x in range(width) for y in range(height)]
        # Empty list to hold the maze pieces
        maze_pieces = []

        center_piece = MazePiece([Point(3, 3), Point(3, 4), Point(4, 3), Point(4, 4)])
        for point in center_piece.center_points:
            unoccupied_tiles.remove(point)
        maze_pieces.append(center_piece)

        # Generate a list of all possible piece presets
        piece_presets = MazePiece.generate_piece_presets()

        # Shuffle the presets and put the default 1 square preset shape at the end to reduce frequency
        default_preset = piece_presets[0]
        piece_presets.remove(default_preset)
        random.shuffle(piece_presets)
        piece_presets.append(default_preset)

        # While there are still unoccupied_tiles
        while unoccupied_tiles:

            # Choose a random tile
            current_tile_point = random.choice(unoccupied_tiles)
            for preset in piece_presets:

                fits = True
                for center_point in preset.center_points:

                    # Calculate displacement from selected point to current tile point
                    displacement = current_tile_point - center_point
                    # Deep copy the preset so it doesn't get modified when we translate it
                    copied_preset = copy.deepcopy(preset)
                    # Translate the preset to the start point
                    copied_preset.translate(displacement)

                    fits = True
                    # For each point in the
                    for point in copied_preset.center_points:
                        if point.x > width - 1 or point.x < 0 or point.y > height - 1 or point.y < 0 or point not in unoccupied_tiles:
                            fits = False
                            break

                    if fits:
                        for point in copied_preset.center_points:
                            if point in unoccupied_tiles:
                                unoccupied_tiles.remove(point)
                        maze_pieces.append(copied_preset)
                        break

                if fits:
                    break

        return maze_pieces

    @staticmethod
    def generate_piece_presets():

        # Direction to vector translate dictionary
        direction_vector_map = {"L": Vector(-1, 0), "R": Vector(1, 0), "U": Vector(0, 1), "D": Vector(0, -1)}

        # Empty list to store the resulting presets
        piece_presets = []

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

            # Cycle through each point and each rotation and generate all possible pieces for the shape preset
            for point in points:
                # i represents the number of 90 degree rotations applied
                for i in range(4):
                    # Create a MazePiece object with the points
                    # Use deepcopy so that the pieces don't modify each others' points
                    piece_preset = MazePiece(copy.deepcopy(list(points)))
                    # Rotate it around the current point with the current angle
                    piece_preset.rotate(i * 90, point)
                    # Add it to the list of piece presets if its not already in the list
                    if piece_preset not in piece_presets:
                        piece_presets.append(piece_preset)

        # Return all the piece presets
        return piece_presets
