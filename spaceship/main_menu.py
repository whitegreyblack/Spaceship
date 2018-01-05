import os
import sys
import random
from collections import namedtuple
from bearlibterminal import terminal as term
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
import spaceship.cc_strings as strings
from .setup_game import setup, setup_font, setup_menu, output
from .screen_functions import *
from .options import Option

class Engine:
    def __init__(self, scene):
        self.scene = scene
        self.proceed = True

    def run(self):
        while self.proceed:
            print('Scene: ', self.scene)
            ret = self.scene.run()
            print('Return ', ret)
            if isinstance(ret, Scene):
                self.scene = ret
            else:
                self.proceed = False

    def change_scene(self, title):
        self.scene = self.scene.scene(title)

'''
def connect_scenes(scene_a, scene_b):
    scene_a.add_scene(scene_b)
    scene_b.add_scene(scene_a)

    scene_a.add_child_scene(scene_b)
    scene_b.add_parent_scene(scene_a)
'''
class Scene:
    def __init__(self, width, height, scene_id):
        '''Initializes window and screen dimensions and title for the scene'''
        self.width, self.height = width, height
        self.sid = scene_id

        self.proceed = True

        # scenes is a dictionary holding other scene objects
        self.scenes = {}
        self.setup()

    def __repr__(self):
        return self.sid

    def setup(self):
        pass
    
    def run(self):
        while self.proceed:
            self.draw()
        
        self.proceed = True
        if hasattr(self, 'ret'):
            return self.ret

    def draw(self):
        pass

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, h):
        self.__height = h

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, w):
        self.__width = w

    def check_scene(self, scene):
        # if scene.title in self.scenes.keys():
        #     raise ValueError('Same title already in scene')
        # elif scene.width != self.width:
        m = None
        if self == scene:
            m = 'Incoming scene is duplicate of current scene'

        elif scene.width != self.width:
            m = 'Incoming scene does not have the same width as current scene'

        elif scene.height != self.height:
            m = 'Incoming scene does not have the same height as current scene'

        else:
            for key in self.scenes.keys():
                if scene.sid in self.scenes[key].keys():
                    m = 'Same Title already in scene'
        if m:
            raise ValueError(m)
        return True

    def scene_child(self, sid):
        if isinstance(sid, Scene):
            title = title.sid

        try:
            return self.scenes[1][sid]

        except KeyError:
            raise KeyError('No parent scene with that title')

        except:
            raise

    @property
    def children(self):
        '''Returns a list of children scene objects'''
        # return [self.scenes[(title, scene for title, scene in self.scenes.keys() if scene == 0]
        if 1 not in self.scenes.keys():
            return []

        return [self.scenes[1][title] for title in self.scenes[1].keys()]

    def add_scene_child(self, scene):
        self.check_scene(scene)
        # self.scenes[(scene.title, 0)] = scene
        # self.scenes[0][scene.title] = scene
        if 1 not in self.scenes.keys():
            self.scenes[1] = { scene.sid: scene }

        else:
            self.scenes[1][scene.sid] = scene
    
    def scene_parent(self, sid):
        if isinstance(sid, Scene):
            sid = sid.sid

        try:
            return self.scenes[0][sid]

        except KeyError:
            raise KeyError('No parent scene with that title')

        except:
            raise

    def add_scene_parent(self, scene):
        self.check_scene(scene)
        # self.scenes[(scene.title, 1)] = scene
        # self.scenes[1][scene.title] = scene
        if 0 not in self.scenes.keys():
            self.scenes[0] = { scene.sid: scene }

        else:
            self.scenes[0][scene.sid] = scene 

    @property
    def parents(self):
        '''Returns a list of parent scene objects'''
        # return [self.scenes[(title, scene)] for title, scene in self.scenes.keys() if scene == 1]
        if 0 not in self.scenes.keys():
            return []
        elif len(self.scenes.keys()) == 1:
            return [self.scenes[0][sid] for sid in self.scenes[0].keys()].pop()
        return [self.scenes[0][sid] for sid in self.scenes[0].keys()]

    
