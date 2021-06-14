from globals import GhostAIState, BlockWallType, GhostType

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

# Pickup settings
MAZE_POINT_RADIUS_FACTOR = 0.3
MAZE_POWER_PELLET_RADIUS_FACTOR = 0.6
POWER_PELLET_QUANTITY = 5

# Entity settings
ENTITY_SIZE_FACTOR = 1.5

PAC_MAN_SPEED = 5

GHOST_SPEED = 3

GHOST_START_STATE = GhostAIState.SCATTER
GHOST_STATE_SCHEDULE = (15, 15, 15, 15, 15, 15)

GHOST_EYE_SEPARATION_FACTOR = 0.38
GHOST_EYE_VERTICAL_OFFSET_FACTOR = 0.4
GHOST_EYE_RADIUS_FACTOR = (0.13, 0.15)
GHOST_PUPIL_OFFSET_FACTOR = 0.05
GHOST_PUPIL_RADIUS_FACTOR = 0.085

GHOST_ANIMATION_FRAME_RATE = 8

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
GHOST_FRIGHTENED_ANIMATION_FILES = ("E_G_F0.png", "E_G_F1.png")

# Debug Settings
DISPLAY_BOUND_BORDER = False
DISPLAY_MAZE_GRIDLINES = True
DISPLAY_GHOST_TARGET = False
BOUND_BORDER_COLOR = BLUE
