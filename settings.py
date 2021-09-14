from enum_types import *
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
MAZE_WIDTH = WIDTH_TILE_COUNT * TILE_SCALE_FACTOR + 3
MAZE_HEIGHT = HEIGHT_TILE_COUNT * TILE_SCALE_FACTOR + 3
maze_piece_shape_presets = [
    [""],
    ["L", "LU"],
    ["L", "LL", "LLU"],
    ["L", "LL", "LLU", "LLUU"],
    ["L", "D", "DR"],
    ["L", "LL"],
    ["U", "L", "R", "D"],
    ["U", "UU", "L", "LL", "R", "RR", "D", "DD"],
    ["U", "UU", "L", "LL", "D", "DD"],
    ["U", "R", "L"]
]

MAZE_CAGE_BOUNDS = Bounds(11, 11, 7, 4)
GHOST_CAGE_EXIT = Point(14, 10)

# Pickup settings
MAZE_POINT_RADIUS_FACTOR = 0.3
MAZE_POWER_PELLET_RADIUS_FACTOR = 0.6
POWER_PELLET_QUANTITY = 6
POWER_PELLET_MAX_X = 8
POINT_PICKUP_VALUE = 10
POWER_PELLET_PICKUP_VALUE = 50
FRUIT_PICKUP_VALUE = 400
FRUIT_SPAWN_CHANCE = 1
FRUIT_COOLDOWN_DURATION = 20

# General game settings
DEFAULT_POINTS_DIGITS = 4
PACMAN_LIVES = 3
GAME_START_DURATION = 4
GHOST_EATEN_PAUSE_DURATION = 0.8
LEVEL_FINISH_DURATION = 4
GAME_OVER_DURATION = 3
INITIAL_GHOST_POINT_VALUE = 200

# Entity settings
ENTITY_SIZE_FACTOR = 1.5
ENTITY_COLLISION_DISTANCE = 0.8

# Pacman settings
PAC_MAN_SPEED = 8
PACMAN_SPAWN_DISTANCE_THRESHOLD = 10
PACMAN_ANIMATION_FRAME_RATE = 15
PACMAN_DEATH_ANIMATION_FRAME_RATE = 5
PACMAN_DEATH_SOUND_DELAY = 0.65

# Ghost settings
GHOST_SPEED = 5
GHOST_START_STATE = GhostAIState.SCATTER
GHOST_STATE_SCHEDULE = (15, 15, 15, 15, 15, 15)
GHOST_FRIGHTENED_DURATION = 10
GHOST_EYE_SEPARATION_FACTOR = 0.38
GHOST_EYE_VERTICAL_OFFSET_FACTOR = 0.4
GHOST_EYE_RADIUS_FACTOR = (0.13, 0.15)
GHOST_PUPIL_OFFSET_FACTOR = (0.05, 0.07)
GHOST_PUPIL_RADIUS_FACTOR = 0.09
GHOST_ANIMATION_FRAME_RATE = 8

# Events
GAME_START = pygame.USEREVENT + 1
FRIGHTENED_MODE_START = pygame.USEREVENT + 2
FRIGHTENED_MODE_END = pygame.USEREVENT + 3
GHOST_EATEN_START = pygame.USEREVENT + 4
GHOST_EATEN_END = pygame.USEREVENT + 5
PACMAN_DEATH = pygame.USEREVENT + 6
LEVEL_RESET = pygame.USEREVENT + 7
LEVEL_FINISH = pygame.USEREVENT + 8
NEXT_LEVEL = pygame.USEREVENT + 9
GAME_OVER = pygame.USEREVENT + 10
RETURN_TO_START = pygame.USEREVENT + 11
FRUIT_SPAWN_READY = pygame.USEREVENT + 12

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
MAZE_PATH_COLOR = BLACK
MAZE_EMPTY_COLOR = BLACK
MAZE_POINT_COLOR = WHITE
GHOST_EYE_COLOR = WHITE
GHOST_PUPIL_COLOR = BLUE

# UI Settings
FONT_NAME = "Joystix"


# Files and file paths

SAVE_FILE_PATH = "Saves"
PIECE_PRESETS_FILE = "piece_presets.pickle"
HIGHSCORE_FILE = "highscore.pickle"


