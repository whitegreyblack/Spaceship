import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from bearlibterminal import terminal as term

def setup():
    term.open()
    term.set(
        "window: resizeable=true, size={}x{}, cellsize={}x{}, title='Spaceship'".format(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            8, 16))

if __name__ == "__main__":
    setup()
    term.refresh()
    term.read()