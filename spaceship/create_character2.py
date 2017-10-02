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
from spaceship.setup import setup, alphabet, toChr, output, setup_menu
from textwrap import wrap
from collections import namedtuple
import descriptions as desc

_world="Calabaston"
_race="RACE  : {:>10}"
_subrace="Subrace: {:>11}"
_class="CLASS : {:>10}"
_place="PLACE : {:>10}"
_mod=" +[c=#00ffff]{}[/c]"
_sts="   TOTAL RB  CB "
_str="STR:  [c=#00ffff]{:>2}[/c]"
_con="CON:  [c=#00ffff]{:>2}[/c]"
_cha="CHA:  [c=#00ffff]{:>2}[/c]"
_per="PER:  [c=#00ffff]{:>2}[/c]"
_dex="DEX:  [c=#00ffff]{:>2}[/c]"
_int="INT:  [c=#00ffff]{:>2}[/c]"
_wis="WIS:  [c=#00ffff]{:>2}[/c]"
_luc="LUC:  [c=#00ffff]{:>2}[/c]"
_head="HEAD  : {:>20}"
_neck="NECK  : {:>20}"
_body="BODY  : {:>20}"
_arms="ARMS  : {:>20}"
_hand="HANDS : {:>20}"
_wpn1="LHAND : {:>20}"
_wpn2="RHAND : {:>20}"
_wpn3="THROW : {:>20}"
_rng1="RING1 : {:>20}"
_rng2="RING2 : {:>20}"
_wais="WAIST : {:>20}"
_legs="LEGS  : {:>20}"
_feet="FEET  : {:>20}"
_misc="MISC  : {:>20}"

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
    setup_menu()
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
    
    skills = namedtuple("Skills", "skills")
    equipment = namedtuple("Equipment", "hd nk bd ar hn lh rh lr rr wa lg ft")
    character = namedtuple("Character", "race subrace classe")
    indices = namedtuple("Index", "Character Race Subrace Class")
    stats = namedtuple("Stats", "str dex con int wis cha")
    races = namedtuple("Race", "race location stats bonus")
    classes = namedtuple("Class", "classes bonuses equipment")
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
    # "hd nk bd ar hn lh rh th wa lg ft"
    class_options = [
        # "Barbarian",
        classes("Druid", stats(0, 0, 1, 0, 1, 0), 
            equipment(
                "",
                "",
                "thick fur coat",
                "thick fur bracers",
                "",
                "wooden staff",
                "",
                "ring of nature",
                "ring of earth",
                "leather belt",
                "",
                "leather boots")),
        classes("Cleric", stats(0, 0, 0, 0, 2, 0), 
            equipment(
                "hood",
                "holy symbol",
                "light robe",
                "",
                "",
                "mace",
                "small shield",
                "ring of power",
                "ring of light",
                "rope belt",
                "",
                "leather sandals")),
        # "Fighter",
        # "Paladin",
        classes("Bowman", stats(0, 2, 0, 0, 0, 0),
            equipment(
                "hood",
                "whistle",
                "heavy cloak",
                "leather bracers",
                "cloth gloves",
                "short sword",
                "small dagger",
                "",
                "",
                "leather belt",
                "common pants",
                "leather boots")),
        # "Sorcerer",
        # "Rogue",
        classes("Wizard", stats(0, 0, 0, 2, 0, 0),            
            equipment(
                "hood",
                "amulet of power",
                "light robe",
                "",
                "",
                "quarterstaff",
                "",
                "ring of water",
                "ring of fire",
                "rope belt",
                "",
                "leather sandals")),
        classes("Squire", stats(1, 0, 1, 0, 0, 0),             
            equipment(
                "leather cap",
                "",
                "leather armor",
                "leather bracers",
                "cloth gloves",
                "long sword",
                "medium shield",
                "",
                "",
                "leather belt",
                "common pants",
                "leather boots")),
    ]
    length = SCREEN_WIDTH//2
    row = 5
    col1 = 3
    col2 = 26
    col3 = 48 
    while True:
        term.layer(0)
        # term.clear()
        border(BORDER_WIDTH, [0], "#")
        border(BORDER_WIDTH, BORDER_HEIGHT, toChr("2550"))

        # title and subtitle
        term.puts(center(" "+_title+" ", SCREEN_WIDTH), 0," "+ _title + " ")
        subtitle = subtitle_text(character_index)
        x = center(subtitle, SCREEN_WIDTH)
        term.clear_area(0, 1, BORDER_WIDTH, 1)
        term.puts(x, 1, subtitle)

        # Race Details
        term.clear_area(0, 7, SCREEN_WIDTH, 21)
        race, location, stats, rbonus = race_options[race_index]
        occu, cbonus, eq = class_options[class_index]
        term.puts(col1, row+0, _race.format(race))
        term.puts(col1, row+1, _place.format(location))
        term.puts(col1, row+2, _class.format(""))

        # Level Details
        term.puts(col1, row+4, "LEVEL : {:>10}".format(1))
        term.puts(col1, row+5, "EXP   : {:>10}".format(80))
        term.puts(col1, row+6, "GOLD  : {:>10}".format(250))
        term.puts(col1, row+7, "Skills:")
        term.puts(col1+3, row+8, "Skill 1")
        term.puts(col1+3, row+9, "Skill 1")


        # Stats
        term.puts(col2, row+0, "HP: ")
        term.puts(col2, row+1, "MP: ")
        term.puts(col2, row+2, "SP: ")
        term.puts(col2, row+4, _sts)
        term.puts(col2, row+5, _str.format(stats.str+rbonus.str) + (_mod.format(rbonus.str) if rbonus.str else ""))
        term.puts(col2, row+6, _dex.format(stats.dex+rbonus.dex) + (_mod.format(rbonus.dex) if rbonus.dex else ""))
        term.puts(col2, row+7, _con.format(stats.con+rbonus.con) + (_mod.format(rbonus.con) if rbonus.con else ""))
        term.puts(col2, row+8, _int.format(stats.int+rbonus.int) + (_mod.format(rbonus.int) if rbonus.int else ""))
        term.puts(col2, row+9, _wis.format(stats.wis+rbonus.wis) + (_mod.format(rbonus.wis) if rbonus.wis else ""))
        term.puts(col2, row+10, _cha.format(stats.cha+rbonus.cha) + (_mod.format(rbonus.cha) if rbonus.cha else ""))

        # Traits

        # Equipment "hd nk bd ar hn lh rh lr rr wa lg ft"
        term.puts(col3, row+1, _head.format(""))
        term.puts(col3, row+2, _neck.format(""))
        term.puts(col3, row+3, _body.format(""))
        term.puts(col3, row+4, _arms.format(""))
        term.puts(col3, row+5, _hand.format(""))
        term.puts(col3, row+6, _wpn1.format(""))
        term.puts(col3, row+7, _wpn2.format(""))
        term.puts(col3, row+8, _rng1.format(""))
        term.puts(col3, row+9, _rng2.format(""))
        term.puts(col3, row+10, _wais.format(""))
        term.puts(col3, row+11, _legs.format(""))
        term.puts(col3, row+12, _feet.format(""))

        # Description
        term.puts(1, 19, join(race_descriptions[race_index], SCREEN_WIDTH-2))

        # Clears one row on the terminal
        term.clear_area(0, 3, SCREEN_WIDTH, 3)
        # Classes
        for option, i in zip(race_options, range(len(race_options))):
            x, y = 13+11*i, 2
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
            x, y = 13+11*i, 4
            option = pad(option.classes, length=8)
            unselected(x, y, option)

        if character_index > 0:
            term.clear_area(1, 19, SCREEN_WIDTH-1, SCREEN_HEIGHT-19)
            term.puts(1, 19, join(class_descriptions[class_index], SCREEN_WIDTH-2))
            term.puts(col1, 9, _class.format(occu))
            term.puts(col2, row+5, _str.format(stats.str+rbonus.str+cbonus.str) + (_mod.format(rbonus.str) if rbonus.str else "    ") + (_mod.format(cbonus.str) if cbonus.str else ""))
            term.puts(col2, row+6, _dex.format(stats.dex+rbonus.dex+cbonus.dex) + (_mod.format(rbonus.dex) if rbonus.dex else "    ") + (_mod.format(cbonus.dex) if cbonus.dex else ""))
            term.puts(col2, row+7, _con.format(stats.con+rbonus.con+cbonus.con) + (_mod.format(rbonus.con) if rbonus.con else "    ") + (_mod.format(cbonus.con) if cbonus.con else ""))
            term.puts(col2, row+8, _int.format(stats.int+rbonus.int+cbonus.int) + (_mod.format(rbonus.int) if rbonus.int else "    ") + (_mod.format(cbonus.int) if cbonus.int else ""))
            term.puts(col2, row+9, _wis.format(stats.wis+rbonus.wis+cbonus.wis) + (_mod.format(rbonus.wis) if rbonus.wis else "    ") + (_mod.format(cbonus.wis) if cbonus.wis else ""))
            term.puts(col2, row+10, _cha.format(stats.cha+rbonus.cha+cbonus.cha) + (_mod.format(rbonus.cha) if rbonus.cha else "    ") + (_mod.format(cbonus.cha) if cbonus.cha else ""))
            

            # CLASS OPTIONS
            for option, i in zip(class_options, range(len(class_options))):
                x, y = 13+11*i, 4
                option = pad(option.classes, length=8)
                if i == class_index:
                    if character_index == 1:
                        # arrow(x, y)
                        selected(x, y, option)
                    else:
                        passed(x, y, option)
                else:
                    unselected(x, y, option)

            # EQUIPMENT LIST
            term.puts(col3, row+1, _head.format(eq.hd))
            term.puts(col3, row+2, _neck.format(eq.nk))
            term.puts(col3, row+3, _body.format(eq.bd))
            term.puts(col3, row+4, _arms.format(eq.ar))
            term.puts(col3, row+5, _hand.format(eq.hn))
            term.puts(col3, row+6, _wpn1.format(eq.lh))
            term.puts(col3, row+7, _wpn2.format(eq.rh))
            term.puts(col3, row+8, _rng1.format(eq.lr))
            term.puts(col3, row+9, _rng2.format(eq.rr))
            term.puts(col3, row+10, _wais.format(eq.wa))
            term.puts(col3, row+11, _legs.format(eq.lg))
            term.puts(col3, row+12, _feet.format(eq.ft))

        # FINISH button
        if character_index > 1:
            x = pad(finish, length=8)
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
