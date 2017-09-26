import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from bearlibterminal import terminal as term
from spaceship.setup import setup

def convert_map():
    pass

def world_map():
    term.set("U+E000: ./fonts/font88.png, size=8x8, align=top-left")
    term.clear()
    term.put(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 0xE000+7*16+15)
    term.puts(SCREEN_WIDTH//2-1, SCREEN_HEIGHT//2, ':')
    term.refresh()
    term.read()
    
def local_map():
    pass

if __name__ == "__main__":
    setup()
    world_map()