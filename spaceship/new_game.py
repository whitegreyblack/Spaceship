# main implementation of core mechanics
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.action import commands
from spaceship.setup_game import setup_game
from spaceship.tools import bresenhams, deltanorm, movement
from spaceship.maps.base import hextup, hexone, toInt
from spaceship.maps.base import Map
from spaceship.maps.city import City
from spaceship.maps.wild import *
from spaceship.maps.cave import Cave
from spaceship.item import Item
from spaceship.units.player import Player
from spaceship.create_character import create_character as create
from spaceship.screen_functions import center, surround, selected
from spaceship.dungeon import build_terrain, build_dungeon
from spaceship.setup_game import setup, output, setup_font
from bearlibterminal import terminal as term
from spaceship.gamelog import GameLogger
from random import randint, choice
from collections import namedtuple
from namedlist import namedlist
from spaceship.world import World
from time import clock
from textwrap import wrap
import shelve

# screens:
#   Main Menu
#     Continue, Options, Create Character, New Name
#   Main Game:
#     World, Local, Inventory/Backpack

class Level: Global, World, Local = -1, 0, 1
# class WorldView: Geo, Pol, King = range(3)

def new_game(character=None, world=None, turns=0):
    def save_game(x, y, action):
        nonlocal proceed

        gamelog.add("Save and exit game? (Y/N)")
        log_box()
        term.refresh()
        code = term.read()
        if code != term.TK_Y:
            return

        if not os.path.isdir('saves'):
            print('saved folder does not exist - creating folder: "./saves"')
            os.makedirs('saves')
        # prepare strings for file writing -- player_hash used for same name/different character saves
        name = player.name.replace(' ', '_')
        desc = player.job + " " + str(player.level)
        with shelve.open('./saves/{}'.format(name + "(" + str(abs(hash(desc)))) + ")", 'n') as save_file:
            save_file['save'] = desc
            save_file['player'] = player
            save_file['world'] = calabaston
            save_file['turns'] = turns
        proceed = False

    def refresh(lines=[]):
        for line in lines:
            gamelog.add(line)
        term.clear()
        if player.height == -1:
            world_map_box()
        else:
            map_box()
        status_box()
        log_box()
        term.refresh()

    # END SETUP TOOLS
    # ---------------------------------------------------------------------------------------------------------------------#
    # Keyboard input

    def key_input():
        '''Handles keyboard input and keypress transformation'''
        nonlocal proceed

        key = term.read()
        while key in (term.TK_SHIFT, term.TK_CONTROL, term.TK_ALT):
            # skip any non-action keys
            key = term.read()
        
        if key in (term.TK_ESCAPE, term.TK_CLOSE):
            # exit command -- maybe need a back to menu screen?
            if term.state(term.TK_SHIFT):
                exit('Early Exit')
            else:
                proceed = False
            return tuple(None for _ in range(4))
        elif any(key == press for press, shift in commands.keys()):
            return commands[(key, term.state(term.TK_SHIFT))]
        else:
            return tuple(None for _ in range(4))

    def onlyOne(container):
        return len(container) == 1

    def eightsquare(x, y):
        print(x, y)
        squares = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        space = namedtuple("Space", ("x","y"))
        for i, j in squares:
            print(i, j)
            yield space(x + i, y + j)
        # return [space(x+i,y+j) for i, j in list(num_movement.values())]

    def process_movement(x, y):
        nonlocal player, turns
        if  player.height() == Level.World:
            if (x, y) == (0, 0):
                gamelog.add("You wait in the area")
                turns += 1
            else:
                tx = player.wx + x
                ty = player.wy + y

                if calabaston.walkable(tx, ty):
                    player.save_position_global()
                    player.travel(x, y)
                    turns += 1
                else:
                    travel_error = "You cannot travel there"
                    gamelog.add(travel_error)

        else:
            if (x, y) == (0, 0):
                gamelog.add("You rest for a while")
                turns += 1
            else:
                tx = player.mx + x
                ty = player.my + y

                if dungeon.walkable(tx, ty):
                    if not dungeon.occupied(tx, ty):
                        player.move(x, y)
                        if dungeon.square(tx, ty).items and randint(0, 5):
                            pass_item_messages = [
                                "You pass by an item.",
                                "There is something here."
                                "Your feet touches an object."
                            ]
                            gamelog.add(pass_item_message[randint(0, len(pass_item_messages)-1)])
                        turns += 1
                    else:
                        unit = dungeon.get_unit(tx, ty)
                        if unit.friendly():
                            unit.move(-x, -y)
                            player.move(x, y)
                            gamelog.add("You switch places with the {}".format(unit.job))
                        else:
                            if player.calculate_attack_chance() == 0:
                                gamelog.add("You try attacking the {} but miss".format(unit.job))
                            else:
                                damage = player.calculate_attack_damage() * (2 if chance == 2 else 1)
                                unit.health -= damage
                                log = "You {} attack the {} for {} damage. ".format(
                                    "crit and" if chance == 2 else "", unit.job, damage)
                                log += "The {} has {} health left".format(unit.job, max(unit.health, 0))
                                gamelog.add(log)

                                if unit.health < 1:
                                    gamelog.add("You have killed the {}! You gain {} exp".format(unit.job, unit.xp))
                                    player.gain_exp(unit.xp)

                                    if player.check_exp():
                                        gamelog.add("You level up. You are now level {}".format(player.level))
                                        gamelog.add("You feel much stronger")

                                    item = unit.drops()

                                    if item:
                                        dungeon.square(*unit.position()).items.append(item)
                                        gamelog.add("The {} has dropped {}".format(unit.job, item.name))

                                    dungeon.remove_unit(unit)
                        turns += 1
                else:
                    if dungeon.out_of_bounds(tx, ty):
                        gamelog.add("You reached the edge of the map")
                    else:
                        walkChars = {
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
                        ch = dungeon.square(tx, ty).char
                        if ch == "~":
                            gamelog.add("You cannot swim")
                        else:
                            gamelog.add("You walk into {}".format(walkChars[ch]))

    def key_process(x, y):
        walkChars = {
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

        walkBlock = "walked into {}"
        tposx = player.mx + x
        tposy = player.my + y

        # 3 variables involved in walking
        # OUT-OF-BOUNDS -- is player within the map?
        # WALKABLE -- is the tile a walkable tile?
        # BLOCKEd -- is the tile blocked?
        walkable = dungeon.walkable(tposx, tposy)
        if walkable:
            occupied = dungeon.occupied(tposx, tposy)
            if not occupied:
                player.move(x, y)

                if dungeon.square(tposx, tposy).items and randint(0, 1):
                    # randint condition to give off a chance for message print
                    gamelog.add("There is something here")

            else:
                unit = dungeon.get_unit(tposx, tposy)

                if unit.friendly():
                    gamelog.add("You displace the {}".format(unit.job))
                    unit.move(-x, -y)
                    player.move(x, y)

                else:
                    chance = player.calculate_attack_chance()

                    if chance == 0:
                        gamelog.add("You try attacking the {} but miss".format(unit.job))

                    else:
                        damage = player.calculate_attack_damage() * (2 if chance == 2 else 1)
                        unit.health -= damage
                        log = "You {} attack the {} for {} damage. ".format(
                            "crit and" if chance == 2 else "", unit.job, damage)
                        log += "The {} has {} health left".format(unit.job, max(unit.health, 0))
                        gamelog.add(log)

                        if unit.health < 1:
                            gamelog.add("You have killed the {}! You gain {} exp".format(unit.job, unit.xp))
                            player.gain_exp(unit.xp)

                            if player.check_exp():
                                gamelog.add("You level up. You are now level {}".format(player.level))
                                gamelog.add("You feel much stronger")

                            item = unit.drops()

                            if item:
                                dungeon.square(*unit.position()).items.append(item)
                                gamelog.add("The {} has dropped {}".format(unit.job, item.name))

                            dungeon.remove_unit(unit)
       
        else:
            if dungeon.out_of_bounds(tposx, tposy):
                # out of bounds error
                gamelog.add("Reached the edge of the map")

            else:
                # block error -- differentiate between land and water blocks
                ch = dungeon.square(tposx, tposy).char

                if ch == "~":
                    gamelog.add('you cannot swim')
                else:
                    gamelog.add(walkBlock.format(walkChars[ch]))

        for unit in list(dungeon.get_units()):
            x, y = 0, 0
            if randint(0, 1):
                # if true then the unit is moving
                x, y = num_movement[choice(list(num_movement.keys()))]
                tposx, tposy = unit.x + x, unit.y + y
                walkable = dungeon.walkable(tposx, tposy)

                if walkable:
                    occupied = dungeon.occupied(tposx, tposy) or \
                        (tposx, tposy) == player.position_local()

                    if not occupied:
                        unit.move(x, y)

                    else:
                        if (tposx, tposy) == player.position_local():
                            other = player

                        else:
                            other = dungeon.get_unit(tposx, tposy)

                            if other.unit_id == unit.unit_id:
                                # make sure the unit being compared is not itself
                                continue

                        if unit.friendly():
                            # other.move(-x, -y)
                            # unit.move(x, y)
                            unit.displace(other, x, y)

                        else:
                            other.health -= 1
                            
                            log = "The {}({}) attacks {}({}). ".format(
                                unit.job, unit.unit_id,
                                "you" if other == player else ("the " + other.job),
                                other.unit_id)
                            log += "{} {} health left".format(
                                "You have " if other == player else "the " + other.job + " has",
                                player.health if other == player else other.health)
                            gamelog.add(log)

                            if other.health < 1:
                                gamelog.add("The {} has killed {}".format(
                                    unit.job,
                                    "you" if other == player else "the " + other.job))

                                if other == player:
                                    gamelog.add("You Died!")
                                else:
                                    dungeon.remove_unit(other)

    def open_player_screen(x, y, key):
        '''Game function to handle player equipment and inventory'''
        def profile():
            '''Handles player profile screen'''
            term.clear()

            for i in range(screen_width):
                term.puts(i, 1, '#')
            term.puts(center('profile  ', screen_width), 1, ' Profile ')

            for colnum, column in enumerate(list(player.get_profile())):
                term.puts(col + (20 * colnum), row, column)

        def inventory():
            '''Handles inventory screen'''
            term.clear()

            # title backpack
            for i in range(screen_width):
                term.puts(i, 1, '#')
            term.puts(center('backpack  ', screen_width), 1, ' Backpack ')

            for index, item in player.get_inventory():
                letter = chr(ord('a') + index) + ". "
                item_desc = item.__str__() if item else ""

                term.puts(
                    col,
                    row + index * (2 if screen_height > 25 else 1),
                    letter + item_desc)

        def equipment():
            '''Handles equipment screen'''
            term.clear()

            for i in range(screen_width):
                term.puts(i, 1, '#')

            term.puts(center(' inventory ', screen_width), 1, ' Inventory ')
            
            for index, part, item in player.get_equipment():
                letter = chr(ord('a') + index)
                body_part = ".  {:<10}: ".format(part)
                item_desc = item.__str__() if item else ""

                term.puts(
                    col,
                    row + index * (2 if screen_height > 25 else 1),
                    letter + body_part + item_desc)

        col, row = 1, 3
        playscreen = False
        current_screen = key
        current_range = 0
        while True:
            term.clear()

            if current_screen == "i":
                equipment()
            elif current_screen == "v":
                inventory()
            else:
                profile()

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

    def attackUnit(x, y, k):
        nonlocal turns
        def attack(x, y):
            unit = dungeon.get_unit(x, y)
            log = "You attack the {}. ".format(unit.job)
            unit.health -= 1           
            log += "The {} has {} health left. ".format(unit.job, unit.health)
            if dungeon.maptype == "city":
                dungeon.reduce_unit_relationships(100)
                # dungeon.reduce_relationship(100)
                log += "Your relationship with {} has decreased by {} ".format(
                    dungeon.map_name, 100)
            for l in wrap(log, width=screen_width):
                gamelog.add(l)

            # if unit.r is not "human": # condition should be more complex
            if unit.health < 1:
                gamelog.add("You have killed the {}! You gain 15 exp".format(unit.job))
                dungeon.remove_unit(unit)

        attackables = []
        for i, j in eightsquare(x, y):
            if (i, j) != (x, y) and dungeon.get_unit(i, j):
                attackables.append((i, j))
        
        if not attackables:
            gamelog.add("Nothing you can attack. You want to punch the floor?")
        
        elif onlyOne(attackables):
            attack(*attackables.pop())

        else:
            gamelog.add("Who do you want to attack?")
            code = term.read()
            if code in key_movement:
                cx, cy = key_movement[code]
            elif code in num_movement:
                cx, cy = num_movement[code]
            else:
                return
            if (x+cx, y+cy) in attackables:
                attack(x + cx, y + cy)

        turns += 1

    def interactUnit(x, y, action):
        """Allows talking with other units"""
        def talkUnit(x, y):
            unit = dungeon.get_unit(x, y)
            gamelog.add(unit.talk())
            # gamelog.add(um.talkTo(x, y))
            refresh()

        interactables = []
        for i, j in eightsquare(x, y):
            # dungeon.has_unit(i, j) -> returns true or false if unit is on the square
            if (i, j) != (x, y) and dungeon.get_unit(i, j):
                interactables.append((i, j))

        # no interactables
        if not interactables:
            gamelog.add("No one to talk with")

        # only one interactable
        elif onlyOne(interactables):
            # i, j = interactables.pop()
            talkUnit(*interactables.pop())

        # many interactables
        else:
            gamelog.add("Which direction?")   
            refresh()
            code = term.read()

            if code in key_movement:
                cx, cy = key_movement[code]
            elif code in num_movement:
                cx, cy = num_movement[code]
            else:
                return

            if (x+cx, y+cy) in interactables:
                talkUnit(x+cx, y+cy)

    def interactItem(x, y, key):
        nonlocal turns
        def pickItem():
            item = dungeon.square(x, y).items.pop()
            player.inventory.append(item)
            gamelog.add("You pick up a {}".format(item.name))
        
        if key == ",": # pickup
            # if player.backpack.full():
            if len(player.inventory) >= 25:
                # earlly exit
                gamelog.add("Backpack is full")
                return

            items = dungeon.square(x, y).items
            if items:
                if len(items) == 1:
                    pickItem()
                # TODO                
                # else:
                #     glog.add("opening pick up menu")
                #     pick_menu(items)
            else:
                gamelog.add("Nothing to pick up")
        turns += 1

    def interactDoor(x, y, key):
        """Allows interaction with doors"""
        nonlocal turns
        def openDoor(i, j):
            gamelog.add("Opened door")
            dungeon.open_door(i, j)
            dungeon.unblock(i, j)

        def closeDoor(i, j):
            gamelog.add("Closed door")
            dungeon.close_door(i, j)
            dungeon.reblock(i, j)

        char = "+" if key is "o" else "/"

        reachables = []
        for i, j in eightsquare(x, y):
            if (i, j) != (x, y):
                isSquare = 0
                try:
                    isSquare = dungeon.square(i, j).char is char
                except IndexError:
                    gamelog.add("out of bounds ({},{})".format(i, j))
                if isSquare:
                    reachables.append((i, j))

        if not reachables:
            gamelog.add("No {} near you".format("openables" if key is "o" else "closeables"))
        
        elif onlyOne(reachables):
            i, j = reachables.pop()
            openDoor(i, j) if key is "o" else closeDoor(i, j)

        else:
            gamelog.add("There is more than one door near you. Which direction?")
            log_box()
            term.refresh()
            code = term.read()

            if code in key_movement:
                cx, cy = key_movement[code]
            elif code in num_movement:
                cx, cy = num_movement[code]
            else:
                return

            if (x+cx, y+cy) in reachables:
                openDoor(x+cx, y+cy) if key is 'o' else closeDoor(x+cx, y+cy)

        turns += 1
        # map_box()

    def interactStairs(x, y, k):
        nonlocal dungeon
        """Allows interactions with stairs"""

        if k == ">":  
            #  differentiate going up versus down
            if player.position_local() == dungeon.getDownStairs():                

                if not dungeon.hasSublevel():
                    sublevel = Cave(
                        width=term.state(term.TK_WIDTH),
                        height=term.state(term.TK_HEIGHT),
                        max_rooms=randint(15, 20))

                    sublevel.addParent(dungeon)
                    dungeon.addSublevel(sublevel)

                dungeon = dungeon.getSublevel()
                player.move_height(1)
                player.reset_position_local(*dungeon.getUpStairs())

            else:
                gamelog.add('You cannot go downstairs without stairs.')
                
        else:
            # map at the location exists -- determine type of map
            if player.position_global() in calabaston.enterable_legend.keys():
                # check if you're in a city
                player.move_height(-1)
                dungeon = dungeon.getParent()

            elif calabaston.is_wilderness(*player.position_global()):
                # check for wilderness type map
                player.move_height(-1)
                dungeon = dungeon.getParent()

            elif player.position_local() == dungeon.getUpStairs():
                # check if you're in a dungeon
                # dungeon will have parent -- need to differentiate between
                # world and first level dungeon
                player.move_height(-1)
                dungeon = dungeon.getParent()

            else:
                gamelog.add('You cannot go upstairs without stairs.')

            if isinstance(dungeon, World):
                # we unrefrence the dungeon only if it is at level 0
                dungeon = None
                player.reset_position_local(0, 0)

    def enter_map(x, y, a):
        '''Logic:
            if at world level, check if there exists a map
            if exists -> enter
            else -> build the map and add it to the world
        '''
        def determine_map(map_type):
            '''Helper function to determine wilderness map'''
            if map_type == "plains":
                return Plains
            elif map_type == "grassland":
                return Grassland
            elif map_type == "forest":
                return Forest
            elif map_type == "dark woods":
                return Woods
            elif map_type == "hills":
                return Hills
            else:
                raise ValueError("Map Type Not Implemented: {}".format(map_type))

        def get_wilderness_enterance(x, y):
            '''Helper function to determine start position when entering wilderness map'''
            return (max(int(location.width * x - 1), 0), 
                    max(int(location.height * y - 1), 0))

        if not calabaston.mapAt(*player.position_global()):
            # map does not exist yet -- create one
            if player.position_global() in calabaston.enterable_legend.keys():
                # map type should be a city
                fileloc = calabaston.enterable_legend[player.position_global()].lower().replace(' ','_')
                img_name = "./assets/maps/" + fileloc + ".png"
                cfg_name = "./assets/maps/" + fileloc + ".cfg"

                location = City(
                    map_id=fileloc,
                    map_img=img_name,
                    map_cfg=cfg_name,
                    width=term.state(term.TK_WIDTH), 
                    height=term.state(term.TK_HEIGHT))

                player.reset_position_local(location.width // 2, location.height // 2)

            elif player.position_global() in calabaston.dungeon_legend.keys():
                # map type should be a cave
                location = Cave(
                    width=term.state(term.TK_WIDTH),
                    height=term.state(term.TK_HEIGHT),
                    max_rooms=randint(15, 20))

                player.reset_position_local(*location.getUpStairs())

            else:
                # map type should be in the wilderness
                tile = calabaston.access(*player.position_global())
                # neighbors = calabaston.access_neighbors(*player.position_global())
                
                location = determine_map(tile.land)(
                    width=term.state(term.TK_WIDTH),
                    height=term.state(term.TK_HEIGHT))

                x, y = player.get_position_global_on_enter()
                player.reset_position_local(*get_wilderness_enterance(x, y))
        
            location.addParent(calabaston)
            calabaston.add_location(location, *(player.position_global()))

        else:
            # location already been built -- retrieve from world map_data
            # player position is different on map enter depending on map location
            location = calabaston.get_location(*player.position_global())
            if player.position_global() in calabaston.enterable_legend.keys():
                # re-enter a city
                player.reset_position_local(location.width // 2, location.height // 2)

            elif player.position_global() in calabaston.dungeon_legend.keys():
                # re-enter dungeon
                player.reset_position_local(*location.getUpStairs())

            else:
                # reenter a wilderness
                x, y = player.get_position_global_on_enter()
            
                player.reset_position_local(*get_wilderness_enterance(x, y))
                
        player.move_height(1)
    
    actions={
        0: {
            '>': enter_map,
            '@': open_player_screen,
            'i': open_player_screen,
            'v': open_player_screen,
            'S': save_game,
        },
        1: {
            '>': interactStairs,
            '<': interactStairs,
            'a': attackUnit,
            'o': interactDoor,
            'c': interactDoor,
            ',': interactItem,
            '@': open_player_screen,
            'i': open_player_screen,
            'v': open_player_screen,
        },
    }

    def process_action(player, action):
        nonlocal turns
        try:
            if player.height() == Level.World:
                actions[max(0, min(player.height(), 1))][action](player.wx, player.wy, action)
            else:
                actions[max(0, min(player.height(), 1))][action](player.mx, player.my, action)
        except KeyError:
            gamelog.add("Invalid CommanD")
    # End Keyboard Functions
    # ---------------------------------------------------------------------------------------------------------------------#
    # Graphic functions

    def graphics(integer: int) -> None:
        def toBin(n):
            return list(bin(n).replace('0b'))
        if not 0 < integer < 8:
            raise ValueError("Must be within 0-7")

    def border():
        # status border
        border_line =  "[color=dark #9a8478]"+chr(toInt("25E6"))+"[/color]"

        # y axis
        for i in range(0, 80, 2):
            if i < 20:
                term.puts(screen_width - 20 + i, 0, border_line)
                term.puts(screen_width - 20 + i, 10, border_line)
            if i < 60:
                term.puts(i, screen_height - 6, border_line)
            term.puts(i, screen_height - 1, border_line)
        
        # x axis
        for j in range(35):
            if j < 6:
                term.puts(0, screen_height - 6 + j, border_line)
            term.puts(screen_width - 20, j, border_line)
            term.puts(screen_width - 1, j, border_line)

    def status_box():
        col, row = 1, 2
        term.puts(col, row - 1, player.name)
        term.puts(col, row + 0, player.gender)
        term.puts(col, row + 1, player.race)
        term.puts(col, row + 2, player.job)

        term.puts(col, row + 4, "LVL: {:>6}".format(player.level))
        term.puts(col, row + 5, "EXP: {:>6}".format("{}/{}".format(player.exp, player.advexp)))

        term.puts(col, row + 7, "HP:  {:>6}".format("{}/{}".format(player.hp, player.total_hp)))
        term.puts(col, row + 8, "MP:  {:>6}".format("{}/{}".format(player.mp, player.total_mp)))
        term.puts(col, row + 9, "SP:  {:>6}".format(player.sp))

        term.puts(col, row + 11, "STR: {:>6}".format(player.str)) 
        term.puts(col, row + 12, "CON: {:>6}".format(player.con))
        term.puts(col, row + 13, "DEX: {:>6}".format(player.dex))
        term.puts(col, row + 14, "INT: {:>6}".format(player.int))
        term.puts(col, row + 15, "WIS: {:>6}".format(player.wis))
        term.puts(col, row + 16, "CHA: {:>6}".format(player.cha))

        term.puts(col, row + 18, "GOLD:{:>6}".format(player.gold))

        # sets the location name at the bottom of the status bar
        if player.position_global() in calabaston.enterable_legend.keys():
            location = calabaston.enterable_legend[player.position_global()]
            term.bkcolor('grey')
            term.puts(0, 0, ' ' * screen_width)
            term.bkcolor('black')
            term.puts(center(surround(location), screen_width), 0, surround(location))

        elif player.position_global() in calabaston.dungeon_legend.keys():
            location = calabaston.dungeon_legend[player.position_global()]

        else:
            location = ""

        term.puts(col, row + 20, "{}".format(location))

    def log_box():
        nonlocal turns
        messages = gamelog.write().messages
        if messages:
            for idx in range(len(messages)):
                # offput by 1 for border and then # of lines logger is currently set at
                term.puts(
                    14 if player.height() == -1 else 1, 
                    screen_height - len(messages) + idx, 
                    messages[idx][1])

        term.puts(1, screen_height-3, 'Turns: {:<4}'.format(turns))

    def map_box():
        term.composition(False)
        dungeon.fov_calc([(player.mx, player.my, player.sight * 2)])

        for x, y, lit, ch in dungeon.output(player.mx, player.my, []):
            term.puts(x + 13, y + 1, "[color={}]".format(lit) + ch + "[/color]")

        # term.refresh()refresh()
        
    def world_legend_box():
        length, offset, height = 14, 12, 0
        world_name = surround(calabaston.name, length=length)
        selected(center(world_name, offset), height, world_name)   

        height += 1        
        # this is purely a ui enhancement. Actually entering a city is not that much different
        # than entering a dungeon/wilderness area
        if player.position_global() in calabaston.enterable_legend.keys():
            # check if player position is over a city/enterable area
            city_name = calabaston.enterable_legend[player.position_global()]
            enterable_name = surround(city_name, length=length)
            selected(center(enterable_name, offset), height, enterable_name)
            # try:
            #     gamelog.add(calabaston.city_descriptions[city_name])
            # except:
            #     gamelog.add("\n\n")

        elif player.position_global() in calabaston.dungeon_legend.keys():
            # check if player position is over a dungeon position
            dungeon_name = surround(calabaston.dungeon_legend[player.position_global()], length=length)
            selected(center(dungeon_name, offset), height, dungeon_name)

        else:
            # Add land types to the overworld ui
            landtype = surround(calabaston.get_landtype(*player.position_global()), length=length)
            selected(center(landtype, offset), height, landtype)
            

        for char, color, desc, i in calabaston.legend():
            # finally print the lengend with character and description
            term.puts(0, height + i + 2, "[c={}] {}[/c] {}".format(color, char, desc))

    def world_map_box():
        '''Displays the world map tiles in the terminal'''
        screen_off_x, screen_off_y = 14, 0
        for x, y, col, ch in calabaston.draw(*(player.position_global())):
            term.puts(
                x + screen_off_x, 
                y + screen_off_y, 
                "[c={}]{}[/c]".format(col, ch))

    screen_width, screen_height = term.state(term.TK_WIDTH), term.state(term.TK_HEIGHT)
    
    # very first thing is game logger initialized to output messages on terminal
    gamelog = GameLogger(3 if term.state(term.TK_HEIGHT) <= 25 else 4)

    # process character
    if not character:
        # improperly accessed new_game --> early exit
        return output(proceed=False, value="No Character Data Input")

    if not world:
        # unpack character tuple to create a player object
        player = Player(character)

        # create the world from scratch
        # TODO: chain function so World().load() or keep as seperate functions: init() and load()?
        calabaston = World(screen_width, screen_height)
        calabaston.load(
                    "./assets/worldmap.png", 
                    "./assets/worldmap_territories.png",
                    "./assets/worldmap_kingdoms.png")   

    else:
        # coming from a save file -- player object already defined
        player = character

        # coming from a save file -- world already definied
        calabaston = world    

        # coming from a save file -- turns already defined
        turns = turns

    proceed = True
    dungeon = None
    
    '''
    while True:
        clear()
        render()
        refresh()
        
        for unit in unitlist:
            unit.take_turn
    '''
    while proceed:
        term.clear()
        if player.height() == Level.World:
            gamelog.maxlines = 2
            world_map_box()
            world_legend_box()
            log_box()
        else:
            gamelog.maxlines = 4 if term.state(term.TK_HEIGHT) > 25 else 2
            if dungeon == None:
                # player.move_height(-1)
                dungeon = calabaston.get_location(*player.position_global())
                # player.move_height(1)

                if player.height() == 0:
                    # iterates down until sublevel is found
                    for i in range(player.height()):
                        dungeon = dungeon.getSublevel()
                        
            map_box()
            status_box()
            log_box()

        term.refresh()

        # handle player movements and action
        x, y, k, action = key_input()
        if k is not None:
            process_action(player, k)

        elif all(z is not None for z in [x, y]):
            process_movement(x, y)

        else:
            print('Command not yet implemented')

        if not proceed:
            break

        # for all units -- do action
        if player.height() != Level.World and dungeon:
            dungeon.process_unit_actions()

    # player.dump()
    # gamelog.dumps()           
    return "Safe Exit"
# End New Game Menu

if __name__ == "__main__":
    setup()
    setup_font('unscii-8', 8, 16)
    character = create().value
    setup_game()
    setup_font('unscii-8-thin', 8, 16)

    # setup_font('unscii-8', 8 ,8)
    new_game(character)
