import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
import spaceship.constants as consts
from spaceship.screen_functions import center, longest, colored
from bearlibterminal import terminal as term
from spaceship.setup import setup
from collections import namedtuple

# from win32api import GetSystemMetrics as sysize

class Option:
    def __init__(self, title, opt=None, subopts=None):
        self.title = title
        # opt list
        self.opts = [opt] if opt else []
        # opt index
        self.optindex = 0
        # subopt list
        self.subopts = [subopts] if subopts else []
        # subopt pointers
        self.suboptindex = [-1] if subopts else []
        # list of expansions
        self.expand = set()

    def option(self):
        return self.opts[self.optindex]

    def suboption(self):
        return self.subopts[self.optindex][self.suboptindex[self.optindex]]

    def suboptsize(self):
        return len(self.subopts[self.optindex])

    def reset_all(self):
        self.optindex = 0
        self.suboptindex = [-1 for i in range(len(self.opts))]
        self.collapse_all()

    def expansion(self, n: int):
        if n > len(self.opts):
            raise IndexError('invalid index for expansion')

        if n not in self.expand:
            self.expand.add(n)

    def expand_all(self):
        for i in range(len(self.opts)):
            if i not in self.expand:
                self.expand.add(i)

    def collapse(self, n: int):
        if n > len(self.opts):
            raise IndexError('invalid index for collapse')

        if n in self.expand:
            self.expand.remove(n)

    def collapse_all(self):
        self.expand = set()

    def add_opt(self, opt: str, subopts: list):
        self.opts.append(opt)
        self.subopts.append(subopts)
        self.suboptindex.append(-1)

    def move_pointer(self, move: int):
        self.optindex = self.optindex+move

    def correct_pointer(self):
        self.optindex = max(min(self.optindex, len(self.opts)-1), 0)
    
    def move_subpointer(self, move: int):
        self.suboptindex[self.optindex] += move
    
    def correct_subpointer(self):
        self.suboptindex[self.optindex] = max(
            min(self.suboptindex[self.optindex], len(self.subopts[self.optindex])-1), -1)

# TODO: expanding list
option = Option("Options Screen")
# 80x25 -> 8x16 | 80x50 -> 8x8 | 160x50 -> 16x16 | FullScreen -> 16x16
option.add_opt("Screen Size", ["80x25", "80x50", "160x50",]) 
                                # "Full Screen: {}x{}".format(sysize(0), sysize(1))])
option.add_opt("Cell Size", ["Auto", "8x16", "8x8", "16x16"])
option.add_opt("Font Choice", ["Default", "IBM_CGA", "Andale", "Courier", "Unscii-8", "Unscii-8-thin", "VeraMono"])
option.add_opt("Coloring", ["Dynamic", "Dark", "Light", "Colorblind"])

