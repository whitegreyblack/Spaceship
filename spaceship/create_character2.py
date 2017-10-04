import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.constants import MENU_SCREEN_WIDTH as SCREEN_WIDTH
from spaceship.constants import MENU_SCREEN_HEIGHT as SCREEN_HEIGHT
from spaceship.constants import CM_BORDER_HEIGHT as BORDER_HEIGHT
from spaceship.constants import CM_BORDER_WIDTH as BORDER_WIDTH
from bearlibterminal import terminal as term
from spaceship.new_name import new_name
from spaceship.screen_functions import *
from spaceship.continue_game import continue_game
from spaceship.setup import setup, alphabet, toChr, output, setup_menu, setup_font
from textwrap import wrap
from collections import namedtuple
import descriptions as desc
from d2 import *

_world="Calabaston"

_col1="""
Gender  : {:>10}
Race    : {:>10}
Capital : {:>10}
Class   : {:>10}

Gold    : {:>10}
Level   : {:>10}
Exp     : {:>10}

HP      : [c=#00ffff]{:>10}[/c]
MP      : [c=#00ffff]{:>10}[/c]
SD      : [c=#00ffff]{:>10}[/c]
"""[1:]

_col2="""
SKILLS  : \n  {}\n  {}

   TOTAL  GB  RB  CB 
STR : [c=#00ffff]{:>2}[/c] 
CON : [c=#00ffff]{:>2}[/c] 
DEX : [c=#00ffff]{:>2}[/c] 
INT : [c=#00ffff]{:>2}[/c] 
WIS : [c=#00ffff]{:>2}[/c] 
CHA : [c=#00ffff]{:>2}[/c] 
"""[1:]

_col3="""
HEAD  : {:<5}\nNECK  : {:<5}\nBODY  : {:<5}\nARMS  : {:<5}\nHANDS : {:<5}\nLHAND : {:<5}
RHAND : {:<5}\nRING1 : {:<5}\nRING2 : {:<5}\nWAIST : {:<5}\nLEGS  : {:<5}\nFEET  : {:<5}"""[1:]

