import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.constants import SCREEN_HEIGHT, SCREEN_WIDTH, FONT_HEIGHT, FONT_WIDTH
from bearlibterminal import terminal as term
from collections import namedtuple

palette = {
    ',': "E02C",
    '`': "E027",
    '.': "E007",
    '#': "E023",
    '+': "E02B",
    '/': "E02F",
    'O': "E07F",
    '|': "E0E7",
}

def setup():
    term.open()
    term.set(
        "window: resizeable=true, size={}x{}, cellsize={}x{}, title='Spaceship'".format(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            FONT_WIDTH, 
            FONT_HEIGHT))
    term.set("U+E000: ./fonts/cga88_black.png, size=8x8, align=center")
    term.composition(False)
if __name__ == "__main__":
    setup()
    term.refresh()
    term.read()