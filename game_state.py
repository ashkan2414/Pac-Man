import globals
from game_component import GameComponent
from maze import *
from entity import *


class GameState(GameComponent):

    def __init__(self, parent, scale, state_type):
        super().__init__(parent, scale)
        self.type = state_type


class StartMenu(GameState):

    def __init__(self, parent, scale):
        super().__init__(parent, scale, globals.GameStateType.START_MENU)


class SettingMenu(GameState):

    def __init__(self, parent, scale):
        super().__init__(parent, scale, globals.GameStateType.SETTING_MENU)


class GameMenu(GameState):

    def __init__(self, parent, scale):
        super().__init__(parent, scale, globals.GameStateType.GAME_MENU)

        maze_scale = Bounds(0.5, 0.50, 0.96, 0)
        maze_scale.height = maze_scale.width * ASPECT_RATIO

        self.maze = Maze(self, maze_scale)
        self.child_game_components.append(self.maze)
        self.pacman = Pacman(self, maze_scale, PAC_MAN_SPEED, None)
        self.child_game_components.append(self.pacman)
        self.ghosts = {GhostType.BLINKY: Blinky(self, maze_scale, GHOST_SPEED, None),
                       GhostType.INKY: Inky(self, maze_scale, GHOST_SPEED, None),
                       GhostType.BINKY: Binky(self, maze_scale, GHOST_SPEED, None),
                       GhostType.CLYDE: Clyde(self, maze_scale, GHOST_SPEED, None)}
        self.child_game_components += list(self.ghosts.values())

    def start(self):
        self.maze.generate_maze()

        print(self.maze.width, self.maze.height)
        super().start()

    def draw(self):
        self.surface.fill(BLACK)
        super().draw()
