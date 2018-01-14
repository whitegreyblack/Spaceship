import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.screen_functions import *
from bearlibterminal import terminal as term
from spaceship.setup_game import setup
from spaceship.new_game import new_game
import shelve
'''
# The flow tree for playing the game
Main Menu
 | \
 |  \
 |  Continue Game
 |  /
 | /
New Game
'''

def continue_game():
    '''Handles save file opening to continue previously saved games'''

    def get_saves_info():
        '''Combines get_saves and get_descs functions'''
        save_files, save_descs = [], []

        for root, dirs, files in os.walk('saves', topdown=True):
            for f in files:
                if f.endswith('.dat'):
                    save_files.append(f.replaces('.dat', ''))
                    with shelve.open(f, 'r') as save:
                        save_descs.append(save['save'])

        return save_files, save_descs

    def get_saves():
        '''Handles the retrieving of saved data files'''
        save_files = []
        for root, dirs, files in os.walk('saves', topdown=True):
            # get all files in the save directory and parse their file names
            for f in files:
                if f.endswith('.dat'):
                    save_files.append(f.replace('.dat', ''))
        return save_files

    def get_saves_desc():
        '''Handles the retrieving of saved data file descriptions'''
        if not save_files:
            # no save files yet -- early exit
            return []
        
        file_descs = []
        for save_file in save_files:
            with shelve.open("./saves/" + save_file, 'r') as save:
                file_descs.append(save['save'])

        return file_descs

    def no_saves():
        '''Handles printing the no save ui screen to terminal'''
        term.puts(
            center(
                'No Saved Games', 
                term.state(term.TK_WIDTH)), 
            term.state(term.TK_HEIGHT)//2, 
            'NO SAVED GAMES')

    def saves_exists():
        '''Handles printing the saved files to terminal'''
        if len(save_files) != len(save_files_desc):
            raise ValueError("Save files number does not match save files descs number")

        # save screen header
        for i in range(term.state(term.TK_WIDTH)):
            term.puts(i, 0, '#')
        term.puts(center('Saved Files  ', term.state(term.TK_WIDTH)), 0, ' Saved Files ')

        # list the saved files
        for i, (save, desc) in enumerate(zip(save_files, save_files_desc)):
            # split the save file string from plain and hash text
            save = save.split('(')[0]
            letter = chr(ord('a') + i) + '. '
            if i == save_index:
                save = "[c=#00FFFF]{}[/c]".format(save)
            term.puts(1, 3 + i, letter + save + " :- " + desc)
    
    # saved files list and index
    save_index = 0
    save_files = get_saves()
    save_files_desc = get_saves_desc()

    while True:    
        term.clear()

        if not os.path.isdir('saves') or os.listdir('saves') == []:
            # make sure either folder does not exist or empty folder
            no_saves()

        else:
            # any other case triggers branch
            saves_exists()

        term.refresh()
        code = term.read()

        if code == term.TK_ENTER and save_files:

            try:
                # use context manager to make sure file handling is safe
                with shelve.open("./saves/" + save_files[save_index], 'r') as save:
                    # since shelve serializes objects into data we can unpack directly from the dictionary
                    new_game(character=save['player'], world=save['world'])

            except FileNotFoundError:
                term.puts(0, term.state(term.TK_HEIGHT - 1), 'File Not Found')
                
            finally:    
                break # --> makes sure we exit loop to return directly to new screen
                    
        elif code == term.TK_DOWN:
            save_index = min(save_index + 1, len(save_files)-1)

        elif code == term.TK_UP:
            save_index = max(save_index - 1, 0)

        elif code == term.TK_ESCAPE:
            break

    return True
# End Continue Menu

if __name__ == "__main__":
    setup()
    continue_game()