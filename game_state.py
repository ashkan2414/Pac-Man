import globals
from game_component import GameComponent
from maze import *
from player import *


class GameState(GameComponent):

    def __init__(self, state_type):
        super().__init__()
        self.type = state_type


class StartMenu(GameState):

    def __init__(self):
        super().__init__(globals.GameStateType.START_MENU)

    def process_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                globals.game.set_game_state(globals.GameStateType.GAME_MENU)

        super().process_events(event)

    def draw(self):
        GUITools.draw_text("PAC-MAN", globals.game.screen, [globals.size[0] // 2, 100],
                           FONT, HEADER_SIZE, (170, 130, 60))

        super().draw()


class SettingMenu(GameState):

    def __init__(self):
        super().__init__(globals.GameStateType.SETTING_MENU)


class GameMenu(GameState):

    def __init__(self):
        super().__init__(globals.GameStateType.GAME_MENU)
        self.maze = Maze()

        self.player = Player(PAC_MAN_SPEED, None)
        self.child_game_components.append(self.player)

    def start(self):
        self.maze.generate_maze()

        path_found = False

        for x in range(self.maze.width):
            for y in range(self.maze.height):
                if self.maze[x][y] == MazeBlockType.PATH:
                    self.player.set_start_location(Point(x, y))
                    path_found = True
                    break

            if path_found:
                break

        super().start()

    def process_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
                # self.maze = generate_maze()

        super().process_events(event)

    def draw(self):
        globals.game.screen.fill(WHITE)
        for x in range(self.maze.width):
            for y in range(self.maze.height):

                block_type = self.maze[x][y]
                if block_type == MazeBlockType.WALL:
                    color = (10, 10, 10)
                elif block_type == MazeBlockType.PATH:
                    color = (65, 65, 65)
                else:
                    color = WHITE

                pygame.draw.rect(globals.game.screen, color,
                                 (x * BLOCK_PIXEL_SIZE + BLOCK_PIXEL_SIZE, y * BLOCK_PIXEL_SIZE + BLOCK_PIXEL_SIZE,
                                  BLOCK_PIXEL_SIZE, BLOCK_PIXEL_SIZE))

        color = (100, 100, 100)
        for x in range(self.maze.width + 1):
            pygame.draw.line(globals.game.screen, color, (x * BLOCK_PIXEL_SIZE + BLOCK_PIXEL_SIZE, BLOCK_PIXEL_SIZE),
                             (x * BLOCK_PIXEL_SIZE + BLOCK_PIXEL_SIZE, (self.maze.height + 1) * BLOCK_PIXEL_SIZE))

        for y in range(self.maze.height + 1):
            pygame.draw.line(globals.game.screen, color, (BLOCK_PIXEL_SIZE, y * BLOCK_PIXEL_SIZE + BLOCK_PIXEL_SIZE),
                             ((self.maze.width + 1) * BLOCK_PIXEL_SIZE, y * BLOCK_PIXEL_SIZE + BLOCK_PIXEL_SIZE))

        super().draw()
