from enum import Enum

delta_time = 0
game = None
size = (0, 0)


class MazeBlockType(Enum):
    EMPTY = 0
    WALL = 1
    PATH = 2


class BlockPickupType(Enum):
    NONE = 0
    POINT = 1
    POWER_PELLET = 2


class BlockWallType(Enum):
    CENTER = 0
    CORNER = 1
    SIDE = 2
    EDGE_OUTER_CORNER = 3
    EDGE_SIDE = 4
    EDGE_INNER_CORNER = 5


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
    PINKY = 1
    INKY = 2
    CLYDE = 3


class ButtonState(Enum):
    NORMAL = 0
    HOVER = 1
    CLICKED = 2
