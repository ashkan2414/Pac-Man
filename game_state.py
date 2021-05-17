from enum import Enum
from settings import *
import globals
import pygame


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


class StartMenu(GameState):

    def __init__(self):
        super().__init__(GameStateType.START_MENU)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                globals.game.running = False


class SettingMenu(GameState):

    def __init__(self):
        super().__init__(GameStateType.SETTING_MENU)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                globals.game.running = False


class GameMenu(GameState):

    def __init__(self):
        super().__init__(GameStateType.GAME_MENU)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                globals.game.running = False
