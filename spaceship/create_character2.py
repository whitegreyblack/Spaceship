import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.constants import MENU_SCREEN_WIDTH as SCREEN_WIDTH
from spaceship.constants import MENU_SCREEN_HEIGHT as SCREEN_HEIGHT
from spaceship.constants import CM_BORDER_HEIGHT as BORDER_HEIGHT
from spaceship.constants import CM_BORDER_WIDTH as BORDER_WIDTH
from bearlibterminal import terminal as term
from spaceship.screen_functions import *
from spaceship.continue_game import continue_game
from spaceship.setup import setup, alphabet, toChr, output
from textwrap import wrap
from collections import namedtuple
import descriptions as desc

character_template="""
Character Info
Race: {race:>8}
Subrace: {subrace:>5}
Class: {classes:>7}

STR
CON
CHA
PER
DEX
WIL
WIS
LUC
"""[1:]
print(character_template.format(race='aa',subrace='bb',classes='cc'))
def create_character():

    race_descriptions=[
        desc.race_human,
        desc.race_dwarf,
        desc.race_elven,
        desc.race_ishtahari,
        "Orcs are brutish creatures. Born in clans",
        "Goblins are short but quick creatures",
        "Trolls are large and lumbering creatures",
    ]

    subrace_descriptions=[
        [
            "Citizen servents residing in the Rodash Empire", 
            "Travelers who wander the continent of Auriel", 
            "Humans living outside of the borders of the Rodash Empire",
            "Sadukar are those who live in the Icy Gaze north of the Empire",
        ],
        [
            "Family name for mining dwarves from the clan in the Iron Hills",
            "Family name for the royal dwarves from the Triple Shining Mountain",
            "Family name for the military dwarf clan from Stone Keep",
        ],
        [
            "Family name for the elite elven family residing in the Emerald Forest",
            "Local elven family name for the elves residing in the woods of Arundel",
            "Drow are banished elves residing in the forest hills of the Dark Forest",
        ],
        [
            "Ishma are the titles for light-element users of magic",
            "Ishta are the titles for void-element users of magic",
        ],
        [
            "Mountain orcs reside in the Shadows of Mount Huron",
            "Greenskins reside in swamplands East of Ravenflow",
            "Grayskins are found everywhere on the continent of Auriel",
        ],
        [
            "Goblins live in the caves and hills along the Storm-wrought hills and caves",
            "Hobgoblins are a special type of goblin born among goblins but with more strength",
        ],
        [
            "Cave trolls live among the many shelters provided by the Storm-wrought Ridge",
            "Forest trolls reside in the northern and colder area of the Dark Forest",
            "Ice trolls prefer to live in the coldest areas of the Icy Gaze",
        ]

    ]

    class_descriptions=[
        desc.knight, 
        desc.barbarian,
        desc.cleric,
        desc.druid,
        # desc.fighter,
        desc.paladin,
        desc.ranger,
        desc.sorcerer,
        desc.rogue,
        desc.wizard,
    ]

    def subtitle_text(i):
        text = "Choose your {}"
        if i == 0:
            return text.format("race")
        elif i == 1:
            return text.format("subclass")
        elif i == 2:
            return text.format("class")
        else:
            return "Press (ENTER) to finish"

    character = namedtuple("Character", "race subrace classe")
    indices = namedtuple("Index", "Character Race Subrace Class")
    races = namedtuple("Race", "race subraces")
    classes = namedtuple("Class", "classes description")
    character_title = "Character Creation"
    character_help = "Press (?) for info on a selected race, subrace or class"
    finish = "FINISH"
    character_index = 0
    race_index = 0
    subrace_index = 0
    class_index = 0
    bonuses = {
        "STR": "+{} to Strength",
        "CON": "+{} to Constitution",
        "WIS": "+{} to Wisdom",
        "DEX": "+{} to Dexterity",
        "CHA": "+{} to Charisma",
        "WIL": "+{} to Willpower",
        "PER": "+{} to Perception",
        "LUC": "+{} to Luck"
    }
    race_options = [
        races("Human", ["Empire", "Nomad", "Fremen", "Sadurkar"]),
        races("Dwarf", ["Ironborn", "Goldbeard", "Stonekeep"]),
        races("Elf", ["Highborn", "Woodland", "Drow"]),
        races("Ishtahari", ["Ishma", "Ishta"]),
        races("Orc", ["Mountain", "Greenskin", "Grayskin"]),
        races("Goblin", ["Normal", "Hobgoblin"]),
        races("Troll", ["Cave", "Forest","Ice"]),
    ]
    class_options = [
        "Knight",
        "Barbarian",
        "Cleric",
        "Druid",
        # "Fighter",
        "Paladin",
        "Ranger",
        "Sorcerer",
        "Rogue",
        "Wizard",
    ]
    length = SCREEN_WIDTH//2
    while True:
        term.layer(0)
        # term.clear()
        border(BORDER_WIDTH, BORDER_HEIGHT, toChr("2550"))

        # title and subtitle
        term.puts(center(character_title, SCREEN_WIDTH//2), 1, character_title)
        subtitle = subtitle_text(character_index)
        x = center(subtitle, SCREEN_WIDTH//2)
        term.clear_area(0, 2, BORDER_WIDTH, 1)
        term.puts(x, 2, subtitle)

        # Bonuses
        # x, y = SCREEN_WIDTH//2-1, 1
        # # point(x, y)
        # term.puts(x, y, bonuses["STR"].format(2)+"; "+bonuses["CON"].format(1))

        # RACE | SUBRACE | CLASS Descriptions
        x, y = SCREEN_WIDTH//2-1, 1
        term.clear_area(x, y, SCREEN_WIDTH-x, SCREEN_HEIGHT)
        term.puts(x, y, character_template.format(
            race=race_options[race_index].race,
            subrace=(race_options[race_index].subraces[subrace_index] if character_index >= 1 else ""), 
            classes=(class_options[class_index] if character_index >= 2 else "")))
        # if character_index == 0:
        #     # point(x, y)
        #     term.puts(x, y, join(race_descriptions[race_index], length))
        #     #term.printf(x, y, race_descriptions[race_index])
        # if character_index == 1:
        #     # point(x, y)
        #     term.puts(x, y, join(subrace_descriptions[race_index][subrace_index], length))
        # if character_index == 2:
        #     # point(x, y)
        #     term.puts(x, y, join(class_descriptions[class_index], length))
        # races
        x = 3
        term.clear_area(x-2, 4, 11, BORDER_HEIGHT[1]-BORDER_HEIGHT[0]-2)
        for option, i in zip(race_options, range(len(race_options))):
            y = 4+i*2
            race = pad(option.race)
            if i == race_index:
                if character_index == 0:
                    arrow(x, y)
                    selected(x, y, race)
                else:
                    passed(x, y, race)
            else:
                unselected(x, y, race)
        

        # sub races
        if character_index > 0:
            x = 15
            subraces = race_options[race_index].subraces
            for subrace, i in zip(subraces, range(len(subraces))):
                y = 4+i*2+race_index*2
                subrace = pad(subrace)
                if i == subrace_index:
                    if character_index == 1:
                        arrow(x, y)
                        selected(x, y, subrace)
                    else:
                        passed(x, y, subrace)
                else:
                    unselected(x, y, subrace)

        # class list
        if character_index > 1:
            x = 27
            for classes, i in zip(class_options, range(len(class_options))):
                y = 4+i*2
                classes = pad(classes)
                if i == class_index:
                    if character_index == 2:
                        arrow(x, y)
                        selected(x, y, classes)
                    else:
                        passed(x, y, classes)
                else:
                    unselected(x, y, classes)
        # footer
        lines = split(character_help, SCREEN_WIDTH//2-3)
        for text, i in zip(lines, range(len(lines))):
            term.puts(center(text, 37)+1, 22+i, text)

        # FINISH button
        if character_index > 2:
            x = pad(finish)
            selected(center(x, 20), SCREEN_HEIGHT-3, x)
        # else:
        #     unselected(SCREEN_WIDTH-len(finish)-3, SCREEN_HEIGHT-3, finish)

        term.refresh()
        code = term.read()
        while code in (term.TK_SHIFT, term.TK_ALT, term.TK_CONTROL,):
            code = term.read()

        # UP key
        if code == term.TK_UP:
            increment = -1
            if character_index == 0:
                race_index = modify(increment, race_index, len(race_options))
            elif character_index == 1:
                subrace_index = modify(increment, subrace_index, len(race_options[race_index].subraces))
            elif character_index == 2:
                class_index = modify(increment, class_index, len(class_options))

        # DOWN key
        elif code == term.TK_DOWN:
            increment = 1
            if character_index == 0:
                race_index = modify(increment, race_index, len(race_options))
            elif character_index == 1:
                subrace_index = modify(increment, subrace_index, len(race_options[race_index].subraces))
            elif character_index == 2:
                class_index = modify(increment, class_index, len(class_options))

        # ENTER and RIGHT keys move forward
        elif code in (term.TK_ENTER, term.TK_RIGHT):
            # this is the finalized output if sucessful
            if code == term.TK_ENTER and character_index == 3:
                return output(proceed=True, 
                              value=character(
                                        race_options[race_index].race, 
                                        race_options[race_index].subraces[subrace_index],
                                        class_options[class_index]))

            character_index = modify(1, character_index, 4)
        
        # LEFT key moves back
        elif code in (term.TK_LEFT,):
            character_index = modify(-1, character_index, 4)
            if character_index == 0:
                subrace_index = 0
            elif character_index == 1:
                class_index = 0
        # ESCAPE exists if on the first list else moves back one
        elif code in (term.TK_ESCAPE,):
            if term.state(term.TK_SHIFT,):
                return output(
                        proceed=False,
                        value="Exit to Desktop")
            if character_index == 0:
                return output(
                        proceed=False,
                        value="Exit to Menu")
            else:
                character_index -= 1
        
        # handles the questionmark key inputs
        elif code in (term.TK_SHIFT,) and (term.read() in (term.TK_SLASH,) and term.state(term.TK_SHIFT)):
            print('shfited')
            term.layer(1)
            term.puts(0, 0, 'asdfffffff')
            term.puts(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 'asf')
            term.refresh()
            term.read()
	
if __name__ == "__main__":
    setup()
    try:
        print(create_character())
    except KeyboardInterrupt:
        print('quit')
    print('done')
