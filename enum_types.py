from enum import *


class MazeBlockType(Enum):
    EMPTY = 0
    WALL = 1
    PATH = 2
    BARRIER = 3


class BlockPickupType(Enum):
    NONE = 0
    POINT = 1
    POWER_PELLET = 2
    FRUIT = 3


class BlockWallType(Enum):
    CENTER = 0
    CORNER = 1
    SIDE = 2
    EDGE_OUTER_CORNER = 3
    EDGE_SIDE = 4
    EDGE_INNER_CORNER = 5
    EDGE_BARRIER_SIDE = 6
    EDGE_CONNECTOR_SIDE = 7
    EDGE_CONNECTOR_CORNER = 8


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


class SoundTrack(Enum):
    GAME_START = 0
    GHOST_SIREN = 1
    POINT_EATEN_1 = 2
    POINT_EATEN_2 = 3
    FRUIT_EATEN = 4
    GHOST_EATEN = 5
    SCARED_GHOST_SIREN = 6
    GHOST_RETREATING = 7
    PACMAN_DEATH = 8
    LEVEL_FINISH = 9


class SoundPlayMode(Enum):
    RESTART = 0
    LAYER = 1
    CONTINUE = 2
    TIMED = 3
