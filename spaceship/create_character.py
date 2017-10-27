import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')

from collections import namedtuple
from textwrap import wrap

from bearlibterminal import terminal as term

import spaceship.cc_strings as strings
# from spaceship.constants import CM_BORDER_HEIGHT as BORDER_HEIGHT
# from spaceship.constants import CM_BORDER_WIDTH as BORDER_WIDTH
# from spaceship.constants import MENU_SCREEN_HEIGHT as SCREEN_HEIGHT
# from spaceship.constants import MENU_SCREEN_WIDTH as SCREEN_WIDTH
from spaceship.continue_game import continue_game
from spaceship.new_name import new_name
from spaceship.screen_functions import *
from spaceship.setup import output, setup, setup_font, setup_menu, toChr, setup_ext
from random import randint 
# str_title = "Character Creation"
# str_help = "Press (?) for info on a selected race, subrace or class"
# def create_character_small_term():
#     def cc_border():
#     '''Border for Create Character Screen'''
#     # border(BORDER_WIDTH, [0], "#")
#     # border(BORDER_WIDTH, [10, 39], toChr("2550"))
#     term.bkcolor('darkest grey')
#     for i in range(BORDER_WIDTH-2):
#         term.puts(i+1, 1, ' ')
#         term.puts(i+1, 35, ' ')
#     for i in range(35):
#         term.puts(1, i+1, ' ')
#         term.puts(BORDER_WIDTH-2, i+1, ' ')
#     term.bkcolor('dark brown')
#     for i in range(20):
#         term.puts(BORDER_WIDTH//2-10+i, 1, ' ')
#     term.bkcolor('black')

#     term.border()

