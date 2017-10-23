import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from bearlibterminal import terminal as term
from screen_functions import center

class Option:
    def __init__(self, title, opt=None, subopts=None):
        self.title = title
        self.opts = [opt] if opt else []
        self.subopts = [subopts] if subopts else []
        self.expand = []
        self.optindex = 0
        self.suboptindex = 0

    def expansion(self, n: int):
        if n > len(self.opts):
            raise IndexError('invalid index for expansion')

        if n not in self.expand:
            self.expand.append(n)

    def collapse(self, n: int):
        if n > len(self.opts):
            raise IndexError('invalid index for collapse')

        if n in self.expand:
            self.expand.remove(n)

    def add_opt(self, opt: str, subopts: list):
        self.opts.append(opt)
        self.subopts.append(subopts)

    def move_pointer(self, move: int):
        self.optindex = max(min(self.optindex+move, len(self.opts)-1), 0)
    
    def move_subpointer(self, move: int):
        self.suboptindex += move
        
        if self.suboptindex < 0:
            self.suboptindex = -1
            self.optindex -= 1

        elif self.suboptindex > len(self.subopts[self.optindex]) - 1:
            self.suboptindex = -1
            self.optindex += 1
        # self.suboptindex = max(min(self.suboptindex+move, len(self.subopts[self.optindex])-1), 0)

if __name__ == "__main__":
    term.open()
    term.set('window: size=80x24, title="Option Expansion"')
    option = Option("Options Screen")
    option.add_opt("option a", ["suboption 1", "suboption 2", "suboption 3"])
    option.add_opt("option b", ["suboption 1", "suboption 2"])

    if not option.opts:
        raise AttributeError("No opts to display")

    while True:
        term.clear()
        term.puts(center(option.title, term.state(term.TK_WIDTH)), 1, option.title)
        height = 3
        for index, opt in enumerate(option.opts):
            selected = index == option.optindex
            expanded = index in option.expand
            if selected:
                # newopt = "[c=#00ffff]{}[/c]".format(opt) if selected else opt
                if expanded:
                    opt = "[[-]]" + opt
                else:
                    opt = "[[+]]" + "[c=#00ffff]{}[/c]".format(opt) if selected else opt
            else:
                if expanded:
                    opt = "[[-]]" + opt
                else:
                    opt = "[[+]]" + opt
            term.puts(term.state(term.TK_WIDTH)//5, height, opt)
            height += 1
            if expanded:
                for index, subopt in enumerate(option.subopts[index]):
                    if selected:
                        subopt = "[c=#00ffff]{}[/c]".format(subopt) if index == option.suboptindex else subopt
                    term.puts(term.state(term.TK_WIDTH)//4, height, subopt)
                    height += 1

        term.refresh()
        key = term.read()
        if key in (term.TK_CLOSE, term.TK_Q, term.TK_ESCAPE):
            break
        elif key == term.TK_ENTER:
            if option.optindex in option.expand:
                option.collapse(option.optindex)
            else:
                option.expansion(option.optindex)
        elif key == term.TK_DOWN:
            if len(option.expand):
                option.move_subpointer(1)
            else:
                option.move_pointer(1)
        elif key == term.TK_UP:
            if len(option.expand):
                option.move_subpointer(-1)
            else:
                option.move_pointer(-1)