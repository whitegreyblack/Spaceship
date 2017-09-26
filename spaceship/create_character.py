import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from bearlibterminal import terminal as term
from spaceship.screen_functions import *
from spaceship.continue_game import continue_game
from spaceship.setup import setup
from textwrap import wrap
from collections import namedtuple


character = namedtuple("Character", "race subrace classe")

race_descriptions=[
    "Humans are the most versitile blah blah",
    "Dwarves are hardy creatures",
    "The elven folk are skinny people",
    "Ishtahari are oldest race",
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
    "Warriors are skilled in melee combat",
    "Hunters are proeficient with ranged combat",
    "Mages use elemental magic to vanquish their foes",
    "Assassins are quick and silent killers in the dark",
    "Mercenaries are suited with any type of physical combat",   
]

def join(string, length):
    return "\n".join(wrap(string, length))

def create_character():

    def unselected(x, y, text):
        term.puts(x, y, text)

    def selected(x, y, text):
        term.bkcolor("white")
        term.puts(x, y, "[color=black]{}[/color]".format(text))
        term.bkcolor("black")

    def passed(x, y, text):
        term.bkcolor("grey")
        term.puts(x, y, text)
        term.bkcolor("black")      

    def title_text(i):
        text = "Choose your {}"
        if i == 0:
            return text.format("race")
        elif i == 1:
            return text.format("subclass")
        elif i == 2:
            return text.format("class")
        else:
            return "Press (ENTER) to finish"

    def modify(increment, index, options):
        index += increment
        if not 0 <= index < options:
            index = max(0, min(index, options-1))
        return index

    races = namedtuple("Race", "race subraces")
    character_title = "Character Creation"
    character_help = "Press (?) for info on a selected race, subrace or class"
    race_title = "Choose your race"
    class_title = "Choose your class"
    character_index = 0
    race_index = 0
    subrace_index = 0
    class_index = 0
    race_options = [
        races("Human", ["Empire", "Nomad", "Fremen", "Sadurkar"]),
        races("Dwarf", ["Ironborn", "Goldbeard", "Stonekeep"]),
        races("Elf", ["Highborn", "Woodland", "Drow"]),
        races("Ishtahari", ["Ishma", "Ishta"]),
        races("Orc", ["Mountain", "Greenskin", "Grayskin"]),
        races("Goblin", ["Normal", "Hobgoblin"]),
        races("Troll", ["Cave", "Forest", "Ice"]),
    ]
    class_options = [
        "Warrior",
        "Hunter",
        "Mage",
        "Assassin",
        "Mercenary",
    ]
    length = SCREEN_WIDTH//2
    while True:
        term.clear()
        term.puts(center(character_title, SCREEN_WIDTH), 1, character_title)
        term.puts(center(race_title, SCREEN_WIDTH), 2, race_title)
        term.puts(SCREEN_WIDTH//2-1, 4, join(race_descriptions[race_index] if character_index >= 0 else "", length))
        term.puts(SCREEN_WIDTH//2-1, 7, join(subrace_descriptions[race_index][subrace_index] if character_index >= 1 else "", length))
        term.puts(SCREEN_WIDTH//2-1, 10, join(class_descriptions[class_index] if character_index >= 2 else "", length))

        # races
        for option, i in zip(race_options, range(len(race_options))):
            race, _ = option
            if i == race_index:
                selected(3, 4+i*2, race) if character_index == 0 else passed(3, 4+i*2, race)
            else:
                unselected(3, 4+i*2, race)
        # sub races
        subraces = race_options[race_index].subraces
        if character_index > 0:
            for subrace, i in zip(subraces, range(len(subraces))):
                if i == subrace_index:
                    selected(15, 4+i*2, subrace) if character_index == 1 else passed(15, 4+i*2, subrace)
                else:
                    unselected(15, 4+i*2, subrace)

        # class list
        if character_index > 1:
            for classes, i in zip(class_options, range(len(class_options))):
                if i == class_index:
                    selected(27, 4+i*2, classes) if character_index == 2 else passed(27, 4+i*2, classes)
                else:
                    unselected(27, 4+i*2, classes)

        # finish button
        if character_index > 2:
            selected(SCREEN_WIDTH-len('finish')-3, SCREEN_HEIGHT-3, 'FINISH')
        else:
            unselected(SCREEN_WIDTH-len('finish')-3, SCREEN_HEIGHT-3, 'FINISH')

        # footer
        term.puts(center(character_help, SCREEN_WIDTH), SCREEN_HEIGHT-1, character_help)

        term.refresh()
        code = term.read()

        if code == term.TK_UP:
            increment = -1
            if character_index == 0:
                race_index = modify(increment, race_index, len(race_options))
            elif character_index == 1:
                subrace_index = modify(increment, subrace_index, len(race_options[race_index].subraces))
            elif character_index == 2:
                class_index = modify(increment, class_index, len(class_options))

        elif code == term.TK_DOWN:
            increment = 1
            if character_index == 0:
                race_index = modify(increment, race_index, len(race_options))
            elif character_index == 1:
                subrace_index = modify(increment, subrace_index, len(race_options[race_index].subraces))
            elif character_index == 2:
                class_index = modify(increment, class_index, len(class_options))


        elif code in (term.TK_ENTER, term.TK_RIGHT):
            # this is the finalized output if sucessful
            if code == term.TK_ENTER and character_index == 3:
                return character(
                        race_options[race_index].race, 
                        race_options[race_index].subraces[subrace_index],
                        class_options[class_index]
                )
            character_index = modify(1, character_index, 4)
        
        elif code in (term.TK_LEFT,):
            if character_index == 0:
                race_index = 0
            elif character_index == 1:
                subclass_index = 0
            elif character_index == 2:
                class_index = 0
            character_index = modify(-1, character_index, 4)

        elif code in (term.TK_ESCAPE,):
            return

if __name__ == "__main__":
    setup()
    try:
        create_character()
    except KeyboardInterrupt:
        print('quit')
    print('done')
