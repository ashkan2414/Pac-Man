import globals
from maze import *
from settings import *
from globals import GhostType
from animation import *


class Entity(GameComponent):
    speed = 5

    def __init__(self, parent, scale):
        super().__init__(parent, scale)
        self.location = Point(0, 0)
        self.block_target = Point(0, 0)
        self.direction = Vector(0, 0)
        self.maze = self.parent.maze
        self.aspect_ratio = self.maze.aspect_ratio
        self.animator = Animator()

    def set_start_location(self, start_location):
        self.location = start_location
        self.block_target = start_location

    def start(self):
        x = random.randrange(0, self.maze.width - 1)
        y = random.randrange(0, self.maze.height - 1)
        while self.maze.point(Point(x, y)) != MazeBlockType.PATH:
            x = random.randrange(0, self.maze.width - 1)
            y = random.randrange(0, self.maze.height - 1)

        self.location = Point(x, y)
        self.block_target = self.location

        self.animator.start()
        super().start()

    def update(self):

        if (self.block_target - self.location).vector().normalised() != self.direction:
            self.location = self.block_target

        self.location += self.direction * self.speed * globals.delta_time

        self.animator.update()
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
    home_location = None
    scatter_target = None
    color = None
    ghost_type = None

    def __init__(self, parent, scale):
        super().__init__(parent, scale)
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

        animation = []
        for image in GHOST_ANIMATION_FILES:
            animation.append(pygame.image.load(image))
            pixels = pygame.PixelArray(animation[-1])
            pixels.replace(RED, self.color, 0.15)
            del pixels
        self.animator.add_animation(Animation("Normal", animation, GHOST_ANIMATION_FRAME_RATE))
        self.animator.set_animation("Normal")

        animation = []
        for image in GHOST_FRIGHTENED_ANIMATION_FILES:
            animation.append(pygame.image.load(image))
        self.animator.add_animation(Animation("Frightened", animation, GHOST_ANIMATION_FRAME_RATE))

    def start(self):
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

            if self.current_state == GhostAIState.FRIGHTENED:
                self.animator.set_animation("Frightened")
            elif self.current_state == GhostAIState.EATEN:
                self.animator.set_animation(None)
            else:
                self.animator.set_animation("Normal")

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

        if directions:
            best_direction = [directions[0], 10000]
            for direction in directions:
                distance = Point.distance(self.location + direction, target)
                if distance < best_direction[-1]:
                    best_direction = [direction, distance]
            return best_direction[0]

        else:
            return Vector(0, 0)

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
        size = self.maze.block_pixel_size * ENTITY_SIZE_FACTOR
        image_bounds = Bounds(self.maze.block_pixel_size * (self.location.x + (1 - ENTITY_SIZE_FACTOR) / 2),
                              self.maze.block_pixel_size * (self.location.y + (1 - ENTITY_SIZE_FACTOR) / 2),
                              size,
                              size)

        draw_image(self.surface, self.animator.get_current_frame(), image_bounds)

        eye_separation = size * GHOST_EYE_SEPARATION_FACTOR
        eye1_center = Point(image_bounds.x + (size - eye_separation) / 2,
                            image_bounds.y + image_bounds.h * GHOST_EYE_VERTICAL_OFFSET_FACTOR)
        eye2_center = Point(image_bounds.x + (size + eye_separation) / 2, eye1_center.y)

        pupil1_center = eye1_center + self.direction * size * GHOST_PUPIL_OFFSET_FACTOR
        pupil2_center = eye2_center + self.direction * size * GHOST_PUPIL_OFFSET_FACTOR

        draw_ellipse(self.surface, WHITE, eye1_center, GHOST_EYE_RADIUS_FACTOR[0] * size,
                     GHOST_EYE_RADIUS_FACTOR[1] * size)
        draw_ellipse(self.surface, WHITE, eye2_center, GHOST_EYE_RADIUS_FACTOR[0] * size,
                     GHOST_EYE_RADIUS_FACTOR[1] * size)

        pygame.draw.circle(self.surface, GHOST_PUPIL_COLOR, (pupil1_center.x, pupil1_center.y),
                           size * GHOST_PUPIL_RADIUS_FACTOR)
        pygame.draw.circle(self.surface, GHOST_PUPIL_COLOR, (pupil2_center.x, pupil2_center.y),
                           size * GHOST_PUPIL_RADIUS_FACTOR)

        if DISPLAY_GHOST_TARGET:
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
        self.direction = self.choose_direction(Point.rounded(self.parent.pacman.location))
        self.target_location = self.parent.pacman.location


class Pinky(Ghost):
    ghost_type = GhostType.PINKY
    scatter_target = Point(0, 0)
    color = PINK

    def chase_state(self):
        self.direction = self.choose_direction(self.parent.pacman.location + (self.parent.pacman.direction * 4))
        self.target_location = self.parent.pacman.location + (self.parent.pacman.direction * 4)


class Inky(Ghost):
    ghost_type = GhostType.INKY
    scatter_target = Point(29, 29)
    color = CYAN

    def chase_state(self):
        blinky = self.parent.ghosts.get(GhostType.BLINKY)
        target_location = (self.parent.pacman.location - blinky.location) + self.parent.pacman.location
        self.direction = self.choose_direction(target_location)
        self.target_location = target_location


class Clyde(Ghost):
    ghost_type = GhostType.CLYDE
    scatter_target = Point(0, 29)
    color = ORANGE

    def chase_state(self):
        if Point.distance(self.location, self.parent.pacman.location) >= 8:
            self.target_location = self.parent.pacman.location
        else:
            self.target_location = self.scatter_target
        self.direction = self.choose_direction(self.target_location)
