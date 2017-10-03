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
from spaceship.setup import setup, alphabet, toChr, output, setup_menu, setup_font
from textwrap import wrap
from collections import namedtuple
import descriptions as desc
from d2 import *

_world="Calabaston"
_race="RACE  : {:>10}"
_subrace="Subrace: {:>11}"
_class="CLASS : {:>10}"
_place="PLACE : {:>10}"
_mod=" [c=#00ffff]{:>2}[/c]"
_sts="      TOTAL  RB  CB "
_str="STR    : [c=#00ffff]{:>2}[/c] "
_con="CON    : [c=#00ffff]{:>2}[/c] "
_cha="CHA    : [c=#00ffff]{:>2}[/c] "
_per="PER    : [c=#00ffff]{:>2}[/c] "
_dex="DEX    : [c=#00ffff]{:>2}[/c] "
_int="INT    : [c=#00ffff]{:>2}[/c] "
_wis="WIS    : [c=#00ffff]{:>2}[/c] "
_luc="LUC    : [c=#00ffff]{:>2}[/c] "
_head="HEAD  : {:<5}"
_neck="NECK  : {:<5}"
_body="BODY  : {:<5}"
_arms="ARMS  : {:<5}"
_hand="HANDS : {:<5}"
_wpn1="LHAND : {:<5}"
_wpn2="RHAND : {:<5}"
_wpn3="THROW : {:<5}"
_rng1="RING1 : {:<5}"
_rng2="RING2 : {:<5}"
_wais="WAIST : {:<5}"
_legs="LEGS  : {:<5}"
_feet="FEET  : {:<5}"
_misc="MISC  : {:<5}"

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

# print(_template.format(race='aa',subrace='bb',classes='cc'))
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
        races("Beast", "Tiphmore", HUMAN, BEAST_BONUS),
        # Capital of Yugahdahrum
        races("Dwarf", "Dun Badur", HUMAN, DWARF_BONUS),
        # Aurundel -- Capital of Auriel in the Emerald Forest
        races("Elf", "Aurundel", HUMAN, ELVEN_BONUS),
        # races("Ishtahari", ["Ishma", "Ishta"]),
        # Renmar -- Capital of Rodash Empire
        races("Human", "Renmar", HUMAN, HUMAN_BONUS),
        # Lok Gurrah, Capital of Oggrahgar
        races("Orc", "Lok Gurrah", HUMAN, ORCEN_BONUS),
    ]
    # "hd nk bd ar hn lh rh th wa lg ft"
    class_options = [
        # "Barbarian",
        classes("druid", DRUIDS, 
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
        classes("cleric", CLERIC, 
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
        classes("archer", ARCHER,
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
        classes("wizard", WIZARD,            
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
        classes("squire", SQUIRE,             
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
    setup_font('unscii-8-thin', 8, 16)
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
        term.puts(col1, row+8, "Skills:")
        term.puts(col1+3, row+9, "Skill 1")
        term.puts(col1+3, row+10, "Skill 1")


        # Stats
        srow = row
        term.puts(col2, srow+1, "Health :     {:>2}".format(stats.str+rbonus.str+(stats.con+rbonus.con)*2))
        term.puts(col2, srow+2, "Mana   :     {:>2}".format((stats.int+rbonus.int)*2+stats.wis+rbonus.wis))
        term.puts(col2, srow+3, "Speed  :     {:>2}".format(1+(stats.dex+rbonus.dex)//3))

        term.puts(col2, srow+5, _sts)
        term.puts(col2, srow+6, _str.format(stats.str+rbonus.str) + _mod.format(rbonus.str))
        term.puts(col2, srow+7, _con.format(stats.con+rbonus.con) + _mod.format(rbonus.con))
        term.puts(col2, srow+8, _dex.format(stats.dex+rbonus.dex) + _mod.format(rbonus.dex))
        term.puts(col2, srow+9, _int.format(stats.int+rbonus.int) + _mod.format(rbonus.int))
        term.puts(col2, srow+10, _wis.format(stats.wis+rbonus.wis) + _mod.format(rbonus.wis))
        term.puts(col2, srow+11, _cha.format(stats.cha+rbonus.cha) + _mod.format(rbonus.cha))

        # Traits

        # Equipment "hd nk bd ar hn lh rh lr rr wa lg ft"
        erow = row
        term.puts(col3, erow+1, _head.format(""))
        term.puts(col3, erow+2, _neck.format(""))
        term.puts(col3, erow+3, _body.format(""))
        term.puts(col3, erow+4, _arms.format(""))
        term.puts(col3, erow+5, _hand.format(""))
        term.puts(col3, erow+6, _wpn1.format(""))
        term.puts(col3, erow+7, _wpn2.format(""))
        term.puts(col3, erow+8, _rng1.format(""))
        term.puts(col3, erow+9, _rng2.format(""))
        term.puts(col3, erow+10, _wais.format(""))
        term.puts(col3, erow+11, _legs.format(""))
        term.puts(col3, erow+12, _feet.format(""))

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
            term.puts(col2, row+6, _str.format(stats.str+rbonus.str+cbonus.str) + _mod.format(rbonus.str) + " " + (_mod.format(cbonus.str)))
            term.puts(col2, row+7, _con.format(stats.con+rbonus.con+cbonus.con) + _mod.format(rbonus.con) + " " + (_mod.format(cbonus.con)))
            term.puts(col2, row+8, _dex.format(stats.dex+rbonus.dex+cbonus.dex) + _mod.format(rbonus.dex) + " " + (_mod.format(cbonus.dex)))
            term.puts(col2, row+9, _int.format(stats.int+rbonus.int+cbonus.int) + _mod.format(rbonus.int) + " " + (_mod.format(cbonus.int)))
            term.puts(col2, row+10, _wis.format(stats.wis+rbonus.wis+cbonus.wis) + _mod.format(rbonus.wis) + " " + (_mod.format(cbonus.wis)))
            term.puts(col2, row+11, _cha.format(stats.cha+rbonus.cha+cbonus.cha) + _mod.format(rbonus.cha) + " " + (_mod.format(cbonus.cha)))
            

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
