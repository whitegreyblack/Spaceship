import os
import sys
import shelve
import random
import textwrap
from time import sleep, time
from collections import namedtuple
from bearlibterminal import terminal as term
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
import strings
from screen_functions import *
from .scene import Scene

# some helper objects used in character creation
equipment = namedtuple("Equipment", "hd nk bd ar hn lh rh lr rr wa lg ft")
inventory = namedtuple("Inventory", "inventory")
genders = namedtuple("Gender", "gender bonus")
races = namedtuple("Race", "race location stats bonus gold skills eq")
classes = namedtuple("Class", "classes bonuses equipment")

# return type
player=namedtuple("Player",
    "home gold stats gender gbonus race rbonus \
    job jbonus skills equipment inventory")

class Create(Scene):
    def __init__(self, sid='create_menu'):
        super().__init__(sid)

    def reset(self):
        self.shorten = self.height <= 25
        self.delim, self.row, self.row_bonus = "\n", 11, 11

        if self.shorten:
            self.delim, self.row, self.row_bonus = "", 5, 6
        
        self.col1, self.col2, self.col3 = 3, 26, 49

        self.inv_screen = -1
        self.race_index = 0
        self.class_index = 0
        self.gender_index = 0
        self.character_index = 0

        self.grid = [[3, 26, 48], 5]
        self.length = self.width // 2

    def setup(self):
        self.reset()
        self.title = "Character Creation"
        self.help = "Press (?) for info on a switch race, subrace or class"

        self.gender_options = [
            genders("Male", strings.MALE),
            genders("Female", strings.FEMALE),
        ]

        # race objects and options
        self.race_options = [
            # Tiphmore -- Largest Free City in Calabaston
            races("Beast", "Tiphmore", strings.HUMAN, strings.BEAST_BONUS, 300,
                  ("thick fur", "animal senses"),
                  equipment("", "", "", "", "", ("long spear", "ring of ice"),
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

        # class objects and options
        self.class_options = [
            classes("Druid", strings.DRUIDS,
                    equipment("", "", "thick fur coat", "thick fur bracers",
                              "", "wooden staff", "", "ring of nature",
                              "ring of earth", "leather belt", "",
                              "leather boots")),

            classes("Cleric", strings.CLERIC,
                    equipment("cloth hood", "holy symbol", "light robe", "", "",
                              "mace", "small shield", "ring of power",
                              "ring of light", "rope belt", "",
                              "leather sandals")),

            classes("Archer", strings.ARCHER,
                    equipment("cloth hood", "whistle", "heavy cloak",
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
        # description options
        self.descriptions = [
            [strings.start],
            [strings.race_beast, strings.race_dwarf, strings.race_elven,
                strings.race_human, strings.race_orcen,],
            [strings.class_druid, strings.class_cleric, strings.class_wizard,
                strings.class_archer, strings.class_squire,]]

    def draw(self):
        term.clear()
        self.cc_border()
        self.draw_title()
        self.draw_subtitle()

        # Gender Race and Class Varialbes
        gender, gbonus = self.gender_row()
        race, location, stats, rbonus, gold, skills, req = self.race_row()
        occu, cbonus, ceq = self.class_row()

        # BONUS
        if self.character_index == 0:
            total = strings.stats(*(sum(stats) for stats in zip(strings.HUMAN, 
                                                                gbonus)))

        elif self.character_index == 1:
            total = strings.stats(*(sum(stats) for stats in zip(stats, 
                                                                gbonus, 
                                                                rbonus)))
        else:
            total = strings.stats(*(sum(stats) for stats in zip(stats,
                                                                gbonus,
                                                                rbonus,
                                                                cbonus)))

        # STATUS :- ATTRIBUTES
        hp = total.str + total.con * 2
        mp = total.int + total.wis * 2
        sp = total.dex // 5

        # STATUS :- BACKGROUND
        term.puts(self.col1, self.row + 1, strings._col1.format(
            gender,
            race if self.character_index > 0 else "",
            location if self.character_index > 0 else "",
            occu if self.character_index > 1 else "",
            gold if self.character_index > 0 else 0,
            1, 80, hp, mp, sp,
            delim=self.delim))

        # STATUS :- SKILLS
        term.puts(self.col2, self.row + 1, strings._col2.format(
            *("" for _ in range(2)) if self.character_index < 1 else skills,
            *(total),
            delim=self.delim))

        
        # STATUS :- GENDER BONUSES
        term.puts(
            self.col2 + 9, 
            self.row + (12 if not self.shorten else 7), 
            strings._bon.format(
                *self.transform_values(gbonus), 
                delim=self.delim))

        # STATUS :- RACE BONUSES
        # if self.character_index > 0:
        term.puts(
            self.col2 + 12, 
            self.row + (12 if not self.shorten else 7), 
            strings._bon.format(
                *(self.transform_values(rbonus) if self.character_index > 0 
                else (0 for _ in range(6))),
                    delim=self.delim))
            
        # STATUS :- CLASS BONUSES
        term.puts(
            self.col2 + 15, 
            self.row + (12 if not self.shorten else 7), 
            strings._bon.format(
                *self.transform_values(cbonus) if self.character_index > 1
                else (0 for _ in range(6)),
                delim=self.delim))

        # STATUS :- Item bonuses
        term.puts(
            self.col2 + 18, 
            self.row + (12 if not self.shorten else 7), 
            strings._bon.format(*(0 for _ in range(6)), delim=self.delim))

        # EQUIPMENT and INVENTORY
        eq, inv = None, None
        if self.character_index > 0:
            if self.character_index >= 2:
                eq, inv = self.form_equipment(req, ceq)

            else:
                eq, inv = self.form_equipment(req, ["" for _ in range(12)])

            # check if flag is set to show inventory or equipment
            if self.inv_screen < 0:
                x, y = self.col3, self.row + 1
                term.puts(x, y,
                    strings._col3.format(
                        *(e if len(e) > 0 else "" for e in eq),
                        delim=self.delim))

            else:
                for item, i in zip(inv, range(len(inv))):
                    x, y = self.col3, self.row + i + 1
                    string = "{}.{}".format(chr(ord('a') + i), item)
                    term.puts(x, y, string)

        else:
            term.puts(
                self.col3, 
                self.row + 1, 
                strings._col3.format(
                    *("" for _ in range(12)),
                    delim=self.delim))

        # FOOTER
        self.description_row()
        term.refresh()

        code = term.read()
        while code in (term.TK_SHIFT, term.TK_ALT, term.TK_CONTROL,):
            # ignores key modifiers -- keyboard think of it as a single key
            code = term.read()

        if code == term.TK_LEFT:
            if self.character_index == 0:
                self.gender_index = modify(
                    increment=-1, 
                    index=self.gender_index, 
                    options=len(self.gender_options))

            elif self.character_index == 1:
                self.race_index = modify(
                    increment=-1, 
                    index=self.race_index, 
                    options=len(self.race_options))

            elif self.character_index == 2:
                self.class_index = modify(
                    increment=-1, 
                    index=self.class_index, 
                    options=len(self.class_options))

        elif code == term.TK_RIGHT:
            if self.character_index == 0:
                self.gender_index = modify(
                    increment=1, 
                    index=self.gender_index, 
                    options=len(self.gender_options))

            elif self.character_index == 1:
                self.race_index = modify(
                    increment=1, 
                    index=self.race_index, 
                    options=len(self.race_options))

            elif self.character_index == 2:
                self.class_index = modify(
                    increment=1, 
                    index=self.class_index, 
                    options=len(self.class_options))

        elif code == term.TK_UP:
            self.character_index = modify(-1, self.character_index, 4)
            if self.character_index <= 2:
                self.inv_screen = -1

        elif code == term.TK_DOWN:
            self.character_index = modify(
                increment=1, 
                index=self.character_index, 
                options=4)

        # Toggles V Key
        elif code == term.TK_V and self.character_index > 1:
            self.inv_screen *= -1

        # Randomize selection -- maybe remove since its more of a debugging usage
        elif code == term.TK_8:
            # only randomizes if shift-8 is pressed -- else it's just pressing 8
            if term.state(term.TK_SHIFT) and self.character_index <= 1:
                # lets not randomize if you've already switch a gender
                # its not much more effort to finish creating your character
                # name = "Random name"
                self.gender_index = random.randint(0, 1)
                gender = self.gender_row(draw=False)
                self.race_index = random.randint(0, 4)
                race = self.race_row(draw=False)
                self.class_index = random.randint(0, 4)
                job = self.class_row(draw=False)
                eq, inv = self.form_equipment(race.eq, job.equipment)
                self.ret['kwargs'] = {
                    'player': player(
                        # name,
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
                        inv)
                }
                self.ret['scene'] = 'name_menu'
                self.proceed = False
                self.reset()

        # ENTER AFTER CHOOSING ALL 3 BACKGROUND CHOICES
        elif code == term.TK_ENTER:
            # check to see if we are at the final index
            if self.character_index == 3:
                gender = self.gender_row(draw=False)
                race = self.race_row(draw=False)
                job = self.class_row(draw=False)

                self.ret['kwargs'] = {
                    'player': player(
                    # name,
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
                    inv)
                }

                self.ret['scene'] = 'name_menu'
                self.proceed = False
                self.reset()

            else:
                self.character_index += 1

        elif code in (term.TK_ESCAPE,):
            if term.state(term.TK_SHIFT):
                self.proceed = False
                # self.ret = output(
                #         proceed=False,
                #         value="Exit to Desktop")
                self.ret['scene'] = ''

            elif self.character_index == 0:
                self.proceed = False
                # self.ret = self.scene_parent('main_menu')
                self.ret['scene'] = 'main_menu'

            else:
                self.character_index -= 1
                if self.character_index <= 1:
                    self.inv_screen = -1

    def cc_border(self):
        '''Border for Create Character Screen'''
        term.bkcolor('darkest grey')

        # top/bot lines horizontal border
        for i in range(self.width):
            term.puts(i, 1 if not self.shorten else 0, ' ')
            term.puts(i, 35 if not self.shorten else 18, ' ')
        
        # left/right lines vertical border
        for i in range(35 if not self.shorten else 18):
            term.puts(0, i + 1, ' ')
            term.puts(self.width - 1, i + 1, ' ')

    def draw_title(self):
        '''Adds the title to top of screen'''
        title = " " + self.title + " "
        term.bkcolor('brown')
        term.puts(
            center(title, self.width), 
            1 if not self.shorten else 0, 
            "[c=black]" + self.title + "[/c]")
        term.bkcolor('black')

    def subtitle_text(self, i):
        text = "Choose your {}"
        if i == 0:
            return text.format("gender")
        elif i == 1:
            return text.format("race")
        elif i == 2:
            return text.format('class | Press "v" to view your inventory')
        else:
            return "Press (ENTER) to finish"

    def draw_subtitle(self):
        '''Adds text underneath the title'''
        # subtitle -- clears subtitle area to make space for new subtitle text
        subtitle = self.subtitle_text(self.character_index)
        x = center(subtitle, self.width)
        y = 3 if not self.shorten else 1
        term.puts(x, y, subtitle)
        term.bkcolor('black')

    def gender_row(self, draw=True):
        '''Returns a tuple "gender" according to the gender_index'''
        if draw:
            # for option, index in zip(self.gender_options, 
            #                          range(len(self.gender_options))):
            for index, option in enumerate(self.gender_options):
                x, y = 24 + 22 * index, 5 if not self.shorten else 2
                gender = pad(option.gender, length=8)
                if index == self.gender_index:
                    if self.character_index == 0:
                        switch(x, y, gender, bg_before='white', color='black')
                    else:
                        switch(x, y, gender, bg_before='grey')
                else:
                    switch(x, y, gender)

        return self.gender_options[self.gender_index]

    def race_row(self, draw=True):
        '''Returns a tuple "race" according to the race_index'''
        # RACE OPTIONS
        if draw:
            # for option, i in zip(race_options, range(len(race_options))):
            for index, option in enumerate(self.race_options):
                x, y = 13 + 11 * index, 7 if not self.shorten else 3
                race = pad(option.race, length=8)
                if index == self.race_index:
                    if self.character_index == 1:
                        switch(x, y, race, bg_before='white', color='black')
                    elif self.character_index > 1:
                        switch(x, y, race, bg_before='grey')
                    else:
                        switch(x, y, race)
                else:
                    switch(x, y, race)

        return self.race_options[self.race_index]

    def class_row(self, draw=True):
        '''Returns a tuple "class" according to class_index'''
        if draw:
            # for option, i in zip(class_options, range(len(class_options))):
            for index, option in enumerate(self.class_options):
                x, y = 13 + 11 * index, 9 if not self.shorten else 4
                option = pad(option.classes, length=8)
                if index == self.class_index:
                    if self.character_index == 2:
                        switch(x, y, option, bg_before='white', color='black')
                    elif self.character_index > 2:
                        switch(x, y, option, bg_before='grey')
                    else:
                        switch(x, y, option)
                else:
                    switch(x, y, option)

        return self.class_options[self.class_index]

    def description_row(self):
        '''Returns the descriptions according to character_index'''
        primary = min(self.character_index, 2)

        secondary = self.class_index if self.character_index >= 2 \
            else self.race_index if self.character_index == 1 \
            else self.character_index

        description = self.descriptions[primary][secondary]

        term.puts(1, 37 if not self.shorten else (self.row + 14), 
            join(description.replace('\n',''), self.width - 2, self.delim))

    def transform_values(self, values):
        return ("+[c=#00ff00]" + str(v) + "[/c]" if v > 0
                else "-[c=#ff0000]" + str(abs(v)) + "[/c]" if v < 0
                else v 
                for v in values)

    def form_equipment(self, race_eq, class_eq):
        def get_eq(x):
            eq = []
            if x != "":
                if isinstance(x, tuple):
                    for xx in x:
                        eq.append(xx)

                else:
                    eq.append(x)
            return eq

        def flatten(container):
            return [ item for items in container for item in items ]

        inv = []

        for r, c in zip(class_eq, race_eq):
            inv.append(get_eq(r) + get_eq(c))

        eqp = [ i.pop(0) if len(i) > 0 else [] for i in inv ]
        return eqp, flatten(inv)

def test_hero():
    c = Create()
    gender = c.gender_row(draw=False)
    race = c.race_row(draw=False)
    job = c.class_row(draw=False)
    eq, inv = c.form_equipment(race.eq, job.equipment)

    return {'player': player(
        # name,
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
        inv),
    'name': 'Grey',
    }


if __name__ == "__main__":
    term.open()
    c = Create()
    ret = c.run()
    print(ret)