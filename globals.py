from enum import Enum

game = None
size = (0, 0)


class GameStateType(Enum):
    START_MENU = 0
    SETTING_MENU = 1
    GAME_MENU = 2
