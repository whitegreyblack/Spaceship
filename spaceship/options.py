import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
import spaceship.constants as consts
from spaceship.screen_functions import center, longest, colored
from spaceship.constants import MENU_SCREEN_WIDTH as SCREEN_WIDTH
from spaceship.constants import MENU_SCREEN_HEIGHT as SCREEN_HEIGHT
from bearlibterminal import terminal as term
from spaceship.setup import setup
from collections import namedtuple

def options():
    width, height = SCREEN_WIDTH, SCREEN_HEIGHT
    options = namedtuple("Options", "fs to dc")
    full_screen = False
    tile_output = "8x16"
    full_colors = False

    option_title = "options"
    option_index = 0
    option_options = ['full screen', 'tile output', 'dynamic coloring']
    '''
    (o) fullscreen [unchecked] 
    (v) fullscreen [checked]
    '''
    while True:

        term.clear()
        # options title
        term.puts(center(option_title, width), 3, option_title.upper())

        # options
        for option, i in zip(option_options, range(len(option_options))):
            option = "[color=orange]{}[/color]".format(option) if i == option_index else option
            term.puts(width//8, height//4+i*2, option)

        # back option
        term.puts(center('back', width), height-2, colored('back') if option_index == 3 else 'back')
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
                return options(
                        full_screen,
                        tile_output,
                        full_colors,)
            else:
                print("You picked the options for {}".format(option_options[option_index]))
        elif code in (term.TK_CLOSE, term.TK_ESCAPE):
            return options(
                full_screen,
                tile_output,
                full_colors,)

if __name__ == "__main__":
    setup()
    print(options())
