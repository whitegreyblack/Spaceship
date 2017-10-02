import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.constants import *
from bearlibterminal import terminal as term
from collections import namedtuple

output = namedtuple("Out", "proceed value")
opout = namedtuple("Out", "proceed options")
ccout = namedtuple("Out", "proceed player")
nnout = namedtuple("Out", "proceed name")
ngout = namedtuple("Out", "proceed error")
cgout = namedtuple("Out", "proceed error")

alphabet = {
    '(': "E028",
    ')': "E029",
    "?": "E03F",
    'A': "E041", 
    'B': "E042",
    'C': "E043",
    'D': "E044",
    'E': "E045",
    'F': "E046",
    'G': "E047",
    'H': "E048",
    'I': "E049",
    'J': "E04A",
    'K': "E04B",
    'L': "E04C",
    'M': "E04D",
    'N': "E04E",
    'O': "E04F",
    'P': "E050",
    'a': "E061",
    'b': "E062",
    'c': "E063",
    'd': "E064",
    'e': "E065",
    'f': "E066",
    'g': "E067",
    'h': "E068",
    'i': "E069",
    'j': "E06A",
    'k': "E06B",
    'l': "E06C",
    'm': "E06D",
    'n': "E06E",
    'o': "E06F",
    'p': "E070",
    'q': "E071",
    'r': "E072",
    's': "E073",
    't': "E074",
    'u': "E075",
    'v': "E076",
    'w': "E077",
    'x': "E078",
    'y': "E079",
    'z': "E080",
}

palette = {
    # ',': "E02C",
    ',': "E0F9",
    # '`': "E027",
    ',': "E0F9",
    '.': "E0F9",
    '#': "E023",
    '+': "E02B",
    '/': "E02F",
    'o': "E07F",
    # '|': "E0E7",
    '|': "E007",
    # ';': "E03B",
    ';': "E0F9",
    # ':': "E03A",
    ':': "E0FE",
    '@': "E040",
    # 'x': "E078",
    'x': "E0F9",
    '~': "E0F7",
    '=': "E03D",
    'R': "E052",
    'r': "E072",
    '(': "E028",
}

def toChr(intval):
    try:
        return chr(toInt(intval))
    except TypeError:
        print("TOCHR ERROR: ", intval)
        raise

def toInt(hexval):
    try:
        return int(hexval, 16)
    except TypeError:
        print("TOINT ERROR: ", hexval)
        raise

def alphabetize(text):    
    return list(map(lambda x: toChr(alphabet[x]) if x in alphabet.keys() else x, list(text)))

def setup():
    term.open()
    term.set("U+E000: ./fonts/cga88_black.png, size=8x8, align=center")
    term.composition(False)

def setup_menu():
    term.set(
        "window: size={}x{}, cellsize={}x{}, title='Spaceship'".format(
            MENU_SCREEN_WIDTH,
            MENU_SCREEN_HEIGHT,
            MENU_FONT_WIDTH, 
            MENU_FONT_HEIGHT))

def setup_game():
    term.set(
        "window: size={}x{}, cellsize={}x{}, title='Spaceship'".format(
            GAME_SCREEN_WIDTH,
            GAME_SCREEN_HEIGHT,
            GAME_FONT_WIDTH, 
            GAME_FONT_HEIGHT))

def setup_font(font, cx, cy):
    term.set("font: ./fonts/{}.ttf, size={}x{}".format(font, cx, cy))

if __name__ == "__main__":
    setup()
    term.refresh()
    term.read()
