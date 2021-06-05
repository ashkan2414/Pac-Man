ASPECT_RATIO = 5/4
START_SIZE = (1500, int(1500//ASPECT_RATIO))
MIN_SIZE = (400, int(400//ASPECT_RATIO))
FPS = 144

WIDTH_TILE_COUNT = 9
HEIGHT_TILE_COUNT = 9

CENTER_PIECE_WIDTH = 3
CENTER_PIECE_HEIGHT = 2

TILE_SCALE_FACTOR = 3
BLOCK_PIXEL_SIZE = 30


PAC_MAN_SPEED = 5


FONT = "ariel black"
HEADER_SIZE = 48

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


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)
