import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from bearlibterminal import terminal as term
from screen_functions import center

class Option:
    def __init__(self, title, opt=None, subopts=None):
        self.title = title
        # options list
        self.opts = [opt] if opt else []
        # options index
        self.optindex = 0
        # suboptions list
        self.subopts = [subopts] if subopts else []
        # suboptions pointers
        self.suboptindex = [-1] if subopts else []
        # list of expansions
        self.expand = set()

    def option(self) -> str:
        '''Return current option'''
        return self.opts[self.optindex]

    def suboption(self) -> str:
        '''Return current suboption'''
        return self.subopts[self.optindex][self.suboptindex[self.optindex]]

    def expansion(self, n: int) -> None:
        '''Expand the current option list if it is not currently collapsed'''
        if n > len(self.opts):
            raise IndexError('invalid index for expansion')

        if n not in self.expand:
            self.expand.add(n)

    def collapse(self, n: int) -> None:
        '''Collapse the current list if it is not currently expanded'''
        if n > len(self.opts):
            raise IndexError('invalid index for collapse')

        if n in self.expand:
            self.expand.remove(n)

    def add_opt(self, opt: str, subopts: list) -> None:
        '''Add a header option to the option'''
        self.opts.append(opt)
        self.subopts.append(subopts)
        self.suboptindex.append(-1)

    def move_pointer(self, move: int) -> None:
        '''Increment optindex by the value of move'''
        self.optindex = self.optindex + move

    def correct_pointer(self) -> None:
        '''Clamp optindex to be within the bounds of the options length'''
        self.optindex = max(min(self.optindex, len(self.opts) - 1), 0)
    
    def move_subpointer(self, move: int) -> None:
        '''Increment suboptindex by the value of move'''
        self.suboptindex[self.optindex] += move
    
    def correct_subpointer(self) -> None:
        '''Clamp suboptindex to be within the bounds of the suboptions length'''
        self.suboptindex[self.optindex] = max(min(
            self.suboptindex[self.optindex], 
            len(self.subopts[self.optindex])-1), 0)

    def reset_all(self):
        '''Reset and close all option lists'''
        self.optindex = 0
        self.suboptindex = [-1 for i in range(len(self.opts))]
        self.collapse_all()

    def collapse_all(self):
        '''Collapse all option lists that are not collapsed'''
        self.expand = set()

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
                    opt = "[[-]] " + "[c=#00ffff]{}[/c]".format(opt)

                else:
                    opt = "[[+]] " + "[c=#00ffff]{}[/c]".format(opt)

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