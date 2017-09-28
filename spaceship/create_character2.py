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

_world="Calabaston"
_race="RACE  : {:>10}"
_subrace="Subrace: {:>11}"
_class="CLASS : {:>10}"
_place="PLACE : {:>10}"
_mod=" (+{})"
_sts="   TOTAL  RB   CB"
_str="STR:  {:>2}"
_con="CON:  {:>2}"
_cha="CHA:  {:>2}"
_per="PER:  {:>2}"
_dex="DEX:  {:>2}"
_int="INT:  {:>2}"
_wis="WIS:  {:>2}"
_luc="LUC:  {:>2}"
_head="HEAD  : {}"
_neck="NECK  : {:10}"
_body="BODY  : {:10}"
_arms="ARMS  : {:10}"
_hand="HANDS : {:10}"
_wpn1="LHAND : {:10}"
_wpn2="RHAND : {:10}"
_wpn3="THROW : {:10}"
_rng1="RING1 : {:10}"
_rng2="RING2 : {:10}"
_wais="WAIST : {:10}"
_legs="LEGS  : {:10}"
_feet="FEET  : {:10}"
_misc="MISC  : {:10}"

_template="""
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
print(_template.format(race='aa',subrace='bb',classes='cc'))
def create_character():

    race_descriptions=[
        desc.race_human,
        desc.race_dwarf,
        desc.race_elven,
        # desc.race_ishtahari,
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
        # elif i == 1:
        #     return text.format("subclass")
        elif i == 1:
            return text.format("class")
        else:
            return "Press (ENTER) to finish"

    character = namedtuple("Character", "race subrace classe")
    indices = namedtuple("Index", "Character Race Subrace Class")
    stats = namedtuple("Stats", "str dex con int wis cha")
    races = namedtuple("Race", "race location stats bonus")
    classes = namedtuple("Class", "classes bonuses")
    _title = "Character Creation"
    _help = "Press (?) for info on a selected race, subrace or class"
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
        # "str dex con int wis cha"

        #Tiphmore -- Largest Free City in Calabaston
        races("Beast", "Tiphmore", stats(15, 10, 12, 9, 10, 7), stats(1, 0, 0, 1, 0, 0)),
        # Capital of Yugahdahrum
        races("Dwarf", "Dun Badur", stats(13, 11, 14, 10, 9, 6), stats(1, 0, 1, 0 ,0 ,0)),
        # Aurundel -- Capital of Auriel in the Emerald Forest
        races("Elf", "Aurundel", stats(13, 13, 10, 10, 9, 8), stats(0, 1, 0, 0, 1, 0)),
        # races("Ishtahari", ["Ishma", "Ishta"]),
        # Renmar -- Capital of Rodash Empire
        races("Human", "Renmar", stats(13, 11, 12, 10, 9, 8), stats(0, 1, 1, 0, 0, 0)),
        # Lok Gurrah, Capital of Oggrahgar
        races("Orc", "Lok Gurrah", stats(17, 12, 13, 8, 7, 6), stats(1, 0, 1, 0, 0, 0)),
    ]
    class_options = [
        # "Barbarian",
        classes("Druid", stats(0, 0, 1, 0, 1, 0)),
        classes("Cleric", stats(0, 0, 0, 0, 2, 0)),
        # "Fighter",
        # "Paladin",
        classes("Ranger", stats(0, 2, 0, 0, 0, 0)),
        # "Sorcerer",
        # "Rogue",
        classes("Wizard", stats(0, 0, 0, 2, 0, 0)),
        classes("Warrior", stats(1, 0, 1, 0, 0, 0)),
    ]
    length = SCREEN_WIDTH//2
    while True:
        term.layer(0)
        # term.clear()
        border(BORDER_WIDTH, BORDER_HEIGHT, toChr("2550"))

        # title and subtitle
        term.puts(center(_title, SCREEN_WIDTH), 0, _title)
        subtitle = subtitle_text(character_index)
        x = center(subtitle, SCREEN_WIDTH)
        # term.clear_area(0, 1, BORDER_WIDTH, 1)
        term.puts(x, 1, subtitle)

        # Bonuses
        # x, y = SCREEN_WIDTH//2-1, 1
        # # point(x, y)
        # term.puts(x, y, bonuses["STR"].format(2)+"; "+bonuses["CON"].format(1))

        # Race Details
        term.clear_area(0, 7, SCREEN_WIDTH, 21)
        race, location, stats, rbonus = race_options[race_index]
        occu, cbonus = class_options[class_index]
        term.puts(1, 7, _race.format(race))
        term.puts(1, 8, _place.format(location))
        term.puts(1, 9, _class.format(""))
        # Stats
        term.puts(1, 11, _sts)
        term.puts(1, 12, _str.format(stats.str+rbonus.str) + (_mod.format(rbonus.str) if rbonus.str else ""))
        term.puts(1, 13, _dex.format(stats.dex+rbonus.dex) + (_mod.format(rbonus.dex) if rbonus.dex else ""))
        term.puts(1, 14, _con.format(stats.con+rbonus.con) + (_mod.format(rbonus.con) if rbonus.con else ""))
        term.puts(1, 15, _int.format(stats.int+rbonus.int) + (_mod.format(rbonus.int) if rbonus.int else ""))
        term.puts(1, 16, _wis.format(stats.wis+rbonus.wis) + (_mod.format(rbonus.wis) if rbonus.wis else ""))
        term.puts(1, 17, _cha.format(stats.cha+rbonus.cha) + (_mod.format(rbonus.cha) if rbonus.cha else ""))
        # Traits
        # Equipment
        term.puts(22, 7, _head.format("Leather Helmet"))
        term.puts(22, 8, _neck.format(""))
        term.puts(22, 9, _body.format("Leather Armor"))
        term.puts(22, 10, _arms.format("Leather Bracers"))
        term.puts(22, 11, _hand.format(""))
        term.puts(22, 12, _wpn1.format("Short Sword"))
        term.puts(22, 13, _wpn2.format(""))
        term.puts(22, 14, _wpn3.format("Wooden Arrows(x25)"))
        term.puts(22, 15, _wais.format(""))
        term.puts(22, 16, _legs.format("Common Pants"))
        term.puts(22, 17, _feet.format("Boots"))

        # Description
        term.puts(1, 19, join(race_descriptions[race_index], SCREEN_WIDTH-2))
        # RACE | SUBRACE | CLASS Descriptions
        # x, y = SCREEN_WIDTH//2-1, 1
        # term.clear_area(x, y, SCREEN_WIDTH-x, SCREEN_HEIGHT)
        # term.puts(x, y, character_template.format(
        #     race=race_options[race_index].race,
        #     subrace=(race_options[race_index].subraces[subrace_index] if character_index >= 1 else ""), 
        #     classes=(class_options[class_index] if character_index >= 2 else "")))
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

        # Clears one row on the terminal
        term.clear_area(0, 3, SCREEN_WIDTH, 3)
        # Classes
        for option, i in zip(race_options, range(len(race_options))):
            x, y = 13+11*i, 3
            race = pad(option.race, length=8)
            if i == race_index:
                if character_index == 0:
                    # arrow(x, y)
                    selected(x, y, race)
                else:
                    passed(x, y, race)
            else:
                unselected(x, y, race)

        for option, i in zip(class_options, range(len(class_options))):
            x, y = 13+11*i, 5
            option = pad(option.classes, length=8)
            unselected(x, y, option)

        if character_index > 0:
            term.puts(1, 9, _class.format(occu))
            # term.puts(1, 12, _str.format(stats.str+rbonus.str+cbonus.str) + (_mod.format(rbonus.str+cbonus.str) if rbonus.str+cbonus.str else ""))
            # term.puts(1, 13, _dex.format(stats.dex+rbonus.dex+cbonus.dex) + (_mod.format(rbonus.dex+cbonus.dex) if rbonus.dex+cbonus.dex else ""))
            # term.puts(1, 14, _con.format(stats.con+rbonus.con+cbonus.con) + (_mod.format(rbonus.con+cbonus.con) if rbonus.con+cbonus.con else ""))
            # term.puts(1, 15, _int.format(stats.int+rbonus.int+cbonus.int) + (_mod.format(rbonus.int+cbonus.int) if rbonus.int+cbonus.int else ""))
            # term.puts(1, 16, _wis.format(stats.wis+rbonus.wis+cbonus.wis) + (_mod.format(rbonus.wis+cbonus.wis) if rbonus.wis+cbonus.wis else ""))
            # term.puts(1, 17, _cha.format(stats.cha+rbonus.cha+cbonus.cha) + (_mod.format(rbonus.cha+cbonus.cha) if rbonus.cha+cbonus.cha else ""))
            term.puts(1, 12, _str.format(stats.str+rbonus.str+cbonus.str) + (_mod.format(rbonus.str) if rbonus.str else "     ") + (_mod.format(cbonus.str) if cbonus.str else ""))
            term.puts(1, 13, _dex.format(stats.dex+rbonus.dex+cbonus.dex) + (_mod.format(rbonus.dex) if rbonus.dex else "     ") + (_mod.format(cbonus.dex) if cbonus.dex else ""))
            term.puts(1, 14, _con.format(stats.con+rbonus.con+cbonus.con) + (_mod.format(rbonus.con) if rbonus.con else "     ") + (_mod.format(cbonus.con) if cbonus.con else ""))
            term.puts(1, 15, _int.format(stats.int+rbonus.int+cbonus.int) + (_mod.format(rbonus.int) if rbonus.int else "     ") + (_mod.format(cbonus.int) if cbonus.int else ""))
            term.puts(1, 16, _wis.format(stats.wis+rbonus.wis+cbonus.wis) + (_mod.format(rbonus.wis) if rbonus.wis else "     ") + (_mod.format(cbonus.wis) if cbonus.wis else ""))
            term.puts(1, 17, _cha.format(stats.cha+rbonus.cha+cbonus.cha) + (_mod.format(rbonus.cha) if rbonus.cha else "     ") + (_mod.format(cbonus.cha) if cbonus.cha else ""))
            term.clear_area(40, 7, SCREEN_WIDTH-41, 21)
            term.puts(40, 7, class_descriptions[class_index])

            for option, i in zip(class_options, range(len(class_options))):
                x, y = 13+11*i, 5
                option = pad(option.classes, length=8)
                if i == class_index:
                    if character_index == 1:
                        # arrow(x, y)
                        selected(x, y, option)
                    else:
                        passed(x, y, option)
                else:
                    unselected(x, y, option)
        # x = 3
        # term.clear_area(x-2, 4, 11, BORDER_HEIGHT[1]-BORDER_HEIGHT[0]-2)
        # for option, i in zip(race_options, range(len(race_options))):
        #     y = 4+i*2
        #     race = pad(option.race)
        #     if i == race_index:
        #         if character_index == 0:
        #             arrow(x, y)
        #             selected(x, y, race)
        #         else:
        #             passed(x, y, race)
        #     else:
        #         unselected(x, y, race)
        

        # # sub races
        # if character_index > 0:
        #     x = 15
        #     subraces = race_options[race_index].subraces
        #     for subrace, i in zip(subraces, range(len(subraces))):
        #         y = 4+i*2+race_index*2
        #         subrace = pad(subrace)
        #         if i == subrace_index:
        #             if character_index == 1:
        #                 arrow(x, y)
        #                 selected(x, y, subrace)
        #             else:
        #                 passed(x, y, subrace)
        #         else:
        #             unselected(x, y, subrace)

        # # class list
        # if character_index > 1:
        #     x = 27
        #     for classes, i in zip(class_options, range(len(class_options))):
        #         y = 4+i*2
        #         classes = pad(classes)
        #         if i == class_index:
        #             if character_index == 2:
        #                 arrow(x, y)
        #                 selected(x, y, classes)
        #             else:
        #                 passed(x, y, classes)
        #         else:
        #             unselected(x, y, classes)

        # footer
        # lines = split(character_help, SCREEN_WIDTH//2-3)
        # for text, i in zip(lines, range(len(lines))):
        #     term.puts(center(text, 37)+1, 22+i, text)
        # term.puts(center(_help, SCREEN_WIDTH), SCREEN_HEIGHT-1, _help)

        # FINISH button
        if character_index > 1:
            x = pad(finish)
            selected(center(x, 20), SCREEN_HEIGHT-3, x)
        # else:
        #     unselected(SCREEN_WIDTH-len(finish)-3, SCREEN_HEIGHT-3, finish)

        term.refresh()
        code = term.read()
        while code in (term.TK_SHIFT, term.TK_ALT, term.TK_CONTROL,):
            code = term.read()

        if code == term.TK_LEFT:
            if character_index == 0:
                race_index = modify(-1, race_index, 5)
            elif character_index == 1:
                class_index = modify(-1, class_index, 5)
            
        elif code == term.TK_RIGHT:
            if character_index == 0:
                race_index = modify(1, race_index, 5)
            elif character_index == 1:
                class_index = modify(1, class_index, 5)

        elif code == term.TK_UP:
            character_index = modify(-1, character_index, 3)

        elif code == term.TK_DOWN:
            character_index = modify(1, character_index, 3)

        
        # # UP key
        # if code == term.TK_UP:
        #     increment = -1
        #     if character_index == 0:
        #         race_index = modify(increment, race_index, len(race_options))
        #     elif character_index == 1:
        #         subrace_index = modify(increment, subrace_index, len(race_options[race_index].subraces))
        #     elif character_index == 2:
        #         class_index = modify(increment, class_index, len(class_options))

        # # DOWN key
        # elif code == term.TK_DOWN:
        #     increment = 1
        #     if character_index == 0:
        #         race_index = modify(increment, race_index, len(race_options))
        #     elif character_index == 1:
        #         subrace_index = modify(increment, subrace_index, len(race_options[race_index].subraces))
        #     elif character_index == 2:
        #         class_index = modify(increment, class_index, len(class_options))

        # # ENTER and RIGHT keys move forward
        # elif code in (term.TK_ENTER, term.TK_RIGHT):
        #     # this is the finalized output if sucessful
        #     if code == term.TK_ENTER and character_index == 3:
        #         return output(proceed=True, 
        #                       value=character(
        #                                 race_options[race_index].race, 
        #                                 race_options[race_index].subraces[subrace_index],
        #                                 class_options[class_index]))

        #     character_index = modify(1, character_index, 4)
        
        # # LEFT key moves back
        # elif code in (term.TK_LEFT,):
        #     character_index = modify(-1, character_index, 4)
        #     if character_index == 0:
        #         subrace_index = 0
        #     elif character_index == 1:
        #         class_index = 0

        # ESCAPE exists if on the first list else moves back one
        if code in (term.TK_ESCAPE,):
            # if term.state(term.TK_SHIFT,):
            #     return output(
            #             proceed=False,
            #             value="Exit to Desktop")
            if character_index == 0:
                return output(
                        proceed=False,
                        value="Exit to Menu")
            else:
                character_index -= 1
        
        # # handles the questionmark key inputs
        # elif code in (term.TK_SHIFT,) and (term.read() in (term.TK_SLASH,) and term.state(term.TK_SHIFT)):
        #     print('shfited')
        #     term.layer(1)
        #     term.puts(0, 0, 'asdfffffff')
        #     term.puts(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 'asf')
        #     term.refresh()
        #     term.read()
	
if __name__ == "__main__":
    setup()
    try:
        print(create_character())
    except KeyboardInterrupt:
        print('quit')
    print('done')
