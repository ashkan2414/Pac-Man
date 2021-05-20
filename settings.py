ASPECT_RATIO = 5/4
START_SIZE = (1500, int(1500//ASPECT_RATIO))
MIN_SIZE = (400, int(400//ASPECT_RATIO))
FPS = 60

WIDTH_TILE_COUNT = 9
HEIGHT_TILE_COUNT = 9

CENTER_PIECE_WIDTH = 3
CENTER_PIECE_HEIGHT = 2

BLOCK_DIVISION = 3
BLOCK_SIZE = 20


FONT = "ariel black"
HEADER_SIZE = 48

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
