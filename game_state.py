import globals
from game_component import GameComponent
from maze import *
from entity import *


class GameState(GameComponent):

    def __init__(self, bounds, state_type):
        super().__init__(bounds)
        self.type = state_type


class StartMenu(GameState):

    def __init__(self, bounds):
        super().__init__(bounds, globals.GameStateType.START_MENU)

    def process_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                globals.game.set_game_state(globals.GameStateType.GAME_MENU)

        super().process_events(event)

    def draw(self):
        super().draw()


class SettingMenu(GameState):

    def __init__(self, bounds):
        super().__init__(bounds, globals.GameStateType.SETTING_MENU)


class GameMenu(GameState):

    def __init__(self, bounds):
        super().__init__(bounds, globals.GameStateType.GAME_MENU)

        maze_bounds = Bounds(bounds.x + BLOCK_PIXEL_SIZE, bounds.y + BLOCK_PIXEL_SIZE, 0, 0)
        maze_bounds.width = globals.size[0] - maze_bounds.x
        maze_bounds.height = globals.size[1] - maze_bounds.y

        self.maze = Maze(maze_bounds)
        self.child_game_components.append(self.maze)
        self.player = Player(maze_bounds, PAC_MAN_SPEED, None)
        self.child_game_components.append(self.player)
        self.enemy = Enemy(maze_bounds, 5, None)
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

    def process_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
                # self.maze = generate_maze()

        super().process_events(event)

    def draw(self):
        globals.game.screen.fill(WHITE)

        super().draw()
