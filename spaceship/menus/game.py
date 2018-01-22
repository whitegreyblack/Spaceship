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
from .scene import Scene
from screen_functions import *
from action import commands_player
from gamelog import GameLogger
from ..classes.item import Ring, Potion, Armor, Weapon, sort
from ..classes.wild import wilderness
from ..classes.player import Player
from ..classes.world import World
from ..classes.city import City
from ..classes.cave import Cave

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

    def setup(self):
        # self.reset()
        self.actions = {
            0: {
                # '@': self.draw_screens,
                'q': self.draw_screens,
                'v': self.draw_screens,
                'S': self.action_save,
                '>': self.action_enter_map,
            },
            1: {
                # '@': self.draw_screens,
                'q': self.draw_screens,
                'v': self.draw_screens,
                '<': self.action_stairs_up,
                '>': self.action_stairs_down,
                'c': self.action_door_close,
                'o': self.action_door_open,
                ',': self.action_item_pickup,
                'd': self.action_item_drop,
                'u': self.action_item_use,
                'e': self.action_item_eat,
                't': self.action_unit_talk,
            },
        }

        # player screen variables
        self.row_spacing = 2 if self.height > 25 else 1
        self.screen_col, self.screen_row = 1, 3
        self.status_col, self.status_row = 0, 1
        self.main_x, self.main_y = 14, 0
        self.log_width, self.log_height = self.width, 2
        self.main_width = self.width - self.main_x
        self.main_height = self.height - self.log_height

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
                map_link="./spaceship/assets/worldmap.png")
            self.world.units_add([self.player])

        self.gamelog = GameLogger(
            width=self.width,
            screenlinelimit=3 if self.height <= 25 else 4,
            footer="_" + self.player.name + "_" + self.player.job)

        while self.proceed and self.player.is_alive:
            self.draw()
            self.process_units()
            if self.map_change:
                self.determine_map_location()

        self.proceed = True
        if hasattr(self, 'ret'):
            return self.ret

    def draw(self):
        term.clear()
        self.draw_log(refresh=False)
        self.draw_status()
        self.draw_world()
        term.refresh()

    def clear_log(self):
        term.clear_area(
            0, 
            self.height - self.log_height - 1, 
            self.width, 
            self.log_height + 1)

    def draw_log(self, log=None, color="white", refresh=True):
        if log:
            self.gamelog.add(log, color=color)

        self.clear_log()
        
        messages = self.gamelog.write()

        for index, msg in enumerate(messages):
            term.puts(
                x=1,
                y=self.height + index - self.log_height - 1,
                s="[c={}]{}[/c]".format(msg.color, msg.message))
        
        if refresh:
            term.refresh()

    def draw_world(self):
        '''Handles drawing of world features and map'''
        x, y = self.player.position if self.player.height >= 1 \
            else self.player.location

        g0 = isinstance(self.location, World)

        if g0:
            sight = self.player.sight_world

        elif isinstance(self.location, City):
            sight = self.player.sight_city

        else:
            sight = self.player.sight_norm

        self.location.fov_calc([(x, y, sight)])
        # self.location.fov_calc([(x, y, sight), (5, 5, sight)])

        for x, y, col, ch in self.location.output(x, y):
            term.puts(
                x=x + self.main_x,
                y=y + self.main_y,
                s="[c={}]{}[/c]".format(col, ch))

        # sets the location name at the bottom of the status bar
        if g0:
            location = None

            if self.player.location in self.world.enterable_legend.keys():
                location = self.world.enterable_legend[self.player.location]

            elif self.player.location in self.world.dungeon_legend.keys():
                location = self.world.dungeon_legend[self.player.location]

            if location:
                term.bkcolor('dark grey')
                term.puts(
                    x=self.main_x, 
                    y=0, 
                    s=' ' * (self.width - self.main_x))
                    
                term.bkcolor('black')
                location_offset = center(
                                    text=surround(location), 
                                    width=self.width - self.main_x)
                term.puts(
                    x=self.main_x + location_offset,
                    y=0, 
                    s=surround(location))

    def draw_screen_header(self, header=None):
        '''Draws a line across the top of the window'''
        term.bkcolor('dark grey')
        for i in range(self.width - self.main_x):
            term.puts(self.main_x + i, 0, ' ')
        term.bkcolor('black')
        if header:
            string = surround(header)
            term.puts(
                center(string, self.width + self.main_x), 0, string)
                
    def draw_status(self):
        '''Handles player status screen'''
        term.puts(self.status_col, self.status_row,
            strings.status.format(
                *self.player.status(), self.turns))

    def draw_profile(self):
        '''Handles player profile screen'''

        # draws header border
        for i in range(self.width):
            term.puts(i, 0, '#')
        term.puts(center('profile  ', self.width), 0, ' Profile ')

        for colnum, column in enumerate(list(self.player.profile())):
            term.puts(
                x=self.screen_col + (20 * colnum), 
                y=self.screen_row, 
                s=column)

    def clear_main(self):
        term.clear_area(
            self.main_x, 
            0, 
            self.width - self.main_x,
            self.height - self.log_height - 1)

    def clear_item_box(self):
        term.clear_area(
            self.width // 2, 
            2, 
            self.width // 2, 
            self.height - 5)

    def draw_equipment(self):
        '''Handles equipment screen'''

        # draws header border
        self.draw_screen_header('Equipment')

        equipment = list(self.player.equipment)

        for index, (part, item) in enumerate(equipment):
            if item:
                item = item.__str__()
            else:
                item = ""

            body = ". {:<10}: ".format(
                part.replace("eq_", "").replace("_", " "))

            letter = chr(ord('a') + index)
            term.puts(
                x=self.screen_col + self.main_x,
                y=self.screen_row + index * self.row_spacing,
                s=letter + body + item)

    def draw_item_header(self, item_header):
        '''Handles drawing of the item grouping header'''
        term.puts(
            x=self.screen_col + self.main_x,
            y=self.screen_row + self.index_row * self.row_spacing,
            s=item_header)
        self.index_row += 1

    def draw_item_row(self, item_desc):
        '''Handles drawing the list of an item group to the screen'''
        letter = chr(ord('a') + self.item_row) + ". "
        term.puts(
            x=self.screen_col + self.main_x,
            y=self.screen_row + self.index_row * self.row_spacing,
            s=letter + item_desc) 
        self.index_row += 1
        self.item_row += 1

    def draw_item_grouping(self, header, container):
        '''Handler to determine if we need to draw items or not'''
        if container:
            self.draw_item_header("   __" + header + "__")
            for element in container:
                self.draw_item_row(element.__str__())
            self.index_row += 1

    def draw_inventory(self, items, string=strings.cmd_inv_none):
        '''Handles drawing of the inventory screen along with the specific 
        groupings of each item type and their modification effects
        '''
        # keep track of items and row index
        self.item_row = 0
        self.index_row = 0

        # header for inventory
        self.draw_screen_header('Inventory')

        if not items:
            term.puts(
                x=center(string, self.width - self.main_x) + self.main_x,
                y=3,
                s=string)

        else:
            for header, items in list(sort(items).items()):
                self.draw_item_grouping(header, items)

    def draw_pickup(self, items):
        self.draw_screen_header('Pickup Items')
        for group, items in sort(items).items():
            if group not in 'food others'.split():
                group = list(group + 's')
                group[0] = group[0].upper()
                group = "".join(group)
            self.draw_item_grouping(group, items)

    def draw_inventory_by_group(self, items, part):
        '''Handles drawing of the inventory screen along with the specific 
        item type and their modification effects
        '''
        pass

    def draw_unequip_confirm(self, item):
        string = strings.cmd_unequip_confirm.format(item)
        term.puts(x=center(string, self.width), y=self.height - 5, s=string)
