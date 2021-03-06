import shelve
import random
import textwrap
from time import sleep, time
from collections import namedtuple
from bearlibterminal import terminal as term
import spaceship.strings as strings
from spaceship.menus.scene import Scene
from spaceship.screen_functions import *
import spaceship.tools as tools
import spaceship.action as actions
from spaceship.gamelog import GameLogger
from spaceship.classes.item import Item, Potion, sort
from spaceship.classes.wild import wilderness
from spaceship.classes.player import Player
from spaceship.classes.world import World
from spaceship.classes.city import City
from spaceship.classes.cave import Cave
from spaceship.classes.point import Point, spaces

enter_maps = {
    'cave': Cave,
    'city': City,
    'wild': wilderness
}

class Level: GLOBAL, WORLD, LOCAL = -1, 0, 1
class Maps: CITY, CAVE, WILD, WORLD = range(4)

class Start(Scene):
    def __init__(self, sid='start_game'):
        super().__init__(scene_id=sid)

    def reset(self):
        self.log = []
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
                '>': self.action_enter_map, # Done
            },
            1: {
                # '@': self.draw_screens,
                'q': self.draw_screens,
                'v': self.draw_screens,
                '<': self.action_stairs_up, # done
                '>': self.action_stairs_down, # done
                'c': self.action_door_close, # done
                'o': self.action_door_open, # done
                ',': self.action_item_pickup,
                'd': self.action_item_drop,
                'u': self.action_item_use,
                'e': self.action_item_eat,
                't': self.action_unit_talk,
                'T': self.actions_ranged,
                'z': self.actions_ranged,
                'l': self.actions_ranged,
                's': self.draw_spells,
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
            world_map_path = strings.IMG_PATH + "worldmap.png"

            self.player = Player(player, name)
            self.location = self.world = World(map_name="Calabston", 
                                               map_link=world_map_path)
            self.location.units_add([self.player])

        self.gamelog = GameLogger(
            width=self.main_width,
            screenlinelimit=3 if self.height <= 25 else 4,
            footer="_" + self.player.name + "_" + self.player.job)

        while self.proceed and self.player.is_alive:
            # term.clear()
            self.draw()
            term.refresh()

            # self.location.process()

            self.process_units()
            if self.map_change:
                self.change_map_location()

            # term.delay (1000 // 75)

        self.proceed = True
        if hasattr(self, 'ret'):
            return self.ret

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
            action = actions.commands_player[(key, shifted)]
        except KeyError:
            pass
            
        return action

    def process_units(self):
        # for unit in self.location.units:
        #     self.unit = unit
        #     self.process_turn()
        if isinstance(self.location, World):
            for unit in self.location.units:
                self.unit = unit
                self.process_turn()

        elif len(list(self.location.units)) == 1:
                self.unit = self.player
                self.process_turn()

        else:
            # for unit in self.location.units:
            #     self.unit = unit
            #     self.process_turn()
            for self.unit in self.location.units:
                self.unit.energy.gain()

            if any(u.energy.ready() for u in self.location.units):
            # for self.unit in self.location.units:
            #     if self.unit == self.player and not self.unit.energy.ready():
            #         break
                for self.unit in self.location.units:
                    for _ in range(self.unit.energy.turns):
                        # print(self.unit.unit_id, self.unit.race)
                        self.unit.energy.reset()
                        self.process_turn()   
        # else:   
        #     for unit in self.location.units:
        #         unit.energy.gain()

        #     for unit in self.location.units:
        #         self.unit = unit
        #         for turn in range(self.unit.energy.turns):
        #             self.unit.energy.reset()
        #             self.process_turn()

        if self.turn_inc:
            self.turns += 1
            self.turn_inc = False

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

    def process(self):
        action = None
        if isinstance(self.unit, player):
            action = self.key_input()
        else:
            if hasattr(self.unit, 'acts'):
                units = {u.local: u for u in self.location.units if u != self.units}
                positions = self.location.fov_calc_blocks(*self.unit.local, 
                                                          self.unit.sight_norm)
                tiles = {position: self.location.square(*position) for position in positions}
                action = self.unit.acts(units, tiles)

        if not self.player.is_alive:
            self.proceed = False
            return
    
        if not self.proceed:
            return

    def process_turn_player(self):
        action = self.key_input()

        if not self.proceed:
            return

        self.process_handler(*action)

    def process_turn_unit(self):
        if hasattr(self.unit, 'acts'):
            units = {u.local: u for u in self.location.units if u != self.unit}

            # subset of positions possible that can be seen due to sight
            positions = self.location.fov_calc_blocks(*self.unit.local,
                                                      self.unit.sight_norm)
            # units = {self.location.unit_at(*position).position: 
            #               self.location.unit_at(*position) 
            #             for position in positions if self.location.unit_at(*position) }

            # if self.player not in units.values():
            #     return

            # tile info for every position that can be seen
            tiles = { position: self.location.square(*position) 
                      for position in positions }

            # get the action variable after putting in 
            # all the info into unit.act
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
                self.unit, self.location, self.log = divided[action]()
            except TypeError:
                divided[action](action)
            except KeyError:
                raise
                invalid_command = strings.cmd_invalid.format(action)
                self.log.append(invalid_command)

        except KeyError:
            raise
            invalid_command = strings.cmd_invalid.format(action)
            self.log.append(invalid_command)

    def process_move_unit_to_empty(self, x, y):
        occupied_player = self.player.local == (x, y)
        occupied_unit = self.location.occupied(x, y)

        if not occupied_player and not occupied_unit:
            self.unit.local = Point(x, y)
            return None

        return occupied_player, occupied_unit

    def process_movement_unit(self, x, y):
        if (x, y) != (0, 0):
            point = self.unit.local + (x, y)

            if self.location.walkable(*point):
                unit_bools = self.process_move_unit_to_empty(*point)

                if not unit_bools:
                    return

                else:
                    occupied_player, occupied_unit = unit_bools

                    if occupied_unit:
                        unit = self.location.unit_at(*point)

                    else:
                        unit = self.player

                    player = isinstance(unit, Player)
                    safe_location = isinstance(self.location, City)
                    friendly_unit = unit.friendly(self.unit)
                    if safe_location or friendly_unit:
                        self.unit.displace(unit)
                        unit.energy.reset()
                        # log = strings.movement_unit_displace.format(
                        #     self.unit.__class__.__name__, 
                        #     unit.race if not player else "you")
                        # self.log.append(log)

                    else:
                        chance = self.unit.calculate_attack_chance()

                        if chance == 0:
                            pass
                            log = "The {} tries attacking {} but misses".format(
                                self.unit.race, 
                                "you" if player else "the " + unit.race)
                            self.log.append(log)

                        else:
                            damage = self.unit.calculate_attack_damage()

                            if chance == 2:
                                damage *= 2

                            
                            unit.cur_hp -= damage
                            
                            # if self.location.check_light_level(*point):
                            #     term.layer(1)
                            #     term.puts(
                            #         *(point + (self.main_x, self.main_y)),
                            #         '[c=red]*[/c]')

                            #     term.refresh()

                            #     term.clear_area(*(point + (self.main_x, self.main_y)),
                            #         1, 1)
                            #     term.layer(0)
                                
                            log = "The {} attacks {} for {} damage".format(
                                self.unit.race,
                                "you" if player else "the " + unit.race,
                                damage)
                            self.log.append(log)

                            if not unit.is_alive:
                                log = "The {} has killed {}!".format(
                                    self.unit.race,
                                    "you" if player else "the " + unit.race)

                                self.log.append(log)

                                # if player:
                                #     exit('DEAD')

                                item = None
                                if hasattr(unit, 'drops'):
                                    item = unit.drops()
                                
                                if item:
                                    self.location.item_add(*unit.local, item)
                                    self.log.append("The {} has dropped {}".format(
                                        unit.race, item.name))

                                self.location.unit_remove(unit)
                            
    def process_movement(self, x, y):
        # moving on world map
        if self.player.height == Level.WORLD:
            if (x, y) == (0, 0):
                self.log.append(strings.movement_wait_world)

            else:
                point = self.player.world + (x, y)
                if self.location.walkable(*point):
                    self.player.save_location()
                    self.player.travel(x, y)
                    
                else:
                    self.log.append(strings.movement_move_error)

        # moving on local map    
        else:
            if (x, y) == (0, 0):
                self.log.append(strings.movement_wait_local)
                self.turn_inc = True

            else:
                point = self.player.local + (x, y)
                if self.location.walkable(*point):
                    if not self.location.occupied(*point):
                        self.player.move(x, y)
                        msg_chance = random.randint(0, 5)

                        if self.location.items_at(*point) and msg_chance:
                            item_message = random.randint(
                                a=0, 
                                b=len(strings.pass_by_item) - 1)
                            self.log.append(strings.pass_by_item[item_message])
                    else:
                        unit = self.location.unit_at(*point)
                        safe_location = isinstance(self.location, City)
                        friendly_unit = unit.friendly(self.unit)                        
                        if safe_location or friendly_unit:
                            self.player.displace(unit)
                            unit.energy.reset()
                            switch = "You switch places with the {}.".format(
                                                unit.__class__.__name__.lower())
                            self.log.append(switch)

                        else:
                            chance = self.player.calculate_attack_chance()

                            if chance == 0:
                                log = f"You miss the {unit.race}."
                                self.log.append(log)

                            else:
                                damage = self.player.calculate_attack_damage()
                                # if chance returns crit ie. a value of 2 
                                # then multiply damage by 2
                                if chance == 2:
                                    damage *= 2

                                unit.cur_hp -= damage
                                
                                # if self.location.check_light_level(*point):
                                #     term.puts(
                                #         *(point + (self.main_x, self.main_y)),
                                #         '[c=red]*[/c]')
                                #     term.refresh()

                                log = "You{}attack the {} for {} damage. ".format(
                                    " crit and " if chance == 2 else " ", 
                                    unit.race, 
                                    damage)
                                self.log.append(log)

                                if unit.cur_hp < 1:
                                    self.log.append("You have killed the {}! ".format(unit.race))
                                    self.log.append("You gain {} exp.".format(unit.xp))
                                    self.player.gain_exp(unit.xp)

                                    if self.player.check_exp():
                                        log = "You level up. You are now level {}.".format(self.player.level)
                                        self.log.append(log)
                                        self.log.append("You feel much stronger now.")

                                    item = unit.drops()

                                    if item:
                                        self.location.item_add(*unit.local, item)
                                        self.log.append("The {} has dropped {}.".format(unit.race, 
                                                                                        item.name))

                                    self.location.unit_remove(unit)

                                else:
                                    log += "The {} has {} health left.".format(
                                        unit.race, 
                                        max(0, unit.cur_hp))
                                    self.log.append(log)

                    self.turn_inc = True

                else:
                    '''
                    moving outside of current map
                        moving on top level (one level below world) then
                        try to move into the new map if it is not water
                    '''
                    if self.location.out_of_bounds(*point):
                        self.log.append(strings.movement_move_oob)

                    else:
                        ch = self.location.square(*point).char

                        if ch == "~":
                            log = strings.movement_move_swim
                        else:
                            log = strings.movement_move_block.format(
                                strings.movement_move_chars[ch])

                        self.log.append(log)

    def draw(self):
        self.draw_log(refresh=False)

        self.draw_status()

        self.draw_world()

    def draw_log(self, log=None, color="white", refresh=False):
        self.gamelog.draw(log if log else " ".join(self.log), color, refresh)
        if self.log:
            self.log = []

    def draw_world(self):
        '''Handles drawing of world features and map'''
        point = self.player.local if self.player.height >= 1 \
            else self.player.world

        g0 = isinstance(self.location, World)

        if g0:
            sight = self.player.sight_world

        elif isinstance(self.location, City):
            sight = self.player.sight_city

        else:
            sight = self.player.sight_norm

        self.location.fov_calc([(*point, sight)])
        for (x, y), string in self.location.output(*point):
            term.puts(x=x + self.main_x, 
                      y=y + self.main_y,
                      s=string)

        # sets the location name at the bottom of the status bar
        if g0:
            location = None

            if self.player.world in self.world.cities.keys():
                location = self.world.cities[self.player.world]

            elif self.player.world in self.world.dungeons.keys():
                location = self.world.dungeons[self.player.world]

            if location:
                self.draw_screen_header(location)

    def draw_screen_header(self, header=None):
        '''Draws a line across the top of the window'''
        term.bkcolor('dark grey')
        term.puts(self.main_x, 0, ' ' * (self.width - self.main_x))
        term.bkcolor('black')

        if header:
            string = surround(header)
            term.puts(center(string, self.width + self.main_x), 0, string)
                
    def draw_status(self):
        '''Handles player status screen'''
        term.puts(self.status_col, 
                  self.status_row,
                  strings.status.format(*self.player.status(), self.turns))

    def clear_status(self):
        term.clear_area(0, 0, self.width - self.main_width, self.height)

    def draw_profile(self):
        '''Handles player profile screen'''

        # draws header border
        term.puts(i, 0, '#' * self.width)
        term.puts(center('profile  ', self.width), 0, ' Profile ')

        for colnum, column in enumerate(list(self.player.profile())):
            term.puts(x=self.screen_col + (20 * colnum), 
                      y=self.screen_row, 
                      s=column)

    def clear_main(self):
        term.clear_area(self.main_x, 0, 
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

    def draw_item_grouping(self, group, items, index, item):
        '''Handler to determine if we need to draw items or not'''
        if items:
            if group not in 'food others'.split():
                group = list(group + 's')
                group[0] = group[0].upper()
                group = "".join(group)
            
            term.puts(x=self.screen_col + self.main_x,
                      y=self.screen_row + index * self.row_spacing,
                      s="   __" + group + "__")
            index += 1

            for i in items:
                letter = chr(ord('a') + item) + ". "
                term.puts(x=self.screen_col + self.main_x,
                          y=self.screen_row + index * self.row_spacing,
                          s=letter + i.__str__()) 
                index += 1
                item += 1
            return index + 1, item
        return index, item

    def draw_inventory(self, items, index, row, string=strings.cmd_inv_none):
        '''Handles drawing of the inventory screen along with the specific 
        groupings of each item type and their modification effects
        '''
        self.draw_screen_header('Inventory')
        if not items:
            string_pos = center(string, self.main_width)
            term.puts(string_pos + self.main_x, 3, string)
        else:
            for group, items in list(sort(items).items()):          
                index, row = self.draw_item_grouping(group, items, index, row)
        return index, row
        
    def draw_pickup(self, items, index, row):
        '''Handles drawing of the items located on the ground along with 
        specific groupings of each item type and their modification effects
        '''
        self.draw_screen_header('Pickup Items')
        for group, items in sort(items).items():
            index, row = self.draw_item_grouping(group, items, index, row)
        return index, row
            
    def draw_screen_log(self, log):
        strings = wrap(log, self.main_width)
        for index, string in enumerate(strings):
            term.puts(x=center(string, self.main_width) + self.main_x, 
                      y=self.height + index - 5, 
                      s=string)

    def clear_screen_log(self):
        term.clear_area(self.main_x, self.height - 5, self.main_width, 2)

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
        
    def draw_spells(self):
        spells = [
            ('Fireball', "Cast a fireball at target area and deal aoe damage?"),
            ('Frost Bolt', "Cast a freezing missile at target and hit all enemies in its path?"),
            ('Lightning', "Cast a lightning bolt at target area and deal aoe damage?"),
        ]

        log = ""
        selected = None
        update_status = False
        spell_index = 0
        self.clear_main()
        self.draw_screen_header('Spells')
        self.clear_screen_log()
        self.draw_screen_log("What would you like to do?")

        while True:
            if log:
                self.clear_screen_log()
                self.draw_screen_log(log)
                log = ""
            
            for index, spell in enumerate(spells):
                letter = chr(ord('a') + index) + '. '
                term.puts(
                    x=self.screen_col + self.main_x,
                    y=self.screen_row + index * self.row_spacing,
                    s=letter + spell[0]
                )
            term.refresh()

            code = term.read()
            if code == term.TK_ESCAPE:
                break
            elif term.TK_A <= code < term.TK_A + len(spells):
                selected = code - term.TK_A
                log = spells[selected][1]
            elif selected is not None and code in (term.TK_Y, term.TK_ENTER, selected + term.TK_A):
                self.log.append("You cast {}".format(spells[selected][0]))     
                break

    def draw_screens(self, key):

        def unequip_item(code):
            nonlocal log, update_status
            try:
                string = strings.cmd_unequip_confirm.format(item.name)
            except AttributeError:
                string = strings.cmd_unequip_confirm.format(item)
            
            self.clear_screen_log()
            self.draw_screen_log(string)
            term.refresh()

            confirm = term.read()

            if confirm in (term.TK_Y, term.TK_ENTER, code):
                self.player.unequip(part)
                try:
                    log = strings.cmd_unequip.format(item.name)
                except AttributeError:
                    log = strings.cmd_unequip.format(item)
                update_status = True

            else:
                self.clear_screen_log()

        def equip_item(part):
            nonlocal log, update_status

            if part in ('hand_left', 'hand_right'):
                if self.player.holding_two_handed_weapon():
                    _, li = next(self.player.item_on('hand_left'))
                    _, ri = next(self.player.item_on('hand_right'))
                    print(li, ri)
                    log = strings.cmd_equip_two_hand.format(
                        part, 
                        li if li else ri,
                        'left hand' if li else 'right hand',)
                    return 

            items = list(self.player.inventory_type(part))
            
            if not items:
                log = strings.cmd_equip_none

            else:
                while True:
                    self.clear_main()
                    self.draw_inventory(items)
                    self.clear_screen_log()
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
                        log = strings.cmd_equip_invalid

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
            self.clear_screen_log()
            self.draw_screen_log(strings.cmd_switch_iv)

        while True:
            if log:
                self.draw_log(log)
                log = ""

            if update_status:
                self.clear_main()
                self.clear_status()
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
                    self.clear_screen_log()
                    self.draw_screen_log(strings.cmd_inv_funcs.format(item))
                    
                    # while True:
                    #     term.refresh()
                    #     selection = term.read()
                    #     if selection == term.TK_U:
                    #         if self.player.item_eat(item):
                    #             self.draw_screen_log(
                    #                 strings.cmd_use_item.format(item))
                    #             break
                    #         else:
                    #             self.draw_screen_log(
                    #                 strings.cmd_cannot_use_item)
                    # 
                    #     elif selection == term.TK_D:
                    #     elif selection == term.TK_E:
                    #         if self.player.item_eat(item):
                    #             self.draw_screen_log(
                    #                 strings.cmd_eat_item.format(item))
                    #             break
                    #         else:
                    #             self.draw_screen_log(
                    #                 strings.cmd_cannot_eat_item)
                    # 
                    #     elif selection == term.TK_Q:
                    #         self.draw_screen_log('Equip it using the other way')
                    #     else:
                    #         self.draw_screen_log("Invalid instruction.")
                    #         term.refresh()
                    #         break
                    # 
                    # self.draw_screen_log(strings.cmd_switch_iv)
            else:
                log = ""

            # elif code == term.TK_2 and term.state(term.TK_SHIFT):
            #     @ goes to profile
            #     current_screen = '@'
            # elif code == term.TK_UP:
            #     if current_range > 0: current_range -= 1
            # elif code == term.TK_DOWN:
            #     if current_range < 10: current_range += 1

        # term.clear()

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
        file_path = './spaceship/saves/{}'.format(desc)
        
        with shelve.open(file_path, 'n') as save_file:
            save_file['desc'] = desc
            save_file['player'] = self.player
            save_file['world'] = self.world
            save_file['turns'] = self.turns  

        self.proceed = False  
        self.ret['scene'] = 'main_menu'
        self.reset()

    def change_map_location(self):
        '''Given player coordinates, determines player current location and 
        adds player object to that location
        '''
        if self.player.height == Level.WORLD:
            self.location = self.world
        
        else:
            self.location = self.world.location(*self.player.world)

            if self.player.height > 1:
                for i in range(self.player.height - 1):
                    self.location = self.location.sublevel
        self.map_change = False

    # Map Changes -- These return unit, location, log -- maybe change for all actions?
    def action_enter_map(self):
        return actions.enter_map(self.player, self.location, enter_maps)

    def action_stairs_down(self):
        return actions.go_down_stairs(self.player, self.location, Cave)

    def action_stairs_up(self):
        return actions.go_up_stairs(self.player, self.location, Maps)

    def action_door_close(self):
        return actions.close_door(self.player, self.location, self.draw_log)
                    
    def action_door_open(self):
        return actions.open_door(self.player, self.location, self.draw_log)

    def action_unit_talk(self):
        return actions.converse(self.player, self.location, self.draw_log)

    def action_item_pickup(self):
        return actions.pickup_item(self.player, 
                                   self.location, 
                                   self.clear_main,
                                   self.draw_pickup,
                                   self.draw_log)

    def action_item_drop(self):
        return actions.drop_item(self.player, 
                                 self.location, 
                                 self.clear_main, 
                                 self.draw_inventory, 
                                 self.draw_log, 
                                 self.draw_screen_log)

    def action_item_use(self):
        return actions.use_item(self.player, 
                                self.area, 
                                self.clear_main,
                                self.draw_inventory,
                                self.draw_screen_log,
                                self.draw_status)

    def action_item_eat(self):
        return actions.eat_item(self.player,
                                self.area,
                                self.clear_main,
                                self.draw_inventory,
                                self.draw_screen_log,
                                self.draw_status)
        # def eat_item(item):
        #     nonlocal log
        #     self.player.item_eat(item)
        #     if hasattr(item, 'name'):
        #         item_name = item.name
        #     else:
        #         item_name = item
        #     log = strings.cmd_eat_item.format(item_name)
            
        # log = ""
        # items = list(self.player.inventory_prop('eat'))

        # while True:
        #     self.clear_main()
        #     self.draw_inventory(items, strings.cmd_use_none)

        #     if items:
        #         self.draw_screen_log(strings.cmd_eat_query)
        #     else:
        #         self.draw_screen_log(strings.cmd_eat_none)

        #     if log:
        #         self.draw_log(log)
        #         log = ""

        #     term.refresh()

        #     code = term.read()
        #     if code == term.TK_ESCAPE:
        #         break
                
        #     elif term.TK_A <= code < term.TK_A + len(items):
        #         eat_item(items[code - 4])
        #         items = list(self.player.inventory_prop('eat'))
        #         self.draw_status()

    def actions_ranged(self, key):
        def look():
            nonlocal position, code, shifted

            action = actions.commands_player[(code, shifted)]
            new_pos = position + (action.x, action.y)

            in_bounds = self.player.local.distance(new_pos) < sight
            lighted = self.location.check_light_level(*new_pos) > 0

            char, color = '', 'white'

            if in_bounds and lighted:
                if position == self.player.local:
                    char, color = '@', 'white'
                else:
                    unit = self.location.unit_at(*position)
                    if unit:    
                        char, color = unit.character, unit.foreground

                    square = self.location.square(*position)

                    if not char and square.items:
                        item = square.items[-1]
                        char, color = item.char, item.color
                    
                    if not char and not square.items:
                        char, color = square.char, square.color

                term.clear_area(*(position + (self.main_x, self.main_y)), 1, 1)
                position = new_pos 

        def throw():
            nonlocal position
            points = tools.bresenhams(self.player.local, position)
            term.layer(1)
            for point in points:
                translate = Point(self.main_x, self.main_y) + point
                symbol = term.pick(*translate)
                color = term.pick_color(*translate)
                term.composition(False)
                term.puts(*translate, "[c=red]/[/c]")
                term.composition(True)
                term.refresh()
                term.clear_area(*translate, 1, 1)
                term.refresh()

        def zap():
            nonlocal position
            points = tools.bresenhams(self.player.local, position)
            for point in points[1:]:
                unit = self.location.unit_at(*point)
                if unit:
                    unit.cur_hp -= 10
                    self.log.append(f"You zap the {unit.race} with lightning.")
                    if not unit.is_alive:
                        item = unit.drops()
                        self.location.unit_remove(unit)
                        self.log.append(f"The {unit.race} dies from shock.")
                        if item:
                            self.location.item_add(*point, item)
                            item_name = item.name if hasattr(item, "name") else item
                            self.log.append(f"The {unit.race} drops {item_name}.")

                translate = Point(self.main_x, self.main_y) + point
                term.puts(*translate, "[c=yellow]-[/c]")
                term.refresh()

        code, shifted = None, None
        position, color, char = self.player.local, 'white', 'x'
        proceed = True
        
        if key == "T":
            color = "red"
        elif key == "z":
            color = "yellow"
        
        if (self.location, City):
            sight = self.player.sight_city
        else:
            sight = self.player.sight_norm

        term.layer(1)
        # term.composition(False)
        while proceed:
            term.puts(*(position + (self.main_x, self.main_y)), 
                f'[c={color}]x[/c]')
            term.refresh()

            code = term.read()
            shifted = term.state(term.TK_SHIFT)
            if code == term.TK_ESCAPE:
                proceed = False

            elif term.TK_RIGHT <= code <= term.TK_UP:
                look()

            elif term.TK_KP_1 <= code <= term.TK_KP_9:
                look()

            elif code == term.TK_ENTER:
                if key == "l":
                    self.draw_log("You look at the spot")

                elif key == "T":
                    throw()
                    self.draw_log("You throw something")
                    proceed = False

                else:
                    zap()
                    proceed = False

            elif code == term.TK_T and key == "T":
                throw()
                self.draw_log("You throw something")
                proceed = False

            elif code == term.TK_Z and key == "z":
                zap()
                self.draw_log("You zap something")
                proceed = False
        # term.composition(True)
        term.clear_area(self.main_x, 
                        self.main_y, 
                        self.width - self.main_x,
                        self.height - self.main_y)
        term.layer(0)
        print(self.log)

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