BUTTON_FILE_PATH = "Assets\\Button"
START_BUTTON_FILE_PATH = os.path.join(BUTTON_FILE_PATH, "Start Button")
START_BUTTON_NORMAL_ANIMATION = (START_BUTTON_FILE_PATH, "Start_Button_Normal")
START_BUTTON_HOVER_ANIMATION = (START_BUTTON_FILE_PATH, "Start_Button_Hover")

QUIT_BUTTON_FILE_PATH = os.path.join(BUTTON_FILE_PATH, "Quit Button")
QUIT_BUTTON_NORMAL_ANIMATION = (QUIT_BUTTON_FILE_PATH, "Quit_Button_Normal")
QUIT_BUTTON_HOVER_ANIMATION = (QUIT_BUTTON_FILE_PATH, "Quit_Button_Hover")

GHOST_FILE_PATH = "Assets\\Entity\\Ghost"
GHOST_NORMAL_ANIMATION = (GHOST_FILE_PATH, "Normal_Ghost")
GHOST_FRIGHTENED_ANIMATION = (GHOST_FILE_PATH, "Frightened_Ghost")

PACMAN_FILE_PATH = "Assets\\Entity\\Pacman"
PACMAN_MOVING_ANIMATION = (PACMAN_FILE_PATH, "Pacman_Moving")
PACMAN_IDLE_ANIMATION = (PACMAN_FILE_PATH, "Pacman_Idle")
PACMAN_DEATH_ANIMATION = (PACMAN_FILE_PATH, "Pacman_Death")


MAZE_FILE_PATH = "Assets\\Maze"
BLOCK_WALL_IMAGES = {BlockWallType.CENTER: "Wall_Block_Center.png", BlockWallType.SIDE: "Wall_Block_Side.png",
                     BlockWallType.CORNER: "Wall_Block_Corner.png", BlockWallType.EDGE_SIDE: "Wall_Block_Edge_Side.png",
                     BlockWallType.EDGE_INNER_CORNER: "Wall_Block_Edge_Inner_Corner.png",
                     BlockWallType.EDGE_OUTER_CORNER: "Wall_Block_Edge_Outer_Corner.png",
                     BlockWallType.EDGE_BARRIER_SIDE: "Wall_Block_Edge_Barrier_Side.png",
                     BlockWallType.EDGE_CONNECTOR_SIDE: "Wall_Block_Edge_Connector_Side.png",
                     BlockWallType.EDGE_CONNECTOR_CORNER: "Wall_Block_Edge_Connector_Corner.png"}
BLOCK_BARRIER_IMAGE = "Barrier_Block.png"
FRUIT_IMAGE = "Fruit.png"

ICON_FILE_PATH = "Assets\\Icons"
PACMAN_LIFE_ICON_IMAGE = "Pacman_Life_Icon.png"
START_MENU_TITLE_LOGO = "Start_Menu_Title_Logo.png"


SOUND_FILE_PATH = "Assets\\Sounds"
SOUND_FILES = {SoundTrack.SCARED_GHOST_SIREN: "Scared_Ghost_Siren.wav", SoundTrack.GHOST_EATEN: "Ghost_Eaten.wav",
               SoundTrack.GAME_START: "Game_Start.wav", SoundTrack.GHOST_SIREN: "Ghost_Siren.wav",
               SoundTrack.POINT_EATEN_1: "Point_Eaten_1.wav", SoundTrack.POINT_EATEN_2: "Point_Eaten_2.wav",
               SoundTrack.FRUIT_EATEN: "Fruit_Eaten.wav", SoundTrack.GHOST_RETREATING: "Ghost_Retreating.wav",
               SoundTrack.PACMAN_DEATH: "Pacman_Death.wav", SoundTrack.LEVEL_FINISH: "Level_Finish.wav"}

SOUND_VOLUME = {SoundTrack.SCARED_GHOST_SIREN: 0.5, SoundTrack.GHOST_EATEN: 1, SoundTrack.GAME_START: 0.8,
                SoundTrack.GHOST_SIREN: 1,
                SoundTrack.POINT_EATEN_1: 0.5, SoundTrack.POINT_EATEN_2: 0.5, SoundTrack.FRUIT_EATEN: 1,
                SoundTrack.GHOST_RETREATING: 0.8,
                SoundTrack.PACMAN_DEATH: 1, SoundTrack.LEVEL_FINISH: 1}


# Debug Settings
DISPLAY_BOUND_BORDER = False
DISPLAY_MAZE_GRIDLINES = False
DISPLAY_GHOST_TARGET = False
BOUND_BORDER_COLOR = BLUE
