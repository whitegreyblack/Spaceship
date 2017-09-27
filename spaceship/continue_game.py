import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.constants import MENU_SCREEN_WIDTH as SCREEN_WIDTH
from spaceship.constants import MENU_SCREEN_HEIGHT as SCREEN_HEIGHT
from spaceship.screen_functions import *
from bearlibterminal import terminal as term
from spaceship.setup import setup

# Begin continue Menu
def continue_game():
    term.clear()
    term.puts(center('No Saved Games', SCREEN_WIDTH), SCREEN_HEIGHT//2, 'NO SAVED GAMES')
    term.refresh()
    term.read()
    return True
# End Continue Menu

if __name__ == "__main__":
    setup()
    continue_game()