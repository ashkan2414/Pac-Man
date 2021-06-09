import sys
from game_state import *

pygame.init()


class PACMAN(GameComponent):

    def __init__(self, bounds):
        super().__init__(bounds)
        self.screen = pygame.display.set_mode(bounds.size(), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True

        globals.game = self
        globals.size = bounds.size()

        self.states = {globals.GameStateType.START_MENU: StartMenu(bounds),
                       globals.GameStateType.SETTING_MENU: SettingMenu(bounds),
                       globals.GameStateType.GAME_MENU: GameMenu(bounds)}

        self.current_state = None
        self.set_game_state(globals.GameStateType.GAME_MENU)


    def run(self):
        while self.running:
            globals.delta_time = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                self.process_events(event)
            self.update()
            self.draw()
            pygame.display.update()

        # Exit the program
        pygame.quit()
        sys.exit()

    def process_events(self, event):
        if event.type == pygame.QUIT:
            globals.game.running = False
        if event.type == pygame.VIDEORESIZE:
            new_size = list(event.dict['size'])

            if new_size[0] < MIN_SIZE[0]:
                new_size[0] = MIN_SIZE[0]
            if new_size[1] < MIN_SIZE[1]:
                new_size[1] = MIN_SIZE[1]

            size_change = (abs(new_size[0] - globals.size[0]), abs(new_size[1] - globals.size[1]))
            if size_change[0] > size_change[1]:
                new_size[1] = int(new_size[0] // ASPECT_RATIO)
            else:
                new_size[0] = int(new_size[1] * ASPECT_RATIO)

            self.screen = pygame.display.set_mode(new_size, pygame.RESIZABLE)
            globals.size = tuple(new_size)

        super().process_events(event)

    def update(self):
        super().update()

    def set_game_state(self, state_type):

        if self.current_state is not None:
            self.current_state.end()
            self.child_game_components.remove(self.current_state)

        new_state = self.states.get(state_type)

        if new_state is not None:
            self.current_state = new_state
            self.child_game_components.append(self.current_state)
            self.current_state.start()
