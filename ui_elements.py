from animation import Animator
from game_component import *
from tools import *


class Button(GameComponent):

    def __init__(self, parent, scale, normal, hover=None, clicked=None, func=None):
        super().__init__(parent, scale)

        if not hover and clicked:
            hover = hover
        elif not hover and not clicked:
            hover = normal
            clicked = normal
        elif hover and not clicked:
            clicked = hover

        self.current_state = ButtonState.NORMAL
        self.last_state = ButtonState.NORMAL
        self.function = func
        self.aspect_ratio = normal.frames[0].get_width() / normal.frames[0].get_height()

        self.animator = Animator()
        self.animator.add_animation(normal)
        self.animator.add_animation(hover)
        self.animator.add_animation(clicked)

    def start(self):
        self.current_state = ButtonState.NORMAL
        self.last_state = ButtonState.NORMAL
        self.animator.set_animation(self.current_state)

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if self.current_state == ButtonState.HOVER:
                self.current_state = ButtonState.CLICKED
        else:
            if self.current_state == ButtonState.CLICKED:
                self.current_state = ButtonState.HOVER

        super().process_event(event)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.bounds.is_within(mouse_pos[0], mouse_pos[1]):
            if not self.current_state == ButtonState.CLICKED:
                self.current_state = ButtonState.HOVER
        else:
            self.current_state = ButtonState.NORMAL

        if self.function and self.current_state == ButtonState.CLICKED and self.current_state != self.last_state:
            self.function()

        self.animator.set_animation(self.current_state)

        self.last_state = self.current_state
        self.animator.update()
        super().update()

    def draw(self):
        self.surface.fill(EMPTY)
        image_bounds = self.as_bounds.copy()
        image_bounds.x = 0
        image_bounds.y = 0
        draw_image(self.surface, self.animator.get_current_frame(), image_bounds)
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


class IconBar(GameComponent):

    def __init__(self, parent, scale, icon_image, icon_count):
        super().__init__(parent, scale)
        self.image = icon_image
        self.count = icon_count
        self.current_num = self.count
        self.aspect_ratio = (icon_count * self.image.get_width()) / self.image.get_height()
        self.scaled_image = icon_image

    def start(self):
        self.current_num = self.count
        self.draw_surface()

    def draw_surface(self):
        self.surface.fill(EMPTY)
        for i in range(self.current_num):
            self.surface.blit(self.scaled_image, (i*self.scaled_image.get_width(), 0))

    def on_scale(self, container_bounds):
        super().on_scale(container_bounds)
        self.scaled_image = pygame.transform.smoothscale(self.image, (self.as_bounds.width//self.count,
                                                                      self.as_bounds.height))
        self.draw_surface()

    def set_current_num(self, num):
        if num != self.current_num and 0 <= num <= self.count:
            self.current_num = num
            self.draw_surface()


class Icon(GameComponent):

    def __init__(self, parent, scale, image):
        super().__init__(parent, scale)
        self.image = image
        self.aspect_ratio = self.image.get_width()/self.image.get_height()
        self.scaled_image = image

    def start(self):
        self.draw_surface()

    def draw_surface(self):
        self.surface.fill(EMPTY)
        self.surface.blit(self.scaled_image, (0, 0))

    def on_scale(self, container_bounds):
        super().on_scale(container_bounds)
        self.scaled_image = pygame.transform.smoothscale(self.image, self.as_bounds.size())
        self.draw_surface()