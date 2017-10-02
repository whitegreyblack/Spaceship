import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.constants import MENU_SCREEN_WIDTH as SCREEN_WIDTH
from spaceship.constants import MENU_SCREEN_HEIGHT as SCREEN_HEIGHT
from bearlibterminal import terminal as term
from spaceship.screen_functions import *
from spaceship.setup import setup, output, toChr
from spaceship.maps import toInt

def new_name(character) -> (int, str):
    def border():
        for k in range(SCREEN_WIDTH):
            term.puts(k, 3, toChr("2550"))
            term.puts(k, SCREEN_HEIGHT-3, toChr("2550"))
        for i in range(x-w, x+w):
            term.puts(i, y-2, "{}".format(chr(toInt('2550'))))
            term.puts(i, y, "{}".format(chr(toInt('2550'))))
        for j in range(y-2, y+1):
            term.puts(x-w, j, "{}".format(chr(toInt('2551'))))
            term.puts(x+w, j, "{}".format(chr(toInt('2551'))))
        term.puts(x-w, y-2, "{}".format(chr(toInt('2554'))))
        term.puts(x+w, y-2, "{}".format(chr(toInt('2557'))))
        term.puts(x-w, y, "{}".format(chr(toInt('255A'))))
        term.puts(x+w, y, "{}".format(chr(toInt('255D'))))
    direction_name = 'Enter in your name or leave blank for a random name'
    direction_exit = 'Press [[ESC]] if you wish to exit character creation'

    x = SCREEN_WIDTH//2
    w = SCREEN_WIDTH//5
    y = SCREEN_HEIGHT//2
    #term.clear_(x-w, y-3, x, 6)area

    term.clear()
    border()
    term.puts(center(direction_name, x*2), y-4, direction_name)
    term.puts(center(direction_exit[2:], x*2), y+2, direction_exit)
    result, text = term.read_str(x-w+1, y-1, "", 30)

    if result:
        term.bkcolor("white")
        term.puts(x-w+1, y-1, "[color=black]{}[/color]".format(text))
        term.bkcolor("black")
    return output(proceed=result, value=text)


if __name__ == "__main__":
    setup()
    name = new_name(None)
    term.refresh()
