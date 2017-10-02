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
    def text():
        term.puts(center(direction_name, xhalf*2), yhalf-4, direction_name)
        term.puts(center(direction_exit[2:], xhalf*2), yhalf+2, direction_exit)

    def border():
        for k in range(SCREEN_WIDTH):
            term.puts(k, 3, toChr("2550"))
            term.puts(k, SCREEN_HEIGHT-3, toChr("2550"))
        for i in range(xhalf-fifth, xhalf+fifth):
            term.puts(i, yhalf-2, "{}".format(chr(toInt('2550'))))
            term.puts(i, yhalf, "{}".format(chr(toInt('2550'))))
        for j in range(yhalf-2, yhalf+1):
            term.puts(xhalf-fifth, j, "{}".format(chr(toInt('2551'))))
            term.puts(xhalf+fifth, j, "{}".format(chr(toInt('2551'))))

        term.puts(xhalf-fifth, yhalf-2, "{}".format(chr(toInt('2554'))))
        term.puts(xhalf+fifth, yhalf-2, "{}".format(chr(toInt('2557'))))
        term.puts(xhalf-fifth, yhalf, "{}".format(chr(toInt('255A'))))
        term.puts(xhalf+fifth, yhalf, "{}".format(chr(toInt('255D'))))


    direction_name = 'Enter in your name or leave blank for a random name'
    direction_exit = 'Press [[ESC]] if you wish to exit character creation'
    xhalf = SCREEN_WIDTH//2
    yhalf = SCREEN_HEIGHT//2
    fifth = SCREEN_WIDTH//5

    term.clear()
    border()
    text()
    result, text = term.read_str(xhalf-fifth+1, yhalf-1, "", 30)

    if result:
        term.bkcolor("white")
        term.puts(xhalf-fifth+1, yhalf-1, "[color=black]{}[/color]".format(text))
        term.bkcolor("black")
        term.refresh()
        
    return output(proceed=result, value=text)


if __name__ == "__main__":
    setup()
    name = new_name(None)
    term.refresh()
