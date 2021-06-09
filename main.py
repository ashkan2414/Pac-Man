from pac_man import PACMAN

from tools import Bounds
from settings import *
import globals

globals.game = PACMAN(Bounds(0, 0, START_SIZE[0], START_SIZE[1]))

if __name__ == '__main__':
    globals.game.run()
