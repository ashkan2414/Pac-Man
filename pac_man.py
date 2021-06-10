import sys
from game_state import *
from tools import *

pygame.init()


class PACMAN(GameComponent):

    def __init__(self, parent, scale):
        super().__init__(parent, scale)
        self.states = {globals.GameStateType.START_MENU: StartMenu(self, Bounds(0.5, 0.5, 1, 1)),
                       globals.GameStateType.SETTING_MENU: SettingMenu(self, Bounds(0.5, 0.5, 1, 1)),
                       globals.GameStateType.GAME_MENU: GameMenu(self, Bounds(0.5, 0.5, 1, 1))}

        self.current_state = None
        self.set_game_state(globals.GameStateType.GAME_MENU)

    def scale(self, container_bounds):
        super().scale()

    def set_game_state(self, state_type):

        if self.current_state is not None:
            self.current_state.end()
            self.child_game_components.remove(self.current_state)

        new_state = self.states.get(state_type)

        if new_state is not None:
            self.current_state = new_state
            self.child_game_components.append(self.current_state)
            self.current_state.start()
