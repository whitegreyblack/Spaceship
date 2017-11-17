import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.constants import MENU_SCREEN_WIDTH as SCREEN_WIDTH
from spaceship.constants import MENU_SCREEN_HEIGHT as SCREEN_HEIGHT
from spaceship.screen_functions import *
from bearlibterminal import terminal as term
from spaceship.setup_game import setup
import shelve
# Begin continue Menu
def continue_game():
    def no_saves():
        term.puts(
            center(
                'No Saved Games', 
                term.state(term.TK_WIDTH)), 
            term.state(term.TK_HEIGHT)//2, 
            'NO SAVED GAMES')
    
    def saves_exists():
        for root, dirs, files in os.walk('saves', topdown=True):
            for f in files:
                if f.endswith('.dat'):
                    save_files.append(f.replace('.dat', ''))

        for i, save in enumerate(save_files):
            term.puts(1, 3 + i, save)
    
    save_index = 0
    save_files = []
    while True:    
        term.clear()
        if not os.path.isdir('saves') or os.listdir('saves') == []:
            no_saves()
        else:
            saves_exists()
        term.refresh()
        code = term.read()

        if code == term.TK_ENTER and save_files:
            print('/saves/' + save_files[save_index])
            with shelve.open("./saves/" + save_files[save_index], 'r') as save:
                world_map = save['world']
                player = save['player']

            print(player.name, world_map)
            exit("Finished opening file")
        elif code == term.TK_ESCAPE:
            break

    return True
# End Continue Menu

if __name__ == "__main__":
    setup()
    continue_game()