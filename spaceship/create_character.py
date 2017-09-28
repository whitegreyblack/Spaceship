import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.constants import MENU_SCREEN_WIDTH as SCREEN_WIDTH
from spaceship.constants import MENU_SCREEN_HEIGHT as SCREEN_HEIGHT
from bearlibterminal import terminal as term
from spaceship.screen_functions import *
from spaceship.continue_game import continue_game
from spaceship.setup import setup, alphabet, toChr, output
from textwrap import wrap
from collections import namedtuple
import descriptions as desc

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
        "Warriors are skilled in melee combat",
        "Hunters are proeficient with ranged combat",
        "Mages use elemental magic to vanquish their foes",
        "Assassins are quick and silent killers in the dark",
        "Mercenaries are suited with any type of physical combat",   
    ]

    def join(string, length):
        # use regex to replace [*]
        return "\n".join(wrap(string, length))

    def pad(string, center=True, length=9):
        padding = length - len(string)
        if center:
            return padding//2 * " " + string.upper() + (padding+1)//2 * " " if padding else string.upper()
        return string.upper() + padding * " " if padding else string.upper()

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

    def modify(increment, index, options):
        index += increment
        if not 0 <= index < options:
            index = max(0, min(index, options-1))
        return index

    def border():
        for x in range(SCREEN_WIDTH):
            term.puts(x, 3, toChr("2550"))
            term.puts(x, SCREEN_HEIGHT-3, toChr("2550"))

    def arrow(x, y):
        term.puts(x-2, y, ">")

    def point(x, y):
        term.puts(x-2, y, "*")

    character = namedtuple("Character", "race subrace classe")
    indices = namedtuple("Index", "Character Race Subrace Class")
    races = namedtuple("Race", "race subraces")
    character_title = "Character Creation"
    character_help = "Press (?) for info on a selected race, subrace or class"
    finish = "FINISH"
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
        races("Troll", ["Cave", "Forest","Ice"]),
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
        term.layer(0)
        term.clear()
        border()

        # title and subtitle
        term.puts(center(character_title, SCREEN_WIDTH//2), 1, character_title)
        subtitle = subtitle_text(character_index)
        x = center(subtitle, SCREEN_WIDTH//2)
        term.puts(x, 2, subtitle)

        # RACE | SUBRACE | CLASS Descriptions
        x = SCREEN_WIDTH//2-1
        if character_index >= 0:
            y = 4
            point(x, y)
            term.puts(x, y, join(race_descriptions[race_index], length))
            #term.printf(x, y, race_descriptions[race_index])
        if character_index >= 1:
            y = 8
            point(x, y)
            term.puts(x, y, join(subrace_descriptions[race_index][subrace_index], length))
        if character_index >= 2:
            y = 12
            point(x, y)
            term.puts(x, y, join(class_descriptions[class_index], length))

        # races
        x = 3
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
                y = 4+i*2
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

        # FINISH button
        if character_index > 2:
            x = pad(finish)
            selected(center(x, SCREEN_WIDTH), SCREEN_HEIGHT-3, x)
        # else:
        #     unselected(SCREEN_WIDTH-len(finish)-3, SCREEN_HEIGHT-3, finish)

        # footer
        term.puts(center(character_help, SCREEN_WIDTH), SCREEN_HEIGHT-2, character_help)

        term.refresh()
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
            if term.state in (term.TK_SHIFT,):
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
