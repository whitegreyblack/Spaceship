import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from bearlibterminal import terminal as term
from screen_functions import center

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

    def expansion(self, n: int):
        if n > len(self.opts):
            raise IndexError('invalid index for expansion')

        if n not in self.expand:
            self.expand.add(n)

    def collapse(self, n: int):
        if n > len(self.opts):
            raise IndexError('invalid index for collapse')

        if n in self.expand:
            self.expand.remove(n)

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
        
        # # moving up
        # if self.suboptindex < 0:
        #     self.move_pointer(-1)
        #     if self.optindex == 0:
        #         self.suboptindex = len(self.subopts[self.optindex]) - 1
        #     else:
        #         self.suboptindex = 0

        # # moving down
        # elif self.suboptindex > len(self.subopts[self.optindex]) - 1:
        #     self.move_pointer(1)
        #     if self.optindex == len(self.opts):
        #         self.suboptindex = len(self.subopts[self.optindex]) - 1
        #     else:
        #         self.suboptindex = -1
        # # self.suboptindex = max(min(self.suboptindex+move, len(self.subopts[self.optindex])-1), 0)
    
    def correct_subpointer(self):
        self.suboptindex[self.optindex] = max(min(self.suboptindex[self.optindex], len(self.subopts[self.optindex])-1), 0)

if __name__ == "__main__":
    term.open()
    term.set('window: size=80x24, title="Option Expansion"')
    option = Option("Options Screen")
    option.add_opt("option a", ["suboption 1", "suboption 2", "suboption 3"])
    option.add_opt("option b", ["suboption 1", "suboption 2"])
    option.add_opt("option c", ["suboption 1", "suboption 2", "suboption 3"])
    if not option.opts:
        raise AttributeError("No opts to display")

    while True:
        term.clear()
        print(option.optindex, option.suboptindex)
        term.puts(center(option.title, term.state(term.TK_WIDTH)), 1, option.title)
        height = 3
        for index, opt in enumerate(option.opts):
            selected = index == option.optindex
            expanded = index in option.expand
            if selected:
                if expanded:
                    opt = "[[-]] " + "[c=#00ffff]{}[/c]".format(opt) if selected else opt
                else:
                    opt = "[[+]] " + "[c=#00ffff]{}[/c]".format(opt) if selected else opt
            else:
                if expanded:
                    opt = "[[-]] " + opt
                else:
                    opt = "[[+]] " + opt
                    
            term.puts(term.state(term.TK_WIDTH)//5, height, opt)
            height += 1
            if expanded:
                for index, subopt in enumerate(option.subopts[index]):
                    if selected:
                        if index == option.suboptindex[option.optindex]:
                            subopt = "[c=#00ffff]{}[/c]".format(subopt)
                        else:
                             subopt = subopt
                    term.puts(term.state(term.TK_WIDTH)//4, height, subopt)
                    height += 1

        term.refresh()
        key = term.read()
        if key in (term.TK_CLOSE, term.TK_Q, term.TK_ESCAPE):
            break
        elif key == term.TK_ENTER:
            if option.optindex in option.expand:
                if option.suboptindex[option.optindex] != -1:
                    print('SELECTED: {}|{}'.format(
                        option.opts[option.optindex], 
                        option.subopts[option.optindex][option.suboptindex[option.optindex]]))
                else:
                    option.collapse(option.optindex)
            else:
                option.expansion(option.optindex)
                # option.move_subpointer(1)
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
            else:
                option.move_pointer(-1)
                option.correct_pointer()