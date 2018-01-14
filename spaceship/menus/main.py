import os
import sys
import shelve
import random
from collections import namedtuple
from bearlibterminal import terminal as term
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
import strings as strings
from screen_functions import *
from .options import Options
from .scene import Scene
from .game import Start

'''
Notes: Propagating Game Variables Through Scenes
    Since starting a new game will need a character parameter
    we need to embed CONTiNUE, START, and NAME into the GAME
    screen.

    So on main screen:
        If either continue or new game is switch:
            Then Start Game runs
        Elif Options is switch:
            Then options menu runs
        Else:
            Selected quit quits game
            Everything else does nothing
''' 
class Main(Scene):
    def __init__(self, sid='main_menu'):
        super().__init__(sid)

    def setup(self):
        self.index = -1
        
        self.version = 'version 0.1.3'
        self.developed_by = 'Developed using BearLibTerminal'
        
        self.options = [
                "[[c]] continue",
                '[[n]] new game',
                '[[o]] options',
                '[[q]] quit']

        self.reset()       

    def reset(self):
        self.reset_size()
        self.title_height = 1 if self.height <= 25 else self.height // 5
        self.title = self.calc_title()
        options_header_offset = self.title_height + len(self.title.split('\n'))
        self.options_height = self.calc_options_heights(options_header_offset, 3)

    def calc_title(self):
        if self.height <= 25:
            return strings.GAME_TITLE_SHORT
        else:
            return strings.GAME_TITLE

    def calc_options_heights(self, header_offset:int, footer_offset:int) -> list:
        '''Returns the height values for the options based on screen height'''
        def calculate(option):
            half_height = total_height // 2
            quarter_height = total_height // 4

            return header_offset + half_height - quarter_height + option

        total_height = self.height - header_offset - footer_offset

        return [calculate(option * 2) for option in range(4)]

    def draw(self):
        term.clear()

        # title header -- multiplying space with title length to center title
        term.puts(
            center(' ' * (len(self.title.split('\n')[0])), self.width), 
            self.title_height, 
            self.title)

        # options
        length, option = longest(self.options)
        x = center(length - 2, self.width)

        for option, index in zip(self.options, range(len(self.options))):
            if index == self.index:
                option = "[color=#00FFFF]{}[/color]".format(option)
            term.puts(x, self.options_height[index], option)

        # FOOTER and VERSION
        term.puts(
            center(len(self.version), self.width), 
            self.height - 4, 
            self.version)

        term.puts(center(self.developed_by, self.width), 
            self.width - 2, 
            self.developed_by)

        term.refresh()
        code = term.read()

        # key (CNOQ, ENTER)
        if code == term.TK_C or (code == term.TK_ENTER and self.index == 0):
            # proceed = continue_game()
            # self.ret = self.scene_child('continue_menu')
            self.ret['scene'] = 'continue_menu'
            self.proceed = False

        # key press on N or enter on NEW GAME
        elif code == term.TK_N or (code == term.TK_ENTER and self.index == 1):
            # proceed = start_new_game()
            # self.ret = self.scene_child('create_menu')
            self.ret['scene'] = 'create_menu'
            self.proceed = False

        # key press on O or enter on OPTIONS
        elif code == term.TK_O or (code == term.TK_ENTER and self.index == 2):
            # options()
            # height = update_start_screen() + len(self.title.split('\n'))
            # self.options_height = calc_option_heights(height, 3)
            # self.ret = self.scene_child('options_menu')
            self.ret['scene'] = 'options_menu'
            self.proceed = False

        # key press on Q or enter on QUIT
        elif code == term.TK_Q or (code == term.TK_ENTER and self.index == 3):
            self.proceed = False

        # KEYS (UP, DOWN)
        elif code in (term.TK_UP, term.TK_DOWN):
            if code == term.TK_UP:
                self.index -= 1
            else: 
                self.index += 1
            if not 0 <= self.index < len(self.options):
                self.index = max(0, min(self.index, len(self.options) - 1))

        elif code in (term.TK_CLOSE, term.TK_ESCAPE):
            self.ret['scene'] = 'exit_desktop'
            self.proceed = False

if __name__ == "__main__":
    term.open()
    m = Main()
    m.run()