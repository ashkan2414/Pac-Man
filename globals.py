from enum import Enum

delta_time = 0
game = None
size = (0, 0)


class GameStateType(Enum):
    START_MENU = 0
    SETTING_MENU = 1
    GAME_MENU = 2


class GhostAIState(Enum):
    SCATTER = 0
    CHASE = 1
    FRIGHTENED = 2
    EATEN = 3


class GhostType(Enum):
    BLINKY = 0
    BINKY = 1
    INKY = 2
    CLYDE = 3
