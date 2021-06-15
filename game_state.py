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

        maze_scale = BoundScale(0.5, 0.54, 0.95, 0.87)

        self.maze = Maze(self, maze_scale)
        self.child_game_components.append(self.maze)
        self.ghosts = {GhostType.BLINKY: Blinky(self, maze_scale),
                       GhostType.INKY: Inky(self, maze_scale),
                       GhostType.PINKY: Pinky(self, maze_scale),
                       GhostType.CLYDE: Clyde(self, maze_scale)}
        self.child_game_components += list(self.ghosts.values())
        self.pacman = Pacman(self, maze_scale)
        self.child_game_components.append(self.pacman)

        self.frightened_timer = 0
        self.pause_timer = 0

        self.score_text = Text(self, BoundScale(0.1, 0.05, 0.15, 0.04), "", WHITE, "ARIEL", 60, True)
        self.child_game_components.append(self.score_text)

    def start(self):
        self.frightened_timer = 0
        self.pause_timer = 0
        super().start()

    def pause(self, duration):
        self.set_children_pause(True)
        self.pause_timer = duration

    def ghost_eaten(self):
        self.pause(GHOST_EATEN_PAUSE_TIME)
        for ghost in self.ghosts.values():
            if ghost.current_state == GhostAIState.EATEN:
                ghost.set_pause(False)

    def pacman_death(self):
        self.pause(30)
        self.pacman.set_pause(False)

    def pacman_death_end(self):
        self.set_pause(False)
        self.frightened_timer = 0
        self.pause_timer = 0

        for component in self.child_game_components:
            if not isinstance(component, Maze):
                component.start()

    def set_frightened_mode(self):
        for ghost in self.ghosts.values():
            ghost.set_state(GhostAIState.FRIGHTENED)
        self.frightened_timer = 0

    def update(self):

        if self.pause_timer:
            self.pause_timer -= globals.delta_time
            if self.pause_timer <= 0:
                self.pause_timer = 0
                self.set_children_pause(False)
        else:
            frightened_mode = False
            for ghost in self.ghosts.values():
                if ghost.current_state == GhostAIState.FRIGHTENED:
                    frightened_mode = True
                    break

            if frightened_mode:
                self.frightened_timer += globals.delta_time
                if self.frightened_timer > GHOST_FRIGHTENED_DURATION:
                    for ghost in self.ghosts.values():
                        if ghost.current_state == GhostAIState.FRIGHTENED:
                            ghost.set_state(ghost.normal_state)
                    self.frightened_timer = 0
            else:
                self.frightened_timer = 0

            self.score_text.set_text(str(self.pacman.points))

        super().update()

    def draw(self):
        self.surface.fill(BLACK)
        super().draw()