def options():
    def parse_screensize(p, screensize):
        if "Full Screen" in screensize:
            sx, sy = sysize(0)//term.state(term.TK_CELL_WIDTH), sysize(1)//term.state(term.TK_CELL_HEIGHT)
            print(sx, sy)
        else:
            sx, sy = list(map(lambda x: int(x), screensize.split('x')))
        if (p['gx'], p['gy']) != (sx, sy):
            p['gx'], p['gy'] = sx, sy
            return p, True
        return p, False

    def parse_cellsize(p, cellsize):
        if cellsize == "Auto":
            if p['cx'] != 'Auto':
                p['cx'], p['cy'] = "auto", None
                return p, True
        else:
            print(cellsize, p)
            print(term.font('Courier'))
            cx, cy = list(map(lambda x: int(x), cellsize.split('x')))
            if (p['cx'], p['cy']) != (cx, cy):
                p['cx'], p['cy'] = (cx, cy)
                return p, True
        return p, False

    def parse_fonts(p, font):
        print(p)
        if option == "Default":
            term.set('font: default, size={}{}'.format(
                p['cx'], 
                'x'+str(p['cy']) if p['cy'] != p['cx'] else ''))

        else:
            print(font, p['cx'], p['cy'])
            if p['cx'] == "auto":
                cy = 8 if font not in ("Andale, Courier, VeraMono") else 16
                term.set("font: ./fonts/{}.ttf, size={}{}".format(
                    font, 
                    8, cy)) 
            else:
                term.set("font: ./fonts/{}.ttf, size={}{}".format(
                    font, 
                    p['cx'], 
                    'x'+str(p['cy']) if p['cy'] != p['cx'] else ''))
            # p['cx'], p['cy'] = "auto", None
            reset_screen(p)

    def reset_screen(properties):
        print(properties)
        if properties['cx'] == "auto":
            term.set("window: size={}x{}, cellsize={}".format(
                properties['gx'],
                properties['gy'],
                properties['cx'],
            ))
        else:
            term.set("window: size={}x{}, cellsize={}x{}".format(*(v for _, v in properties.items())))
        term.refresh()

    prop = {
        'gx': term.state(term.TK_WIDTH),
        'gy': term.state(term.TK_HEIGHT),
        'cx': term.state(term.TK_CELL_WIDTH),
        'cy': term.state(term.TK_CELL_HEIGHT),
    }

    while True:

        term.clear()

        # options title
        term.puts(center(option.title, term.state(term.TK_WIDTH)), 1, option.title)

        # options
        height = 3
        print(option.optindex, option.suboptindex)
        for index, opt in enumerate(option.opts):
            selected = index == option.optindex
            expanded = index in option.expand
            if selected:
                opt = ("[[-]] " if expanded else "[[+]] ") + "[c=#00ffff]{}[/c]".format(opt)
            else:
                opt = ("[[-]] " if expanded else "[[+]] ") + opt

            term.puts(term.state(term.TK_WIDTH)//5, height, opt)
            height += term.state(term.TK_HEIGHT)//25
            if expanded:
                for index, subopt in enumerate(option.subopts[index]):
                    if selected:
                        if index == option.suboptindex[option.optindex]:
                            subopt = "[c=#00ffff]{}[/c]".format(subopt)
                        else:
                             subopt = subopt
                    term.puts(term.state(term.TK_WIDTH)//4+3, height, subopt)
                    height += term.state(term.TK_HEIGHT)//25
            height += term.state(term.TK_HEIGHT)//25
        term.puts(term.state(term.TK_WIDTH)//5, height+1, "{}".format(term.state(term.TK_WIDTH)))
        term.puts(term.state(term.TK_WIDTH)//5, height+2, "{}".format(term.state(term.TK_HEIGHT)))
        term.puts(term.state(term.TK_WIDTH)//5, height+3, "{}".format(term.state(term.TK_CELL_WIDTH)))
        term.puts(term.state(term.TK_WIDTH)//5, height+4, "{}".format(term.state(term.TK_CELL_HEIGHT)))

        term.refresh()
        key = term.read()

        if key in (term.TK_CLOSE, term.TK_Q, term.TK_ESCAPE):
            option.reset_all()
            break
        
        elif key == term.TK_ENTER:
            if option.optindex in option.expand:
                # action stuff
                if option.suboptindex[option.optindex] != -1:
                    print('SELECTED: {}|{}'.format(
                        option.opts[option.optindex], 
                        option.subopts[option.optindex][option.suboptindex[option.optindex]]))
                    if option.option() == "Screen Size":                       
                        print(prop)
                        prop, changed = parse_screensize(prop, option.suboption())
                        if changed:
                            print('changing screen properties')
                            reset_screen(prop)
                        print(prop)
                    elif option.option() == "Cell Size":
                        print(prop)
                        prop, changed = parse_cellsize(prop, option.suboption())
                        if changed:
                            print('changing cell properties')
                            reset_screen(prop)
                        print(prop)
                    elif option.option() == "Font Choice":
                        parse_fonts(prop, option.suboption())
                else:
                    option.collapse(option.optindex)
            else:
                option.expansion(option.optindex)
                # option.move_subpointer(1)

        # Arrow keys (UP | DOWN)
        elif key == term.TK_DOWN:
            if len(option.expand):
                option.move_subpointer(1)
                option.correct_subpointer()
            else:
                option.move_pointer(1)
                option.correct_pointer()
        elif key == term.TK_UP:
            if len(option.expand):
                option.move_subpointer(-1)
                option.correct_subpointer()
            else:
                option.move_pointer(-1)
                option.correct_pointer()

if __name__ == "__main__":
    setup()
    print(options())
