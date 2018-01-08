import os
import sys
import shelve
import random
from collections import namedtuple
from bearlibterminal import terminal as term
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

import spaceship.cc_strings as strings
from .setup_game import setup, setup_font, setup_menu, output, toChr
from .screen_functions import *
from .scene import Scene
from .action import commands
from .gamelog import GameLogger
from .classes.player import Player
from .classes.world import World
from .classes.wild import wilderness
from .classes.city import City
from .classes.cave import Cave

class Level: Global, World, Local = -1, 0, 1

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
        self.do_action = True
        self.map_change = False
        self.gamelog = GameLogger(3 if self.height <= 25 else 4)

    def setup(self):
        self.reset()
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
                'c': self.action_interact_door_close,
                'o': self.action_interact_door_open,
            },
        }

        # player screen variables
        self.player_screen_col, self.player_screen_row = 1, 3
        self.player_status_col, self.player_status_row = 1, 2

    def run(self):  
        self.reset_size()
        if isinstance(self.ret['kwargs']['player'], Player):
            self.player = self.ret['kwargs']['player']
            self.world = self.ret['kwargs']['world']
            self.turns = self.ret['kwargs']['turns']
        else:
            player = self.ret['kwargs']['player']
            name = self.ret['kwargs']['name']
            self.player = Player(player, name)

            self.world = World(
                map_name="Calabston", 
                map_link="./assets/worldmap.png")
            self.location = self.world

        # print(self.player.name)
        # print(self.world.map_name)

        # while self.proceed and self.player.is_alive():
        while self.proceed and self.player.is_alive:
            self.draw()
        
        self.proceed = True
        if hasattr(self, 'ret'):
            return self.ret

    def draw(self):
        term.clear()
        self.draw_log()
        self.draw_player_status()

        if self.map_change:
            self.determine_map_location()

        self.draw_world()
        term.refresh()
        turn_inc = False

        if self.do_action:
            action = self.key_input()
            if not self.proceed:
                return

            self.process_handler(*action)

    def draw_log(self):
        for index, message in enumerate(self.gamelog.write().messages):
            term.puts(
                x=14 if self.player.height == Level.Global else 1,
                y=self.height - 2 + index,
                s=message[1]
            )

    def draw_world(self):
        screen_off_x, screen_off_y = 14, 0
        x, y = self.player.position if self.player.height >= 1 else self.player.location
        self.location.fov_calc([(x, y, self.player.sight * 2)])

        for x, y, col, ch in self.location.output(x, y):
            term.puts(
                x=x + screen_off_x,
                y=y + screen_off_y,
                s="[c={}]{}[/c]".format(col, ch))

    def draw_player_status(self):
        col, row = 1, 2
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

        # sets the location name at the bottom of the status bar
        if self.player.location in self.world.enterable_legend.keys():
            location = self.world.enterable_legend[self.player.location]
            term.bkcolor('grey')
            term.puts(14, 0, ' ' * (self.width - 14))
            term.bkcolor('black')
            term.puts(
                x=14 + center(surround(location), self.width - 14), 
                y=0, 
                s=surround(location))

        # elif self.player.location in self.world.dungeon_legend.keys():
        #     location = self.world.dungeon_legend[self.player.location]

        # else:
        #     location = ""

        # term.puts(col, row + 20, "{}".format(location))

    def draw_player_profile(self):
        '''Handles player profile screen'''
        term.clear()

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
        term.clear()

        # draws header border
        for i in range(self.width):
            term.puts(i, 1, '#')
        term.puts(center(' inventory ', self.width), 1, ' Inventory ')
        
        for index, (part, item) in enumerate(self.player.equipment()):
            letter = chr(ord('a') + index)
            body_part = ".  {:<10}: ".format(part)
            item_desc = item.__str__() if item else ""

            term.puts(
                x=self.player_screen_col,
                y=self.player_screen_row + index * (2 if self.height > 25 else 1),
                s=letter + body_part + item_desc)

    def draw_player_inventory(self):
        '''Handles inventory screen'''
        term.clear()

        # draws header border for the backpack
        for i in range(self.width):
            term.puts(i, 1, '#')
        term.puts(center('backpack  ', self.width), 1, ' Backpack ')

        for index, item in enumerate(self.player.inventory()):
            letter = chr(ord('a') + index) + ". "
            item_desc = item.__str__() if item else ""

            term.puts(
                x=self.player_screen_col,
                y=self.player_screen_row + index * (2 if self.height > 25 else 1),
                s=letter + item_desc)
    
    def draw_player_screens(self, key):
        playscreen = False
        current_screen = key
        current_range = 0

        while True:
            term.clear()

            if current_screen == "i":
                self.draw_player_equipment()
            elif current_screen == "v":
                self.draw_player_inventory()
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

    def process_handler(self, x, y, k, key):
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
            self.actions[max(0, min(self.player.height, 1))][action]()
        except TypeError:
            self.actions[max(0, min(self.player.height, 1))][action](action)
        except KeyError:
            invalid_command = "'{}' is not a valid command".format(action)
            self.gamelog.add(invalid_command)

    def process_movement(self, x, y):
        turn_inc = 0
        if  self.player.height == Level.World:
            if (x, y) == (0, 0):
                self.gamelog.add("You wait in the area")
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
                    self.gamelog.add(travel_error)
        else:
            if (x, y) == (0, 0):
                self.gamelog.add("You rest for a while")
                turn_inc = True
            else:
                tx = self.player.x + x
                ty = self.player.y + y

                if self.location.walkable(tx, ty):
                    if not self.location.occupied(tx, ty):
                        self.player.move(x, y)
                        if self.location.square(tx, ty).items and random.randint(0, 5):
                            pass_item_messages = [
                                "You pass by an item.",
                                "There is something here."
                                "Your feet touches an object."
                            ]
                            item_message = random.randint(0, len(pass_item_messages) - 1)
                            self.gamelog.add(
                                pass_item_messages[item_message])
                        turn_inc = True
                    else:
                        unit = self.location.get_unit(tx, ty)
                        if unit.friendly:
                            unit.move(-x, -y)
                            self.player.move(x, y)
                            log = "You switch places with the {}".format(
                                unit.race)
                            self.gamelog.add(log)
                        else:
                            chance = self.player.calculate_attack_chance()
                            if chance == 0:
                                log = "You try attacking the {} but miss".format(
                                    unit.race)
                                self.gamelog.add(log)
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
                                    
                                log += "The {} has {} health left. ".format(
                                                        unit.race, 
                                                        max(unit.cur_health, 0))
                                self.gamelog.add(log)

                                if unit.cur_health < 1:
                                    log += "You have killed the {}! ".format(
                                                                    unit.race)
                                    log += "You gain {} exp.".format(unit.xp)
                                    self.gamelog.add(log)
                                    self.player.gain_exp(unit.xp)

                                    if self.player.check_exp():
                                        self.gamelog.add("You level up. You are now level {}".format(self.player.level))
                                        self.gamelog.add("You feel much stronger")

                                    item = unit.drops()

                                    if item:
                                        self.location.square(*unit.position).items.append(item)
                                        self.gamelog.add("The {} has dropped {}".format(
                                                                    unit.race, 
                                                                    item.name))

                                    self.location.remove_unit(unit)
                                else:
                                    log += "The {} has {} health left".format(
                                        unit.race, 
                                        max(0, unit.cur_health))
                                    self.gamelog.add(log)

                                    term.puts(tx + 13, ty + 1, '[c=red]*[/c]')
                                    term.refresh()

                        turn_inc = True
                else:
                    if self.location.out_of_bounds(tx, ty):
                        self.gamelog.add("You reached the edge of the map")
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
                            self.gamelog.add("You cannot swim")
                        else:
                            self.gamelog.add("You walk into {}".format(
                                                                walkChars[ch]))
                            term.puts(tx + 14, ty, '[c=red]X[/c]')
                            # term.refresh()
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
            else:
                self.ret['scene'] = 'main_menu'
                self.proceed = False

        try:
            # discover the command and set as current action
            action = commands[(key, shifted)]
        except KeyError:
            pass

        return action

    def single_element(self, container):
        return len(container) == 1

    def spaces(self, x, y):
        squares = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        space = namedtuple("Space", ("x","y"))
        for i, j in squares:
            yield space(x + i, y + j)

    def action_save(self):
        self.gamelog.add("Save and exit game? (Y/N)")
        self.draw_log()
        term.refresh()
        
        # User input -- confirm selection
        code = term.read()
        if code != term.TK_Y:
            return

        if not os.path.isdir('saves'):
            log = 'saved folder does not exist - creating folder: "./saves"'
            self.gamelog.add(log)
            os.makedirs('saves')
            self.draw_log()
            term.refresh()
    
        # prepare strings for file writing
        # player_hash used for same name / different character saves
        name = self.player.name.replace(' ', '_')
        desc = self.player.job + " " + str(self.player.level)
        file_path = './saves/{}'.format(name + "(" + str(abs(hash(desc)))) + ")"
        
        with shelve.open(file_path, 'n') as save_file:
            save_file['save'] = desc
            save_file['player'] = self.player
            save_file['world'] = self.world
            save_file['turns'] = self.turns  

        self.proceed = False  
        self.ret['scene'] = 'main_menu'
        self.reset()

    def determine_map_location(self):
        print('changing maps')
        if self.player.height == Level.World:
            print('Global map')
            self.location = self.world
        
        else:
            print('local map')
            self.location = self.world.location(*self.player.location)
            if self.player.height > 1:
                print('sub map')
                for i in range(self.player.height - 1):
                    print('went down')
                    self.location = self.location.getSublevel()

        print(self.location)

        self.map_change = False

    def determine_map_on_enter(self, map_type):
        '''Helper function to determine type of wilderness map'''
        try:
            return wilderness[map_type]
        except KeyError:
            raise ValueError("Map Type Not Implemented: {}".format(map_type))

    def determine_map_enterance(self, x, y):
        '''Helper function to determine start position when entering wild'''
        return (max(int(self.location.width * x - 1), 0), 
                max(int(self.location.height * y - 1), 0))

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

                self.player.position = location.getUpStairs()

            else:
                # map type should be in the wilderness
                tile = self.world.square(*self.player.location)
                # neighbors = world.access_neighbors(*player.location)
                
                location = self.determine_map_on_enter(tile.tile_type)(
                    width=term.state(term.TK_WIDTH),
                    height=term.state(term.TK_HEIGHT))

                x, y = self.player.get_position_on_enter()
                self.player.position = self.determine_map_enterance(x, y)
        
            location.addParent(self.world)
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
                self.player.position = location.getUpStairs()

            else:
                # reenter a wilderness
                x, y = self.player.get_position_on_enter()
                self.player.position = self.determine_map_enterance(x, y)
                
        self.player.move_height(1)
        self.map_change = True

    def action_interact_stairs_down(self):
        if self.player.position == self.location.getDownStairs():
            if not self.location.hasSublevel():
                location = Cave(
                    width=self.width,
                    height=self.height,
                    max_rooms=random.randint(15, 20))
                
                location.addParent(self.location)
                self.location.addSublevel(location)

            self.location = self.location.getSublevel()
            self.player.move_height(1)
            self.player.position = self.location.getUpStairs()
        else:
            self.gamelog.add('You cannot go downstairs without stairs')

    def action_interact_stairs_up(self):
        if self.player.location in self.world.enterable_legend.keys():
            self.player.move_height(-1)
            self.location = self.location.getParent()

        elif self.world.location_is(*self.player.location, 2):
            self.player.move_height(-1)
            self.location = self.location.getParent()

        elif self.player.position == self.location.getUpStairs():
            self.player.move_height(-1)
            self.location = self.location.getParent()
        
        else:
            self.gamelog.add('You cannot go upstairs without stairs')
            self.draw_log()
            term.refresh()

        if isinstance(self.location, World):
            self.player.position = (0, 0)

    def action_interact_door_close(self):
        def close_door(i, j):
            self.gamelog.add('Closing door.')
            term.puts(i + 14, j, "[c=red]/[/c]")
            self.location.close_door(i, j)
            self.location.reblock(i, j)

        doors = []
        for i, j in self.spaces(*self.player.position):
            if (i, j) != (self.player.position):
                valid_space = False
                try:
                    if self.location.square(i, j).char == '/':
                        doors.append((i, j))
                except IndexError:
                    self.gamelog.add('Out of bounds ({}, {})'.format(i, j))

        if not doors:
            self.gamelog.add('No open doors next to you')
        elif self.single_element(doors):
            i, j = doors.pop()
            close_door(i, j)
        else:
            self.gamelog.add("There is more than one door near you. Which door?")
            self.draw_log()
            term.refresh()

            code = term.read()
            try:
                cx, cy, a, act = commands[(code, term.state(term.TK_SHIFT))]
                if act == "move" and (x + cx, y + cy) in doors:
                    close_door(x + cx, y + cy)
                else:
                    self.gamelog.add("Canceled closing door.")

            except:
                self.gamelog.add("Canceled closing door.")
                self.log_box()
                term.refresh()

    def action_interact_door_open(self):
        def open_door(i, j):
            self.gamelog.add('Opening door.')
            term.puts(i + 14, j, "[c=red]+[/c]")
            self.location.open_door(i, j)
            self.location.unblock(i, j)
        
        doors = []
        for i, j in self.spaces(*self.player.position):
            if (i, j) != (self.player.position):
                valid_space = False
                try:
                    if self.location.square(i, j).char == "+":
                        doors.append((i, j))
                        
                except IndexError:
                    self.gamelog.add('Out of bounds ({}, {})'.format(i, j))
        
        if not doors:
            self.gamelog.add('No closed doors next to you.')
        elif self.single_element(doors):
            i, j = doors.pop()
            open_door(i, j)
        else:
            self.gamelog.add("There is more than one closed door near you. Which door?")
            self.draw_log()
            term.refresh()

            code = term.read()
            try:
                cx, cy, a, act = commands[(code, term.state(term.TK_SHIFT))]
                if act == "move" and (x + cx, y + cy) in doors:
                    open_door(x + cx, y + cy)
                else:
                    self.gamelog.add("Canceled opening door.")
                    
            except:
                self.gamelog.add("Canceled opening door.")
                self.log_box()
                term.refresh()

    def action_interact_unit_attack_melee(self):
        pass

    def action_interact_unit_attack_ranged(self):
        pass

    def action_interact_unit_displace(self):
        pass

    def action_interact_item_pickup(self, x, y):
        def pickup_item():
            pass

    def action_interact_item_drop(self):
        pass

    def action_interact_item_use(self):
        pass