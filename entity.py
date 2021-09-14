import random

from animation import *
from game_component import *
from managers import *


class Entity(GameComponent):
    """
    Entities are the various game objects that navigate around the maze such as ghosts or pacman

    ...

    Attributes:
    -----------
    location (Point): The location of the entity
    block_target (Point): The next block the entity is travelling towards
    direction (Vector): The current direction the entity is travelling in
    animator (Animator): Handles animates the entity
    size (int): The pixel size of the entity


    Static Attributes:
    ------------------
    speed (int): The speed of the entity
    traversable_blocks (tuple): A tuple of the blocks that the entity can travel on

    Methods:
    --------
    def on_target_block(self):
        Returns whether the entity has reached the target block

    def get_drawing_bounds(self):
        Returns the drawing bounds of the entity
    """
    speed = 5
    traversable_blocks = (MazeBlockType.PATH,)

    def __init__(self, parent, scale):
        super().__init__(parent, scale)
        self.aspect_ratio = self.parent.maze.aspect_ratio

        self.location = Point(0, 0)
        self.block_target = Point(0, 0)
        self.direction = Vector(0, 0)
        self.animator = Animator()
        self.size = 0

    def start(self):
        self.animator.start()
        # Update once to setup the first drawing
        self.update()
        # Pause until the game start event
        self.set_pause(True)
        super().start()

    def process_event(self, event):

        if event.type == GAME_START:
            self.set_pause(False)
        elif event.type == LEVEL_RESET:
            self.start()
        elif event.type == LEVEL_FINISH:
            self.set_enable(False)
        elif event.type == GAME_OVER:
            self.set_pause(True)
        super().process_event(event)

    def update(self):
        # If not travelling in the direction of the block target, teleport to the block target
        # This prevents the entities from flying off the map in case of a program interruption such as scaling
        if (self.block_target - self.location).vector().normalised() != self.direction:
            self.location = self.block_target

        # Moving in the current direction
        self.location += self.direction * self.speed * globals.delta_time

        # Update animator
        self.animator.update()
        super().update()

    def on_scale(self, container_bounds):
        # Teleport to block target on scale
        self.location = self.block_target
        # Copy bounds and surface from maze
        self.as_bounds = self.parent.maze.as_bounds.copy()
        self.bounds = self.parent.maze.bounds.copy()
        self.surface = self.parent.maze.surface.copy()
        # Calculate size
        self.size = self.parent.maze.block_size * ENTITY_SIZE_FACTOR

    def on_target_block(self):
        """
        Returns whether the entity has reached the target block

        Returns:
            bool: Whether the entity has reached the target block
        """
        return Point.distance(self.location, self.block_target) < self.speed * globals.delta_time

    def get_drawing_bounds(self):
        """
        Returns the drawing bounds of the entity

        Returns:
            Bounds: The drawing bounds of the entity
        """
        return Bounds(self.parent.maze.block_size * (self.location.x + (1 - ENTITY_SIZE_FACTOR) / 2),
                      self.parent.maze.block_size * (self.location.y + (1 - ENTITY_SIZE_FACTOR) / 2),
                      self.size,
                      self.size)


