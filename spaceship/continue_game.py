import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.screen_functions import *
from bearlibterminal import terminal as term
from spaceship.setup_game import setup
import shelve
# Begin continue Menu
def continue_game():

    def get_saves():
        '''Retrieves save files'''
        save_files = []
        for root, dirs, files in os.walk('saves', topdown=True):
            # get all files in the save directory and parse their file names
            for f in files:
                if f.endswith('.dat'):
                    save_files.append(f.replace('.dat', ''))
        return save_files

    def no_saves():
        '''Prints no save ui screen to terminal'''
        term.puts(
            center(
                'No Saved Games', 
                term.state(term.TK_WIDTH)), 
            term.state(term.TK_HEIGHT)//2, 
            'NO SAVED GAMES')

    def saves_exists():
        '''Prints saved files to terminal'''
        # save screen header
        for i in range(term.state(term.TK_WIDTH)):
            term.puts(i, 0, '#')
        term.puts(center('Saved Files  ', term.state(term.TK_WIDTH)), 0, ' Saved Files ')

        # list the saved files
        for i, save in enumerate(save_files):
            if i == save_index:
                save = "[c=#00FFFF]{}[/c]".format(save)
            term.puts(1, 3 + i, save)
    
    save_index = 0
    save_files = get_saves()
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

        elif 

        elif code == term.TK_ESCAPE:
            break



    return True
# End Continue Menu

if __name__ == "__main__":
    setup()
    continue_game()