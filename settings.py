from globals import GhostAIState, BlockWallType

ASPECT_RATIO = 17 / 17
START_SIZE = (1000, int(1000 // ASPECT_RATIO))
MIN_SIZE = (400, int(400 // ASPECT_RATIO))
FPS = 144

WIDTH_TILE_COUNT = 9
HEIGHT_TILE_COUNT = 9

CENTER_PIECE_WIDTH = 3
CENTER_PIECE_HEIGHT = 2

TILE_SCALE_FACTOR = 3

WALL_THICKNESS_FACTOR = 0.2

MAZE_POINT_RADIUS_FACTOR = 0.3
MAZE_POWER_PELLET_RADIUS_FACTOR = 0.6

BLOCK_WALL_IMAGE_NAMES = {BlockWallType.CENTER: "M_WB_Center.png", BlockWallType.SIDE: "M_WB_Side.png",
                          BlockWallType.CORNER: "M_WB_Corner.png", BlockWallType.EDGE_SIDE: "M_WB_Edge_Side",
                          BlockWallType.EDGE_INNER_CORNER: "M_WB_Edge_Inner_Corner",
                          BlockWallType.EDGE_OUTER_CORNER: "M_WB_Edge_Outer_Corner"}

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

PAC_MAN_SPEED = 5
GHOST_SPEED = 3

GHOST_START_STATE = GhostAIState.SCATTER
GHOST_STATE_SCHEDULE = (15, 15, 15, 15, 15, 15)

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

MAZE_WALL_COLOUR = (0, 0, 240)
MAZE_PATH_COLOR = BLACK
MAZE_EMPTY_COLOR = BLACK
MAZE_POINT_COLOR = WHITE

FONT = "pac"
HEADER_SIZE = 48

# Debug Settings
DISPLAY_BOUND_BORDER = False
DISPLAY_MAZE_GRIDLINES = False
BOUND_BORDER_COLOR = BLUE
