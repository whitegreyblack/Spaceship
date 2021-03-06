# import os
# import sys
import shelve
import random
import textwrap
from time import sleep, time
from collections import namedtuple
from bearlibterminal import terminal as term
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
import spaceship.strings as strings
from .screen_functions import *
from .action import commands_player
from .gamelog import GameLogger
from .scene import Scene
from .classes.wild import wilderness
from .classes.player import Player
from .classes.world import World
from .classes.city import City
from .classes.cave import Cave

class Name(Scene):
    def __init__(self, sid='name_menu'):
        super().__init__(scene_id=sid)

    def setup(self):
        self.direction_name = 'Enter in your name or leave blank for a random name'
        self.direction_exit = 'Press [[ESC]] if you wish to exit character creation'
        self.direction_exit_program = 'Press [[Shift]]+[[ESC]] to exit to main menu'
        self.xhalf = self.width // 2
        self.fifth = self.width // 5
        self.yhalf = self.height // 2
        self.final_name = 'Grey'
        self.invalid = False

    def draw_text(self):
        term.puts(
            x=center(self.direction_name, self.xhalf * 2), 
            y=self.yhalf - 5, 
            s=self.direction_name)
        term.puts(
            x=center(self.direction_exit[2:], self.xhalf * 2), 
            y=self.yhalf + 4, 
            s=self.direction_exit)
        term.puts(
            x=center(self.direction_exit_program[2:], self.xhalf * 2), 
            y=self.yhalf + 8, 
            s=self.direction_exit_program)

    def draw_border(self):
        # for k in range(SCREEN_WIDTH):
        #     term.puts(k, 3, toChr("2550"))
        #     term.puts(k, SCREEN_HEIGHT-3, toChr("2550"))

        # horizontal border variables
        hor_lo = self.xhalf - self.fifth
        hor_hi = self.xhalf + self.fifth
        
        # vertical border variables
        ver_lo = self.yhalf - 2
        ver_hi = self.yhalf

        # draw horizontal border
        for i in range(hor_lo, hor_hi):
            term.puts(i, ver_lo, "{}".format(toChr('2550')))
            term.puts(i, ver_hi, "{}".format(toChr('2550')))
        
        # draw vertical border
        for j in range(ver_lo, ver_hi):
            term.puts(hor_lo, j, "{}".format(toChr('2551')))
            term.puts(hor_hi, j, "{}".format(toChr('2551')))

        # corner border
        term.puts(hor_lo, ver_lo, "{}".format(toChr('2554')))
        term.puts(hor_hi, ver_lo, "{}".format(toChr('2557')))
        term.puts(hor_lo, ver_hi, "{}".format(toChr('255A')))
        term.puts(hor_hi, ver_hi, "{}".format(toChr('255D')))

    def random_name(self):
        return 'Grey'

    def draw(self):
        term.clear()
        self.draw_border()
        self.draw_text()

        term.puts(
            x=self.xhalf - self.fifth + 1, 
            y=self.yhalf - 1,
            s=self.final_name)
        
        if self.invalid:
            term.puts(
                self.xhalf - self.fifth + 1, 
                self.yhalf + 1, 
                '[c=red]{} is not a valid character[/c]'.format(
                    chr(term.state(term.TK_WCHAR))))

        self.invalid = False
        term.refresh()

        key = term.read()
        if key == term.TK_ESCAPE:
            if term.state(term.TK_SHIFT):
                # shift escape -> to desktop
                self.ret['scene'] = 'exit_desktop'

            # elif not self.final_name:
            else:
                self.ret['scene'] = 'create_menu'

            # else:
            #     self.final_name = self.final_name[0:len(self.final_name) - 1]
            #     self.ret = 'start_game'
            self.final_name = ''
            self.proceed = False

        elif key == term.TK_ENTER:
            if not self.final_name:
                self.final_name = self.random_name()

            self.ret['scene'] = 'start_game'
            self.ret['kwargs'].update({'name': self.final_name})
            self.proceed = False

        elif key == term.TK_BACKSPACE:
            if self.final_name:
                self.final_name = self.final_name[0:len(self.final_name) - 1]

        elif term.check(term.TK_WCHAR) and len(self.final_name) < 30:
            # make sure these characters are not included in names
            if chr(term.state(term.TK_WCHAR)) not in (
                '1234567890!@#$%^&&*()-=_+,./<>?";[]{}\|~`'):
                self.final_name += chr(term.state(term.TK_WCHAR))
            else:
                self.invalid = True

if __name__ == "__main__":
    term.open()
    n = Name()
    n.run()