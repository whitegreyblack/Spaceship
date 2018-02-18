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
from .scene import Scene
from .option import Option

class Options(Scene):
    def __init__(self, sid='options_menu'):
        super().__init__(sid)

    def setup(self):
        self.option = Option("Options Screen")
        # 80x25 -> 8x16 | 80x50 -> 8x8 | 160x50 -> 16x16 | FullScreen -> 16x16
        self.option.add_opt("Screen Size", 
            ["80x25", "80x50", "160x50", "160x100"]) 
            
        # "Full Screen: {}x{}".format(sysize(0), sysize(1))])
        self.option.add_opt("Cell Size", ["Auto", "8x16", "8x8", "16x16"])

        self.option.add_opt("Font Choice", 
            ["Default", "Source", "Fira", "Fira-Bold", "IBM_CGA", "Andale", 
             "Courier", "Unscii-8", "Unscii-8-thin", "VeraMono"])

        self.option.add_opt("Coloring", 
            ["Dynamic", "Dark", "Light", "Colorblind"])
        
        self.prop = {
            'gx': term.state(term.TK_WIDTH),
            'gy': term.state(term.TK_HEIGHT),
            'cx': term.state(term.TK_CELL_WIDTH),
            'cy': term.state(term.TK_CELL_HEIGHT),            
        }
    
    def parse_screensize(self, screensize):
        if "Full Screen" in screensize:
            sx = sysize(0) // term.state(term.TK_CELL_WIDTH)
            sy = sysize(1) // term.state(term.TK_CELL_HEIGHT)
        else:
            sx, sy = list(map(lambda x: int(x), screensize.split('x')))

        if (self.prop['gx'], self.prop['gy']) != (sx, sy):
            self.prop['gx'], self.prop['gy'] = sx, sy
            return True
        return False

    def parse_cellsize(self, cellsize):
        if cellsize == "Auto":
            if self.prop['cx'] != 'Auto':
                self.prop['cx'], self.prop['cy'] = "auto", None
                return True
        else:
            cx, cy = list(map(lambda x: int(x), cellsize.split('x')))
            if (self.prop['cx'], self.prop['cy']) != (cx, cy):
                self.prop['cx'], self.prop['cy'] = (cx, cy)
                return True
        return False

    def parse_fonts(self, font):
        if self.option == "Default":
            term.set('font: default, size={}{}'.format(
                self.prop['cx'], 
                'x' + str(self.prop['cy']) if self.prop['cy'] != self.prop['cx'] else ''))

        else:
            if self.prop['cx'] == "auto":
                cy = 8 if font not in ("Andale, Courier, VeraMono") else 16
                term.set("font: ./fonts/{}.ttf, size={}{}".format(
                    font, 
                    8, cy)) 
            else:
                term.set("font: ./fonts/{}.ttf, size={}{}".format(
                    font, 
                    self.prop['cx'], 
                    'x'+str(self.prop['cy']) if self.prop['cy'] != self.prop['cx'] else ''))

    def reset_screen(self):
        if self.prop['cx'] == "auto":
            term.set("window: size={}x{}, cellsize={}".format(
                self.prop['gx'],
                self.prop['gy'],
                self.prop['cx'],
            ))
        else:
            term.set("window: size={}x{}, cellsize={}x{}".format(
                *(v for _, v in self.prop.items())))
        term.refresh()        

    def draw(self):
        term.clear()

        # options title
        term.puts(
            x=center(self.option.title, term.state(term.TK_WIDTH)), 
            y=1, 
            s=self.option.title)

        # options
        height = 3

        for index, opt in enumerate(self.option.opts):
            switch = index == self.option.optindex
            expanded = index in self.option.expand

            if switch:
                opt = ("[[-]] " if expanded else "[[+]] ") + \
                "[c=#00ffff]{}[/c]".format(opt)
            else:
                opt = ("[[-]] " if expanded else "[[+]] ") + opt

            term.puts(term.state(term.TK_WIDTH) // 5, height, opt)
            height += term.state(term.TK_HEIGHT) // 25
            if expanded:
                for index, subopt in enumerate(self.option.subopts[index]):
                    if switch:
                        if index == self.option.suboptindex[self.option.optindex]:
                            subopt = "[c=#00ffff]{}[/c]".format(subopt)
                        else:
                             subopt = subopt

                    term.puts(
                        x=term.state(term.TK_WIDTH) // 4 + 3, 
                        y=height, 
                        s=subopt)
                    height += term.state(term.TK_HEIGHT) // 25

            height += term.state(term.TK_HEIGHT)//25

        # Debug: Shows terminal properties -- Can remove later
        term.puts(
            x=term.state(term.TK_WIDTH) // 5, 
            y=height + 1, 
            s="{}".format(term.state(term.TK_WIDTH)))
        term.puts(
            x=term.state(term.TK_WIDTH) // 5, 
            y=height + 2, 
            s="{}".format(term.state(term.TK_HEIGHT)))
        term.puts(
            x=term.state(term.TK_WIDTH) // 5, 
            y=height + 3, 
            s="{}".format(term.state(term.TK_CELL_WIDTH)))
        term.puts(
            x=term.state(term.TK_WIDTH) // 5, 
            y=height + 4, 
            s="{}".format(term.state(term.TK_CELL_HEIGHT)))
        
        term.refresh()

        # User input during options screen
        key = term.read()

        if key in (term.TK_CLOSE, term.TK_Q, term.TK_ESCAPE):
            self.option.reset_all()
            self.ret['scene'] = 'main_menu'
            self.proceed = False
        
        elif key == term.TK_ENTER:
            if self.option.optindex in self.option.expand:
                # action stuff
                if self.option.suboptindex[self.option.optindex] != -1:
                    if self.proceed:
                        print('SELECTED: {}|{}'.format(
                            self.option.opts[self.option.optindex], 
                            self.option.subopts[self.option.optindex][self.option.suboptindex[self.option.optindex]]))

                    if self.option.option() == "Screen Size":                       
                        if self.parse_screensize(self.option.suboption()):
                            self.reset_screen()

                    elif self.option.option() == "Cell Size":
                        if self.parse_cellsize(self.option.suboption()):
                            self.reset_screen()

                    elif self.option.option() == "Font Choice":
                        self.parse_fonts(
                            self.prop, 
                            self.option.suboption())
                        self.reset_screen()

                else:
                    self.option.collapse(self.option.optindex)
            else:
                self.option.expansion(self.option.optindex)
                # option.move_subpointer(1)

        # Arrow keys (UP | DOWN)
        elif key == term.TK_DOWN:
            if len(self.option.expand):
                self.option.move_subpointer(1)
                self.option.correct_subpointer()

            else:
                self.option.move_pointer(1)
                self.option.correct_pointer()

        elif key == term.TK_UP:
            if len(self.option.expand):
                self.option.move_subpointer(-1)
                self.option.correct_subpointer()

            else:
                self.option.move_pointer(-1)
                self.option.correct_pointer()

if __name__ == "__main__":
    term.open()
    o = Options()
    o.run()