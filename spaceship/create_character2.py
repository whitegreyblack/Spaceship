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
_race="RACE    : {:>10}"
_subrace="Subrace: {:>11}"
_class="CLASS   : {:>10}"
_place="PLACE   : {:>10}"
_sts="""
      TOTAL  RB  CB 
STR    : [c=#00ffff]{:>2}[/c] 
CON    : [c=#00ffff]{:>2}[/c] 
DEX    : [c=#00ffff]{:>2}[/c] 
INT    : [c=#00ffff]{:>2}[/c] 
WIS    : [c=#00ffff]{:>2}[/c] 
CHA    : [c=#00ffff]{:>2}[/c] 
"""[1:]
_bon="""
{:>2}
{:>2}
{:>2}
{:>2}
{:>2}
{:>2}
"""[1:]

_equipment="""
HEAD  : {:<5}
NECK  : {:<5}
BODY  : {:<5}
ARMS  : {:<5}
HANDS : {:<5}
LHAND : {:<5}
RHAND : {:<5}
RING1 : {:<5}
RING2 : {:<5}
WAIST : {:<5}
LEGS  : {:<5}
FEET  : {:<5}
"""[1:]

# print(_template.format(race='aa',subrace='bb',classes='cc'))
def create_character():
    setup_menu()
    race_descriptions=[
        desc.race_beast,
        desc.race_dwarf,
        desc.race_elven,
        desc.race_human,
        desc.race_orcen,
    ]

    class_descriptions=[
        desc.class_druid,
        desc.class_cleric,
        desc.class_wizard,
        desc.class_archer,
        desc.class_squire,
    ]

    def subtitle_text(i):
        text = "Choose your {}"
        if i == 0:
            return text.format("race")
        # elif i == 1:
        #     return text.format("subclass")
        elif i == 1:
            return text.format("class")
        elif 1 < i < 15:
            return text.format("equipment")
        else:
            return "Press (ENTER) to finish"
    
    def transform_values(values):
        return tuple("+[c=#00ff00]"+str(v)+"[/c]" if v > 0 else "-[c=#ff0000]"+str(abs(v))+"[/c]" if v < 0 else v for v in values) 

    character = namedtuple("Character", "race subrace classe")
    indices = namedtuple("Index", "Character Race Subrace Class")
    stats = namedtuple("Stats", "str dex con int wis cha")

    _title = "Character Creation"
    _help = "Press (?) for info on a selected race, subrace or class"
    finish = "FINISH"
    character_index = 0
    race_index = 0
    subrace_index = 0
    class_index = 0

    races = namedtuple("Race", "race location stats bonus gold skills eq")
    stats = namedtuple("Stats", "str dex con int wis cha")
    equipment = namedtuple("Equipment", "hd nk bd ar hn lh rh lr rr wa lg ft")
    classes = namedtuple("Class", "classes bonuses equipment")

    race_options = [
        #Tiphmore -- Largest Free City in Calabaston
        races("Beast", "Tiphmore", HUMAN, BEAST_BONUS, 300, ("thick fur", "animal senses"),             
            equipment(
                "",
                "",
                "",
                "",
                "",
                ("long spear", "silver sword"),
                "",
                "",
                "",
                "",
                "",
                "")),
        # Capital of Yugahdahrum
        races("Dwarf", "Dun Badur", HUMAN, DWARF_BONUS, 250, ("dark vision", "dwarven fortitude"),
            equipment(
                "horned helmet",
                "gold necklace",
                "",
                "",
                "",
                ("battle axe", "copper pick"),
                "",
                "",
                "",
                "",
                "",
                "")),
        # Aurundel -- Capital of Auriel in the Emerald Forest
        races("Elf", "Aurundel", HUMAN, ELVEN_BONUS, 250, ("forest spirit", "nimble"),
            equipment(
                "",
                "",
                "elven chainmail",
                "",
                "",
                "mithril dagger",
                "mithril dagger",
                "",
                "",
                "",
                "",
                "")),
        # races("Ishtahari", ["Ishma", "Ishta"]),
        # Renmar -- Capital of Rane Empire
        races("Human", "Renmar", HUMAN, HUMAN_BONUS, 200, ("", ""),
            equipment(
                "",
                "",
                "",
                "",
                "",
                "broadsword",
                "medium shield",
                "",
                "",
                "",
                "",
                "")),
        # Lok Gurrah, Capital of Oggrahgar
        races("Orc", "Lok Gurrah", HUMAN, ORCEN_BONUS, 150, ("thick skin", "bloodrage"),
            equipment(
                "metal cap",
                "",
                "metal armor",
                "",
                "",
                "warhammer",
                "",
                "",
                "",
                "",
                "",
                "")),
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
    def cc_border():
        border(BORDER_WIDTH, [0], "#")
        border(BORDER_WIDTH, BORDER_HEIGHT, toChr("2550"))

    def eq_border():
        border(SCREEN_WIDTH-24, [row], "#")

    def title():
        term.puts(center(" "+_title+" ", SCREEN_WIDTH), 0," "+ _title + " ")

    def subtitle():
        # subtitle -- clears subtitle area to make space for new subtitle text
        subtitle = subtitle_text(character_index)
        x = center(subtitle, SCREEN_WIDTH)
        term.puts(x, 1, subtitle)

    def race_row():
        for option, i in zip(race_options, range(len(race_options))):
            x, y = 13+11*i, 2
            race = pad(option.race, length=8)
            if i == race_index:
                if character_index == 0:
                    selected(x, y, race)
                else:
                    passed(x, y, race)
            else:
                unselected(x, y, race)

    def class_row():
        # CLASS OPTIONS
        for option, i in zip(class_options, range(len(class_options))):
            x, y = 13+11*i, 4
            option = pad(option.classes, length=8)
            if i == class_index:
                if character_index == 1:
                    # arrow(x, y)
                    selected(x, y, option)
                elif character_index > 1:
                    passed(x, y, option)
                else:
                    unselected(x, y, option)
            else:
                unselected(x, y, option)

    # FONT OPTION
    setup_font('unscii-8-thin', 8, 16)
    length = SCREEN_WIDTH//2
    grid = [[3, 26, 48], 5]

    row = 5
    col1 = 3
    col2 = 26
    col3 = 48 

    while True:
        term.layer(0)
        term.clear()

        cc_border()
        title()
        subtitle()

        race_row()
        class_row()

        # Race Details
        race, location, stats, rbonus, gold, skills, req = race_options[race_index]
        occu, cbonus, ceq = class_options[class_index]
        total = tuple(s+r for s, r in zip(stats, rbonus))
        term.puts(col1, row+1, _race.format(race))
        term.puts(col1, row+2, _place.format(location))
        term.puts(col1, row+3, _class.format(""))

        # Level Details
        term.puts(col1, row+5, "LEVEL   : {:>10}".format(1))
        term.puts(col1, row+6, "EXP     : {:>10}".format(80))
        term.puts(col1, row+7, "GOLD    : {:>10}".format(gold))
        term.puts(col1, row+8, "SKILLS  : \n  {}\n  {}".format(*skills))

        if not character_index:
            # Player Data
            term.puts(col2, row+1, "HEALTH :         {:>2}".format(stats.str+rbonus.str+(stats.con+rbonus.con)*2))
            term.puts(col2, row+2, "MANA   :         {:>2}".format((stats.int+rbonus.int)+(stats.wis+rbonus.wis)*2))
            term.puts(col2, row+3, "SPEED  :         {:>2}".format(1+(stats.dex+rbonus.dex)//5))

            # Player Stats
            term.puts(col2, row+5, _sts.format(*total))
            term.puts(col2+13, row+6, _bon.format(*transform_values(rbonus)))
            # Traits

            # Equipment "hd nk bd ar hn lh rh lr rr wa lg ft"
            erow = row
            term.puts(col3, row+1, _equipment.format(*("" for _ in range(12))))

            # Description
            term.puts(1, 19, join(race_descriptions[race_index], SCREEN_WIDTH-2))

        else:
            # class/job to stats
            term.puts(col1, 8, _class.format(occu))

            # Writes Description to Footer
            term.puts(1, 19, join(class_descriptions[class_index], SCREEN_WIDTH-2))

            # Player Data
            term.puts(col2, row+1, "HEALTH :         {:>2}".format(stats.str+rbonus.str+cbonus.str+(stats.con+rbonus.con+cbonus.con)*2))
            term.puts(col2, row+2, "MANA   :         {:>2}".format((stats.int+rbonus.int+cbonus.int)+(stats.wis+rbonus.wis+cbonus.wis)*2))
            term.puts(col2, row+3, "SPEED  :         {:>2}".format(1+(stats.dex+rbonus.dex+cbonus.dex)//5))

            # builds totals including cbonus this time
            total = tuple(stat+racebonus+classbonus for stat, racebonus, classbonus in zip(stats, rbonus, cbonus))
            term.puts(col2, row+5, _sts.format(*total))
            term.puts(col2+13, row+6, _bon.format(*transform_values(rbonus)))
            term.puts(col2+17, row+6, _bon.format(*transform_values(cbonus)))

            # EQUIPMENT LIST
            term.puts(col3, row+1, _equipment.format(*("" for _ in range(12))))
            if character_index >= 2:
                items = list((req[character_index-2], ceq[character_index-2]))
                if '' in items:
                    items.remove('')
                print(items)
                if character_index == 2 and items:
                    term.bkcolor("white")
                    term.puts(col3+8, row+1, "[c=black]{}[/c]".format(items[0]))
                    term.bkcolor("black")
                elif character_index != 2 and items:
                    term.puts(col3+8, row+1, items[0])
                else:
                    term.puts(col3+8, row+1, "None")
                
            # term.puts(col3, row+1, _equipment.format(*eq))

        term.refresh()

# ============================== KEYBOARD INPUT =================================
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
            character_index = modify(-1, character_index, 15)

        elif code == term.TK_DOWN:
            character_index = modify(1, character_index, 15)

        elif code == term.TK_ENTER:
            character_index += 1
        # ESCAPE exists if on the first list else moves back one
        elif code in (term.TK_ESCAPE,):
            if character_index == 0:
                return output(
                        proceed=False,
                        value="Exit to Menu")
            else:
                character_index -= 1
        
	
if __name__ == "__main__":
    setup()
    try:
        print(create_character())
    except KeyboardInterrupt:
        print('quit')
    print('done')
