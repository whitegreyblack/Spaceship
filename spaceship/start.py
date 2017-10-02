import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
import spaceship.constants as consts
from bearlibterminal import terminal as term
from spaceship.constants import MENU_SCREEN_WIDTH as SCREEN_WIDTH
from spaceship.constants import MENU_SCREEN_HEIGHT as SCREEN_HEIGHT
from spaceship.constants import GAME_TITLE_HEIGHT as TITLE_HEIGHT
from spaceship.constants import GAME_TITLE_WIDTH as TITLE_WIDTH
from spaceship.constants import GAME_TITLE as TITLE
from spaceship.constants import GAME_TITLE_VERSION as VERSION
from spaceship.options import options
from spaceship.continue_game import continue_game
from spaceship.create_character import create_character
from spaceship.new_game import new_game
from spaceship.setup import setup, setup_game, setup_menu, setup_font
from spaceship.new_name import new_name
from spaceship.screen_functions import center, longest, colored

def start():
    def splitter(x, y):
        return [z for z in range(x, y, 2)]
    
    setup()
    setup_menu()
    setup_font('Fira', 8, 16)
    proceed = True
    title_index = 0
    title_develop = 'Developed by WGB using Python and BearLibTerminal'
    options_height = splitter(9, SCREEN_HEIGHT)
    title_options = ["[[c]] continue", '[[n]] new game', '[[o]] options', '[[q]] quit']
    width, height = SCREEN_WIDTH, SCREEN_HEIGHT
    title_height = 0
    option_height = 5
    while proceed:
        term.clear() # probably won't need later but using now to make sure title screen is empty
        
        # title header
        term.puts(center('a'*(TITLE_WIDTH-1), SCREEN_WIDTH), title_height, TITLE)

        # VERSION
        term.puts(center(VERSION, SCREEN_WIDTH), title_height+TITLE_HEIGHT+1, VERSION)
        # options
        length, option = longest(title_options)
        x = center(length-2, width)
        for option, i in zip(title_options, range(len(title_options))):
            text = "[color=orange]{}[/color]".format(option) if i == title_index else option
            term.puts(x, options_height[i], text)
        
        # footer 
        term.puts(center(title_develop, width), height-2, title_develop)
        term.refresh()
        code = term.read()

        # key in
        if code in (term.TK_UP, term.TK_DOWN):
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
                cc = create_character()
                if cc.proceed:
                    nn = new_name(cc.value)
                    print(nn)
                    if nn.proceed > 0:
                        proceed = new_game(nn.value, cc.value)
            elif title_index == 2:
                options()
            else:
                proceed = False
        elif code in (term.TK_CLOSE, term.TK_ESCAPE):
            proceed = False        
    
if __name__ == "__main__":
    start()