class Main(Scene):
    def __init__(self, width, height, title='main_menu'):
        super().__init__(width, height, title)

    def setup(self):
        self.index = -1
        
        self.version = 'version 0.1.3'
        self.developed_by = 'Developed using BearLibTerminal'
        
        self.options = [
                "[[c]] continue",
                '[[n]] new game',
                '[[o]] options',
                '[[q]] quit']
        
        self.title_height = 1 if self.height <= 25 else self.height // 5

        self.title = self.calc_title()
        options_header_offset = self.title_height + len(self.title.split('\n'))
        self.options_height = self.calc_options_heights(options_header_offset, 3)

    def calc_title(self):
        if self.height <= 25:
            from .constants import GAME_TITLE_SHORT as game_title
        else:
            from .constatns import GAME_TITLE as game_title
        return game_title

    def calc_options_heights(self, header_offset, footer_offset):
        def calculate(option):
            half_height = total_height // 2
            quarter_height = total_height // 4
            return header_offset + half_height - quarter_height + option
        total_height = self.height - header_offset - footer_offset
        return [calculate(option * 2) for option in range(4)]

    def draw(self):
        term.clear()

        # title header -- multiplying space with title length to center title
        term.puts(
            center(' ' * (len(self.title.split('\n')[0])), self.width), 
            self.title_height, 
            self.title)

        # options
        length, option = longest(self.options)
        x = center(length - 2, self.width)

        for option, index in zip(self.options, range(len(self.options))):
            if index == self.index:
                option = "[color=#00FFFF]{}[/color]".format(option)
            term.puts(x, self.options_height[index], option)

        # FOOTER and VERSION
        term.puts(
            center(len(self.version), self.width), 
            self.height - 4, 
            self.version)

        term.puts(center(self.developed_by, self.width), 
            self.width - 2, 
            self.developed_by)

        term.refresh()
        code = term.read()

        # key (CNOQ, ENTER)
        if code == term.TK_C or (code == term.TK_ENTER and self.index == 0):
            # proceed = continue_game()
            self.ret = self.scene_child('continue_menu')
            self.proceed = False

        # key press on N or enter on NEW GAME
        elif code == term.TK_N or (code == term.TK_ENTER and self.index == 1):
            # proceed = start_new_game()
            self.ret = self.scene_child('start_menu')
            self.proceed = False

        # key press on O or enter on OPTIONS
        elif code == term.TK_O or (code == term.TK_ENTER and self.index == 2):
            # options()
            # height = update_start_screen() + len(self.title.split('\n'))
            # self.options_height = calc_option_heights(height, 3)
            self.ret = self.scene_child('options_menu')
            self.proceed = False

        # key press on Q or enter on QUIT
        elif code == term.TK_Q or (code == term.TK_ENTER and self.index == 3):
            self.proceed = False

        # KEYS (UP, DOWN)
        elif code in (term.TK_UP, term.TK_DOWN):
            if code == term.TK_UP:
                self.index -= 1
            else: 
                self.index += 1
            if not 0 <= self.index < len(self.options):
                self.index = max(0, min(self.index, len(self.options) - 1))

        elif code in (term.TK_CLOSE, term.TK_ESCAPE):
            self.ret = None
            self.proceed = False

class CreateName(Scene):
    pass

