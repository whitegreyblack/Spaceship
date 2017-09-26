import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from bearlibterminal import terminal as term
from spaceship.screen_functions import *
from spaceship.options import options
from spaceship.continue_game import continue_game
from spaceship.create_character import create_character
from spaceship.new_game import new_game
from spaceship.setup import setup
from spaceship.new_name import new_name

def start():
    setup()
    proceed = True
    title_index = 0
    title_develop = 'Developed by WGB using Python and BearLibTerminal'
    title_options = ["(C) continue", '(N) new game', '(O) options', '(Q) quit']
    while proceed:

        term.clear() # probably won't need later but using now to make sure title screen is empty
        title = 'Working Title Screen'	    
        x = center(title, SCREEN_WIDTH)
        # title header
        term.puts(x, SCREEN_HEIGHT//3, title)

        # options
        length, option = longest(title_options)
        x = center(length, SCREEN_WIDTH)
        for option, i in zip(title_options, range(len(title_options))):
            text = "[color=orange]{}[/color]".format(option) if i == title_index else option
            term.puts(x, SCREEN_HEIGHT//2+i*2, text)
        
        # footer 
        term.puts(center(title_develop, SCREEN_WIDTH), SCREEN_HEIGHT-2, title_develop)
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
                proceed = continue_screen()
            elif title_index == 1:
                player = create_character()
                if player:
                    res, name = new_name(player)
                if player and res:
                    proceed = new_game(name, player)
            elif title_index == 2:
                options()
            else:
                proceed = False
        elif code in (term.TK_CLOSE, term.TK_ESCAPE):
            proceed = False        
    
if __name__ == "__main__":
    start()