def create_character():
    row = 11
    col1 = 3
    col2 = 26
    col3 = 49

    inv_screen = -1
    race_index = 0
    class_index = 0
    gender_index = 0
    character_index = 0

    indices = [0, 0, 0]
    grid = [[3, 26, 48], 5]
    length = term.state(term.TK_WIDTH)//2

    str_title = "Character Creation"
    str_help = "Press (?) for info on a selected race, subrace or class"

    # some helper objects used in character creation
    character = namedtuple("Character", "name gender_opt race_opt class_opt")
    equipment = namedtuple("Equipment", "hd nk bd ar hn lh rh lr rr wa lg ft")

    # return type
    player=namedtuple("Player",
        "name home gold stats gender gbonus race rbonus job \
        jbonus skills equipment inventory")
    def subtitle_text(i):
        text = "Choose your {}"
        if i == 0:
            return text.format("gender")
        elif i == 1:
            return text.format("race")
        elif i == 2:
            return text.format('class | Press "v" to view your inventory')
        else:
            return "Press (ENTER) to finish"

    def transform_values(values):
        return tuple("+[c=#00ff00]"+str(v)+"[/c]" if v > 0
                     else "-[c=#ff0000]"+str(abs(v))+"[/c]" if v < 0
                     else v for v in values)

    def cc_border():
        '''Border for Create Character Screen'''
        # border(BORDER_WIDTH, [0], "#")
        # border(BORDER_WIDTH, [10, 39], toChr("2550"))
        term.bkcolor('darkest grey')
        for i in range((term.state(term.TK_WIDTH)-1)-2):
            term.puts(i+1, 1, ' ')
            term.puts(i+1, 35, ' ')
        for i in range(35):
            term.puts(1, i+1, ' ')
            term.puts((term.state(term.TK_WIDTH)-1)-2, i+1, ' ')
        term.bkcolor('dark brown')
        for i in range(20):
            term.puts((term.state(term.TK_WIDTH)-1)//2-10+i, 1, ' ')
        term.bkcolor('black')
        
    def title():
        '''Adds the title to top of screen'''
        title = " " + str_title + " "
        term.bkcolor('brown')
        term.puts(center(title, (term.state(term.TK_WIDTH))), 1, "[c=black]"+title+"[/c]")
        term.bkcolor('black')

    def subtitle():
        '''Adds text underneath the title'''
        # subtitle -- clears subtitle area to make space for new subtitle text
        subtitle = subtitle_text(character_index)
        x = center(subtitle, (term.state(term.TK_WIDTH)))
        term.puts(x, 3, subtitle)
        term.bkcolor('black')

    def gender_row(g=False):
        '''Returns a tuple "gender" according to the gender_index'''
        genders = namedtuple("Gender", "gender bonus")
        gender_options = [
            genders("Male", strings.MALE),
            genders("Female", strings.FEMALE),
        ]
        if not g:
            for option, i in zip(gender_options, range(len(gender_options))):
                x, y = 24+22*i, 5
                gender = pad(option.gender, length=8)
                if i == gender_index:
                    if character_index == 0:
                        selected(x, y, gender)
                    else:
                        passed(x, y, gender)
                else:
                    unselected(x, y, gender)

        return gender_options[gender_index]

    def race_row(r=False):
        '''Returns a tuple "race" according to the race_index'''
        races = namedtuple("Race", "race location stats bonus gold skills eq")
        race_options = [
            # Tiphmore -- Largest Free City in Calabaston
            races("Beast", "Tiphmore", strings.HUMAN, strings.BEAST_BONUS, 300,
                  ("thick fur", "animal senses"),
                  equipment("", "", "", "", "", ("long spear", "silver sword"),
                            "", "", "", "", "", "")),
            # Capital of Yugahdahrum
            races("Dwarf", "Dun Badur", strings.HUMAN, strings.DWARF_BONUS, 250,
                  ("dark vision", "dwarven fortitude"),
                  equipment("horned helmet", "gold necklace", "", "", "",
                            ("battle axe", "copper pick"), "", "", "",
                            "", "", "")),
            # Aurundel -- Capital of Auriel in the Emerald Forest
            races("Elf", "Aurundel", strings.HUMAN, strings.ELVEN_BONUS, 250,
                  ("forest spirit", "nimble"),
                  equipment("", "", "elven chainmail", "", "",
                            "mithril dagger", "mithril dagger",
                            "", "", "", "", "")),
            # Renmar -- Capital of Rane Empire
            races("Human", "Renmar", strings.HUMAN, strings.HUMAN_BONUS, 200,
                  ("", ""),
                  equipment("", "", "", "", "", "broadsword", "medium shield",
                            "", "", "", "", "")),
            # Lok Gurrah, Capital of Oggrahgar
            races("Orc", "Lok Gurrah", strings.HUMAN, strings.ORCEN_BONUS, 150,
                  ("thick skin", "bloodrage"),
                  equipment("metal cap", "", "metal armor", "", "",
                            ("mace", "warhammer"), "", "", "", "", "", "")),
        ]
        # RACE OPTIONS
        if not r:
            for option, i in zip(race_options, range(len(race_options))):
                x, y = 13+11*i, 7
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

    def class_row(c=False):
        '''Returns a tuple "class" according to class_index'''
        classes = namedtuple("Class", "classes bonuses equipment")
        class_options = [
            classes("Druid", strings.DRUIDS,
                    equipment("", "", "thick fur coat", "thick fur bracers",
                              "", "wooden staff", "", "ring of nature",
                              "ring of earth", "leather belt", "",
                              "leather boots")),

            classes("Cleric", strings.CLERIC,
                    equipment("hood", "holy symbol", "light robe", "", "",
                              "mace", "small shield", "ring of power",
                              "ring of light", "rope belt", "",
                              "leather sandals")),

            classes("Archer", strings.ARCHER,
                    equipment("hood", "whistle", "heavy cloak",
                              "leather bracers", "cloth gloves", "short bow",
                              "", "", "", "leather belt", "common pants",
                              "leather boots")),

            classes("Wizard", strings.WIZARD,
                    equipment("hood", "amulet of power", "light robe", "", "",
                              "quarterstaff", "spellbook", "ring of water",
                              "ring of fire", "rope belt", "",
                              "leather sandals")),

            classes("Squire", strings.SQUIRE,
                    equipment("leather cap", "", "leather armor",
                              "leather bracers", "cloth gloves", "long sword",
                              "medium shield", "", "", "leather belt",
                              "common pants", "leather boots")),
        ]

        # CLASS OPTIONS
        if not c:
            for option, i in zip(class_options, range(len(class_options))):
                x, y = 13+11*i, 9
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
        '''Returns the descriptions according to character_index'''
        descriptions = [
            [strings.start],
            [strings.race_beast, strings.race_dwarf, strings.race_elven,
                strings.race_human, strings.race_orcen, ],
            [strings.class_druid, strings.class_cleric, strings.class_wizard,
                strings.class_archer, strings.class_squire, ]]

        primary = min(character_index, 2)

        secondary = class_index if character_index >= 2 \
            else race_index if character_index == 1 \
            else character_index

        term.puts(1, 37, join(
            descriptions[primary][secondary],
            (term.state(term.TK_WIDTH))-2))

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
            # return list(element
            #           for iteratable in container
            #           for element in iteratable)
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

        # Gender Race and Class Varialbes
        gender, gbonus = gender_row()
        race, location, stats, rbonus, gold, skills, req = race_row()
        occu, cbonus, ceq = class_row()

        # BONUS
        if character_index == 0:
            total = strings.STATS(*(s + g for s, g in zip(strings.HUMAN, gbonus)))
        elif character_index == 1:
            total = strings.STATS(*(s + g + r for s, g, r in zip(stats, gbonus, rbonus)))
        else:
            total = strings.STATS(*(s + g + r + c for s, g, r, c in zip(
                                                        stats,
                                                        gbonus,
                                                        rbonus,
                                                        cbonus)))

        # STATUS
        hp = total.str + total.con * 2
        mp = total.int + total.wis * 2
        sp = total.dex // 5

        # BACKGROUND
        term.puts(col1, row + 1, strings._col1.format(
            gender,
            race if character_index > 0 else "",
            location if character_index > 0 else "",
            occu if character_index > 1 else "",
            gold if character_index > 0 else 0,
            1, 80, hp, mp, sp))

        # STATS
        term.puts(col2, row + 1, strings._col2.format(
            *("" for _ in range(2)) if character_index < 1 else skills,
            *(total)))

        term.puts(col2+10, row+11, strings._bon.format(*transform_values(gbonus)))

        if character_index > 0:
            term.puts(col2 + 14, row + 11, strings._bon.format(*transform_values(rbonus)))

        # EQUIPMENT and INVENTORY
        eq, inv = None, None
        if character_index > 1:
            term.puts(col2 + 18, row + 11, strings._bon.format(*transform_values(cbonus)))
            eq, inv = form_equipment(req, ceq)
            # if var is -1 then shows eq else shows inv
            if inv_screen < 0:
                term.puts(col3, row+1, strings._col3.format(
                    *(e if len(e) > 0 else "" for e in eq)))
            else:
                for item, i in zip(inv, range(len(inv))):
                    term.puts(col3, row+1+i, "{}.{}".format(
                                                        chr(ord('a')+i),
                                                        item))
        else:
            term.puts(col3, row+1, strings._col3.format(
                *("" for _ in range(12))))

        # FOOTER
        description_row()
        term.refresh()

        # ====================================================================#
        # ========================= KEYBOARD INPUT ===========================#
        # ====================================================================#
        code = term.read()
        while code in (term.TK_SHIFT, term.TK_ALT, term.TK_CONTROL,):
            # ignores key modifiers -- keyboard think of it as a single key
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
            if character_index <= 2:
                inv_screen = -1

        elif code == term.TK_DOWN:
            character_index = modify(1, character_index, 4)

        # Toggles V Key
        elif code == term.TK_V and character_index > 1:
            inv_screen *= -1

        # Randomize selection
        elif code == term.TK_8:
            if term.state(term.TK_SHIFT):
                name = "Random name"
                gender_index = randint(0, 1)
                gender = gender_row(1)
                race_index = randint(0, 4)
                race = race_row(1)
                class_index = randint(0, 4)
                job = class_row(1)
                eq, inv = form_equipment(race.eq, job.equipment)
                return output(
                        proceed=True,
                        value=player(
                            name,
                            race.location,
                            race.gold,
                            race.stats,
                            gender.gender,
                            gender.bonus,
                            race.race,
                            race.bonus,
                            job.classes,
                            job.bonuses,
                            race.skills,
                            eq,
                            inv))
            

        # ENTER
        elif code == term.TK_ENTER:
            if character_index == 3:
                name = new_name((race, occu))
                print(name)
                if name.proceed == 0:
                    gender = gender_row(1)
                    race = race_row(1)
                    job = class_row(1)
                    return output(
                            proceed=True,
                            value=player(
                                name.value,
                                race.location,
                                race.gold,
                                race.stats,
                                gender.gender,
                                gender.bonus,
                                race.race,
                                race.bonus,
                                job.classes,
                                job.bonuses,
                                race.skills,
                                eq,
                                inv))
            else:
                character_index += 1

        # ESCAPE exists if on the first list else moves back one
        elif code in (term.TK_ESCAPE,):
            if term.state(term.TK_SHIFT):
                return output(
                        proceed=False,
                        value="Exit to Desktop")

            elif character_index == 0:
                return output(
                        proceed=True,
                        value="Exit to Menu")

            else:
                character_index -= 1
                if character_index <= 1:
                    inv_screen = -1


if __name__ == "__main__":
    term.open()
    setup_font('Ibm_cga', 8, 8)
    term.set('window: size=80x50, cellsize=auto, title="Spaceship"')
    try:
        print(create_character())
    except KeyboardInterrupt:
        print('quit')