# 
    def draw_screen_log(self, log):
        self.clear_screen_log()
        term.puts(
            x=center(
                log, 
                self.width - self.main_x) + self.main_x, 
                y=self.height - 5, 
                s=log)

    def clear_screen_log(self):
        term.clear_area(
            self.main_x, 
            self.height - 5, 
            self.width - self.main_x, 
            2)

    def draw_item_border(self):
        term.bkcolor('dark grey')
        for y in (2, self.height - 5):
            term.puts(
                x=self.width // 2 + 1, 
                y=y, 
                s=' ' * (self.width // 2 - 2))
        
        for x in (self.width // 2 + 1, self.width - 2):
            for y in range(self.height - 7):
                term.puts(x, y + 2, ' ')
        term.bkcolor('black')
        
    def draw_screens(self, key):

        def unequip_item(code):
            nonlocal log, update_status
            string = strings.cmd_unequip_confirm.format(item)
            term.puts(x=center(string, self.width), y=self.height - 5, s=string)
            term.refresh()

            confirm = term.read()

            if confirm in (term.TK_Y, term.TK_ENTER, code):
                self.player.unequip(part)
                log = strings.cmd_unequip.format(item)
                update_status = True

        def equip_item(part):
            nonlocal log, update_status
            items = list(self.player.inventory_type(part))
            
            if not items:
                log = strings.cmd_equip_none

            else:
                while True:
                    self.clear_main()
                    self.draw_inventory(items)
                    
                    if log:
                        self.draw_screen_log(log)
                    else:
                        self.draw_screen_log(strings.cmd_equip_query)

                    term.refresh()

                    selection = term.read()
                    if selection == term.TK_ESCAPE:
                        self.clear_screen_log()
                        break

                    elif term.TK_A <= selection < term.TK_A + len(items):
                        item = items[selection - term.TK_A]
                        self.player.equip(part, item)
                        log = strings.cmd_equip.format(item)
                        update_status = True
                        break 

                    else:
                        log = 'Invalid selection'

        log = ""
        current_screen = key
        update_status = False
        items = [item for _, inv in self.player.inventory for item in inv]

        self.clear_main()
        if current_screen == "q":
            self.draw_equipment()
            self.draw_screen_log(strings.cmd_switch_eq)

        elif current_screen == "v":
            self.draw_inventory(items)
            self.draw_screen_log(strings.cmd_switch_iv)

        while True:
            if log:
                self.draw_log(log)
                log = ""

            if update_status:
                self.clear_main()
                self.draw_status()
                update_status = False

                if current_screen == "q":
                    self.draw_equipment()
                    self.draw_screen_log(strings.cmd_switch_eq)

                elif current_screen == "v":
                    items = [item for _, inv in self.player.inventory 
                                        for item in inv]
                    self.draw_inventory(items)
                    self.draw_screen_log(strings.cmd_switch_iv)

            term.refresh()
            
            code = term.read()
            if code in (term.TK_ESCAPE,):
                break

            elif code == term.TK_Q:
                current_screen = 'q'
                update_status = True
                # log = ""

            elif code == term.TK_V:
                # V goes to inventory screen
                current_screen = 'v'
                update_status = True

            elif current_screen == 'q' and term.TK_A <= code <= term.TK_L:
                part, item = next(self.player.item_on(code - 4))

                if item:
                    unequip_item(code)

                else:
                    equip_item(part)

            elif current_screen == 'v':
                if term.TK_A <= code < term.TK_A + len(items):
                    item = items[code - 4]
                    self.draw_screen_log(strings.cmd_inv_funcs.format(item))

            else:
                log = ""

            # elif code == term.TK_2 and term.state(term.TK_SHIFT):
            #     @ goes to profile
            #     current_screen = '@'
            # elif code == term.TK_UP:
            #     if current_range > 0: current_range -= 1
            # elif code == term.TK_DOWN:
            #     if current_range < 10: current_range += 1

        term.clear()

    def process_units(self):
        if isinstance(self.location, World):
            for unit in self.location.units:
                self.unit = unit
                self.process_turn()

        elif len(list(self.location.units)) == 1:
                self.unit = self.player
                self.process_turn()

        else:
            for unit in self.location.units:
                unit.energy.gain()
                self.unit = unit
                while unit.energy.ready():
                    self.unit.energy.reset()
                    self.process_turn()      

        # if isinstance(self.location, World):
        #     self.process_turn_player()
        # else:
        #     for unit in self.location.units:
        #         self.unit = unit
        #         if self.unit.energy.ready():
        #             self.unit.energy.reset()
        #             self.process_turn_unit()
        #         else:
        #             self.unit.energy.gain()

        #     if self.player.energy.ready():
        #         self.process_turn_player()
        #     else:
        #         self.player.energy.gain()

    def process_turn(self):
        if isinstance(self.unit, Player):
            self.process_turn_player()

        else:
            self.process_turn_unit()

    def process_turn_player(self):
        action = self.key_input()

        if not self.proceed:
            return

        self.process_handler(*action)

    def process_turn_unit(self):
        if hasattr(self.unit, 'acts'):
            units = { u.position: u for u in self.location.units 
                                                        if u != self.unit }

            # subset of positions possible that can be seen due to sight
            positions = self.location.fov_calc_blocks(
                                                self.unit.x, 
                                                self.unit.y, 
                                                self.unit.sight_norm)

            # units = { self.location.unit_at(*position).position: self.location.unit_at(*position) 
            #             for position in positions if self.location.unit_at(*position) }

            # if self.player not in units.values():
            #     return

            # tile info for every position that can be seen
            tiles = { position: self.location.square(*position) 
                                                for position in positions }

            # get the action variable after putting in all the info into unit.act
            action = self.unit.acts(units, tiles)
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

        except KeyError:
            invalid_command = "'{}' is not a valid command".format(action)
            self.draw_log(invalid_command)

    def process_move_unit_to_empty(self, tx, ty):
        occupied_player = self.player.position == (tx, ty)
        occupied_unit = self.location.occupied(tx, ty)

        if not occupied_player and not occupied_unit:
            # self.unit.move(tx, ty)
            self.unit.position = (tx, ty)
            return None

        return occupied_player, occupied_unit

    def process_movement_unit(self, x, y):
        if (x, y) != (0, 0):
            tx = self.unit.x + x
            ty = self.unit.y + y

            if self.location.walkable(tx, ty):
                unit_bools = self.process_move_unit_to_empty(tx, ty)

                if not unit_bools:
                    return

                else:
                    occupied_player, occupied_unit = unit_bools

                    if occupied_unit:
                        unit = self.location.unit_at(tx, ty)

                    else:
                        unit = self.player

                    player = isinstance(unit, Player)

                    if isinstance(self.location, City):
                        self.unit.displace(unit)
                        unit.energy.reset()
                        log = "The {} switches places with the {}.".format(
                            self.unit.__class__.__name__, 
                            unit.race if not player else "you")
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

                            unit.cur_hp -= damage

                            term.puts(
                                x=tx + self.main_x, 
                                y=ty + self.main_y, 
                                s='[c=red]{}[/c]'.format(damage if damage <= 9 else '*'))
                            term.refresh()

                            log = "The {} attacks {} for {} damage".format(
                                self.unit.race,
                                "you" if player else "the " + unit.race,
                                damage)

                            self.draw_log(log)
                            self.draw_status()

                            if not unit.is_alive:
                                log = "The {} has killed {}!".format(
                                    self.unit.race,
                                    "you" if player else "the " + unit.race)
                                self.draw_log(log, color="red")

                                if player:
                                    exit('DEAD')

                                item = unit.drops()
                                
                                if item:
                                    self.location.item_add(*unit.position, item)
                                    self.draw_log("The {} has dropped {}".format(
                                        unit.race, item.name))
                                self.location.unit_remove(unit)
                            
    def process_movement(self, x, y):
        turn_inc = 0
        if  self.player.height == Level.WORLD:
            if (x, y) == (0, 0):
                self.draw_log(strings.movement_wait_world)
                turn_inc = True

            else:
                tx = self.player.wx + x
                ty = self.player.wy + y

                if self.location.walkable(tx, ty):
                    self.player.save_location()
                    self.player.travel(x, y)
                    turn_inc = True
                else:
                    self.draw_log(strings.movement_move_error)
        else:
            if (x, y) == (0, 0):
                self.draw_log(strings.movement_wait_local)
                turn_inc = True

            else:
                tx = self.player.x + x
                ty = self.player.y + y

                if self.location.walkable(tx, ty):
                    if not self.location.occupied(tx, ty):
                        self.player.move(x, y)
                        msg_chance = random.randint(0, 5)

                        if self.location.items_at(tx, ty) and msg_chance:
                            item_message = random.randint(
                                a=0, 
                                b=len(strings.pass_by_item) - 1)
                            self.draw_log(
                                strings.pass_by_item[item_message])
                            
                        turn_inc = True

                    else:
                        unit = self.location.unit_at(tx, ty)

                        if isinstance(self.location, City):
                            self.player.displace(unit)
                            unit.energy.reset()
                            log = "You switch places with the {}.".format(
                                                unit.__class__.__name__.lower())
                            self.draw_log(log)

                        else:
                            chance = self.player.calculate_attack_chance()

                            if chance == 0:
                                log = "You try attacking the {} but miss.".format(
                                    unit.race)
                                self.draw_log(log)

                            else:
                                damage = self.player.calculate_attack_damage()
                                # if chance returns crit ie. a value of 2 
                                # then multiply damage by 2
                                if chance == 2:
                                    damage *= 2

                                unit.cur_hp -= damage
                                
                                term.puts(
                                    x=tx + self.main_x, 
                                    y=ty + self.main_y, 
                                    s='[c=red]{}[/c]'.format(damage if damage <= 9 else '*'))
                                term.refresh()

                                log = "You{}attack the {} for {} damage. ".format(
                                    " crit and " if chance == 2 else " ", 
                                    unit.race, 
                                    damage)

                                if unit.cur_hp < 1:
                                    log += "You have killed the {}! ".format(
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
                                        self.location.item_add(*unit.position, item)
                                        self.draw_log("The {} has dropped {}.".format(
                                            unit.race, 
                                            item.name))

                                    self.location.unit_remove(unit)

                                else:
                                    log += "The {} has {} health left.".format(
                                        unit.race, 
                                        max(0, unit.cur_hp))

                                    self.draw_log(log, color="red")

                        turn_inc = True
                else:
                    if self.location.out_of_bounds(tx, ty):
                        self.draw_log(strings.movement_move_oob)

                    else:
                        ch = self.location.square(tx, ty).char

                        if ch == "~":
                            log = strings.movement_move_swim
                        else:
                            log = strings.movement_move_block.format(
                                strings.movement_move_chars[ch])

                        self.draw_log(log)

    def get_input(self):     
        '''Handles input reading and parsing unrecognized keys'''
        key = term.read()
        if key in (term.TK_SHIFT, term.TK_CONTROL, term.TK_ALT):
            # skip any non-action keys
            key = term.read()
          
        shifted = term.state(term.TK_SHIFT)
        return key, shifted

    def key_input(self):
        '''Handles keyboard input and keypress transformation
        Cases:
            Skips any pre-inputs and non-read keys
            if key read is a close command -- close early or set proceed to false
            Elif key is valid command return the command from command list with continue
            Else return invalid action tuple with continue value
        '''
        action = tuple(None for _ in range(4))
        key, shifted = self.get_input()
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
        '''Returns a list of spaces in a 8 space grid with the center (pos 5)
        returned if exclusive is set as false
        '''
        space = namedtuple("Space", ("x","y"))
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if (dx, dy) == (0, 0) and exclusive:
                    continue

                else:
                    yield space(x + dx, y + dy)

    def action_save(self):
        '''Save command: checks save folder and saves the current game objects
        to file before going back to the main menu
        '''
        self.draw_log(strings.cmd_save)
        
        # User input -- confirm selection
        code = term.read()
        if code != term.TK_Y:
            return

        if not os.path.isdir('saves'):
            os.makedirs('saves')
            self.draw_log(strings.cmd_save_folder)

        # prepare strings for file writing
        # hash used for same name / different character saves
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
        '''Given player coordinates, determines player current location and 
        adds player object to that location
        '''
        self.location.unit_remove(self.player)
        if self.player.height == Level.WORLD:
            self.location = self.world
        
        else:
            self.location = self.world.location(*self.player.location)

            if self.player.height > 1:
                for i in range(self.player.height - 1):
                    self.location = self.location.sublevel

        self.location.units_add([self.player])
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
        '''Enter map command: determines which kind of world to create when
        entering a location based on teh world enterable and dungeon dicts.
        If world is already created just load world as current location
        '''
        if not self.world.location_exists(*self.player.location):
            if self.player.location in self.world.enterable_legend.keys():
                fileloc = self.world.enterable_legend[self.player.location]
                fileloc = fileloc.replace(' ', '_').lower()
                img_name = "./spaceship/assets/maps/" + fileloc + ".png"
                cfg_name = "./spaceship/assets/maps/" + fileloc + ".cfg"

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
                    height=self.height,
                    generate=True)

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
                self.player.position = self.determine_map_enterance(
                    x=x, 
                    y=y, 
                    location=location)
                
        self.player.move_height(1)
        self.map_change = True

    def action_stairs_down(self):
        '''Go Down command: Checks player position to the downstairs position
        in the current location. If they match then create a dungeon with the
        player starting position at the upstairs of the new location
        '''
        if self.player.position == self.location.stairs_down:
            if not self.location.sublevel:
                location = Cave(
                    width=self.width,
                    height=self.height,
                    max_rooms=random.randint(15, 20))
                
                self.location.sublevel = location
                location.parent = self.location

            self.player.move_height(1)
            self.location.unit_remove(self.player)
            self.location = self.location.sublevel
            self.location.units_add([self.player])
            self.player.position = self.location.stairs_up


        else:
            self.draw_log("You cannot go downstairs without stairs.")

    def action_stairs_up(self):
        '''Go Up command: Checks player position to the upstairs position
        in the current location. Then determine the parent location 
        and reset position according to the type of parent
        '''
        def move_upstairs():
            self.location.unit_remove(self.player)
            self.location = self.location.parent
            self.player.move_height(-1)
            self.location.units_add([self.player])

        # check if parent of this location is the World Map
        if isinstance(self.location.parent, World):
            move_upstairs()
            # reset position since re-entering world map
            self.player.position = (0, 0)

        # check if parent location is a city, wilderness or dungeon map
        elif isinstance(self.location.parent, (City, Wild, Cave)):
            move_upstairs()
            # reset position to the downstairs in the dungeon
            self.player.position = self.location.stairs_down

        else:
            self.draw_log("You cannot go upstairs without stairs.")

    def action_door_close(self):
        '''Close door command: handles closing doors in a one unit distance
        from the player. Cases can range from no doors, single door, multiple 
        doors, with multiple doors asking for input direction
        '''
        def close_door(x, y):
            self.draw_log(strings.interact_door_close_act)
            self.location.close_door(x, y)

        doors = []
        for pos in self.spaces(*self.player.position):
            if pos != self.player.position:
                try:
                    if self.location.square(*pos).char == '/':
                        doors.append(pos)

                except IndexError:
                    self.draw_log('Out of bounds ({}, {})'.format(*pos))

        if not doors:
            self.draw_log(strings.interact_door_close_none)

        elif single_element(doors):
            close_door(*doors.pop())

        else:
            px, py = self.player.position
            self.draw_log(strings.interact_door_close_many)

            code = term.read()
            shifted = term.state(term.TK_SHIFT)

            try:
                dx, dy, _, act = commands_player[(code, shifted)]

            except:
                self.draw_log(strings.interact_door_close_invalid)

            else:
                if act == "move" and (px + dx, py + dy) in doors:
                    close_door(px + dx, py + dy)

                else:
                    self.draw_log(strings.interact_door_close_error)
                    
    def action_door_open(self):
        '''Open door command: handles opening doors in a one unit distance from
        the player. Cases can range from no doors, single door, multiple 
        doors, with multiple doors asking for input direction
        '''
        def open_door(x, y):
            self.draw_log(strings.interact_door_open_act)
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
            self.draw_log(strings.interact_door_open_none)

        elif single_element(doors):
            open_door(*doors.pop())

        else:
            self.draw_log(strings.interact_door_open_many)

            code = term.read()
            shifted = term.state(term.TK_SHIFT)

            try:
                dx, dy, _, act = commands_player[(code, shifted)]
                    
            except:
                self.draw_log(strings.interact_door_open_invalid)

            else:
                if act == "move" and (px + dx, py + dy) in doors:
                    open_door(px + dx, py + dy)

                else:
                    self.draw_log(strings.interact_door_open_error)

    def action_unit_talk(self):
        def talk_to(x, y):
            self.draw_log(self.location.unit_at(x, y).talk())

        units = []
        px, py = self.player.position

        for pos in self.spaces(*self.player.position):
            if pos != self.player.position:
                try:
                    if self.location.unit_at(*pos):
                        units.append(pos)

                except IndexError:
                    self.draw_log('Out of bounds ({}, {})'.format(*pos))
        
        if not units:
            self.draw_log('No one to talk to')
        
        elif single_element(units):
            talk_to(*units.pop())
    
        else:
            px, py = self.player.position
            log = "There is more than one character near you. Which direction?"
            self.draw_log(log)
            
            code = term.read()
            shifted = term.state(term.TK_SHIFT)

            try:
                dx, dy, _, act = commands_player[(code, shifted)]

            except:
                log = "Invalid direction. Canceled talking to character."
                self.draw_log(log)
            
            else:
                if act == "move" and (px + dx, py + dy) in units:
                    talk_to(px + dx, py + dy)
                
                else:
                    log = "Direction has no unit. "
                    log += "Canceled talking to character"
                    self.draw_log(log)

    def action_unit_attack_melee(self):
        pass

    def action_unit_attack_ranged(self):
        pass

    def action_unit_displace(self):
        pass

    def action_item_pickup(self):
        def pickup_item(item):
            nonlocal log
            if self.player.item_add(item):
                self.location.item_remove(*self.player.position, item)
                log = "You pick up {} and place it in your backpack.".format(
                                                                    item.name)
                log += " Your backpack feels heavier."

            else:
                log = "Backpack is full. Cannot pick up {}.".format(item)

        items = [item for item in self.location.items_at(*self.player.position)]

        log = ""
        if not items:
            self.draw_log("No items on the ground where you stand.")

        else:
            log = ""
            update_items = False
            if single_element(items):
                pickup_item(items.pop())
                self.draw_log(log)

            else:
                self.index_row, self.item_row = 0, 0
                self.clear_main()
                self.draw_pickup(items)

                while True:

                    if log:
                        self.draw_log(log)
                        log = ""
                    
                    if update_items:
                        update_items = False
                        self.index_row, self.item_row = 0, 0
                        items = self.location.items_at(*self.player.position)

                        if not items:
                            break

                        self.clear_main()
                        self.draw_pickup(items)


                    term.refresh()
                    code = term.read()
                    if code == term.TK_ESCAPE:
                        break
                    
                    elif term.TK_A <= code < term.TK_A + len(items):
                        pickup_item(items[code - 4])
    '''
    Notes :- Dropping Items:
        Dropping items will always be dropped from inventory
        If an item is equipped it CANNOT be dropped unless it is unequiped.
        When an item is unequipped the item will be added back to the inventory
        Then the player may drop the item from there
    '''
    def action_item_drop(self):
        def drop_item(item):
            nonlocal log
            self.player.item_remove(item)
            self.location.item_add(*self.player.position, item)
            if hasattr(item, 'name'):
                item_name = item.name
            else:
                item_name = item
            log = "You drop the {} onto the ground.".format(item_name)
            log += " Your backpack feels lighter."
        
        log = ""
        update_items = False
        items = [item for _, inv in self.player.inventory for item in inv]

        while True:
            self.clear_main()
            self.draw_inventory(items)

            if items:
                self.draw_screen_log(strings.cmd_drop_query)

            if log:
                self.draw_log(log)

            term.refresh()            

            code = term.read()
            if code == term.TK_ESCAPE:
                log = ""
                break

            elif term.TK_A <= code < term.TK_A + len(items):
                drop_item(items.pop(code - 4))
                items = [item for _, inv in self.player.inventory 
                            for item in inv]

            else:
                log = ""

    def action_item_use(self):
        def use_item(item):
            nonlocal log
            self.player.item_use(item)
            if hasattr(item, 'name'):
                item_name = item.name
            else:
                item_name = item
            log = strings.cmd_use_item.format(item_name)
        
        log = ""
        items = list(self.player.inventory_prop('use'))

        while True:
            self.clear_main()
            self.draw_inventory(items, strings.cmd_use_none)

            if items:
                self.draw_screen_log(strings.cmd_use_query)
            else:
                self.draw_screen_log(strings.cmd_use_none)

            if log:
                self.draw_log(log)

            term.refresh()

            code = term.read()
            if code == term.TK_ESCAPE:
                break

            elif term.TK_A <= code < term.TK_A + len(items):
                use_item(items[code - 4])
                items = list(self.player.inventory_prop('use'))
                self.draw_status()

            else:
                log = ""

    def action_item_eat(self):
        def eat_item(item):
            nonlocal log
            self.player.item_eat(item)
            if hasattr(item, 'name'):
                item_name = item.name
            else:
                item_name = item
            log = strings.cmd_eat_item.format(item_name)
            
        log = ""
        items = list(self.player.inventory_prop('eat'))

        while True:
            self.clear_main()
            self.draw_inventory(items, strings.cmd_use_none)

            if items:
                self.draw_screen_log(strings.cmd_eat_query)
            else:
                self.draw_screen_log(strings.cmd_eat_none)

            if log:
                self.draw_log(log)

            term.refresh()

            code = term.read()
            if code == term.TK_ESCAPE:
                break
                
            elif term.TK_A <= code < term.TK_A + len(items):
                eat_item(items[code - 4])
                items = list(self.player.inventory_prop('eat'))
                self.draw_status()
            
            else:
                log = ""

if __name__ == "__main__":
    from .make import Create
    term.open()
    c = Create()
    ret = c.run()
    ret['kwargs']['name'] = 'grey'
    print(ret)
    s = Start()
    s.add_args(**ret['kwargs'])
    s.run()