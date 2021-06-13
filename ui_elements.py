from game_component import *
from globals import ButtonState
from tools import *


class Button(GameComponent):

    def __init__(self, parent, scale, normal_image, hover_image=None, clicked_image=None, func=None):
        super().__init__(parent, scale)

        normal = normal_image
        hover = hover_image
        clicked = clicked_image

        if not hover_image and clicked_image:
            hover = clicked_image
        elif not hover_image and not clicked_image:
            hover = normal_image
            clicked = normal_image
        elif hover_image and not clicked_image:
            clicked = hover_image

        self.state_images = {ButtonState.NORMAL: normal, ButtonState.HOVER: hover, ButtonState.CLICKED: clicked}
        self.current_state = ButtonState.NORMAL
        self.last_state = ButtonState.NORMAL
        self.function = func
        self.aspect_ratio = normal.get_width() / normal.get_height()

    def process_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if self.current_state == ButtonState.HOVER:
                self.current_state = ButtonState.CLICKED
        else:
            if self.current_state == ButtonState.CLICKED:
                self.current_state = ButtonState.HOVER

        super().process_events(event)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.bounds.is_within(mouse_pos[0], mouse_pos[1]):
            if not self.current_state == ButtonState.CLICKED:
                self.current_state = ButtonState.HOVER
        else:
            self.current_state = ButtonState.NORMAL

        if self.function and self.current_state == ButtonState.CLICKED and self.current_state != self.last_state:
            self.function()

        self.last_state = self.current_state
        super().update()

    def draw(self):
        self.surface.fill(EMPTY)
        image_bounds = self.as_bounds.copy()
        image_bounds.x = 0
        image_bounds.y = 0
        draw_image(self.surface, self.state_images.get(self.current_state), image_bounds)
        super().draw()
