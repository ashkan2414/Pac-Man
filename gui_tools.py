import pygame


class GUITools:

    @staticmethod
    def draw_text(text, screen, pos, font, size, colour):
        font = pygame.font.SysFont(font, size)

        text = font.render(text, False, colour)
        text_size = text.get_size()

        pos[0] = pos[0] - text_size[0] // 2
        pos[1] = pos[1] - text_size[1] // 2

        screen.blit(text, pos)
