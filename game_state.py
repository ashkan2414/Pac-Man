import globals
from game_component import GameComponent
from maze import *
from entity import *
from ui_elements import *


class StartMenu(GameComponent):

    def __init__(self, parent, scale):
        super().__init__(parent, scale)

        self.start_button = Button(self, BoundScale(0.5, 0.5, 0.2, 0.1), pygame.image.load("B_GameStart.png"),
                                   func=self.start_game)
        self.child_game_components.append(self.start_button)

    @staticmethod
    def start_game():
        globals.game.set_game_state(globals.GameStateType.GAME_MENU)

    def draw(self):
        self.surface.fill(BLACK)
        super().draw()


class SettingMenu(GameComponent):

    def __init__(self, parent, scale):
        super().__init__(parent, scale)


class GameMenu(GameComponent):

    def __init__(self, parent, scale):
        super().__init__(parent, scale)

        maze_scale = BoundScale(0.5, 0.53, 0.95, 0.83)

        self.maze = Maze(self, maze_scale)
        self.child_game_components.append(self.maze)
        self.pacman = Pacman(self, maze_scale)
        self.child_game_components.append(self.pacman)
        self.ghosts = {GhostType.BLINKY: Blinky(self, maze_scale),
                       GhostType.INKY: Inky(self, maze_scale),
                       GhostType.PINKY: Pinky(self, maze_scale),
                       GhostType.CLYDE: Clyde(self, maze_scale)}
        self.child_game_components += list(self.ghosts.values())

    def draw(self):
        self.surface.fill(BLACK)
        super().draw()
