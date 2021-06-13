import globals
from maze import *
from settings import *
from globals import GhostType


class Entity(GameComponent):

    speed = 5

    def __init__(self, parent, scale):
        super().__init__(parent, scale)
        self.location = Point(0, 0)
        self.block_target = Point(0, 0)
        self.direction = Vector(0, 0)
        self.maze = self.parent.maze
        self.aspect_ratio = self.maze.aspect_ratio

    def set_start_location(self, start_location):
        self.location = start_location
        self.block_target = start_location

    def start(self):
        x = random.randrange(0, self.maze.width - 1)
        y = random.randrange(0, self.maze.height - 1)
        while self.maze[x][y] != MazeBlockType.PATH:
            x = random.randrange(0, self.maze.width - 1)
            y = random.randrange(0, self.maze.height - 1)

        self.location = Point(x, y)
        self.block_target = self.location

        super().start()

    def update(self):
        self.location += self.direction * self.speed * globals.delta_time
        super().update()

    def on_scale(self, container_bounds):
        super().on_scale(container_bounds)
        self.location = self.block_target

    def on_block(self):
        return Point.distance(self.location, self.block_target) < self.speed * globals.delta_time


class Pacman(Entity):

    speed = PAC_MAN_SPEED

    def __init__(self, parent, scale):
        super().__init__(parent, scale)
        self.points = 0
        self.next_direction = Vector(0, 0)

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

        if self.on_block():
            self.location = self.block_target
            if self.maze.point(self.location + self.next_direction) == MazeBlockType.PATH:
                self.direction = self.next_direction

            if self.maze.point(self.location + self.direction) == MazeBlockType.PATH:
                self.block_target = self.location + self.direction
            else:
                self.direction = Vector(0, 0)
                self.next_direction = Vector(0, 0)

        super().update()

    def draw(self):
        self.surface.fill(EMPTY)
        pygame.draw.circle(self.surface, (255, 255, 0),
                           (self.location.x * self.maze.block_pixel_size + self.maze.block_pixel_size // 2,
                            self.location.y * self.maze.block_pixel_size + self.maze.block_pixel_size // 2),
                           self.maze.block_pixel_size // 2)

        super().draw()


class Ghost(Entity):
    speed = GHOST_SPEED
    scatter_target = None
    color = None
    ghost_type = None

    def __init__(self, parent, scale):
        super().__init__(parent, scale)
        self.pacman = None
        self.ghosts = None
        self.current_state = GHOST_START_STATE
        self.normal_state = GHOST_START_STATE
        self.state_timer = 0
        self.state_schedule_index = 0
        self.turn_around = False
        self.target_location = Point(0, 0)
        self.state_method_table = {GhostAIState.SCATTER: self.scatter_state,
                                   GhostAIState.CHASE: self.chase_state,
                                   GhostAIState.FRIGHTENED: self.frightened_state,
                                   GhostAIState.EATEN: self.eaten_state}

    def start(self):
        self.pacman = self.parent.pacman
        self.ghosts = self.parent.ghosts
        self.current_state = GHOST_START_STATE
        self.normal_state = GHOST_START_STATE
        self.state_timer = 0
        self.state_schedule_index = 0
        self.direction = Vector(1, 0)
        self.turn_around = False
        super().start()

    def update(self):

        if self.current_state not in (GhostAIState.FRIGHTENED, GhostAIState.EATEN):
            self.state_timer += globals.delta_time

            if self.state_timer > GHOST_STATE_SCHEDULE[self.state_schedule_index] and self.state_schedule_index < len(
                    GHOST_STATE_SCHEDULE) - 1:
                self.state_timer = 0
                if self.current_state == GhostAIState.SCATTER:
                    self.normal_state = GhostAIState.CHASE
                else:
                    self.normal_state = GhostAIState.SCATTER
                self.set_state(self.normal_state)
                self.state_schedule_index += 1

        if self.on_block():
            self.location = self.block_target
            if self.turn_around:
                self.direction = self.direction * -1
                self.turn_around = False
            else:
                self.state_method_table.get(self.current_state)()

            self.block_target = self.location + self.direction

        super().update()

    def set_state(self, new_state):
        if self.current_state != new_state:
            self.current_state = new_state
            self.turn_around = True

    def scatter_state(self):
        self.direction = self.choose_direction(self.scatter_target)
        self.target_location = self.scatter_target

    def chase_state(self):
        pass

    def frightened_state(self):
        self.direction = random.choice(self.get_directions())
        self.target_location = Point(0, 0)

    def eaten_state(self):
        if self.location != self.maze.respawn_point:
            self.direction = self.choose_direction(self.maze.respawn_point)
            self.target_location = self.maze.respawn_point
        else:
            self.set_state(self.normal_state)

    def choose_direction(self, target):

        directions = self.get_directions()
        best_direction = [directions[0], 10000]

        for direction in directions:
            distance = Point.distance(self.location + direction, target)
            if distance < best_direction[-1]:
                best_direction = [direction, distance]

        return best_direction[0]

    def get_directions(self):
        possible_directions = [self.direction,
                               Vector.rounded(Vector.rotated(self.direction, 90, Point(0, 0))),
                               Vector.rounded(Vector.rotated(self.direction, -90, Point(0, 0)))]
        valid_directions = []

        for direction in possible_directions:
            if self.maze.point(Point.rounded(self.location + direction)) == MazeBlockType.PATH:
                valid_directions.append(direction)

        del possible_directions

        return valid_directions

    def draw(self):
        self.surface.fill(EMPTY)
        pygame.draw.circle(self.surface, self.color,
                           (self.location.x * self.maze.block_pixel_size + self.maze.block_pixel_size // 2,
                            self.location.y * self.maze.block_pixel_size + self.maze.block_pixel_size // 2),
                           self.maze.block_pixel_size // 2)

        pygame.draw.circle(self.surface, self.color,
                           (self.target_location.x * self.maze.block_pixel_size + self.maze.block_pixel_size // 2,
                            self.target_location.y * self.maze.block_pixel_size + self.maze.block_pixel_size // 2),
                           self.maze.block_pixel_size // 3)
        super().draw()


class Blinky(Ghost):
    ghost_type = GhostType.BLINKY
    scatter_target = Point(29, 0)
    color = RED

    def chase_state(self):
        self.direction = self.choose_direction(Point.rounded(self.pacman.location))
        self.target_location = self.pacman.location


class Pinky(Ghost):
    ghost_type = GhostType.PINKY
    scatter_target = Point(0, 0)
    color = PINK

    def chase_state(self):
        self.direction = self.choose_direction(self.pacman.location + (self.pacman.direction * 4))
        self.target_location = self.pacman.location + (self.pacman.direction * 4)


class Inky(Ghost):
    ghost_type = GhostType.INKY
    scatter_target = Point(29, 29)
    color = CYAN

    def chase_state(self):
        blinky = self.ghosts.get(GhostType.BLINKY)
        target_location = (self.pacman.location - blinky.location) + self.pacman.location
        self.direction = self.choose_direction(target_location)
        self.target_location = target_location


class Clyde(Ghost):
    ghost_type = GhostType.CLYDE
    scatter_target = Point(0, 29)
    color = ORANGE

    def chase_state(self):
        if Point.distance(self.location, self.pacman.location) >= 8:
            self.target_location = self.pacman.location
        else:
            self.target_location = self.scatter_target
        self.direction = self.choose_direction(self.target_location)


class Animator(GameComponent):

    def __init__(self, parent, scale, animation):
        super().__init__(parent, scale)
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
        neighbour_nodes = [ASNode(self.location - Point(1, 0), self.g + 1, 0, self),
                           ASNode(self.location - Point(-1, 0), self.g + 1, 0, self),
                           ASNode(self.location - Point(0, 1), self.g + 1, 0, self),
                           ASNode(self.location - Point(0, -1), self.g + 1, 0, self)]
        return neighbour_nodes

    def calculate_h(self, target_location):
        self.h = Point.distance(self.location, target_location)

    def calculate_f(self):
        self.f = self.g + self.h


"""
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
"""
