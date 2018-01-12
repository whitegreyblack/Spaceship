import os
import sys
import shelve
import random
import textwrap
from time import sleep, time
from collections import namedtuple
from bearlibterminal import terminal as term
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
import strings
from screen_functions import *
from action import commands_player
from gamelog import GameLogger
from .scene import Scene
from ..classes.wild import wilderness
from ..classes.player import Player
from ..classes.world import World
from ..classes.city import City
from ..classes.cave import Cave

class Continue(Scene):
    def __init__(self, sid='continue_menu'):
        super().__init__(sid)

    def setup(self):
        self.index = 0
        self.loaded = False
        self.files, self.descs = self.saves_info()

    def saves_info(self):
        save_files, save_descs = [], []

        for root, dirs, files in os.walk('saves', topdown=True):
            for f in files:
                if f.endswith('.dat'):
                    file_name = f.replace('.dat', '')

                    if file_name not in save_files:
                        save_files.append(file_name)
                        
                        with shelve.open('./saves/' + file_name, 'r') as save:
                            save_descs.append(save['desc'])

        if len(save_files) != len(save_descs):
            log = "Save files number does not match save files descs number"
            raise ValueError(log)

        return save_files, save_descs

    def saves_exists(self):
        '''Handles listing the saved files to terminal'''
        # save screen header border
        for i in range(self.width):
            term.puts(i, 0, '#')

        # save screen header
        term.puts(
            x=center('Saved Files  ', self.width), 
            y=0, 
            s=' Saved Files ')

        # list the saved files
        for i, (save, desc) in enumerate(zip(self.files, self.descs)):
            # split the save file string from plain and hash text
            save = save.split('(')[0]
            letter = chr(ord('a') + i) + '. '

            if i == self.index:
                save = "[c=#00FFFF]{}[/c]".format(save)

            term.puts(1, 3 + i, letter + save + " :- " + desc)  

    def save_safe(self):
        try:
            with shelve.open("./saves/" + self.files[self.index], 'r') as save:
                self.ret['kwargs'] = {
                    'player': save['player'],
                    'world': save['world'],
                    'turns': save['turns'],
                }
        except FileNotFoundError:
            term.puts(0, self.height, 'File Not Found')
        finally:
            return self.ret['kwargs'] != None

    def draw(self):
        term.clear()

        if not os.path.isdir('saves') or os.listdir('saves') == []:
            # make sure either folder does not exist or empty folder
            term.puts(
                x=center('No Saved Games', term.state(term.TK_WIDTH)), 
                y=term.state(term.TK_HEIGHT) // 2, 
                s='NO SAVED GAMES')
        else:
            # any other case triggers branch
            self.saves_exists()

        term.refresh()
        code = term.read()

        if code == term.TK_ENTER and self.files:
            if self.save_safe():
                self.proceed = False
                self.ret['scene'] = 'start_game' # self.scene_child('new_game')

        elif code == term.TK_DOWN:
            self.index = min(self.index + 1, len(self.files) - 1)

        elif code == term.TK_UP:
            self.index = max(self.index - 1, 0)

        elif code == term.TK_ESCAPE:
            self.proceed = False
            self.ret['scene'] = 'main_menu'

        elif code == term.TK_D:
            print('delete save')

if __name__ == "__main__":
    term.open()
    c = Continue()
    c.run()