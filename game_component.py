import pygame
from tools import Bounds
from settings import *


class GameComponent:

    def __init__(self, parent, scale):
        self.parent = parent
        self.scale = scale
        self.child_game_components = []
        self.bounds = Bounds(0, 0, 500, 500)
        self.surface = pygame.Surface(self.bounds.size(), flags=pygame.SRCALPHA)

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__str__()

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
            self.surface.blit(component.surface, component.bounds.position())

        if DISPLAY_BOUND_BORDER:
            pygame.draw.rect(self.surface, RED, (0, 0, self.bounds.width, self.bounds.height), 2)

    def on_scale(self, container_bounds):
        self.bounds.width = container_bounds.width * self.scale.width
        self.bounds.height = container_bounds.height * self.scale.height
        self.bounds.x = (container_bounds.x + container_bounds.width) * self.scale.x - self.bounds.width // 2
        self.bounds.y = (container_bounds.y + container_bounds.height) * self.scale.y - self.bounds.height // 2

        self.surface = pygame.Surface(self.bounds.size(), flags=pygame.SRCALPHA)

        for component in self.child_game_components:
            component.on_scale(self.bounds)

    def end(self):
        for component in self.child_game_components:
            component.end()
