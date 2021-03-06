from bearlibterminal import terminal as term
from strings import *

def setup():
    term.open()
    term.set("U+E000: ./fonts/cga88_black.png, size=8x8, align=center")
    term.composition(False)

def setup_charsheet():
    term.set("U+E000: ./fonts/cga88_black.png, size=8x8, align=center")

def setup_ext(sx, sy, cx="auto", cy=None):
    term.set(
        "window: size={}x{}, cellsize={}{}, title='Spaceship'".format(
            sx, sy, cx, "x" + str(cy) if cy else ""))

def setup_menu():
    term.set(
        "window: size={}x{}, cellsize=auto, title='Spaceship'".format(
            MENU_SCREEN_WIDTH,
            MENU_SCREEN_HEIGHT))

def setup_game():
    term.set(
        "window: size={}x{}, cellsize=8x8, title='Spaceship'".format(
            GAME_SCREEN_WIDTH,
            GAME_SCREEN_HEIGHT))

def setup_font(font, cx=8, cy=None):
    if font == "default":
        term.set('font: default, size=8')
    else:
        term.set("window: cellsize=8x8")
        cy = 'x' + str(cy) if cy else ''
        term.set("font: ./fonts/{}.ttf, size={}{}".format(font, cx, cy))

if __name__ == "__main__":
    setup()
    setup_font('unscii-8-thin', 8)
    term.refresh()
    term.read()
