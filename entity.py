from game_component import *
from tools import *
import globals
import pygame
from maze import *
from settings import *


class Entity(GameComponent):

    def __init__(self, bounds, speed, animation):
        super().__init__(bounds)
        self.speed = speed
        self.animator = Animator(bounds, animation)
        self.location = Point(0, 0)
        self.target_location = Point(0, 0)
        self.direction = Vector(0, 0)
        self.maze = None

    def set_start_location(self, start_location):
        self.location = start_location
        self.target_location = start_location

    def start(self):
        self.maze = globals.game.states.get(globals.GameStateType.GAME_MENU).maze
        super().start()

    def update(self):
        self.location += self.direction * self.speed * globals.delta_time
        super().update()


class Player(Entity):

    def __init__(self, bounds, speed, animation):
        super().__init__(bounds, speed, animation)
        self.points = 0
        self.next_direction = Vector(0, 0)
        print(globals.size)
        self.surface = pygame.Surface((self.bounds.width, self.bounds.height), flags=pygame.SRCALPHA)

    def start(self):
        self.points = 0
        self.direction = Vector(0, 0)
        self.next_direction = Vector(0, 0)
        super().start()

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

        super().process_events(event)

    def update(self):

        if Point.distance(self.location, self.target_location) < self.speed * globals.delta_time:

            self.location = self.target_location
            if self.maze.point(self.location + self.next_direction) == MazeBlockType.PATH:
                self.direction = self.next_direction

            if self.maze.point(self.location + self.direction) == MazeBlockType.PATH:
                self.target_location = self.location + self.direction
            else:
                self.direction = Vector(0, 0)
                self.next_direction = Vector(0, 0)

        super().update()

    def draw(self):
        self.surface.fill((255, 255, 255, 0))
        pygame.draw.circle(self.surface, (255, 255, 0),
                           (self.location.x * BLOCK_PIXEL_SIZE + BLOCK_PIXEL_SIZE // 2,
                            self.location.y * BLOCK_PIXEL_SIZE + BLOCK_PIXEL_SIZE // 2),
                           BLOCK_PIXEL_SIZE // 2)
        globals.game.screen.blit(self.surface, (self.bounds.x, self.bounds.y))


class Enemy(Entity):

    def __init__(self, bounds, speed, animation):
        super().__init__(bounds, speed, animation)
        self.player = None

    def start(self):
        self.player = globals.game.states.get(globals.GameStateType.GAME_MENU).player
        super().start()

    def update(self):

        if Point.distance(self.location, self.target_location) < self.speed * globals.delta_time:
            self.location = self.target_location
            path = self.get_path(Point.rounded(self.player.location))
            if not path or len(path) == 1:
                self.target_location = self.location
            else:
                self.target_location = path[1]
            self.direction = self.target_location - self.location

        super().update()

    def draw(self):
        pygame.draw.circle(globals.game.screen, (255, 0, 0),
                           (self.location.x * BLOCK_PIXEL_SIZE + int(BLOCK_PIXEL_SIZE * 1.5),
                            self.location.y * BLOCK_PIXEL_SIZE + int(BLOCK_PIXEL_SIZE * 1.5)), BLOCK_PIXEL_SIZE // 2)

    def get_path(self, target):
        open_nodes = [ASNode(self.location, 0, Point.distance(self.location, target))]
        closed_nodes = []

        def lowest_f_score(nodes):
            result = nodes[0]

            for node in nodes:
                if node.f < result.f:
                    result = node
            return result

        def construct_path(end_node):

            path = [end_node.location]

            current_node = end_node
            while current_node.parent:
                path.append(current_node.parent.location)
                current_node = current_node.parent
            path.reverse()
            return path

        while open_nodes:
            current_node = lowest_f_score(open_nodes)
            if current_node.location == target:
                return construct_path(current_node)

            open_nodes.remove(current_node)
            closed_nodes.append(current_node)

            for node in current_node.neighbours():
                if node not in closed_nodes and self.maze.point(node.location) == MazeBlockType.PATH:
                    if node not in open_nodes:
                        node.calculate_h(target)
                        node.calculate_f()
                        open_nodes.append(node)
                    else:
                        existing_node = open_nodes[open_nodes.index(node)]
                        if node.g < existing_node.g:
                            existing_node.g = node.g
                            existing_node.calculate_f()
                            existing_node.parent = current_node

        return False


class ASNode:

    def __init__(self, location, g=0, h=0, parent=None):
        self.location = location
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.parent = parent

    def __eq__(self, other):
        return self.location == other.location

    def __str__(self):
        return str(self.location)

    def __repr__(self):
        return str(self.location)

    def neighbours(self):
        neighbour_nodes = []
        neighbour_nodes.append(ASNode(self.location - Point(1, 0), self.g + 1, 0, self))
        neighbour_nodes.append(ASNode(self.location - Point(-1, 0), self.g + 1, 0, self))
        neighbour_nodes.append(ASNode(self.location - Point(0, 1), self.g + 1, 0, self))
        neighbour_nodes.append(ASNode(self.location - Point(0, -1), self.g + 1, 0, self))
        return neighbour_nodes

    def calculate_h(self, target_location):
        self.h = Point.distance(self.location, target_location)

    def calculate_f(self):
        self.f = self.g + self.h


class Animator(GameComponent):

    def __init__(self, bounds, animation):
        super().__init__(bounds)
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