class Start(Scene):
    def __init__(self, width, height, title='start_menu'):
        super().__init__(width, height, title)

    def setup(self):
        self.shorten = self.height <= 25
        self.delim, self.row, self.row_bonus = "\n", 11, 11
        if self.shorten:
            self.delim, self.row, self.row_bonus= "", 5, 6
        
        self.col1, self.col2, self.col3 = 3, 26, 49

        self.inv_screen = -1
        self.race_index = 0
        self.class_index = 0
        self.gender_index = 0
        self.character_index = 0

        self.indices = [0, 0, 0]
        self.grid = [[3, 26, 48], 5]
        self.length = self.width // 2

        self.title = "Character Creation"
        self.help = "Press (?) for info on a selected race, subrace or class"

        # some helper objects used in character creation
        self.character = namedtuple("Character", "name gender_opt race_opt class_opt")
        equipment = namedtuple("Equipment", "hd nk bd ar hn lh rh lr rr wa lg ft")

        # return type
        self.player=namedtuple("Player",
            "name home gold stats gender gbonus race rbonus job \
            jbonus skills equipment inventory")

        # gender objects and options
        genders = namedtuple("Gender", "gender bonus")
        self.gender_options = [
            genders("Male", strings.MALE),
            genders("Female", strings.FEMALE),
        ]

        # race objects and options
        races = namedtuple("Race", "race location stats bonus gold skills eq")
        self.race_options = [
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

        # class objects and options
        classes = namedtuple("Class", "classes bonuses equipment")
        self.class_options = [
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
            total = strings.STATS(*(s + g for s, g in zip(strings.HUMAN, 
                                                          gbonus)))

        elif self.character_index == 1:
            total = strings.STATS(*(s + g + r for s, g, r in zip(stats, 
                                                                 gbonus, 
                                                                 rbonus)))
        else:
            total = strings.STATS(*(s + g + r + c for s, g, r, c in zip(stats,
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
            self.col2 + 10, 
            self.row + (11 if not self.shorten else 6), 
            strings._bon.format(
                *self.transform_values(gbonus), 
                delim=self.delim))

        # STATUS :- RACE BONUSES
        # if self.character_index > 0:
        term.puts(
            self.col2 + 14, 
            self.row + (11 if not self.shorten else 6), 
            strings._bon.format(
                *(self.transform_values(rbonus) if self.character_index > 0 
                else (0 for _ in range(6))),
                    delim=self.delim))
            
        # STATUS :- CLASS BONUSES
        term.puts(
            self.col2 + 18, 
            self.row + (11 if not self.shorten else 6), 
            strings._bon.format(
                *self.transform_values(cbonus) if self.character_index > 1
                else (0 for _ in range(6)),
                delim=self.delim))

        # EQUIPMENT and INVENTORY
        eq, inv = None, None
        if self.character_index > 1:

            eq, inv = self.form_equipment(req, ceq)
            # if var is -1 then shows eq else shows inv
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
                self.gender_index = modify(-1, self.gender_index, 2)

            elif self.character_index == 1:
                self.race_index = modify(-1, self.race_index, 5)

            elif self.character_index == 2:
                self.class_index = modify(-1, self.class_index, 5)

        elif code == term.TK_RIGHT:
            if self.character_index == 0:
                self.gender_index = modify(1, self.gender_index, 2)

            elif self.character_index == 1:
                self.race_index = modify(1, self.race_index, 5)

            elif self.character_index == 2:
                self.class_index = modify(1, self.class_index, 5)

        elif code == term.TK_UP:
            self.character_index = modify(-1, self.character_index, 4)
            if self.character_index <= 2:
                self.inv_screen = -1

        elif code == term.TK_DOWN:
            self.character_index = modify(1, self.character_index, 4)

        # Toggles V Key
        elif code == term.TK_V and self.character_index > 1:
            self.inv_screen *= -1

        # Randomize selection -- maybe remove since its more of a debugging usage
        elif code == term.TK_8:
            # only randomizes if shift-8 is pressed -- else it's just pressing 8
            if term.state(term.TK_SHIFT) and self.character_index <= 1:
                # lets not randomize if you've already selected a gender
                # its not much more effort to finish creating your character
                name = "Random name"
                self.gender_index = random.randint(0, 1)
                gender = self.gender_row(draw=False)
                self.race_index = random.randint(0, 4)
                race = self.race_row(draw=False)
                self.class_index = random.randint(0, 4)
                job = self.class_row(draw=False)
                eq, inv = self.form_equipment(race.eq, job.equipment)
                self.ret = output(
                        proceed=True,
                        value=self.player(
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
                self.proceed = False

        # ENTER
        elif code == term.TK_ENTER:
            if self.character_index == 3:
                name = new_name((race, occu))
                # print("CHARACTER NAME: {}".format(name.value))
                if name.proceed == 0:
                    gender = self.gender_row(draw=False)
                    race = self.race_row(draw=False)
                    job = self.class_row(draw=False)
                    self.ret = output(
                            proceed=True,
                            value=self.player(
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
                    self.proceed = False
            else:
                self.character_index += 1

        elif code in (term.TK_ESCAPE,):
            if term.state(term.TK_SHIFT):
                self.proceed = False
                self.ret = output(
                        proceed=False,
                        value="Exit to Desktop")

            elif self.character_index == 0:
                self.proceed = False
                self.ret = self.scene_parent('main_menu')

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
            # for option, index in zip(self.gender_options, range(len(self.gender_options))):
            for index, option in enumerate(self.gender_options):
                x, y = 24 + 22 * index, 5 if not self.shorten else 2
                gender = pad(option.gender, length=8)
                if index == self.gender_index:
                    if self.character_index == 0:
                        selected(x, y, gender)
                    else:
                        passed(x, y, gender)
                else:
                    unselected(x, y, gender)

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
                        selected(x, y, race)
                    elif self.character_index > 1:
                        passed(x, y, race)
                    else:
                        unselected(x, y, race)
                else:
                    unselected(x, y, race)

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
                        selected(x, y, option)
                    elif self.character_index > 2:
                        passed(x, y, option)
                    else:
                        unselected(x, y, option)
                else:
                    unselected(x, y, option)

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

    def form_equipment(self, req, ceq):
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

class Options(Scene):
    def __init__(self, width, height, title='options_menu'):
        super().__init__(width, height, title)

    def setup(self):
        self.option = Option("Options Screen")
        # 80x25 -> 8x16 | 80x50 -> 8x8 | 160x50 -> 16x16 | FullScreen -> 16x16
        self.option.add_opt("Screen Size", 
            ["80x25", "80x50", "160x50", "160x100"]) 
            
        # "Full Screen: {}x{}".format(sysize(0), sysize(1))])
        self.option.add_opt("Cell Size", ["Auto", "8x16", "8x8", "16x16"])

        self.option.add_opt("Font Choice", 
            ["Default", "Source", "Fira", "Fira-Bold", "IBM_CGA", "Andale", 
             "Courier", "Unscii-8", "Unscii-8-thin", "VeraMono"])

        self.option.add_opt("Coloring", 
            ["Dynamic", "Dark", "Light", "Colorblind"])
        
        self.prop = {
            'gx': term.state(term.TK_WIDTH),
            'gy': term.state(term.TK_HEIGHT),
            'cx': term.state(term.TK_CELL_WIDTH),
            'cy': term.state(term.TK_CELL_HEIGHT),            
        }
    
    def parse_screensize(self, p, screensize):
        if "Full Screen" in screensize:
            sx, sy = sysize(0)//term.state(term.TK_CELL_WIDTH), sysize(1)//term.state(term.TK_CELL_HEIGHT)
        else:
            sx, sy = list(map(lambda x: int(x), screensize.split('x')))
        if (p['gx'], p['gy']) != (sx, sy):
            p['gx'], p['gy'] = sx, sy
            return p, True
        return p, False

    def parse_cellsize(self, p, cellsize):
        if cellsize == "Auto":
            if p['cx'] != 'Auto':
                p['cx'], p['cy'] = "auto", None
                return p, True
        else:
            cx, cy = list(map(lambda x: int(x), cellsize.split('x')))
            if (p['cx'], p['cy']) != (cx, cy):
                p['cx'], p['cy'] = (cx, cy)
                return p, True
        return p, False

    def parse_fonts(self, p, font):
        if self.option == "Default":
            term.set('font: default, size={}{}'.format(
                p['cx'], 
                'x'+str(p['cy']) if p['cy'] != p['cx'] else ''))

        else:
            if p['cx'] == "auto":
                cy = 8 if font not in ("Andale, Courier, VeraMono") else 16
                term.set("font: ./fonts/{}.ttf, size={}{}".format(
                    font, 
                    8, cy)) 
            else:
                term.set("font: ./fonts/{}.ttf, size={}{}".format(
                    font, 
                    p['cx'], 
                    'x'+str(p['cy']) if p['cy'] != p['cx'] else ''))
            # p['cx'], p['cy'] = "auto", None
            self.reset_screen()

    def reset_screen(self):
        if self.prop['cx'] == "auto":
            term.set("window: size={}x{}, cellsize={}".format(
                self.prop['gx'],
                self.prop['gy'],
                self.prop['cx'],
            ))
        else:
            term.set("window: size={}x{}, cellsize={}x{}".format(*(v for _, v in self.prop.items())))
        term.refresh()        

    def draw(self):
        term.clear()

        # options title
        term.puts(center(self.option.title, term.state(term.TK_WIDTH)), 1, self.option.title)

        # options
        height = 3

        for index, opt in enumerate(self.option.opts):
            selected = index == self.option.optindex
            expanded = index in self.option.expand
            if selected:
                opt = ("[[-]] " if expanded else "[[+]] ") + "[c=#00ffff]{}[/c]".format(opt)
            else:
                opt = ("[[-]] " if expanded else "[[+]] ") + opt

            term.puts(term.state(term.TK_WIDTH)//5, height, opt)
            height += term.state(term.TK_HEIGHT)//25
            if expanded:
                for index, subopt in enumerate(self.option.subopts[index]):
                    if selected:
                        if index == self.option.suboptindex[self.option.optindex]:
                            subopt = "[c=#00ffff]{}[/c]".format(subopt)
                        else:
                             subopt = subopt
                    term.puts(term.state(term.TK_WIDTH)//4+3, height, subopt)
                    height += term.state(term.TK_HEIGHT)//25
            height += term.state(term.TK_HEIGHT)//25
        term.puts(term.state(term.TK_WIDTH)//5, height+1, "{}".format(term.state(term.TK_WIDTH)))
        term.puts(term.state(term.TK_WIDTH)//5, height+2, "{}".format(term.state(term.TK_HEIGHT)))
        term.puts(term.state(term.TK_WIDTH)//5, height+3, "{}".format(term.state(term.TK_CELL_WIDTH)))
        term.puts(term.state(term.TK_WIDTH)//5, height+4, "{}".format(term.state(term.TK_CELL_HEIGHT)))

        term.refresh()
        key = term.read()

        if key in (term.TK_CLOSE, term.TK_Q, term.TK_ESCAPE):
            self.option.reset_all()
            self.ret = self.parents
            self.proceed = False
        
        elif key == term.TK_ENTER:
            if self.option.optindex in self.option.expand:
                # action stuff
                if self.option.suboptindex[self.option.optindex] != -1:
                    if self.proceed:
                        print('SELECTED: {}|{}'.format(
                            self.option.opts[self.option.optindex], 
                            self.option.subopts[self.option.optindex][self.option.suboptindex[self.option.optindex]]))

                    if self.option.option() == "Screen Size":                       
                        self.prop, changed = self.parse_screensize(self.prop, self.option.suboption())
                        if changed:
                            self.reset_screen()
                    elif self.option.option() == "Cell Size":
                        self.prop, changed = self.parse_cellsize(self.prop, self.option.suboption())
                        if changed:
                            self.reset_screen()
                    elif self.option.option() == "Font Choice":
                        self.parse_fonts(self.prop, self.option.suboption())
                else:
                    self.option.collapse(self.option.optindex)
            else:
                self.option.expansion(self.option.optindex)
                # option.move_subpointer(1)

        # Arrow keys (UP | DOWN)
        elif key == term.TK_DOWN:
            if len(self.option.expand):
                self.option.move_subpointer(1)
                self.option.correct_subpointer()

            else:
                self.option.move_pointer(1)
                self.option.correct_pointer()

        elif key == term.TK_UP:
            if len(self.option.expand):
                self.option.move_subpointer(-1)
                self.option.correct_subpointer()

            else:
                self.option.move_pointer(-1)
                self.option.correct_pointer()

class Continue(Scene):
    def __init__(self, width, height, title='continue_menu'):
        super().__init__(width, height, title)

    def setup(self):
        pass

    def draw(self):
        pass

if __name__ == "__main__":
    term.open()
    setup_font('Ibm_cga', cx=8, cy=16)
    term.set('window: size=80x25, cellsize=auto, title="Spaceship", fullscreen=false')
    m = Main(80, 25)
    # m.setup()
    # m.run()
    s = Start(80, 25)
    # s.setup()
    # s.run()
    # print(s.ret)
    o = Options(80, 25)
    # o.setup()
    # o.run()
    c = Continue(80, 25)

    m.add_scene_child(o)
    m.add_scene_child(c)
    m.add_scene_child(s)

    s.add_scene_parent(m)
    o.add_scene_parent(m)
    c.add_scene_parent(m)

    print(m.children)
    print(o.parents)
    e = Engine(m)
    e.run()
    # print([child.title for child in m.children])

    # for scene in (s, c, o):
    #     print([p.title for p in scene.parents])
