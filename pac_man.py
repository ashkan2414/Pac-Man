import sys
from game_state import *

pygame.init()


class PACMAN:

    def __init__(self):
        self.screen = pygame.display.set_mode(START_SIZE, pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.states = {GameStateType.START_MENU: StartMenu(),
                       GameStateType.SETTING_MENU: SettingMenu(),
                       GameStateType.GAME_MENU: GameMenu()}

        self.current_state = None

        self.set_game_state(GameStateType.START_MENU)

        globals.size = START_SIZE

    def run(self):
        while self.running:
            self.current_state.update()
            self.clock.tick(FPS)
            pygame.display.update()
        pygame.quit()
        sys.exit()

    def set_game_state(self, state_type):

        if self.current_state is not None:
            self.current_state.end()

        new_state = self.states.get(state_type)

        if new_state is not None:
            self.current_state = new_state
            self.current_state.start()
