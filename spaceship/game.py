import os
import sys
import shelve
import random
import textwrap
from collections import namedtuple
from bearlibterminal import terminal as term
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
from .setup_game import setup, setup_font, setup_menu, output, toChr
import spaceship.cc_strings as strings
from .classes.wild import wilderness
from .classes.player import Player
from .classes.world import World
from .screen_functions import *
from .gamelog import GameLogger
from .classes.city import City
from .classes.cave import Cave
from .action import commands_player
from .scene import Scene

def single_element(container):
    return len(container) == 1

class Level: GLOBAL, WORLD, LOCAL = -1, 0, 1
class Maps: CITY, CAVE, WILD, WORLD = range(4)

class Start(Scene):
    def __init__(self, sid='start_game'):
        super().__init__(scene_id=sid)

    def reset(self):
        self.turns = 0
        self.world = None
        self.player = None
        self.location = None
        self.waiting = False
        self.turn_inc = False
        self.do_action = False
        self.map_change = False
        self.gamelog = None

        self.reset_size()

    def test_run(self):
        self.ret['kwargs'] = {'player': {}, 'name': 'rando'}

    def setup(self):
        # self.reset()
        self.actions = {
            0: {
                '@': self.draw_player_screens,
                'i': self.draw_player_screens,
                'v': self.draw_player_screens,
                'S': self.action_save,
                '>': self.action_enter_map,
            },
            1: {
                '@': self.draw_player_screens,
                'i': self.draw_player_screens,
                'v': self.draw_player_screens,
                '<': self.action_interact_stairs_up,
                '>': self.action_interact_stairs_down,
                'c': self.action_interact_door_close,
                'o': self.action_interact_door_open,
                'd': self.action_interact_item_drop,
                'u': self.action_interact_item_use,
            },
        }

        self.pass_item_messages = [
            "You pass by an item.",
            "There is something here."
            "Your feet touches an object."
        ]
        self.string_drop = 'Which item to drop?'
        self.string_use = 'Which item to use?'

        # player screen variables
        self.player_screen_col, self.player_screen_row = 1, 3
        self.player_status_col, self.player_status_row = 1, 2
        self.display_offset_x, self.display_offset_y = 14, 0
        self.log_width, self.log_height = self.width, 2
        self.display_width = self.width - self.display_offset_x
        self.display_height = self.height - self.log_height

    def run(self):  
        # self.reset_size()
        self.reset()
        if isinstance(self.ret['kwargs']['player'], Player):
            self.player = self.ret['kwargs']['player']
            self.world = self.ret['kwargs']['world']
            self.turns = self.ret['kwargs']['turns']

        else:
            player = self.ret['kwargs']['player']
            name = self.ret['kwargs']['name']
            self.player = Player(player, name)
            self.location = self.world = World(
                map_name="Calabston", 
                map_link="./assets/worldmap.png")

        self.gamelog = GameLogger(
            screenlinelimit=3 if self.height <= 25 else 4,
            footer="_" + self.player.name + "_" + self.player.job)

        while self.proceed and self.player.is_alive:
            self.draw()
        
        self.proceed = True
        if hasattr(self, 'ret'):
            return self.ret

    def draw(self):
        term.clear()
        self.draw_log(refresh=False)
        self.draw_player_status()

        if self.map_change:
            self.determine_map_location()

        # print(list(u.__class__.__name__ for u in self.location.units))
        # print(self.location.__class__.__name__)
        # print(self.player.position)

        self.draw_world()
        term.refresh()


        # units = list(self.location.units)

        # units.append(self.player)

        # self.process_player_turn()
        if isinstance(self.location, World):
            self.process_player_turn()
        else:
            for unit in self.location.units:
                self.unit = unit
                if self.unit.energy.ready():
                    self.unit.energy.reset()
                    self.process_unit_turn()
                else:
                    self.unit.energy.gain_energy()

            if self.player.energy.ready():
                self.process_player_turn()
            else:
                self.player.energy.gain_energy()

    def draw_log(self, log=None, refresh=True):
        if log:
            self.gamelog.add(log)

        term.clear_area(
            0, 
            self.height - self.log_height - 1, 
            self.width, 
            self.log_height)

        for index, message in enumerate(self.gamelog.write().messages):
            term.puts(
                x=1,
                y=self.height + index - self.log_height - 1,
                s=message[1])
        
        if refresh:
            term.refresh()

    def draw_world(self):
        x, y = self.player.position if self.player.height >= 1 \
            else self.player.location

        g0 = isinstance(self.location, World)
        if g0:
            sight = round(self.player.sight / 1.5)
        else:
            sight = self.player.sight * (2 if isinstance(self.location, City)
                                                                        else 1)
        self.location.fov_calc([(x, y, sight)])

        for x, y, col, ch in self.location.output(x, y):
            term.puts(
                x=x + self.display_offset_x,
                y=y + self.display_offset_y,
                s="[c={}]{}[/c]".format(col, ch))

        # sets the location name at the bottom of the status bar
        if g0:
            location = None
            if self.player.location in self.world.enterable_legend.keys():
                location = self.world.enterable_legend[self.player.location]
            elif self.player.location in self.world.dungeon_legend.keys():
                location = self.world.dungeon_legend[self.player.location]

            if location:
                term.bkcolor('grey')
                term.puts(
                    x=self.display_offset_x, 
                    y=0, 
                    s=' ' * (self.width - self.display_offset_x))
                    
                term.bkcolor('black')
                location_offset = center(text=surround(location), 
                                        width=self.width - self.display_offset_x)
                term.puts(
                    x=self.display_offset_x + location_offset,
                    y=0, 
                    s=surround(location))

    def draw_player_status(self):
        col, row = self.player_status_col, self.player_status_row
        term.puts(col, row - 1, self.player.name)
        term.puts(col, row + 0, self.player.gender)
        term.puts(col, row + 1, self.player.race)
        term.puts(col, row + 2, self.player.job)

        term.puts(col, row + 4, "LVL: {:>6}".format(self.player.level))
        term.puts(col, row + 5, "EXP: {:>6}".format("{}/{}".format(
            self.player.exp, 
            self.player.advexp)))
        term.puts(col, row + 7, "HP:  {:>6}".format("{}/{}".format(
            self.player.cur_health, 
            self.player.max_health)))
        term.puts(col, row + 8, "MP:  {:>6}".format("{}/{}".format(
            self.player.mp, 
            self.player.total_mp)))
        term.puts(col, row + 9, "SP:  {:>6}".format(self.player.sp))

        term.puts(col, row + 11, "STR: {:>6}".format(self.player.str)) 
        term.puts(col, row + 12, "CON: {:>6}".format(self.player.con))
        term.puts(col, row + 13, "DEX: {:>6}".format(self.player.dex))
        term.puts(col, row + 14, "INT: {:>6}".format(self.player.int))
        term.puts(col, row + 15, "WIS: {:>6}".format(self.player.wis))
        term.puts(col, row + 16, "CHA: {:>6}".format(self.player.cha))

        term.puts(col, row + 18, "GOLD:{:>6}".format(self.player.gold))

        # Turn status
        term.puts(1, self.height - 4, 'Turns: {:<4}'.format(self.turns))

        # elif self.player.location in self.world.dungeon_legend.keys():
        #     location = self.world.dungeon_legend[self.player.location]

        # else:
        #     location = ""

        # term.puts(col, row + 20, "{}".format(location))

    def draw_player_profile(self):
        '''Handles player profile screen'''
        # draws header border
        for i in range(self.width):
            term.puts(i, 1, '#')
        term.puts(center('profile  ', self.width), 1, ' Profile ')

        for colnum, column in enumerate(list(self.player.profile())):
            term.puts(
                x=self.player_screen_col + (20 * colnum), 
                y=self.player_screen_row, 
                s=column)

    def draw_player_equipment(self):
        '''Handles equipment screen'''
        # draws header border
        for i in range(self.width):
            term.puts(i, 1, '#')
        term.puts(center(' Equipment ', self.width), 1, ' Equipment ')
        
        # for index, (part, item) in enumerate(self.player.equipment()):
        #     letter = chr(ord('a') + index)
        #     body_part = ".  {:<10}: ".format(part)
        #     item_desc = item.__str__() if item else ""

        for index, (body_part, item_desc) in enumerate(list(self.player.equipment)):
            letter = chr(ord('a') + index)
            term.puts(
                x=self.player_screen_col,
                y=self.player_screen_row + index * (2 if self.height > 25 else 1),
                s=letter + body_part + item_desc)

    def draw_player_inventory(self):
        '''Handles inventory screen'''
        # draws header border for the backpack
        for i in range(self.width):
            term.puts(i, 1, '#')
        term.puts(center('backpack  ', self.width), 1, ' Backpack ')

        for index, item in enumerate(self.player.inventory):
            letter = chr(ord('a') + index) + ". "
            item_desc = item.__str__() if item else ""

            term.puts(
                x=self.player_screen_col,
                y=self.player_screen_row + index * (2 if self.height > 25 else 1),
                s=letter + item_desc)
    
    def draw_player_eq_inv_switch(self):
        term.puts(
            x=center('press v to switch to inventory', self.width), 
            y=self.height - 2,
            s='press v to switch to inventory')

    def draw_player_inv_eq_switch(self):
        term.puts(
            x=center('press i to switch to equipment', self.width), 
            y=self.height - 2,
            s='press i to switch to equipment')

    def draw_player_eq_drop(self):
        term.puts(
            x=center(self.string_drop, self.width),
            y=self.height - 2,
            s=self.string_drop)
        
    def draw_player_eq_use(self):
        term.puts(
            x=center(self.string_use, self.width),
            y=self.height - 2,
            s=self.string_use)

    def draw_player_screens(self, key):
        playscreen = False
        current_screen = key
        current_range = 0

        while True:
            term.clear()

            if current_screen == "i":
                self.draw_player_equipment()
                self.draw_player_eq_inv_switch()
            elif current_screen == "v":
                self.draw_player_inventory()
                self.draw_player_inv_eq_switch()
            else:
                self.draw_player_profile()

            term.refresh()
            code = term.read()

            if code in (term.TK_ESCAPE,):
                if current_screen == 1:
                    current_screen = 0
                else:
                    break

            elif code == term.TK_I:
                current_screen = 'i'

            elif code == term.TK_V:
                # V goes to inventory screen
                current_screen = 'v'
            
            elif code == term.TK_2 and term.state(term.TK_SHIFT):
                # @ goes to profile
                current_screen = '@'

            elif code == term.TK_UP:
                if current_range > 0: current_range -= 1

            elif code == term.TK_DOWN:
                if current_range < 10: current_range += 1
        term.clear()

    def process_player_turn(self):
        action = self.key_input()
        if not self.proceed:
            return
        self.process_handler(*action)

    def process_unit_turn(self):
        if hasattr(self.unit, 'acts'):
            positions = self.location.fov_calc_blocks(
                                                self.unit.x, 
                                                self.unit.y, 
                                                self.unit.sight)
            tiles = { position: self.location.square(*position) 
                                                for position in positions }
            units = { u.position: u for u in self.location.units 
                                                if u != self.unit }
            action = self.unit.acts(self.player, tiles, units)
            print('AI ACTION: ', action)
            if action:
                self.process_handler_unit(*action)

            if not self.player.is_alive:
                self.process = False
                return
            
    def process_handler_unit(self, x, y, k, key):
        if k is not None:
            pass
        elif all(z is not None for z in [x, y]):
            self.process_movement_unit(x, y)
        else:
            return 'skipped-turn'

    def process_handler(self, x, y, k, key,):
        '''Checks actions linearly by case:
        (1) processes non-movement action
            Actions not in movement groupings
        (2) processes movement action
            Keyboard shortcut action grouping
        (3) If action teplate is empty:
            Return skip-action command
        '''
        if k is not None:
            self.process_action(k)
        elif all(z is not None for z in [x, y]):
            self.process_movement(x, y)
        else:
            return 'skipped-turn'

    def process_action(self, action):
        ''' 
        Player class should return a height method and position method
        Position method should return position based on height
        So height would be independent and position would be depenedent on height
        '''
        try:
            divided = self.actions[max(0, min(self.player.height, 1))]
            try:
                divided[action]()
            except TypeError:
                divided[action](action)
            except KeyError:
                invalid_command = "'{}' is not a valid command".format(action)
                self.draw_log(invalid_command)        
        # except TypeError:
        #     print('te')
        #     self.actions[max(0, min(self.player.height, 1))][action](action)

        except KeyError:
            invalid_command = "'{}' is not a valid command".format(action)
            self.draw_log(invalid_command)

    def process_move_unit_to_empty(self):
        occupied_player = self.player.position == (tx, ty)
        occupied_unit = self.location.occupied(tx, ty)
        print(occupied_player, occupied_unit)
        if not occupied_player and not occupied_unit:
            self.unit.move(x, y)
        return occupied_player, occupied_unit

    def process_movement_unit(self, x, y):
        print('unit processing')
        if (x, y) != (0, 0):
            tx = self.unit.x + x
            ty = self.unit.y + y

            if self.location.walkable(tx, ty):
                unit_bools = self.process_move_unit_to_empty()
                if not unit_values:
                    return
                else:
                    occupied_player, occupied_unit = unit_bools
                    if occupied_unit:
                        unit = self.location.unit_at(tx, ty)
                    else:
                        unit = self.player
                    player = isinstance(unit, Player)

                    if not player and unit.friendly:
                        unit.move(-x, -y)
                        self.unit.move(x, y)
                        log = "The {} switches places with the {}".format(
                            self.unit.__class__.__name__, unit.race)
                        self.draw_log(log) 
                    else:
                        chance = self.unit.calculate_attack_chance()
                        if chance == 0:
                            log = "The {} tries attacking {} but misses".format(
                                self.unit.race, 
                                "you" if player else "the " + unit.race)
                            self.draw_log(log)
                        else:
                            damage = self.unit.calculate_attack_damage()
                            if chance == 2:
                                damage *= 2
                            unit.cur_health -= damage
                            log = "The {} attacks {} for {} damage".format(
                                self.unit.race,
                                "you" if player else "the " + unit.race,
                                damage)
                            self.draw_log(log)
                            if not unit.is_alive:
                                log = "The {} has killed {}!".format(
                                    self.unit.race,
                                    "you" if player else "the " + unit.race)
                                self.draw_log(log)
                                if player:
                                    print('YOU DIED -> GOTO EXIT')
                                    exit('DEAD')
                                item = unit.drops()
                                if item:
                                    self.location.item_add(item)
                                    self.draw_log("The {} has dropped {}".format(
                                        unit.race, item.name))
                                self.location.unit_remove(unit)
                            term.puts(
                                x=tx + self.display_offset_x, 
                                y=ty + self.display_offset_y, 
                                s='[c=red]*[/c]')
                            term.refresh()
            else:
                term.puts(
                    x=tx + self.display_offset_x, 
                    y=ty + self.display_offset_y, 
                    s='[c=red]X[/c]')
                term.refresh()
                            
    def process_movement(self, x, y):
        turn_inc = 0
        if  self.player.height == Level.WORLD:
            if (x, y) == (0, 0):
                self.draw_log("You wait in the area")
                turn_inc = True
            else:
                tx = self.player.wx + x
                ty = self.player.wy + y

                if self.location.walkable(tx, ty):
                    self.player.save_location()
                    self.player.travel(x, y)
                    turn_inc = True
                else:
                    travel_error = "You cannot travel there"
                    self.draw_log(travel_error)
        else:
            if (x, y) == (0, 0):
                self.draw_log("You rest for a while")
                turn_inc = True
            else:
                tx = self.player.x + x
                ty = self.player.y + y

                if self.location.walkable(tx, ty):
                    if not self.location.occupied(tx, ty):
                        self.player.move(x, y)
                        msg_chance = random.randint(0, 5)
                        if self.location.square(tx, ty).items and msg_chance:
                            item_message = random.randint(
                                a=0, 
                                b=len(self.pass_item_messages) - 1)
                            self.draw_log(self.pass_item_messages[item_message])
                        turn_inc = True
                    else:
                        unit = self.location.unit_at(tx, ty)
                        if unit.friendly:
                            unit.move(-x, -y)
                            self.player.move(x, y)
                            log = "You switch places with the {}".format(
                                                                    unit.race)
                            self.draw_log(log)
                        else:
                            chance = self.player.calculate_attack_chance()
                            if chance == 0:
                                log = "You try attacking the {} but miss".format(
                                    unit.race)
                                self.draw_log(log)
                            else:
                                damage = self.player.calculate_attack_damage()
                                # if chance returns crit ie. a value of 2 
                                # then multiply damage by 2
                                if chance == 2:
                                    damage *= 2
                                unit.cur_health -= damage

                                log = "You{}attack the {} for {} damage. ".format(
                                    " crit and " if chance == 2 else " ", 
                                    unit.race, 
                                    damage)

                                if unit.cur_health < 1:
                                    log = "You have killed the {}! ".format(
                                        unit.race)
                                    log += "You gain {} exp.".format(unit.xp)
                                    self.draw_log(log)
                                    self.player.gain_exp(unit.xp)

                                    if self.player.check_exp():
                                        log = "You level up. You are now level {}.".format(
                                            self.player.level)
                                        log += " You feel much stronger now."
                                        self.draw_log(log)

                                    item = unit.drops()

                                    if item:
                                        self.location.square(*unit.position).items.append(item)
                                        self.draw_log("The {} has dropped {}".format(
                                            unit.race, 
                                            item.name))

                                    self.location.unit_remove(unit)

                                else:
                                    log += "The {} has {} health left".format(
                                        unit.race, 
                                        max(0, unit.cur_health))
                                    self.draw_log(log, refresh=False)
                                    term.puts(
                                        x=tx + self.display_offset_x, 
                                        y=ty + self.display_offset_y, 
                                        s='[c=red]*[/c]')
                                    term.refresh()

                        turn_inc = True
                else:
                    if self.location.out_of_bounds(tx, ty):
                        self.draw_log("You reached the edge of the map")
                    else:
                        walkChars = {
                            "=": "furniture",
                            "+": "a door",
                            "/": "a door",
                            "o": "a lamp",
                            "#": "a wall",
                            "x": "a post",
                            "~": "a river",
                            "T": "a tree",
                            "f": "a tree",
                            "Y": "a tree",
                            "%": "a wall",
                        }
                        ch = self.location.square(tx, ty).char
                        if ch == "~":
                            self.draw_log("You cannot swim")
                        else:
                            self.draw_log("You walk into {}".format(
                                walkChars[ch]),
                                refresh=False)
                            term.puts(
                                x=tx + self.display_offset_x, 
                                y=ty + self.display_offset_y, 
                                s='[c=red]X[/c]')
                            term.refresh()

    def key_input(self):
        '''Handles keyboard input and keypress transformation
        Cases:
            Skips any pre-inputs and non-read keys
            if key read is a close command -- close early or set proceed to false
            Elif key is valid command return the command from command list with continue
            Else return invalid action tuple with continue value
        '''
        action = tuple(None for _ in range(4))

        key = term.read()
        while key in (term.TK_SHIFT, term.TK_CONTROL, term.TK_ALT):
            # skip any non-action keys
            key = term.read()
            
        shifted = term.state(term.TK_SHIFT)
        if key in (term.TK_ESCAPE, term.TK_CLOSE):
            # exit command -- maybe need a back to menu screen?
            if shifted:
                exit('Early Exit')
            elif self.player.height >= Level.WORLD:
                self.draw_log('Escape key disabled.')
            else:
                self.ret['scene'] = 'main_menu'
                self.proceed = False

        try:
            # discover the command and set as current action
            action = commands_player[(key, shifted)]
        except KeyError:
            pass

        return action

    def spaces(self, x, y, exclusive=True):
        space = namedtuple("Space", ("x","y"))
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if (dx, dy) == (0, 0) and exclusive:
                    continue
                else:
                    yield space(x + dx, y + dy)

    def action_save(self):
        self.draw_log("Save and exit game? (Y/N)")
        
        # User input -- confirm selection
        code = term.read()
        if code != term.TK_Y:
            return

        if not os.path.isdir('saves'):
            os.makedirs('saves')
            log = 'saved folder does not exist - creating folder: "./saves"'
            self.draw_log(log)

        # prepare strings for file writing
        # player_hash used for same name / different character saves
        desc = self.player.desc
        file_path = './saves/{}'.format(desc)
        
        with shelve.open(file_path, 'n') as save_file:
            save_file['desc'] = desc
            save_file['player'] = self.player
            save_file['world'] = self.world
            save_file['turns'] = self.turns  

        self.proceed = False  
        self.ret['scene'] = 'main_menu'
        self.reset()

    def determine_map_location(self):
        if self.player.height == Level.WORLD:
            self.location = self.world
        
        else:
            self.location = self.world.location(*self.player.location)
            if self.player.height > 1:
                for i in range(self.player.height - 1):
                    self.location = self.location.sublevel

        self.map_change = False

    def determine_map_on_enter(self, map_type):
        '''Helper function to determine type of wilderness map'''
        try:
            return wilderness[map_type]
        except KeyError:
            raise ValueError("Map Type Not Implemented: {}".format(map_type))

    def determine_map_enterance(self, x, y, location):
        '''Helper function to determine start position when entering wild'''
        return (max(int(location.width * x - 1), 0), 
                max(int(location.height * y - 1), 0))

    def action_enter_map(self):
        if not self.world.location_exists(*self.player.location):
            if self.player.location in self.world.enterable_legend.keys():
                fileloc = self.world.enterable_legend[self.player.location]
                fileloc = fileloc.replace(' ', '_').lower()
                img_name = "./assets/maps/" + fileloc + ".png"
                cfg_name = "./assets/maps/" + fileloc + ".cfg"

                location = City(
                    map_id=fileloc,
                    map_img=img_name,
                    map_cfg=cfg_name,
                    width=self.width, 
                    height=self.height)

                # on cities enter map in the middle
                self.player.position = location.width // 2, location.height // 2
            
            elif self.player.location in self.world.dungeon_legend.keys():
                # map type should be a cave
                location = Cave(
                    width=self.width,
                    height=self.height,
                    max_rooms=random.randint(15, 20))

                self.player.position = location.stairs_up

            else:
                # map type should be in the wilderness
                tile = self.world.square(*self.player.location)
                # neighbors = world.access_neighbors(*player.location)
                location = self.determine_map_on_enter(tile.tile_type)(
                    width=self.width,
                    height=self.height)

                x, y = self.player.get_position_on_enter()
                self.player.position = self.determine_map_enterance(x, y, location)

            location.parent = self.world
            self.world.location_create(*self.player.location, location)

        else:
            # location already been built -- retrieve from world map_data
            # player position is different on map enter depending on map location
            location = self.world.location(*self.player.location)
            if self.player.location in self.world.enterable_legend.keys():
                # re-enter a city
                self.player.position = location.width // 2, location.height // 2

            elif self.player.location in self.world.dungeon_legend.keys():
                # re-enter dungeon
                self.player.position = location.stairs_up

            else:
                # reenter a wilderness
                x, y = self.player.get_position_on_enter()
                self.player.position = self.determine_map_enterance(x, y, location)
                
        self.player.move_height(1)
        self.map_change = True

    def action_interact_stairs_down(self):
        if self.player.position == self.location.stairs_down:
            if not self.location.sublevel:
                location = Cave(
                    width=self.width,
                    height=self.height,
                    max_rooms=random.randint(15, 20))
                
                self.location.sublevel = location
                location.parent = self.location

            self.location = self.location.sublevel
            self.player.move_height(1)
            self.player.position = self.location.stairs_up
        else:
            self.draw_log('You cannot go downstairs without stairs')

    def action_interact_stairs_up(self):
        def move_upstairs(reset=False):
            self.location = self.location.parent
            self.player.move_height(-1)

            if reset:
                self.player.position = self.location.sublevel

        if self.player.location in self.world.enterable_legend.keys():
            move_upstairs()

        elif self.world.location_is(*self.player.location, 2):
            move_upstairs()

        elif self.player.position == self.location.stairs_up:
            move_upstairs(reset=True)

        else:
            self.draw_log('You cannot go upstairs without stairs')

        if isinstance(self.location, World):
            self.player.position = (0, 0)

    def action_interact_door_close(self):
        def close_door(x, y):
            self.draw_log('Closing door.', refresh=False)
            term.puts(
                x=x + self.display_offset_x, 
                y=y + self.display_offset_y, 
                s="[c=red]+[/c]")
            term.refresh()
            self.location.close_door(x, y)

        doors = []
        px, py = self.player.position
        for x, y in self.spaces(*self.player.position):
            if (x, y) != (px, py):
                try:
                    if self.location.square(x, y).char == '/':
                        doors.append((x, y))

                except IndexError:
                    self.draw_log('Out of bounds ({}, {})'.format(x, y))

        if not doors:
            self.draw_log('No open doors next to you')

        elif single_element(doors):
            close_door(*doors.pop())

        else:
            self.draw_log("There is more than one door near you. Which door?")

            code = term.read()
            shifted = term.state(term.TK_SHIFT)

            try:
                dx, dy, _, act = commands_player[(code, shifted)]

            except:
                raise
                self.draw_log("Invalid direction. Canceled closing door.")

            else:
                if act == "move" and (px + dx, py + dy) in doors:
                    close_door(px + dx, py + dy)

                else:
                    self.draw_log("Direction has no door. Canceled closing door.")
    def action_interact_door_open(self):
        def open_door(x, y):
            self.draw_log('Opening door.')
            term.puts(
                x=x + self.display_offset_x, 
                y=y + self.display_offset_y, 
                s="[c=red]+[/c]")
            term.refresh()
            self.location.open_door(x, y)

        doors = []
        px, py = self.player.position
        for x, y in self.spaces(*self.player.position):
            if (x, y) != (px, py):
                try:
                    if self.location.square(x, y).char == "+":
                        doors.append((x, y))
                        
                except IndexError:
                    self.draw_log('Out of bounds ({}, {})'.format(x, y))
        
        if not doors:
            self.draw_log('No closed doors next to you.')

        elif single_element(doors):
            open_door(*doors.pop())

        else:
            log = "There is more than one closed door near you. Which door?"
            self.draw_log(log)

            code = term.read()
            shifted = term.state(term.TK_SHIFT)

            try:
                dx, dy, _, act = commands_player[(code, shifted)]
                    
            except:
                self.draw_log("Invalid direction. Canceled opening door.")

            else:
                if act == "move" and (px + dx, py + dy) in doors:
                    open_door(px + dx, py + dy)

                else:
                    self.draw_log("Direction has no door. Canceled opening door.")

    def action_interact_unit_attack_melee(self):
        pass

    def action_interact_unit_attack_ranged(self):
        pass

    def action_interact_unit_displace(self):
        pass

    def action_interact_item_pickup(self, x, y):
        def pickup_item(item):
            if len(self.player.inventory) >= 25:
                gamelog.add("Backpack is full. Cannot pick up {}".format(item))

            else:
                self.location.item_remove(item)
                self.player.inventory_item_add(item)
                log = "You pick up {} and place it in your backpack".format(
                                                                    item.name)
                self.draw_log(log)
                self.draw_log("Your backpack feels heavier")
                self.turn_inc = true
        
        items = self.location.square(x, y).items
        if not items:
            self.draw_log('No items on the ground where you stand')

        elif single_element(items):
            pickup_item(item)

        else:
            print('Multiple item pickup screen')

    def action_interact_item_drop(self):
        def drop_item(item):
            pass
        # open up inventory
        while True:
            term.clear()
            self.draw_player_inventory()
            self.draw_player_eq_drop()
            term.refresh()

            items = list(self.player.inventory)
            print(items)

            code = term.read()
            if code in (term.TK_ESCAPE, term.TK_Q):
                break

    def action_interact_item_use(self):
        while True:
            term.clear()
            self.draw_player_inventory()
            self.draw_player_eq_use()
            term.refresh()
            
            items = list(self.player.inventory)
            print(items)

            code = term.read()
            if code in (term.TK_ESCAPE, term.TK_Q):
                break
    
            

if __name__ == "__main__":
    s = Start()
    s.run()

