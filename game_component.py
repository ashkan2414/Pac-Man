import pygame


class GameComponent:

    def __init__(self, bounds):
        self.child_game_components = []
        self.bounds = bounds

    def start(self):
        for component in self.child_game_components:
            component.start()

    def process_events(self, event):
        for component in self.child_game_components:
            component.process_events(event)

    def update(self):
        for component in self.child_game_components:
            component.update()

    def draw(self):
        for component in self.child_game_components:
            component.draw()

    def end(self):
        for component in self.child_game_components:
            component.end()