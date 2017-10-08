import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')

from bearlibterminal import terminal as term

import spaceship.constants as consts
from spaceship.constants import GAME_TITLE as TITLE
from spaceship.constants import GAME_TITLE_HEIGHT as TITLE_HEIGHT
from spaceship.constants import GAME_TITLE_VERSION as VERSION
from spaceship.constants import GAME_TITLE_WIDTH as TITLE_WIDTH
from spaceship.constants import MENU_SCREEN_HEIGHT as SCREEN_HEIGHT
from spaceship.constants import MENU_SCREEN_WIDTH as SCREEN_WIDTH
from spaceship.continue_game import continue_game
from spaceship.create_character import create_character as create_character
from spaceship.new_game import new_game
from spaceship.new_name import new_name
from spaceship.options import options
from spaceship.screen_functions import center, colored, longest
from spaceship.setup import setup, setup_font, setup_game, setup_menu, toChr


def start():
    def border():
        for k in range(SCREEN_WIDTH):
            term.puts(k, SCREEN_HEIGHT-6, toChr("2550"))
            term.puts(k, 5, toChr("2550"))

    def splitter(x, y):
        return [z for z in range(x, y, 2)]
    
    def start_new_game():
        cc = create_character()
        if "Exit" not in cc.value:
            return new_game(cc.value)
        return cc.proceed

    # Terminal Setup
    setup()
    setup_font('Fira', 8, 16)
    setup_menu()

    proceed = True
    title_index = -1
    options_height = splitter(10, SCREEN_HEIGHT)
    title_develop = 'Developed by WGB using Python and BearLibTerminal'
    title_options = ["[[c]] continue", '[[n]] new game', '[[o]] options', '[[q]] quit']
    width, height = SCREEN_WIDTH, SCREEN_HEIGHT
    title_height = 0
    option_height = 5
    while proceed:
        term.clear() # probably won't need later but using now to make sure title screen is empty
        border()
        # title header
        term.puts(center('a'*(TITLE_WIDTH-1), SCREEN_WIDTH), title_height+3, TITLE)

        # options
        length, option = longest(title_options)
        x = center(length-2, width)
        for option, i in zip(title_options, range(len(title_options))):
            text = "[color=orange]{}[/color]".format(option) if i == title_index else option
            term.puts(x, options_height[i], text)
        
        # footer 
        # VERSION
        term.puts(center(VERSION, SCREEN_WIDTH), SCREEN_HEIGHT-4, VERSION)
        term.puts(center(title_develop, width), height-2, title_develop)
        term.refresh()
        code = term.read()

        # key in
        if code in (term.TK_C, term.TK_N, term.TK_O, term.TK_Q):
            # branching
            if code == term.TK_C:
                proceed = continue_game()
            elif code == term.TK_N:
                proceed = start_new_game()
            elif code == term.TK_O:
                options()
            else:
                proceed = False

        elif code in (term.TK_UP, term.TK_DOWN):
            if code == term.TK_UP:
                title_index -= 1
            else: 
                title_index += 1
            if not 0 <= title_index < len(title_options):
                title_index = max(0, min(title_index, len(title_options)-1)) 
                
        elif code in (term.TK_ENTER,):
            if title_index == 0:
                proceed = continue_game()
            elif title_index == 1:
                proceed = start_new_game()
            elif title_index == 2:
                options()
            else:
                proceed = False
        elif code in (term.TK_CLOSE, term.TK_ESCAPE):
            proceed = False        
    
if __name__ == "__main__":
    start()
