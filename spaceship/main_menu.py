import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
from bearlibterminal import terminal as term

from .setup_game import setup, setup_font, setup_menu
from .start import Scene
from .screen_functions import *

class Main(Scene):
    def __init__(self, width, height, title='main_menu'):
        super().__init__(width, height, title)

    def setup(self):
        self.index = -1
        
        self.version = 'version 0.1.3'
        self.developed_by = 'Developed using BearLibTerminal'
        
        self.options = [
                "[[c]] continue",
                '[[n]] new game',
                '[[o]] options',
                '[[q]] quit']
        
        self.title_height = 1 if self.height <= 25 else self.height // 5

        self.title = self.calc_title()
        options_header_offset = self.title_height + len(self.title.split('\n'))
        self.options_height = self.calc_options_heights(options_header_offset, 3)

    def calc_title(self):
        if self.height <= 25:
            from .constants import GAME_TITLE_SHORT as game_title
        else:
            from .constatns import GAME_TITLE as game_title
        return game_title

    def calc_options_heights(self, header_offset, footer_offset):
        total_height = self.height - header_offset - footer_offset
        return [header_offset + total_height // 2 - total_height // 4 + option * 2 for option in range(4)]

    def run(self):
        while self.proceed:
            self.draw()

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

        for option, i in zip(self.options, range(len(self.options))):
            text = "[color=#00FFFF]{}[/color]".format(option) if i == self.index else option
            term.puts(x, self.options_height[i], text)

        # FOOTER and VERSION
        term.puts(center(len(self.version), self.width), self.height - 4, self.version)
        term.puts(center(self.developed_by, self.width), self.width - 2, self.developed_by)

        term.refresh()
        code = term.read()

        # key in (CNOQ, ENTER)
        if code == term.TK_C or (code == term.TK_ENTER and self.index == 0):
            proceed = continue_game()

        elif code == term.TK_N or (code == term.TK_ENTER and self.index == 1):
            proceed = start_new_game()

        elif code == term.TK_O or (code == term.TK_ENTER and self.index == 2):
            options()
            height = update_start_screen()
            self.options_height = calc_option_heights(height+len(GTAS.split('\n')), 3)

        elif code == term.TK_Q or (code == term.TK_ENTER and self.index == 3):
            proceed = False

        # KEYS (UP, DOWN)
        elif code in (term.TK_UP, term.TK_DOWN):
            if code == term.TK_UP:
                self.index -= 1
            else: 
                self.index += 1
            if not 0 <= self.index < len(self.options):
                self.index = max(0, min(self.index, len(self.options) - 1))

        elif code in (term.TK_CLOSE, term.TK_ESCAPE):
            self.proceed = False

class Start(Scene):
    def __init__(self, width, height, title='start_menu'):
        super().__init__(width, height, title)

class Options(Scene):
    def __init__(self, width, height, title='options_menu'):
        super().__init__(width, height, title)

class Continue(Scene):
    def __init__(self, width, height, title='continue_menu'):
        super().__init__(width, height, title)

if __name__ == "__main__":
    term.open()
    setup_font('Ibm_cga', cx=8, cy=8)
    term.set('window: size=80x25, cellsize=auto, title="Spaceship", fullscreen=false')

    m = Main(80, 25)
    m.setup()
    m.run()
    # s = Start(80, 25)
    # o = Options(80, 25)
    # c = Continue(80, 25)

    # m.add_scene_child(o)
    # m.add_scene_child(c)
    # m.add_scene_child(s)

    # s.add_scene_parent(m)
    # o.add_scene_parent(m)
    # c.add_scene_parent(m)

    # print([child.title for child in m.children])

    # for scene in (s, c, o):
    #     print([p.title for p in scene.parents])
