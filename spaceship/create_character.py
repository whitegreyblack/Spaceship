import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from bearlibterminal import terminal as term
from spaceship.screen_functions import *
from spaceship.continue_game import continue_game
from spaceship.setup import setup

characters = [
    """
    Some random info
    Like whatever you want
    Put it all here

    Equipment:
        Blah
        Blah Blah
    Inventory:
        Yep
        Yep Yep
    """[1:],
    """
    Some random info
    Like whatever you want
    Put it all here

    Equipment:
        Blah
        Blah Blah
    Inventory:
        Yep
        Yep Yep
    """[1:],
    """
    Some random info
    Like whatever you want
    Put it all here

    Equipment:
        Blah
        Blah Blah
    Inventory:
        Yep
        Yep Yep
    """[1:],
    """
    Some random info
    Like whatever you want
    Put it all here

    Equipment:
        Blah
        Blah Blah
    Inventory:
        Yep
        Yep Yep
    """[1:],
    """
    Some random info
    Like whatever you want
    Put it all here

    Equipment:
        Blah
        Blah Blah
    Inventory:
        Yep
        Yep Yep
    """[1:],
]

def create_character():
    def get_race():
        pass
    def get_class():
        character_title = "Character Select"
        character_index = 0
        character_options = [
            "Option 1",
            "Option 2",
            "Option 3",
            "Option 4",
            "Option 5",
        ]
        while True:
            term.puts(center(character_title, SCREEN_WIDTH), 1, character_title)
            for option, i in zip(character_options, range(len(character_options))):
                text = "[color=orange]{}[/color]".format(option) if i == character_index else option
                term.puts(3, 3+i, text)
            term.puts(12, 3, characters[character_index])
            if character_index == -1:
                term.puts(center('select', SCREEN_WIDTH), SCREEN_HEIGHT, 'select')
            else:
                term.puts(center('select', SCREEN_WIDTH), SCREEN_HEIGHT, "[color=orange]select[/color]")
            term.refresh()
            code = term.read()
            if code in (term.TK_UP, term.TK_DOWN):
                if code == term.TK_UP:
                    character_index -= 1
                else:
                    character_index += 1
                if not 0 <= character_index < len(character_options):
                    title_index = max(0, min(character_index, len(character_options)-1))
            else:
                break

if __name__ == "__main__":
    setup()
    create_character()