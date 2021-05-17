from enum import Enum
from settings import *
import globals
import pygame
from gui_tools import *


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
        pass

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

    def update(self):
        for event in pygame.event.get():
            GameState.base_events(event)
