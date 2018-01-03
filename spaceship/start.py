import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')

from bearlibterminal import terminal as term

from .constants import GAME_TITLE as TITLE
from .constants import GAME_TITLE_HEIGHT as TITLE_HEIGHT
from .constants import GAME_TITLE_VERSION as VERSION
from .constants import GAME_TITLE_WIDTH as TITLE_WIDTH

if term.state(term.TK_HEIGHT) <= 24:
    from .constants import GAME_TITLE_SHORT as GTAS
else:
    from .constants import GAME_TITLE as GTAS

from .continue_game import continue_game
from .create_character import create_character as create_character
from .new_game import new_game
from .options import options
from .screen_functions import center, colored, longest
from .setup_game import setup, setup_font, setup_menu

debug = False
'''
def connect_scenes(scene_a, scene_b):
    scene_a.add_scene(scene_b)
    scene_b.add_scene(scene_a)

    scene_a.add_child_scene(scene_b)
    scene_b.add_parent_scene(scene_a)
'''
class Scene:
    def __init__(self, width, height, title='Scene'):
        self.width, self.height = width, height
        self.title = title
        
        self.proceed = False

        # scenes is a dictionary holding other scene objects
        self.scenes = {}

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, h):
        self.__height = h

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, w):
        self.__width = w

    def scene(self, title):
        try:
            return self.scenes[title]
        except KeyError:
            print('No scene with that title')
        except:
            raise

    # def add_scene(self, title, priority, scene):
    #     self.scenes[(title, priority)] = scene

    def check_scene(self, scene):
        if scene.title in self.scenes.keys():
            raise ValueError('Same title already in scene')
        elif scene.width != self.width:
            raise ValueError('Incoming scene does not have the same width as current scene')
        elif scene.height != self.height:
            raise ValueError('Incoming scene does not have the same height as current scene')
        return True

    def add_scene_child(self, scene):
        self.check_scene(scene)
        self.scenes[(scene.title, 0)] = scene
    
    def add_scene_parent(self, scene):
        self.check_scene(scene)
        self.scenes[(scene.title, 1)] = scene

    @property
    def children(self):
        '''Returns a list of children scene objects'''
        return [self.scenes[(title, scene)] for title, scene in self.scenes.keys() if scene == 0]

    @property
    def parents(self):
        '''Returns a list of parent scene objects'''
        return [self.scenes[(title, scene)] for title, scene in self.scenes.keys() if scene == 1]

def start():
    def calc_option_heights(hoffset, foffset):
        ''' Calculate the remaining space in between the title header and footer
        to come up with the new height and thus the new middle for options start
        '''
        height =  term.state(term.TK_HEIGHT) - hoffset - foffset
        return [hoffset + height//2-height//4 + i * 2 for i in range(4)]

    def splitter(x, y):
        '''Takes in two points, start and end, and returns a list of all points
        including start point that corresponds with the step integer
        '''
        step = (y - x) // (term.state(term.TK_HEIGHT) // 8)
        return [x + z for z in range(x, y, step)]

    def update_start_screen():
        '''Calculates the height of the title dependant on the screen height'''
        if term.state(term.TK_HEIGHT) <= 25:
            title_height = 1
        else:
            title_height = term.state(term.TK_HEIGHT) // 5
        return title_height

    def start_new_game():
        '''Calls create_character, checks return and sends it to new game'''
        cc = create_character()
        if "Exit" not in cc.value:
            val =  new_game(cc.value)
            return val
        return cc.proceed

    proceed = True
    title_index = -1
    title_version = 'version 0.1.3'
    title_develop = 'Developed using BearLibTerminal'
    title_options = [
            "[[c]] continue",
            '[[n]] new game',
            '[[o]] options',
            '[[q]] quit']
    title_height = update_start_screen()
    options_height = calc_option_heights(title_height + len(GTAS.split('\n')), 3)

    while proceed:
        width, height = term.state(term.TK_WIDTH), term.state(term.TK_HEIGHT)

        term.clear()

        # title header -- multiplying space with title length to center title
        term.puts(center(' ' * (len(GTAS.split('\n')[0])), width), title_height, GTAS)

        # options
        length, option = longest(title_options)
        x = center(length - 2, width)

        for option, i in zip(title_options, range(len(title_options))):
            text = "[color=#00FFFF]{}[/color]".format(option) if i == title_index else option
            term.puts(x, options_height[i], text)

        # FOOTER and VERSION
        term.puts(center(len(title_version), width), height - 4, title_version)
        term.puts(center(title_develop, width), height - 2, title_develop)

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
                title_index = max(0, min(title_index, len(title_options) - 1))

        elif code in (term.TK_CLOSE, term.TK_ESCAPE):
            proceed = False

if __name__ == "__main__":
    term.open()
    setup_font('Ibm_cga', 8, 8)
    term.set('window: size=80x25, cellsize=auto, title="Spaceship", fullscreen=false')
    start()

"""
# main_menu:
    # new_game
    # continue_game
    # play_game

    while 1: # main menu
        while 1: # game loop
            while 1: # key handler
"""