def create_character():
    # setup stuff
    setup_menu()
    setup_font('unscii-8-thin', 8, 16)

    row = 5
    col1 = 3
    col2 = 26
    col3 = 49 

    race_index = 0
    class_index = 0
    gender_index = 0
    character_index = 0

    indices = [0, 0, 0]
    grid = [[3, 26, 48], 5]
    length = SCREEN_WIDTH//2

    str_title = "Character Creation"
    str_help = "Press (?) for info on a selected race, subrace or class"

    character = namedtuple("Character", "name race_opt class_opt") 
    equipment = namedtuple("Equipment", "hd nk bd ar hn lh rh lr rr wa lg ft")

    def subtitle_text(i):
        text = "Choose your {}"
        if i == 0:
            return text.format("gender")
        elif i == 1:
            return text.format("race")
        elif i == 2:
            return text.format("class")
        else:
            return "Press (ENTER) to finish"
    
    def transform_values(values):
        return tuple("+[c=#00ff00]"+str(v)+"[/c]" if v > 0 else "-[c=#ff0000]"+str(abs(v))+"[/c]" if v < 0 else v for v in values) 

    def cc_border():
        border(BORDER_WIDTH, [0], "#")
        border(BORDER_WIDTH, BORDER_HEIGHT, toChr("2550"))

    def eq_border():
        border(SCREEN_WIDTH-24, [row], "#")

    def title():
        term.puts(center(" "+str_title+" ", SCREEN_WIDTH), 0," "+ str_title + " ")

    def subtitle():
        # subtitle -- clears subtitle area to make space for new subtitle text
        subtitle = subtitle_text(character_index)
        x = center(subtitle, SCREEN_WIDTH)
        term.puts(x, 1, subtitle)

    def gender_row():
        genders = namedtuple("Gender", "gender bonus")
        gender_options = [
            genders("Male", MALE),
            genders("Female", FEMALE),
        ]
        for option, i in zip(gender_options, range(len(gender_options))):
            x, y = 24+22*i, 2
            gender = pad(option.gender, length=8)
            if i == gender_index:
                if character_index == 0:
                    selected(x, y, gender)
                else:
                    passed(x, y, gender)
            else:
                unselected(x, y, gender)

        return gender_options[gender_index]

    def race_row():
        races = namedtuple("Race", "race location stats bonus gold skills eq")
        race_options = [
            #Tiphmore -- Largest Free City in Calabaston
            races("Beast", "Tiphmore", HUMAN, BEAST_BONUS, 300, ("thick fur", "animal senses"),             
                equipment("", "", "", "", "", ("long spear", "silver sword"), "", "", "", "", "", "")),
            # Capital of Yugahdahrum
            races("Dwarf", "Dun Badur", HUMAN, DWARF_BONUS, 250, ("dark vision", "dwarven fortitude"),
                equipment("horned helmet", "gold necklace", "", "", "", ("battle axe", "copper pick"), "", "", "", "", "", "")),
            # Aurundel -- Capital of Auriel in the Emerald Forest
            races("Elf", "Aurundel", HUMAN, ELVEN_BONUS, 250, ("forest spirit", "nimble"),
                equipment("", "", "elven chainmail", "", "", "mithril dagger", "mithril dagger", "", "", "", "", "")),
            # Renmar -- Capital of Rane Empire
            races("Human", "Renmar", HUMAN, HUMAN_BONUS, 200, ("", ""),
                equipment("", "", "", "", "", "broadsword", "medium shield", "", "", "", "", "")),
            # Lok Gurrah, Capital of Oggrahgar
            races("Orc", "Lok Gurrah", HUMAN, ORCEN_BONUS, 150, ("thick skin", "bloodrage"),
                equipment("metal cap", "", "metal armor", "", "", ("mace", "warhammer"), "", "", "", "", "", "")),
        ]

        # RACE OPTIONS
        for option, i in zip(race_options, range(len(race_options))):
            x, y = 13+11*i, 3
            race = pad(option.race, length=8)
            if i == race_index:
                if character_index == 1:
                    selected(x, y, race)
                elif character_index > 1:
                    passed(x, y, race)
                else:
                    unselected(x, y, race)
            else:
                unselected(x, y, race)

        return race_options[race_index]

    def class_row():
        classes = namedtuple("Class", "classes bonuses equipment")
        class_options = [
            classes("Druid", DRUIDS, equipment("", "", "thick fur coat", "thick fur bracers", "", "wooden staff", "", 
                "ring of nature", "ring of earth", "leather belt", "", "leather boots")),
            classes("Cleric", CLERIC, equipment("hood", "holy symbol", "light robe", "", "", "mace", "small shield", 
                "ring of power", "ring of light", "rope belt", "", "leather sandals")),
            classes("Archer", ARCHER, equipment("hood", "whistle", "heavy cloak", "leather bracers", "cloth gloves", 
                "short sword", "small dagger", "", "", "leather belt", "common pants", "leather boots")),
            classes("Wizard", WIZARD, equipment("hood", "amulet of power", "light robe", "", "", "quarterstaff", 
                "spellbook", "ring of water",  "ring of fire", "rope belt", "", "leather sandals")),
            classes("Squire", SQUIRE, equipment("leather cap", "", "leather armor", "leather bracers", "cloth gloves", 
                "long sword", "medium shield", "", "", "leather belt", "common pants", "leather boots")),
        ]

        # CLASS OPTIONS
        for option, i in zip(class_options, range(len(class_options))):
            x, y = 13+11*i, 4
            option = pad(option.classes, length=8)
            if i == class_index:
                if character_index == 2:
                    selected(x, y, option)
                elif character_index > 2:
                    passed(x, y, option)
                else:
                    unselected(x, y, option)
            else:
                unselected(x, y, option)

        return class_options[class_index]

    def description_row():
        descriptions=[
            [desc.start],
            [desc.race_beast, desc.race_dwarf, desc.race_elven, desc.race_human, desc.race_orcen,],
            [desc.class_druid, desc.class_cleric, desc.class_wizard, desc.class_archer, desc.class_squire,]]
        
        secondary = class_index if character_index == 2 else \
                    race_index if character_index == 1 else \
                    character_index

        term.puts(1, 19, join(
            descriptions[character_index][secondary], 
            SCREEN_WIDTH-2))

    def form_equipment(req, ceq):
        def get_eq(x):
            eq = []
            if x != "":
                if isinstance(x, tuple):
                    for xx in x:
                        eq.append(xx)
                else:
                    eq.append(x)
            return eq

        def flatten(l):
            # return list(element for iteratable in container for element in iteratable)
            items = []
            for i in l:
                for ii in i:
                    items.append(ii)
            return items

        inv = []
        for r, c in zip(req, ceq):
            inv.append(get_eq(r)+get_eq(c))
        eqp = [i.pop(0) if len(i) > 0 else [] for i in inv]
        return eqp, flatten(inv)

    while True:
        term.clear()

        # header
        cc_border()
        title()
        subtitle()
        
        # # Gender Race and Class Varialbes
        gender, gbonus = gender_row()
        race, location, stats, rbonus, gold, skills, req = race_row()
        occu, cbonus, ceq = class_row()

        if character_index == 0:
            total = STATS(*(s+g for s, g in zip(HUMAN, gbonus)))
        elif character_index == 1:
            total = STATS(*(s+g+r for s, g, r in zip(stats, gbonus, rbonus)))
        else:
            total = STATS(*(s+g+r+c for s, g, r, c in zip(stats, gbonus, rbonus, cbonus)))
        hp = total.str + total.con * 2
        mp = total.int + total.wis * 2
        sp = total.dex // 5 
        term.puts(col1, row+1, _col1.format(
            gender,
            race if character_index > 0 else "",
            location if character_index > 0 else "",
            occu if character_index > 1 else "",
            gold if character_index > 0 else 0,
            1, 80, hp, mp, sp))
        term.puts(col2, row+1, _col2.format(
            *("" for _ in range(2)),
            
        term.puts(col3, row+1, _col3.format(*("" for _ in range(12))))
        # # Background stuff
        # term.puts(col1, row+1, 
        #     _col1.format(
        #         gender, 
        #         "" if character_index < 1 else race, 
        #         "" if character_index < 1 else location, 
        #         "" if character_index < 2 else occu,
        #         1,
        #         80,
        #         "" if character_index < 2 else gold,
        #         HUMAN.str+gbonus.str+(HUMAN.con+gbonus.con)*2 if character_index < 1 else "",
        #         HUMAN.int+gbonus.int+(HUMAN.wis+gbonus.wis)*2 if character_index < 1 else "",
        #         (HUMAN.dex+gbonus.dex)//5))

        # if not character_index:
        #     term.puts(col2, row+1, _skills.format(*("" for _ in range(2))))

        #     # Player Stats
        #     total = tuple(h+g for h, g in zip(HUMAN, gbonus))
        #     term.puts(col2, row+5, _sts.format(*total))
        #     term.puts(col2+10, row+6, _bon.format(*transform_values(gbonus)))

        #     # EQUIPMENT -- initially empty until class is chosen
        #     term.puts(col3, row+1, _equipment.format(*("" for _ in range(12))))

        #     # Description
        #     description_row()

        # elif character_index == 1:
        #     # Player STATUS
        #     # term.puts(col2, row+1, _status.format(
        #     #     stats.str+gbonus.str+rbonus.str+(stats.con+gbonus.con+rbonus.con)*2,
        #     #     stats.int+gbonus.int+rbonus.int+(stats.wis+gbonus.con+rbonus.wis)*2,
        #     #     1+(stats.dex+gbonus.dex+rbonus.dex)//5,
        #     # ))

        #     # STATS
        #     total = tuple(h+g+r for h, g, r in zip(stats, gbonus, rbonus))
        #     term.puts(col2, row+5, _sts.format(*total))
        #     term.puts(col2+10, row+6, _bon.format(*transform_values(gbonus)))
        #     term.puts(col2+14, row+6, _bon.format(*transform_values(rbonus)))

        #     # EQUIPMENT
        #     term.puts(col3, row+1, _equipment.format(*("" for _ in range(12))))

        #     # DESCRIPTION
        #     description_row()
            
        # else:
        #     # STATUS
        #     # term.puts(col2, row+1, _status.format(
        #     #     stats.str+gbonus.str+rbonus.str+cbonus.str+(stats.con+gbonus.con+rbonus.con)*2,
        #     #     stats.int+gbonus.int+rbonus.int+cbonus.int+(stats.wis+gbonus.con+rbonus.wis)*2,
        #     #     1+(stats.dex+gbonus.dex+rbonus.dex+cbonus.dex)//5,
        #     # ))

        #     # builds totals including cbonus this time
        #     total = tuple(s+g+r+c for s, g, r, c in zip(stats, gbonus, rbonus, cbonus))
        #     term.puts(col2, row+5, _sts.format(*total))
        #     term.puts(col2+10, row+6, _bon.format(*transform_values(gbonus)))
        #     term.puts(col2+14, row+6, _bon.format(*transform_values(rbonus)))
        #     term.puts(col2+18, row+6, _bon.format(*transform_values(cbonus)))

        #     # EQUIPMENT LIST
        #     eq, inv = form_equipment(req, ceq)
        #     term.puts(col3, row+1, _equipment.format(*(e if len(e) > 0 else "" for e in eq)))

        #     # Writes Description to Footer
        description_row()
        term.refresh()

        # ===============================================================================#
        # ============================== KEYBOARD INPUT =================================#
        # ===============================================================================#
        code = term.read()
        while code in (term.TK_SHIFT, term.TK_ALT, term.TK_CONTROL,):
            code = term.read()

        if code == term.TK_LEFT:
            if character_index == 0:
                gender_index = modify(-1, gender_index, 2)

            elif character_index == 1:
                race_index = modify(-1, race_index, 5)

            elif character_index == 2:
                class_index = modify(-1, class_index, 5)
            
        elif code == term.TK_RIGHT:
            if character_index == 0:
                gender_index = modify(1, gender_index, 2)

            elif character_index == 1:
                race_index = modify(1, race_index, 5)

            elif character_index == 2:
                class_index = modify(1, class_index, 5)

        elif code == term.TK_UP:
            character_index = modify(-1, character_index, 4)

        elif code == term.TK_DOWN:
            character_index = modify(1, character_index, 4)

        elif code == term.TK_ENTER:
            if character_index == 3:
                name = new_name((race_options[race_index].race, class_options[class_index].classes))
                if name.proceed > -1:
                    return output(
                            proceed=True,
                            value=character(name.value, race_options[race_index], class_options[class_index])) 
            else:
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
