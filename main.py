import sys
from pac_man import PACMAN
from tools import *
from settings import *
import globals

globals.size = START_SIZE
screen = pygame.display.set_mode(globals.size, pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

globals.game = PACMAN(None, BoundScale(0.5, 0.5, 1, 1), Bounds(0, 0, globals.size[0], globals.size[1]))


def run():
    while running:
        globals.delta_time = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            process_events(event)
            globals.game.process_events(event)

        globals.game.update()
        globals.game.draw()
        screen.blit(globals.game.surface, globals.game.bounds.position())
        pygame.display.flip()
        pygame.display.update()

    # Exit the program
    pygame.quit()
    sys.exit()


def process_events(event):
    global running
    global screen

    if event.type == pygame.QUIT:
        running = False
    if event.type == pygame.VIDEORESIZE:
        new_size = list(event.dict['size'])

        if new_size[0] < MIN_SIZE[0]:
            new_size[0] = MIN_SIZE[0]
        if new_size[1] < MIN_SIZE[1]:
            new_size[1] = MIN_SIZE[1]

        size_change = (abs(new_size[0] - globals.size[0]), abs(new_size[1] - globals.size[1]))
        if size_change[0] > size_change[1]:
            new_size[1] = int(new_size[0] // ASPECT_RATIO)
        else:
            new_size[0] = int(new_size[1] * ASPECT_RATIO)

        globals.size = tuple(new_size)
        screen = pygame.display.set_mode(globals.size, pygame.RESIZABLE)
        globals.game.on_scale(Bounds(0, 0, globals.size[0], globals.size[1]))


if __name__ == '__main__':
    run()
