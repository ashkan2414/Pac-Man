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

        maze_scale = Bounds(0.5, 0.56, 0.96, 0)
        maze_scale.height = maze_scale.width * ASPECT_RATIO * (30/32)

        print(maze_scale)

        self.maze = Maze(self, maze_scale)
        self.child_game_components.append(self.maze)
        self.player = Player(self, maze_scale, PAC_MAN_SPEED, None)
        self.child_game_components.append(self.player)
        self.enemy = Enemy(self, maze_scale, GHOST_SPEED, None)
        self.child_game_components.append(self.enemy)

    def start(self):
        self.maze.generate_maze()

        x = random.randrange(0, self.maze.width - 1)
        y = random.randrange(0, self.maze.height - 1)
        while self.maze[x][y] != MazeBlockType.PATH:
            x = random.randrange(0, self.maze.width - 1)
            y = random.randrange(0, self.maze.height - 1)
        self.player.set_start_location(Point(x, y))

        x = random.randrange(0, self.maze.width - 1)
        y = random.randrange(0, self.maze.height - 1)
        while self.maze[x][y] != MazeBlockType.PATH:
            x = random.randrange(0, self.maze.width - 1)
            y = random.randrange(0, self.maze.height - 1)
        self.enemy.set_start_location(Point(x, y))

        super().start()

    def draw(self):
        self.surface.fill(BLACK)
        super().draw()
