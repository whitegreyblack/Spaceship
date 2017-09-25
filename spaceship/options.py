import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from spaceship.screen_functions import *
from bearlibterminal import terminal as term
from spaceship.setup import setup

def options():
    option_title = "options"
    option_index = 0
    option_options = ['full screen', 'tile output', 'dynamic coloring']
    while True:

        term.clear()
        # options title
        term.puts(center(option_title, SCREEN_WIDTH), 3, option_title.upper())

        # options
        for option, i in zip(option_options, range(len(option_options))):
            option = "[color=blue]{}[/color]".format(option) if i == option_index else option
            term.puts(SCREEN_WIDTH//8, SCREEN_HEIGHT//4+i, option)

        # back option
        term.puts(center('back', SCREEN_WIDTH), SCREEN_HEIGHT-2, colored('back') if option_index == 3 else 'back')
        term.refresh()
        code = term.read()

        if code in (term.TK_UP, term.TK_DOWN):
            if code == term.TK_UP:
                option_index -= 1
            else:
                option_index += 1
            if not 0 <= option_index < len(option_options)+1:
                option_index = max(0, min(option_index, len(option_options)))
        elif code in (term.TK_ENTER,):
            print(option_index)
            if option_index == 3:
                print("You picked the options for {}".format('Quit'))
                break
            else:
                print("You picked the options for {}".format(option_options[option_index]))
        elif code in (term.TK_CLOSE, term.TK_ESCAPE):
            break

if __name__ == "__main__":
    setup()
    options()
