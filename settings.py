from globals import GhostAIState, BlockWallType, GhostType
from tools import *

# General settings
ASPECT_RATIO = 17 / 17
START_SIZE = (1000, int(1000 // ASPECT_RATIO))
MIN_SIZE = (400, int(400 // ASPECT_RATIO))
FPS = 144

# Maze generation settings
WIDTH_TILE_COUNT = 9
HEIGHT_TILE_COUNT = 9
TILE_SCALE_FACTOR = 3
MAZE_BARRIER_Y_POSITION = 11

PIECE_PRESETS_FILE_PATH = "piece_presets.pickle"
maze_piece_shape_presets = [
    [""],
    ["L", "LU"],
    ["L", "LL", "LLU"],
    ["L", "LL", "LLU", "LLUU"],
    ["L", "LL"],
    ["L", "LL", "LLL"],
    ["U", "L", "R", "D"],
    ["U", "UU", "L", "LL", "R", "RR", "D", "DD"],
    ["U", "UU", "L", "LL", "D", "DD"],
    ["U", "R", "L"]
]

MAZE_CAGE_BOUNDS = Bounds(11, 11, 7, 4)

# Pickup settings
MAZE_POINT_RADIUS_FACTOR = 0.3
MAZE_POWER_PELLET_RADIUS_FACTOR = 0.6
POWER_PELLET_QUANTITY = 6
POINT_PICKUP_VALUE = 10

# Entity settings
ENTITY_SIZE_FACTOR = 1.5
ENTITY_COLLISION_DISTANCE = 0.8

PAC_MAN_SPEED = 6
PACMAN_ANIMATION_FRAME_RATE = 15
PACMAN_DEATH_ANIMATION_FRAME_RATE = 5

GHOST_SPEED = 5
GHOST_START_STATE = GhostAIState.SCATTER
GHOST_STATE_SCHEDULE = (15, 15, 15, 15, 15, 15)
GHOST_FRIGHTENED_DURATION = 10
GHOST_EYE_SEPARATION_FACTOR = 0.38
GHOST_EYE_VERTICAL_OFFSET_FACTOR = 0.4
GHOST_EYE_RADIUS_FACTOR = (0.13, 0.15)
GHOST_PUPIL_OFFSET_FACTOR = 0.05
GHOST_PUPIL_RADIUS_FACTOR = 0.085
GHOST_ANIMATION_FRAME_RATE = 8
GHOST_EATEN_PAUSE_TIME = 0.8


# Colors
EMPTY = (0, 0, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)

# Game Colors
MAZE_WALL_COLOUR = (0, 0, 240)
MAZE_PATH_COLOR = BLACK
MAZE_EMPTY_COLOR = BLACK
MAZE_POINT_COLOR = WHITE

GHOST_EYE_COLOR = WHITE
GHOST_PUPIL_COLOR = BLUE

FONT = "pac"
HEADER_SIZE = 48

# File Paths
BLOCK_WALL_IMAGE_FILES = {BlockWallType.CENTER: "M_WB_Center.png", BlockWallType.SIDE: "M_WB_Side.png",
                          BlockWallType.CORNER: "M_WB_Corner.png", BlockWallType.EDGE_SIDE: "M_WB_Edge_Side.png",
                          BlockWallType.EDGE_INNER_CORNER: "M_WB_Edge_Inner_Corner.png",
                          BlockWallType.EDGE_OUTER_CORNER: "M_WB_Edge_Outer_Corner.png",
                          BlockWallType.EDGE_BARRIER_SIDE: "M_WB_Edge_Barrier_Side.png",
                          BlockWallType.EDGE_CONNECTOR_SIDE: "M_WB_Edge_Connector_Side.png",
                          BlockWallType.EDGE_CONNECTOR_CORNER: "M_WB_Edge_Connector_Corner.png"}

BLOCK_BARRIER_IMAGE_FILE = "M_BB.png"

GHOST_ANIMATION_FILES = ("E_G_F0.png", "E_G_F1.png")
GHOST_FRIGHTENED_ANIMATION_FILES = ("E_FG_F0.png", "E_FG_F1.png")

PACMAN_MOVING_ANIMATION_FILES = ("E_P_F0.png", "E_P_F1.png", "E_P_F2.png", "E_P_F3.png", "E_P_F4.png", "E_P_F5.png",
                                 "E_P_F6.png", "E_P_F7.png")

PACMAN_IDLE_ANIMATION_FILES = ("E_P_F2.png",)

PACMAN_DEATH_ANIMATION_FILES = ("E_PD_F00.png", "E_PD_F01.png", "E_PD_F02.png", "E_PD_F03.png", "E_PD_F04.png",
                                "E_PD_F05.png", "E_PD_F06.png", "E_PD_F07.png", "E_PD_F08.png", "E_PD_F09.png",
                                "E_PD_F10.png", "E_PD_F11.png", "E_PD_F12.png", "E_PD_F13.png")

# Debug Settings
DISPLAY_BOUND_BORDER = True
DISPLAY_MAZE_GRIDLINES = False
DISPLAY_GHOST_TARGET = False
BOUND_BORDER_COLOR = BLUE