class Pacman(Entity):
    """
    Pacman is the player controlled entity

    Attributes:
    -----------
    dead (bool): Whether pacman has died
    points (int): The number of points collected
    lives (int): The amount of lives left
    next_direction (Vector): The queued direction from user input
    face_direction (Vector): The current direction pacman is facing in (does not have to be moving)
    point_munch_sound (bool): Determines the next munch sound to be used (False: munch 1, True: munch 2)
    """
    speed = PAC_MAN_SPEED
    traversable_blocks = (MazeBlockType.PATH,)

    def __init__(self, parent, scale):
        super().__init__(parent, scale)
        self.dead = False
        self.points = 0
        self.lives = PACMAN_LIVES
        self.next_direction = Vector(0, 0)
        self.face_direction = Vector(0, 0)
        self.point_munch_sound = False
        self.ghost_point_value = INITIAL_GHOST_POINT_VALUE

        # Add pacman animations
        self.animator.add_animation(
            Animation("Moving", load_animation(PACMAN_MOVING_ANIMATION), PACMAN_ANIMATION_FRAME_RATE, True))
        self.animator.add_animation(
            Animation("Idle", load_animation(PACMAN_IDLE_ANIMATION), PACMAN_ANIMATION_FRAME_RATE, True))
        self.animator.add_animation(
            Animation("Death", load_animation(PACMAN_DEATH_ANIMATION), PACMAN_DEATH_ANIMATION_FRAME_RATE, False))

    def start(self):
        self.dead = False
        self.direction = Vector(0, 0)
        self.next_direction = Vector(0, 0)
        self.face_direction = Vector(1, 0)
        self.point_munch_sound = False
        self.ghost_point_value = INITIAL_GHOST_POINT_VALUE

        # Choose a random spawn location
        spawn_location = Point(random.randrange(0, MAZE_WIDTH - 1), random.randrange(0, MAZE_HEIGHT - 1))
        while self.parent.maze.point(spawn_location) != MazeBlockType.PATH or \
                Point.distance(spawn_location, GHOST_CAGE_EXIT) < PACMAN_SPAWN_DISTANCE_THRESHOLD:
            spawn_location = Point(random.randrange(0, MAZE_WIDTH - 1), random.randrange(0, MAZE_HEIGHT - 1))

        self.location = spawn_location
        self.block_target = self.location

        # Remove point at the
        self.parent.maze.point(self.location).pickup_consumed = True
        super().start()

    def process_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.next_direction = Vector(-1, 0)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.next_direction = Vector(1, 0)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.next_direction = Vector(0, 1)
            elif event.key == pygame.K_UP or event.key == pygame.K_u:
                self.next_direction = Vector(0, -1)
        elif event.type == PACMAN_DEATH:
            self.dead = True
        elif event.type == FRIGHTENED_MODE_END:
            self.ghost_point_value = INITIAL_GHOST_POINT_VALUE
        elif event.type == GHOST_EATEN_START:
            self.add_points(self.ghost_point_value)
            print(self.ghost_point_value)
            if self.ghost_point_value == INITIAL_GHOST_POINT_VALUE * 8:
                self.ghost_point_value = INITIAL_GHOST_POINT_VALUE
            else:
                self.ghost_point_value *= 2
            self.set_pause(True)
        elif event.type == GHOST_EATEN_END:
            self.set_pause(False)

        super().process_event(event)

    def update(self):
        if self.on_target_block() and not self.dead:
            self.location = self.block_target  # Teleport to target block to get rid of minor differences
            # If the queued direction is possible
            if self.parent.maze.point(self.location + self.next_direction) in self.traversable_blocks:
                # Set the direction to the queued direction
                self.direction = self.next_direction

            # If the current direction is possible
            if self.parent.maze.point(self.location + self.direction) in self.traversable_blocks:
                # Set the block target the next block in direction
                self.block_target = self.location + self.direction
            # Otherwise
            else:
                # Stop moving
                self.direction = Vector(0, 0)
                self.next_direction = Vector(0, 0)

            # Get block currently on
            block = self.parent.maze.point(self.location)
            # If the pickup has not already been consumed
            if not block.pickup_consumed:
                # If its a point
                if block.pickup_type == BlockPickupType.POINT:
                    self.add_points(POINT_PICKUP_VALUE)  # Add points
                    # Play munch eating sound
                    self.point_munch_sound = not self.point_munch_sound
                    if self.point_munch_sound:
                        SoundManager.sounds.get(SoundTrack.POINT_EATEN_1).play()
                    else:
                        SoundManager.sounds.get(SoundTrack.POINT_EATEN_2).play()

                # If its a power pellet
                elif block.pickup_type == BlockPickupType.POWER_PELLET:
                    self.add_points(POWER_PELLET_PICKUP_VALUE)  # Add points
                    # Post frightened mode start event
                    pygame.event.post(pygame.event.Event(FRIGHTENED_MODE_START))
                    # Remove all current frightened mode end events to refresh timer
                    TimedEventManager.remove_timed_events_of_type(FRIGHTENED_MODE_END)
                    # Schedule new frightened mode end event
                    TimedEventManager.add_timed_event(pygame.event.Event(FRIGHTENED_MODE_END),
                                                      GHOST_FRIGHTENED_DURATION)

                elif block.pickup_type == BlockPickupType.FRUIT:
                    self.add_points(FRUIT_PICKUP_VALUE)  # Add points
                    TimedEventManager.add_timed_event(pygame.event.Event(FRUIT_SPAWN_READY), FRUIT_COOLDOWN_DURATION)

                # Set the pickup consumed to true
                block.pickup_consumed = True

            # If all the points are eaten
            if globals.points_left <= 0:
                # Post level finish event
                pygame.event.post(pygame.event.Event(LEVEL_FINISH))

        if self.dead:
            self.direction = Vector(0, 0)
            self.animator.set_animation("Death")
            if self.animator.finished:
                self.lives -= 1
                if self.lives == 0:
                    pygame.event.post(pygame.event.Event(GAME_OVER))
                else:
                    pygame.event.post(pygame.event.Event(LEVEL_RESET))
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
        self.lives = PACMAN_LIVES

    def add_points(self, amount):
        self.points += amount
        if self.points > globals.highscore:
            globals.highscore = self.points


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

        animation = load_animation(GHOST_NORMAL_ANIMATION)
        for image in animation:
            pixels = pygame.PixelArray(image)
            pixels.replace(RED, self.color, 0.15)
            del pixels
        self.animator.add_animation(Animation("Normal", animation, GHOST_ANIMATION_FRAME_RATE, True))
        self.animator.add_animation(
            Animation("Frightened", load_animation(GHOST_FRIGHTENED_ANIMATION), GHOST_ANIMATION_FRAME_RATE, True))

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

    def process_event(self, event):

        if event.type == FRIGHTENED_MODE_START:
            self.set_state(GhostAIState.FRIGHTENED)
        elif event.type == FRIGHTENED_MODE_END:
            if self.current_state != GhostAIState.EATEN:
                self.set_state(self.normal_state)
        elif event.type == GHOST_EATEN_START:
            if self.current_state != GhostAIState.EATEN or event.ghost == self:
                self.set_pause(True)
        elif event.type == GHOST_EATEN_END:
            self.set_pause(False)
        elif event.type == PACMAN_DEATH:
            self.set_pause(True)

        super().process_event(event)

    def update(self):

        if Point.distance(self.location, self.parent.pacman.location) < ENTITY_COLLISION_DISTANCE:
            if self.current_state == GhostAIState.FRIGHTENED:
                pygame.event.post(pygame.event.Event(GHOST_EATEN_START, ghost=self))
                TimedEventManager.add_timed_event(pygame.event.Event(GHOST_EATEN_END), GHOST_EATEN_PAUSE_DURATION)
                self.set_state(GhostAIState.EATEN)
                globals.ghosts_eaten += 1
                SoundManager.sounds.get(SoundTrack.GHOST_EATEN).play(0, SoundPlayMode.RESTART)

            elif self.current_state == GhostAIState.SCATTER or self.current_state == GhostAIState.CHASE:
                pygame.event.post(pygame.event.Event(PACMAN_DEATH))
                SoundManager.instant_stop()
                SoundManager.sounds.get(SoundTrack.PACMAN_DEATH).play(0, SoundPlayMode.TIMED, PACMAN_DEATH_SOUND_DELAY)

        if self.current_state != GhostAIState.EATEN and self.current_state != GhostAIState.FRIGHTENED:
            self.state_timer += globals.delta_time

            if self.state_timer > GHOST_STATE_SCHEDULE[self.state_schedule_index] and self.state_schedule_index < \
                    len(GHOST_STATE_SCHEDULE) - 1:
                self.state_timer = 0
                if self.current_state == GhostAIState.SCATTER:
                    self.normal_state = GhostAIState.CHASE
                else:
                    self.normal_state = GhostAIState.SCATTER
                self.set_state(self.normal_state)
                self.state_schedule_index += 1

        if self.on_target_block():
            self.location = self.block_target
            if self.turn_around:
                self.direction = self.direction * -1
                self.turn_around = False
            else:
                if MAZE_CAGE_BOUNDS.is_within(self.location.x,
                                              self.location.y) and self.current_state != GhostAIState.EATEN:
                    self.direction = self.get_pathfinding_direction(GHOST_CAGE_EXIT)
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

            pupil1_center = Point(eye1_center.x + self.direction.x * self.size * GHOST_PUPIL_OFFSET_FACTOR[0],
                                  eye1_center.y + self.direction.y * self.size * GHOST_PUPIL_OFFSET_FACTOR[1])
            pupil2_center = Point(eye2_center.x + self.direction.x * self.size * GHOST_PUPIL_OFFSET_FACTOR[0],
                                  eye2_center.y + self.direction.y * self.size * GHOST_PUPIL_OFFSET_FACTOR[1])

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
            globals.ghosts_eaten -= 1
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
