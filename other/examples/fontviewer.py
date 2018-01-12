import sys
from bearlibterminal import terminal

if __name__ == '__main__':
    terminal.open()
    terminal.set("U+E000: ./fonts/scientifica.bdf, size=8x8, align=center")
    terminal.refresh()
    terminal.read()