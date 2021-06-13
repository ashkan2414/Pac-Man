import pygame
from tools import Bounds
from settings import *


class GameComponent:

    def __init__(self, parent, scale):
        self.parent = parent
        self.scale = scale
        self.enabled = True
        self.child_game_components = []
        self.bounds = Bounds(0, 0, 500, 500)
        self.surface = pygame.Surface(self.bounds.size(), flags=pygame.SRCALPHA)
        self.aspect_ratio = None
        self.as_bounds = None

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__str__()

    def start(self):
        for component in self.child_game_components:
            if component.enabled:
                component.start()

    def process_events(self, event):
        for component in self.child_game_components:
            if component.enabled:
                component.process_events(event)

    def update(self):
        for component in self.child_game_components:
            if component.enabled:
                component.update()

    def draw(self):
        for component in self.child_game_components:
            if component.enabled:
                component.draw()
                self.surface.blit(component.surface, component.as_bounds.position())

                if DISPLAY_BOUND_BORDER:
                    pygame.draw.rect(self.surface, RED, component.bounds, 2)
                    pygame.draw.rect(self.surface, YELLOW, component.as_bounds, 2)

    def on_scale(self, container_bounds):
        self.bounds.width = container_bounds.width * self.scale.width
        self.bounds.height = container_bounds.height * self.scale.height
        self.bounds.x = (container_bounds.x + container_bounds.width) * self.scale.x - self.bounds.width / 2
        self.bounds.y = (container_bounds.y + container_bounds.height) * self.scale.y - self.bounds.height / 2

        self.as_bounds = self.bounds.copy()
        if self.aspect_ratio:
            if self.aspect_ratio < self.bounds.aspect_ratio():
                self.as_bounds.width = self.bounds.height * self.aspect_ratio
                self.as_bounds.x += (self.bounds.width-self.as_bounds.width)/2
            elif self.aspect_ratio > self.bounds.aspect_ratio():
                self.as_bounds.height = self.bounds.width / self.aspect_ratio
                self.as_bounds.y += (self.bounds.height - self.as_bounds.height) / 2

        self.surface = pygame.Surface(self.as_bounds.size(), flags=pygame.SRCALPHA)

        for component in self.child_game_components:
            component.on_scale(self.bounds)

    def end(self):
        for component in self.child_game_components:
            component.end()

    def set_enable(self, state):
        self.enabled = state
        for component in self.child_game_components:
            component.set_enable(state)
