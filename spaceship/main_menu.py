import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
from bearlibterminal import terminal as term

from .setup_game import setup, setup_font, setup_menu
from .start import Scene
from .screen_functions import *
from .options import Option
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
            self.proceed = False

class Start(Scene):
    def __init__(self, width, height, title='start_menu'):
        super().__init__(width, height, title)

class Options(Scene):
    def __init__(self, width, height, title='options_menu'):
        super().__init__(width, height, title)

    def setup(self):
        self.option = Option("Options Screen")
        # 80x25 -> 8x16 | 80x50 -> 8x8 | 160x50 -> 16x16 | FullScreen -> 16x16
        self.option.add_opt("Screen Size", ["80x25", "80x50", "160x50", "160x100"]) 
                                        # "Full Screen: {}x{}".format(sysize(0), sysize(1))])
        self.option.add_opt("Cell Size", ["Auto", "8x16", "8x8", "16x16"])
        self.option.add_opt("Font Choice", ["Default", "Source", "Fira", "Fira-Bold", "IBM_CGA", "Andale", "Courier", "Unscii-8", "Unscii-8-thin", "VeraMono"])
        self.option.add_opt("Coloring", ["Dynamic", "Dark", "Light", "Colorblind"])
        
        self.prop = {
            'gx': term.state(term.TK_WIDTH),
            'gy': term.state(term.TK_HEIGHT),
            'cx': term.state(term.TK_CELL_WIDTH),
            'cy': term.state(term.TK_CELL_HEIGHT),            
        }
    
    def parse_screensize(self, p, screensize):
        if "Full Screen" in screensize:
            sx, sy = sysize(0)//term.state(term.TK_CELL_WIDTH), sysize(1)//term.state(term.TK_CELL_HEIGHT)
        else:
            sx, sy = list(map(lambda x: int(x), screensize.split('x')))
        if (p['gx'], p['gy']) != (sx, sy):
            p['gx'], p['gy'] = sx, sy
            return p, True
        return p, False

    def parse_cellsize(self, p, cellsize):
        if cellsize == "Auto":
            if p['cx'] != 'Auto':
                p['cx'], p['cy'] = "auto", None
                return p, True
        else:
            cx, cy = list(map(lambda x: int(x), cellsize.split('x')))
            if (p['cx'], p['cy']) != (cx, cy):
                p['cx'], p['cy'] = (cx, cy)
                return p, True
        return p, False

    def parse_fonts(self, p, font):
        if self.option == "Default":
            term.set('font: default, size={}{}'.format(
                p['cx'], 
                'x'+str(p['cy']) if p['cy'] != p['cx'] else ''))

        else:
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
            self.reset_screen()

    def reset_screen(self):
        if self.prop['cx'] == "auto":
            term.set("window: size={}x{}, cellsize={}".format(
                self.prop['gx'],
                self.prop['gy'],
                self.prop['cx'],
            ))
        else:
            term.set("window: size={}x{}, cellsize={}x{}".format(*(v for _, v in self.prop.items())))
        term.refresh()        

    def run(self):
        while self.proceed:
            self.draw()

    def draw(self):
        term.clear()

        # options title
        term.puts(center(self.option.title, term.state(term.TK_WIDTH)), 1, self.option.title)

        # options
        height = 3

        for index, opt in enumerate(self.option.opts):
            selected = index == self.option.optindex
            expanded = index in self.option.expand
            if selected:
                opt = ("[[-]] " if expanded else "[[+]] ") + "[c=#00ffff]{}[/c]".format(opt)
            else:
                opt = ("[[-]] " if expanded else "[[+]] ") + opt

            term.puts(term.state(term.TK_WIDTH)//5, height, opt)
            height += term.state(term.TK_HEIGHT)//25
            if expanded:
                for index, subopt in enumerate(self.option.subopts[index]):
                    if selected:
                        if index == self.option.suboptindex[self.option.optindex]:
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
            self.option.reset_all()
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
                        self.prop, changed = self.parse_screensize(self.prop, self.option.suboption())
                        if changed:
                            self.reset_screen()
                    elif self.option.option() == "Cell Size":
                        self.prop, changed = self.parse_cellsize(self.prop, self.option.suboption())
                        if changed:
                            self.reset_screen()
                    elif self.option.option() == "Font Choice":
                        self.parse_fonts(self.prop, self.option.suboption())
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

class Continue(Scene):
    def __init__(self, width, height, title='continue_menu'):
        super().__init__(width, height, title)

if __name__ == "__main__":
    term.open()
    setup_font('Ibm_cga', cx=8, cy=16)
    term.set('window: size=80x25, cellsize=auto, title="Spaceship", fullscreen=false')

    # m = Main(80, 25)
    # m.setup()
    # m.run()
    # s = Start(80, 25)
    o = Options(80, 25)
    o.setup()
    o.run()
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
