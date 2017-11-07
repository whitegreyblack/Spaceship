import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')

from bearlibterminal import terminal as term

import spaceship.constants as consts
from spaceship.constants import GAME_TITLE as TITLE
from spaceship.constants import GAME_TITLE_HEIGHT as TITLE_HEIGHT
from spaceship.constants import GAME_TITLE_VERSION as VERSION
from spaceship.constants import GAME_TITLE_WIDTH as TITLE_WIDTH

if term.state(term.TK_HEIGHT) <= 24:
    from spaceship.constants import GAME_TITLE_SHORT as GTAS
else:
    from spaceship.constants import GAME_TITLE as GTAS

from spaceship.constants import GAME_SCREEN_HEIGHT as SCREEN_HEIGHT
from spaceship.constants import GAME_SCREEN_WIDTH as SCREEN_WIDTH
from spaceship.continue_game import continue_game
from spaceship.create_character import create_character as create_character
from spaceship.new_game import new_game
from spaceship.new_name import new_name
from spaceship.options import options
from spaceship.screen_functions import center, colored, longest
from spaceship.setup import setup, setup_font, setup_game, setup_menu, toChr

debug = False

def start():
    def border():
        for k in range(SCREEN_WIDTH):
            term.puts(k, SCREEN_HEIGHT-6, toChr("2550"))
            term.puts(k, 5, toChr("2550"))

    def calc_option_heights(hoffset, foffset):
        ''' Calculate the remaining space in between the title header and footer
        to come up with the new height and thus the new middle for options start
        '''
        height =  term.state(term.TK_HEIGHT) - hoffset - foffset
        return [hoffset + height//2-height//4 + i * 2 for i in range(4)]

    def splitter(x, y):
        step = (y-x) // (term.state(term.TK_HEIGHT) // 8)

        if debug:
            print(y, x)
            print(step)

        return [x+z for z in range(x, y, step)]

    def update_start_screen():
        if term.state(term.TK_HEIGHT) <= 25:
            title_height = 1
        else:
            title_height = term.state(term.TK_HEIGHT)//5

        if debug:
            print("TITLE HEIGHT: ", title_height)

        return title_height

    def start_new_game():
        cc = create_character()
        if "Exit" not in cc.value:
            return new_game(cc.value)
        return cc.proceed

    proceed = True
    title_index = -1
    title_version = 'version 0.0.7'
    title_develop = 'Developed using BearLibTerminal'
    title_options = ["[[c]] continue", '[[n]] new game', '[[o]] options', '[[q]] quit']
    title_height = update_start_screen()
    options_height = calc_option_heights(title_height+len(GTAS.split('\n')), 3)
    option_height = 5

    while proceed:
        width, height = term.state(term.TK_WIDTH), term.state(term.TK_HEIGHT)
        
        if debug:
            print(title_height, options_height)
        
        term.clear()

        # title header
        term.puts(center('a'*(len(GTAS.split('\n')[0])), width), title_height, GTAS)

        # options
        length, option = longest(title_options)
        x = center(length-2, width)

        for option, i in zip(title_options, range(len(title_options))):
            text = "[color=#00FFFF]{}[/color]".format(option) if i == title_index else option
            term.puts(x, options_height[i], text)
        
        # FOOTER and VERSION
        term.puts(center(len(title_version), width), height-4, title_version)
        term.puts(center(title_develop, width), height-2, title_develop)

        term.refresh()
        code = term.read()

        # key in (CNOQ, ENTER)
        if code == term.TK_C or (code == term.TK_ENTER and title_index == 0):
            proceed = continue_game()
        elif code == term.TK_N or (code == term.TK_ENTER and title_index == 1):
            proceed = start_new_game()
        elif code == term.TK_O or (code == term.TK_ENTER and title_index == 2):
            options()
            title_height = update_start_screen()
            options_height = calc_option_heights(title_height+len(GTAS.split('\n')), 3)
        elif code == term.TK_Q or (code == term.TK_ENTER and title_index == 3):
            proceed = False

        # KEYS (UP, DOWN)
        elif code in (term.TK_UP, term.TK_DOWN):
            if code == term.TK_UP:
                title_index -= 1
            else: 
                title_index += 1
            if not 0 <= title_index < len(title_options):
                title_index = max(0, min(title_index, len(title_options)-1)) 

        elif code in (term.TK_CLOSE, term.TK_ESCAPE):
            proceed = False        
    
        else:
            print("Unknown command")

if __name__ == "__main__":
    term.open()
    setup_font('Ibm_cga', 8, 8)
    term.set('window: size=40x25, cellsize=auto, title="Spaceship", fullscreen=false')    
    start()
