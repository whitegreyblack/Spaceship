import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
import spaceship.constants as consts
from bearlibterminal import terminal as term
from spaceship.constants import MENU_SCREEN_WIDTH as SCREEN_WIDTH
from spaceship.constants import MENU_SCREEN_HEIGHT as SCREEN_HEIGHT
from spaceship.options import options
from spaceship.continue_game import continue_game
from spaceship.create_character import create_character
from spaceship.new_game import new_game
from spaceship.setup import setup, setup_game, setup_menu
from spaceship.new_name import new_name
from spaceship.screen_functions import center, longest, colored

def start():
    def splitter(x, y, i):
        return [z for z in range(x, y-x, (y-x)//(i+1))][1:(i+2)]
    
    setup()
    setup_menu()
    proceed = True
    title_index = 0
    title_develop = 'Developed by WGB using Python and BearLibTerminal'
    options_height = splitter(1, SCREEN_HEIGHT-1, 4)
    title_options = ["[[C]]ontinue", '[[N]]ew game', '[[O]]ptions', '[[Q]]uit']
    width, height = SCREEN_WIDTH, SCREEN_HEIGHT
    title_height = 1
    option_height = 5
    print(splitter(3, SCREEN_HEIGHT, 4))
    while proceed:
        term.clear() # probably won't need later but using now to make sure title screen is empty
        
        # title header
        title = 'Working Title Screen'	    
        x = center(title, width)
        term.puts(x, title_height, title)

        # options
        length, option = longest(title_options)
        x = center(length, width)
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
                    if nn.proceed:
                        proceed = new_game(name, player)
            elif title_index == 2:
                options()
            else:
                proceed = False
        elif code in (term.TK_CLOSE, term.TK_ESCAPE):
            proceed = False        
    
if __name__ == "__main__":
    start()
