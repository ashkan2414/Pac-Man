import copy
from enum import Enum
from timeit import default_timer as timer

import globals
from settings import *
from tools import *
from maze import *


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
        super().__init__(globals.GameStateType.START_MENU)

    def update(self):
        for event in pygame.event.get():
            GameState.default_events(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    globals.game.set_game_state(globals.GameStateType.GAME_MENU)

        GUITools.draw_text("PAC-MAN", globals.game.screen, [globals.size[0] // 2, 100],
                           FONT, HEADER_SIZE, (170, 130, 60))


class SettingMenu(GameState):

    def __init__(self):
        super().__init__(globals.GameStateType.SETTING_MENU)

    def update(self):
        for event in pygame.event.get():
            GameState.default_events(event)


class GameMenu(GameState):

    def __init__(self):
        super().__init__(globals.GameStateType.GAME_MENU)
        self.maze = generate_maze()

    def events(self):
        for event in pygame.event.get():
            GameState.default_events(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.maze = generate_maze()

    def draw(self):

        super().draw()

        for x in range(len(self.maze)):
            for y in range(len(self.maze[x])):

                block_type = self.maze[x][y]
                if block_type == MazeBlockType.WALL:
                    color = (10, 10, 10)
                elif block_type == MazeBlockType.PATH:
                    color = (65, 65, 65)
                else:
                    color = WHITE

                pygame.draw.rect(globals.game.screen, color,
                                 (x * BLOCK_SIZE + BLOCK_SIZE, y * BLOCK_SIZE + BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        color = (100, 100, 100)
        for x in range(len(self.maze) + 1):
            pygame.draw.line(globals.game.screen, color, (x * BLOCK_SIZE + BLOCK_SIZE, BLOCK_SIZE),
                             (x * BLOCK_SIZE + BLOCK_SIZE, (len(self.maze[0]) + 1) * BLOCK_SIZE))

        for y in range(len(self.maze[0]) + 1):
            pygame.draw.line(globals.game.screen, color, (BLOCK_SIZE, y * BLOCK_SIZE + BLOCK_SIZE),
                             ((len(self.maze) + 1) * BLOCK_SIZE, y * BLOCK_SIZE + BLOCK_SIZE))
