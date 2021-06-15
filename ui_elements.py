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


class Text(GameComponent):

    def __init__(self, parent, scale, text, color, font_name, size, fit_to_area):
        super().__init__(parent, scale)
        self.text = text
        self.color = color
        self.font_name = font_name
        self.size = size
        self.fit_to_area = fit_to_area
        self.text_surface = None
        self.render()

    def start(self):
        self.render()
        self.draw_surface()

    def on_scale(self, container_bounds):
        super().on_scale(container_bounds)
        self.draw_surface()

    def draw_surface(self):
        self.surface.fill(EMPTY)
        text_image = None
        if self.fit_to_area:
            text_image = pygame.transform.scale(self.text_surface, self.as_bounds.size())
        else:
            text_image = self.text_surface

        self.surface.blit(text_image, (0, 0))

    def render(self):
        self.text_surface = pygame.font.SysFont(self.font_name, self.size).render(self.text, False, self.color)
        if self.fit_to_area:
            self.aspect_ratio = self.text_surface.get_width() / self.text_surface.get_height()

    def set_text(self, new_text):
        if new_text != self.text:
            self.text = new_text
            self.render()
            self.draw_surface()
