import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from bearlibterminal import terminal as term
from spaceship.screen_functions import *
from spaceship.continue_game import continue_game
from spaceship.setup import setup
from collections import namedtuple
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
    races = namedtuple("Race", "race subraces")
    character_title = "Character Creation"
    character_help = """Press [?] for info on a race or class"""[1:]
    race_title = "Choose your race"
    class_title = "Choose your class"
    character_index = 0
    race_index = 0
    class_index = 0
    race_options = [
        races("Human", ["Empire", "Nomad"])
        races("Dwarf", ["Ironborn", ""])
        races("Ishtahari" ,["Ishma", "Ishta"])

    ]
    class_options = [
        "Option 1",
        "Option 2",
        "Option 3",
        "Option 4",
        "Option 5",
    ]
    while True:
        term.puts(center(race_title, SCREEN_WIDTH), 1, race_title)
        for option, i in zip(race_options, range(len(race_options))):
            text = "[color=orange]{}[/color]".format(option) if i == race_index else option
            term.puts(3, 3+i, text)
        term.puts(12, 3, characters[race_index])
        for option, i in zip(class_options, range(len(class_options))):
            text = "[color=orange]{}[/color]".format(option) if i == class_index else option
            term.puts(3, 3+i, text)
        term.puts(12, 3, characters[class_index])
        if class_index == -1:
            term.puts(center('select', SCREEN_WIDTH), SCREEN_HEIGHT, 'select')
        else:
            term.puts(center('select', SCREEN_WIDTH), SCREEN_HEIGHT, "[color=orange]select[/color]")

        if race_index == -1:
            term.puts(center('select', SCREEN_WIDTH), SCREEN_HEIGHT, 'select')
        else:
            term.puts(center('select', SCREEN_WIDTH), SCREEN_HEIGHT, "[color=orange]select[/color]")
        # term.refresh()
        # code = term.read()
        # if code in (term.TK_UP, term.TK_DOWN):
        #     if code == term.TK_UP:
        #         race_index -= 1
        #     else:
        #         race_index += 1
        #     if not 0 <= race_index < len(race_options):
        #         race_index = max(0, min(race_index, len(race_options)-1))
        # elif code in (term.TK_ENTER,):
        #     return 1

        # # term.refresh()
        # # code = term.read()
        # # if code in (term.TK_UP, term.TK_DOWN):
        # #     if code == term.TK_UP:
        # #         class_index -= 1
        # #     else:
        # #         class_index += 1
        # #     if not 0 <= class_index < len(class_options):
        # #         class_index = max(0, min(class_index, len(class_options)-1))
        # # elif code in (term.TK_ENTER,):
        # #     return class_options[class_index]

if __name__ == "__main__":
    setup()
    create_character()
    print('done')