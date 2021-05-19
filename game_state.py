from enum import Enum
from settings import *
import globals
import pygame
from gui_tools import *
from math_tools import *


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
    def base_events(event):
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
            GameState.base_events(event)

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
            GameState.base_events(event)


class GameMenu(GameState):

    def __init__(self):
        super().__init__(GameStateType.GAME_MENU)

        pieces = []

        self.maze = [[True for x in range(10 * BLOCK_DIVISION)] for y in range(10 * BLOCK_DIVISION)]

        for piece in simple_maze:
            points = []
            for point in piece:
                points.append(Point(point[0], point[1]))
            pieces.append(MazePiece(points))

        for piece in pieces:

            points = piece.vertices.copy() + [piece.vertices[0]]
            current_point = points[0]
            for point in points[1:]:
                direction = Vector2(point - current_point).normalised()
                while current_point != point:
                    x = int(current_point.x) + BLOCK_DIVISION // 2
                    y = int(current_point.y) + BLOCK_DIVISION // 2

                    if x < len(self.maze) // 2:
                        self.maze[x][y] = False
                        self.maze[len(self.maze) - 1 - x][y] = False

                    current_point += direction

    def events(self):
        for event in pygame.event.get():
            GameState.base_events(event)

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


direction_vector_map = {"L": Vector2(Point(-1, 0)), "R": Vector2(Point(1, 0)), "U": Vector2(Point(0, 1)),
                        "D": Vector2(Point(0, -1)), }


class MazePiece:

    def __init__(self, points):
        self.center_points = points
        self.vertices = []
        self.calculate_points()

    def calculate_points(self):

        unsorted_vertices = []

        for point in self.center_points:
            half_block = BLOCK_DIVISION // 2
            point.x = point.x * BLOCK_DIVISION + half_block
            point.y = point.y * BLOCK_DIVISION + half_block
            unsorted_vertices.append(point + Point(half_block + 1, half_block + 1))
            unsorted_vertices.append(point + Point(half_block + 1, -half_block))
            unsorted_vertices.append(point + Point(-half_block, half_block + 1))
            unsorted_vertices.append(point + Point(-half_block, -half_block))

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
            next_vertex = [None, -1000]
            for point in unsorted_vertices:
                angle = current_vertex.angle(point)
                if current_vertex.is_collinear(point):
                    vector = Vector2(point - current_vertex)
                    if len(self.vertices) < 2 or not vector.intersects_points(self.vertices[:-1], current_vertex):
                        if angle > next_vertex[1]:
                            next_vertex = [point, angle]
                        elif angle == next_vertex[1]:
                            if current_vertex.distance(point) < current_vertex.distance(next_vertex[0]):
                                next_vertex = [point, angle]

            current_vertex = next_vertex[0]
            unsorted_vertices.remove(next_vertex[0])
            self.vertices.append(next_vertex[0])
