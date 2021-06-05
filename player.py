from game_component import *
from tools import *
import globals
import pygame
from maze import *
from settings import *


class Entity(GameComponent):

    def __init__(self, speed, animation):
        super().__init__()
        self.speed = speed
        self.animator = Animator(animation)
        self.location = Point(0, 0)
        self.target_location = Point(0, 0)
        self.direction = Vector(0, 0)


class Player(Entity):

    def __init__(self, speed, animation):
        super().__init__(speed, animation)
        self.points = 0
        self.next_direction = Vector(0, 0)

    def set_start_location(self, start_location):
        self.location = start_location
        self.target_location = start_location

    def start(self):
        self.points = 0
        self.direction = Vector(0, 0)
        self.next_direction = Vector(0, 0)

    def process_events(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.next_direction = Vector(-1, 0)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.next_direction = Vector(1, 0)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.next_direction = Vector(0, 1)
            elif event.key == pygame.K_UP or event.key == pygame.K_u:
                self.next_direction = Vector(0, -1)

    def update(self):

        maze = globals.game.states.get(globals.GameStateType.GAME_MENU).maze

        if Point.distance(self.location, self.target_location) < self.speed * globals.delta_time:

            self.location = self.target_location
            if maze[self.location.x + self.next_direction.x][
                self.location.y + self.next_direction.y] == MazeBlockType.PATH:
                self.direction = self.next_direction

            if maze[self.location.x + self.direction.x][self.location.y + self.direction.y] == MazeBlockType.PATH:
                self.target_location = self.location + self.direction
                self.location += self.direction * self.speed * globals.delta_time
            else:
                self.direction = Vector(0, 0)
                self.next_direction = Vector(0, 0)

        else:
            self.location += self.direction * self.speed * globals.delta_time

    def draw(self):
        maze = globals.game.states.get(globals.GameStateType.GAME_MENU).maze
        pygame.draw.circle(globals.game.screen, (255, 255, 0),
                           (self.location.x * BLOCK_PIXEL_SIZE + int(BLOCK_PIXEL_SIZE * 1.5),
                            self.location.y * BLOCK_PIXEL_SIZE + int(BLOCK_PIXEL_SIZE * 1.5)), BLOCK_PIXEL_SIZE // 2)


class Animator(GameComponent):

    def __init__(self, animation):
        super().__init__()
        self.animation = animation
        self.current_frame = 0
        self.current_time = 0
        self.animation_time = 0

    def start(self):
        self.current_time = 0
        self.current_frame = 0

    def update(self):
        self.current_time += globals.delta_time

        if self.current_time > self.animation_time:
            self.current_time -= self.animation_time

        self.current_frame = self.animation.get_frame(self.current_time * self.animation.fps)
