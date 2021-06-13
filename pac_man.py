import sys
from game_state import *
from tools import *

pygame.init()


class PACMAN(GameComponent):

    def __init__(self, parent, scale, screen_bounds):
        super().__init__(parent, scale)
        self.states = {globals.GameStateType.START_MENU: StartMenu(self, BoundScale(0.5, 0.5, 1, 1)),
                       globals.GameStateType.SETTING_MENU: SettingMenu(self, BoundScale(0.5, 0.5, 1, 1)),
                       globals.GameStateType.GAME_MENU: GameMenu(self, BoundScale(0.5, 0.5, 1, 1))}

        self.child_game_components = list(self.states.values())

        for component in self.child_game_components:
            component.set_enable(False)

        self.current_state = None
        self.on_scale(screen_bounds)
        self.set_game_state(globals.GameStateType.START_MENU)

    def set_game_state(self, state_type):

        if self.current_state is not None:
            self.current_state.end()
            self.current_state.set_enable(False)

        new_state = self.states.get(state_type)

        if new_state is not None:
            self.current_state = new_state
            self.current_state.set_enable(True)
            self.current_state.start()
