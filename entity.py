import globals
from maze import *
from settings import *
from globals import GhostType
from animation import *


class Entity(GameComponent):
    speed = 5
    traversable_blocks = (MazeBlockType.PATH,)

    def __init__(self, parent, scale):
        super().__init__(parent, scale)
        self.location = Point(0, 0)
        self.block_target = Point(0, 0)
        self.direction = Vector(0, 0)
        self.aspect_ratio = self.parent.maze.aspect_ratio
        self.animator = Animator()
        self.size = 0

    def set_start_location(self, start_location):
        self.location = start_location
        self.block_target = start_location

    def start(self):
        self.animator.start()
        super().start()

    def update(self):
        if (self.block_target - self.location).vector().normalised() != self.direction:
            self.location = self.block_target

        self.location += self.direction * self.speed * globals.delta_time

        self.animator.update()
        super().update()

    def on_scale(self, container_bounds):
        self.location = self.block_target
        self.as_bounds = self.parent.maze.as_bounds.copy()
        self.bounds = self.parent.maze.bounds.copy()
        self.surface = self.parent.maze.surface.copy()
        self.size = self.parent.maze.block_size * ENTITY_SIZE_FACTOR

    def on_block(self):
        return Point.distance(self.location, self.block_target) < self.speed * globals.delta_time

    def get_drawing_bounds(self):
        return Bounds(self.parent.maze.block_size * (self.location.x + (1 - ENTITY_SIZE_FACTOR) / 2),
                      self.parent.maze.block_size * (self.location.y + (1 - ENTITY_SIZE_FACTOR) / 2),
                      self.size,
                      self.size)


class Pacman(Entity):
    speed = PAC_MAN_SPEED
    traversable_blocks = (MazeBlockType.PATH,)

    def __init__(self, parent, scale):
        super().__init__(parent, scale)
        self.dead = False
        self.points = 0
        self.next_direction = Vector(0, 0)
        self.face_direction = Vector(0, 0)

        self.animator.add_animation(
            Animation("Moving", load_animation(PACMAN_MOVING_ANIMATION_FILES), PACMAN_ANIMATION_FRAME_RATE, True))
        self.animator.add_animation(
            Animation("Idle", load_animation(PACMAN_IDLE_ANIMATION_FILES), PACMAN_ANIMATION_FRAME_RATE, True))
        self.animator.add_animation(
            Animation("Death", load_animation(PACMAN_DEATH_ANIMATION_FILES), PACMAN_DEATH_ANIMATION_FRAME_RATE, False))

    def start(self):
        self.dead = False
        self.direction = Vector(0, 0)
        self.next_direction = Vector(0, 0)
        self.face_direction = Vector(1, 0)

        x = random.randrange(0, self.parent.maze.width - 1)
        y = random.randrange(0, self.parent.maze.height - 1)
        while self.parent.maze.point(Point(x, y)) != MazeBlockType.PATH:
            x = random.randrange(0, self.parent.maze.width - 1)
            y = random.randrange(0, self.parent.maze.height - 1)

        self.location = Point(x, y)
        self.block_target = self.location
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

        if self.on_block() and not self.dead:
            self.location = self.block_target
            if self.parent.maze.point(self.location + self.next_direction) in self.traversable_blocks:
                self.direction = self.next_direction

            if self.parent.maze.point(self.location + self.direction) in self.traversable_blocks:
                self.block_target = self.location + self.direction
            else:
                self.direction = Vector(0, 0)
                self.next_direction = Vector(0, 0)

            block = self.parent.maze.point(self.location)
            if block.block_type == MazeBlockType.PATH:
                if not block.pickup_consumed:
                    if block.pickup_type == BlockPickupType.POINT:
                        self.points += POINT_PICKUP_VALUE
                    elif block.pickup_type == BlockPickupType.POWER_PELLET:
                        self.parent.set_frightened_mode()
                block.pickup_consumed = True

        if self.dead:
            self.animator.set_animation("Death")
            if self.animator.finished:
                self.parent.pacman_death_end()
                return
        elif self.direction != Vector(0, 0):
            self.animator.set_animation("Moving")
            self.face_direction = self.direction.copy()
        else:
            self.animator.set_animation("Idle")

        super().update()

    def draw(self):
        self.surface.fill(EMPTY)
        if self.dead:
            image = self.animator.current_frame
        else:
            image = pygame.transform.rotate(self.animator.current_frame, self.face_direction.angular_position() - 90)
        draw_image(self.surface, image, self.get_drawing_bounds())
        super().draw()

    def end(self):
        self.points = 0


