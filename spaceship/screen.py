# screen.py

"""
Wrapper for curses screen class
"""

import curses

class win:
    pass

class Window:

    def __init__(self, title, h, w, y, x):
        self.window = curses.newwin(h, w, y, x)
        self.window.box()
        self.window.hline(2, 1, curses.ACS_HLINE, w-2)
        self.window.addstr(1, 2, title)
        self.window.refresh()

    def clear(self):
        for y in range(3, self.window.getmaxyx()[0]-1):
            self.window.move(y,2)
            self.window.clrtoeol()
        self.window.box()

    def addstr(self, y, x, string, attr=0):
        self.window.addstr(y, x, string, curses.color_pair(attr))

    def refresh(self):
        self.window.refresh()

def main(screen):
    win.top = Window('Top window', 6, 32, 3, 6)
    win.top.addstr(3, 2, 'Test string added.')
    win.top.refresh()
    ch = win.top.window.getch()
    win.top.clear()
    win.top.refresh()
    ch = win.top.window.getch()

class Screen:
    def __init__(self, screen):
        # screen created from wrapper function
        self._screen = screen
    def get_input(self):
        return self._screen.getch()
    def addstr(self, x, y, string, attr=0):
        self._screen.addstr(y, x, string, curses.color_pair(attr))
    def addch(self, x, y, char, attr=0):
        self._screen.addstr(y, x, char, curses.color_pair(attr))
    def erase(self):
        self._screen.erase()
    def refresh(self):
        self._screen.refresh()


# MAIN
curses.wrapper(main)