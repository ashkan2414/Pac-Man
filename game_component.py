from settings import *


class GameComponent:
    """
    A template framework for game components

    ...

    Attributes:
    -----------
    parent (GameComponent): The parent of this game component
    scale (BoundScale):  The relative position and size scale of this game component
    bounds (Bounds): The bounds of this game component surface
    aspect_ratio (float): The maintained surface aspect ratio of this game component
    as_bounds (Bounds): The bounds of this game component surface with the locked aspect ratio
    surface (Surface): The main drawing surface of this game component
    enabled (bool): Whether this game component is enabled or disabled
    paused (bool): Whether this game component is paused
    child_game_components (list): A list of child game components

    Methods:
    --------
    def start(self):
        Sets up the game component

    def process_event(self, event):
        Handles game events

    def update(self):
        Handles all calculations and processes

    def draw(self):
        Draws onto the game component surface

    def on_scale(self, container_bounds):
        Scales the game component bounds and surface

    def end(self):
        Handles de-initializing of the game component

    def set_enable(self, state):
        Sets the game component and all children to a new enable state

    def set_children_enable(self, state):
        Sets all the children to a new enable state

    def set_pause(self, state):
        Sets the game component and all children to a new pause state

    def set_children_pause(self, state):
        Sets all the children to a new pause state
    """

    def __init__(self, parent, scale):
        """
        Returns a new game component

        Parameters:
            parent (GameComponent): The parent of this game component
            scale (BoundScale): The relative position and size scale of this game component

        Returns:
            GameComponent: A new game component
        """
        self.parent = parent
        self.scale = scale
        self.bounds = Bounds(0, 0, 500, 500)
        self.aspect_ratio = None
        self.as_bounds = None
        self.surface = pygame.Surface(self.bounds.size(), flags=pygame.SRCALPHA)
        self.enabled = True
        self.paused = False
        self.child_game_components = []

    def __str__(self):
        """
        Returns the string representation of this game component

        Returns:
            string: The string representation of this game component
        """
        return self.__class__.__name__

    def __repr__(self):
        """
        Returns the string representation of this game component

        Returns:
            string: The string representation of this game component
        """
        return self.__str__()

    def start(self):
        """
        Sets up the game component
        """
        for component in self.child_game_components:
            if component.enabled:
                component.start()

    def process_event(self, event):
        """
        Handles game events

        Parameters:
            event (Event): The event to process
        """
        # Call process events on all children if enabled
        for component in self.child_game_components:
            if component.enabled:
                component.process_event(event)

    def update(self):
        """
        Handles all calculations and processes
        """
        # Call update on all children if enabled and not paused
        for component in self.child_game_components:
            if component.enabled and not component.paused:
                component.update()

    def draw(self):
        """
        Draws onto the game component surface
        """
        # Call draw on all children if enabled and draw their surface onto the game component surface
        for component in self.child_game_components:
            if component.enabled:
                component.draw()
                self.surface.blit(component.surface, component.as_bounds.position())

                if DISPLAY_BOUND_BORDER:
                    # Display children bounds and aspect ratio bounds
                    pygame.draw.rect(self.surface, RED, component.bounds, 2)
                    pygame.draw.rect(self.surface, YELLOW, component.as_bounds, 2)

    def on_scale(self, container_bounds):
        """
        Scales the game component bounds and surface

        Parameters:
            container_bounds (Bounds): The bounds to scale off of
        """
        # Calculate bounds size and position
        self.bounds.width = container_bounds.width * self.scale.width
        self.bounds.height = container_bounds.height * self.scale.height
        self.bounds.x = (container_bounds.x + container_bounds.width) * self.scale.x - self.bounds.width / 2
        self.bounds.y = (container_bounds.y + container_bounds.height) * self.scale.y - self.bounds.height / 2

        self.as_bounds = self.bounds.copy()
        # Calculate aspect ratio size and bounds if aspect ratio is defined
        if self.aspect_ratio:
            if self.aspect_ratio < self.bounds.aspect_ratio():
                self.as_bounds.width = self.bounds.height * self.aspect_ratio
                self.as_bounds.x += (self.bounds.width - self.as_bounds.width) / 2
            elif self.aspect_ratio > self.bounds.aspect_ratio():
                self.as_bounds.height = self.bounds.width / self.aspect_ratio
                self.as_bounds.y += (self.bounds.height - self.as_bounds.height) / 2

        # Create new scaled surface
        self.surface = pygame.Surface(self.as_bounds.size(), flags=pygame.SRCALPHA)

        # Scale all children with the calculated game component bounds
        for component in self.child_game_components:
            component.on_scale(self.bounds)

    def end(self):
        """
        Handles de-initializing of the game component
        """
        for component in self.child_game_components:
            component.end()

    def set_enable(self, state):
        """
        Sets the game component and all children to a new enable state
        """
        self.enabled = state
        self.set_children_enable(state)

    def set_children_enable(self, state):
        """
        Sets all the children to a new enable state
        """
        for component in self.child_game_components:
            component.set_enable(state)

    def set_pause(self, state):
        """
        Sets the game component and all children to a new pause state
        """
        self.paused = state
        self.set_children_pause(state)

    def set_children_pause(self, state):
        """
        Sets all the children to a new pause state
        """
        for component in self.child_game_components:
            component.set_pause(state)