class Ghost(Entity):
    traversable_blocks = (MazeBlockType.PATH, MazeBlockType.EMPTY, MazeBlockType.BARRIER)
    speed = GHOST_SPEED
    spawn_point = Point(0, 0)
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
        self.animator.add_animation(Animation("Normal", animation, GHOST_ANIMATION_FRAME_RATE, True))
        self.animator.add_animation(
            Animation("Frightened", load_animation(GHOST_FRIGHTENED_ANIMATION_FILES), GHOST_ANIMATION_FRAME_RATE, True))

    def start(self):
        self.location = self.spawn_point
        self.block_target = self.spawn_point
        self.current_state = GHOST_START_STATE
        self.normal_state = GHOST_START_STATE
        self.animator.set_animation("Normal")
        self.state_timer = 0
        self.state_schedule_index = 0
        self.direction = Vector(1, 0)
        self.turn_around = False
        super().start()

    def update(self):

        if Point.distance(self.location,
                          self.parent.pacman.location) < ENTITY_COLLISION_DISTANCE:
            if self.current_state == GhostAIState.FRIGHTENED:
                self.parent.ghost_eaten()
                self.set_state(GhostAIState.EATEN)
            elif self.current_state == GhostAIState.SCATTER or self.current_state == GhostAIState.CHASE:
                self.parent.pacman.dead = True
                self.parent.pacman_death()

        if self.current_state != GhostAIState.EATEN and self.current_state != GhostAIState.FRIGHTENED:
            self.state_timer += globals.delta_time

            if self.state_timer > GHOST_STATE_SCHEDULE[
                self.state_schedule_index] and self.state_schedule_index < len(
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
                if MAZE_CAGE_BOUNDS.is_within(self.location.x,
                                              self.location.y) and self.current_state != GhostAIState.EATEN:
                    self.direction = self.get_pathfinding_direction(Point(14, 10))
                else:
                    self.state_method_table.get(self.current_state)()

            self.block_target = self.location + self.direction
        super().update()

    def draw(self):
        self.surface.fill(EMPTY)
        ghost_bounds = self.get_drawing_bounds()
        if self.current_state != GhostAIState.EATEN:
            draw_image(self.surface, self.animator.get_current_frame(), ghost_bounds)

        if self.current_state != GhostAIState.FRIGHTENED:
            eye_separation = self.size * GHOST_EYE_SEPARATION_FACTOR
            eye1_center = Point(ghost_bounds.x + (self.size - eye_separation) / 2,
                                ghost_bounds.y + ghost_bounds.h * GHOST_EYE_VERTICAL_OFFSET_FACTOR)
            eye2_center = Point(ghost_bounds.x + (self.size + eye_separation) / 2, eye1_center.y)

            pupil1_center = eye1_center + self.direction * self.size * GHOST_PUPIL_OFFSET_FACTOR
            pupil2_center = eye2_center + self.direction * self.size * GHOST_PUPIL_OFFSET_FACTOR

            draw_ellipse(self.surface, WHITE, eye1_center, GHOST_EYE_RADIUS_FACTOR[0] * self.size,
                         GHOST_EYE_RADIUS_FACTOR[1] * self.size)
            draw_ellipse(self.surface, WHITE, eye2_center, GHOST_EYE_RADIUS_FACTOR[0] * self.size,
                         GHOST_EYE_RADIUS_FACTOR[1] * self.size)

            pygame.draw.circle(self.surface, GHOST_PUPIL_COLOR, (pupil1_center.x, pupil1_center.y),
                               self.size * GHOST_PUPIL_RADIUS_FACTOR)
            pygame.draw.circle(self.surface, GHOST_PUPIL_COLOR, (pupil2_center.x, pupil2_center.y),
                               self.size * GHOST_PUPIL_RADIUS_FACTOR)

        if DISPLAY_GHOST_TARGET:
            pygame.draw.circle(self.surface, self.color,
                               (self.target_location.x * self.parent.maze.block_size + self.parent.maze.block_size // 2,
                                self.target_location.y * self.parent.maze.block_size + self.parent.maze.block_size // 2),
                               self.parent.maze.block_size // 3)
        super().draw()

    def set_state(self, new_state):
        if self.current_state == GhostAIState.EATEN and new_state == GhostAIState.FRIGHTENED:
            return

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
        self.direction = self.get_direction(self.scatter_target)
        self.target_location = self.scatter_target

    def chase_state(self):
        pass

    def frightened_state(self):
        self.direction = random.choice(self.get_valid_directions())
        self.target_location = Point(0, 0)

    def eaten_state(self):
        if self.location != self.spawn_point:
            self.direction = self.get_pathfinding_direction(self.spawn_point)
            self.target_location = self.spawn_point
        else:
            self.set_state(self.normal_state)

    def get_pathfinding_direction(self, target):
        path = self.get_path(target)
        if path:
            if len(path) == 1:
                return self.get_direction(target)
            else:
                return (path[1] - self.location).vector()
        else:
            return Vector(0, 0)

    def get_direction(self, target):

        directions = self.get_valid_directions()

        if directions:
            best_direction = [directions[0], 10000]
            for direction in directions:
                distance = Point.distance(self.location + direction, target)
                if distance < best_direction[-1]:
                    best_direction = [direction, distance]
            return best_direction[0]

        else:
            return Vector(0, 0)

    def get_valid_directions(self):
        possible_directions = [self.direction,
                               Vector.rounded(Vector.rotated(self.direction, 90, Point(0, 0))),
                               Vector.rounded(Vector.rotated(self.direction, -90, Point(0, 0)))]
        valid_directions = []

        if self.current_state == GhostAIState.EATEN:
            traversable_blocks = self.traversable_blocks
        else:
            traversable_blocks = (MazeBlockType.PATH,)

        for direction in possible_directions:
            if self.parent.maze.point(Point.rounded(self.location + direction)) in traversable_blocks:
                valid_directions.append(direction)

        del possible_directions

        return valid_directions

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
                if node not in closed_nodes and self.parent.maze.point(node.location) in self.traversable_blocks:
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


class Blinky(Ghost):
    spawn_point = Point(13, 13)
    ghost_type = GhostType.BLINKY
    scatter_target = Point(29, 0)
    color = RED

    def chase_state(self):
        self.direction = self.get_direction(Point.rounded(self.parent.pacman.location))
        self.target_location = self.parent.pacman.location


class Pinky(Ghost):
    spawn_point = Point(14, 13)
    ghost_type = GhostType.PINKY
    scatter_target = Point(0, 0)
    color = PINK

    def chase_state(self):
        self.direction = self.get_direction(self.parent.pacman.location + (self.parent.pacman.direction * 4))
        self.target_location = self.parent.pacman.location + (self.parent.pacman.direction * 4)


class Inky(Ghost):
    spawn_point = Point(15, 13)
    ghost_type = GhostType.INKY
    scatter_target = Point(29, 29)
    color = CYAN

    def chase_state(self):
        blinky = self.parent.ghosts.get(GhostType.BLINKY)
        target_location = (self.parent.pacman.location - blinky.location) + self.parent.pacman.location
        self.direction = self.get_direction(target_location)
        self.target_location = target_location


class Clyde(Ghost):
    spawn_point = Point(16, 13)
    ghost_type = GhostType.CLYDE
    scatter_target = Point(0, 29)
    color = ORANGE

    def chase_state(self):
        if Point.distance(self.location, self.parent.pacman.location) >= 8:
            self.target_location = self.parent.pacman.location
        else:
            self.target_location = self.scatter_target
        self.direction = self.get_direction(self.target_location)


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
