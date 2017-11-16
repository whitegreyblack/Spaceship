# main implementation of core mechanics
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.action import key_movement, num_movement, key_actions, action, keypress, world_key_actions, key_shifted_actions
from spaceship.setup_game import setup_game
from spaceship.tools import bresenhams, deltanorm, movement
from spaceship.maps.base import hextup, hexone, toInt
from spaceship.maps.base import Map
from spaceship.maps.city import City
from spaceship.maps.wild import *
from spaceship.maps.cave import Cave
from spaceship.item import Item
from spaceship.player import Player
from spaceship.create_character import create_character as create
from spaceship.screen_functions import center, surround, selected
from bearlibterminal import terminal as term
from spaceship.gamelog import GameLogger
from random import randint, choice
from collections import namedtuple
from namedlist import namedlist
from spaceship.dungeon import build_terrain, build_dungeon
from spaceship.setup_game import setup, output, setup_font
from spaceship.world import World
from time import clock
from textwrap import wrap


# screens:
#   Main Menu
#     Continue, Options, Create Character, New Name
#   Main Game:
#     World, Local, Inventory/Backpack

class Level: World, City, Dungeon = range(3)
class WorldView: Geo, Pol, King = range(3)

debug = False

def new_game(character=None):

    def refresh(lines=[]):
        for line in lines:
            gamelog.add(line)
        term.clear()
        map_box()
        status_box()
        log_box()
        term.refresh()

    # END SETUP TOOLS
    # ---------------------------------------------------------------------------------------------------------------------#
    # Keyboard input

    def key_in_world():
        '''Key processing while player in overworld'''
        nonlocal proceed, exit_status
        keydown = namedtuple("Key_Press", "x y a")
        act, x, y = 0, 0, 0
        code = term.read()

        while code in (term.TK_SHIFT, term.TK_CONTROL, term.TK_ALT):
            code = term.read()
        if code in (term.TK_CLOSE, term.TK_ESCAPE, term.TK_Q):
            proceed = False
            exit_status = True
        # map draw types
        # elif code in (term.TK_P, term.TK_G, term.TK_K):
        #     if code == term.TK_P and wview != WorldView.Pol:
        #         wview = WorldView.Pol
        #     elif code == term.TK_G and wview != WorldView.Geo:
        #         wview = WorldView.Geo
        #     else:
        #         wview = WorldView.King
        #     act = "Do Nothing"
        
        # elif code in (term.TK_COMMA, term.TK_PERIOD):
        #     if code == term.TK_COMMA and term.state(term.TK_SHIFT):
        #         act = "exit"
        #     elif code == term.TK_PERIOD and term.state(term.TK_SHIFT):
        #         act = "enter"
        # ENTER/EXIT COMMAND
        elif code in (term.TK_PERIOD,):
            if term.state(term.TK_SHIFT):
                try:
                    act = world_key_actions[code].key
                except KeyError:
                    raise
        # elif code == term.TK_Z:
        #     act = "Zoom"
        
        # MOVEMENT using ARROW KEYS
        elif code in key_movement:
            x, y = key_movement[code]
        # MOVEMENT using NUMBERPAD keys
        elif code in num_movement:
            x, y = num_movement[code]

        # keyboard keys
        # elif code in key_actions:
        #     act = key_actions[code].key
        # any other key F-keys, Up/Down Pg, etc
        else:
            if code in (term.TK_2,):
                print("clicked 2")
            gamelog.add("unrecognized command")
                
        # make sure we clear any inputs before the next action is processed
        # allows for the program to go slow enough for human playability
        while term.has_input(): 
            term.read()
        if debug:
            gamelog.add("KEY-IN-WORLD: {}, {}, {}".format(x, y, act))
        return keydown(x, y, act)

    def key_in():
        '''Key Processing while player in local map'''
        nonlocal proceed, exit_status
        keydown = namedtuple("Key_Down", ("x", "y", "a"))
        act, x, y = 0, 0, 0
        code = term.read()

        while code in (term.TK_SHIFT, term.TK_CONTROL, term.TK_ALT):
            code = term.read()
        
        # if any([term.state(tk) for tk in (term.TK_SHIFT, term.TK_CONTROL, term.TK_ALT)]):
        #     if debug:
        #         gamelog.add("CTRL | ALT | SHIFT")
        
        if code in (term.TK_ESCAPE, term.TK_CLOSE):
            if term.state(term.TK_SHIFT):
                exit("Easy Exit")
            # gamelog.dumps()
            # proceed = False
            pass

        elif code in key_movement:
            # arrow keys
            x, y = key_movement[code]
        elif code in num_movement:
            # numberpad keys
            x, y = num_movement[code]
        elif code in key_actions and not term.state(term.TK_SHIFT):
            # keyboard keys
            act = key_actions[code].key
        elif code in key_shifted_actions and term.state(term.TK_SHIFT):
            # keyboard shifted keys
            act = key_shifted_actions[code].key
        else:
            # any other key F-keys, Up/Down Pg, etc        
            gamelog.add("unrecognized command")
        
        # make sure we clear any inputs before the next action is processed
        # allows for the program to go slow enough for human playability
        while term.has_input(): 
            term.read()

        return keydown(x, y, act)

    def key_input(level):
        '''Try creating a general purpose key input function that is called by both
        world and map functions
        '''
        nonlocal proceed

        keydown = namedtuple("Key_Down", ("x", "y", "a"))
        act, x, y = 0, 0, 0

        code = term.read()
        while code in (term.TK_SHIFT, term.TK_CONTROL, term.TK_ALT):
            # skip any non-action keys
            code = term.read()
        
        if code in (term.TK_ESCAPE, term.TK_CLOSE):
            # exit command -- maybe need a back to menu screen?
            proceed = False
    

        return

    def onlyOne(container):
        return len(container) == 1

    def eightsquare(x, y):
        space = namedtuple("Space", ("x","y"))
        for i, j in num_movement.values():
            yield space(x + i, y + j)
        # return [space(x+i,y+j) for i, j in list(num_movement.values())]

    def key_process_world(x, y):
        walkBlock = "walked into {}"
        tx = player.wx + x
        ty = player.wy + y

        # inbounds = 0 <= tx < calabaston.w and 0 <= ty < calabaston.h
        walkable = calabaston.walkable(tx, ty) # checks bounds and blocked tiles

        if walkable:
            player.save_position_global()
            player.travel(x, y)
            # description = calabaston.tilehasdescription(tposx, tposy)
            # if description:
            #     gamelog.add(description)
        else:
            # Individually log the specific reason
            sentence = "You cannot move there"
            gamelog.add(sentence)
            # if blocked:
                # =============  START WALK LOG  =================================
                # gamelog.add("Cannot go there {}, {}".format(tx, ty))
                # ===============  END WALK LOG  =================================
            # elif not inbounds:
            #     gamelog.add(walkBlock.format("the edge of the map"))
            #     print("cannot go there", tx, ty)
            gamelog.add("Not walkable")

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

# ================================= START COMBAT LOG ===================================================================
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
# ========================== END COMBAD LOG ============================================================================
# =========================  START WALK LOG  ===========================================================================
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
# ===========================  END WALK LOG  ===========================================================================

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

    def open_player_screen(key):
        '''Game function to handle player equipment and inventory'''
        def profile():
            '''Handles player profile screen'''
            term.clear()

            for i in range(screen_width):
                term.puts(i, 1, '#')
            term.puts(center('profile  ', screen_width), 1, ' Profile ')

            term.puts(col, row, player.get_profile())

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

    def interactUnit(x, y):
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

    def interactDoor(x, y, key):
        """Allows interaction with doors"""
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

        map_box()

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

    def enter_map():
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

    world_actions={
        # '<': exit_map,
        '>': enter_map
    }
    def processWorldAction(key):
        if key == ">":
            world_actions[key]()

    actions={
        'a': attackUnit,
        'o': interactDoor,
        'c': interactDoor,
        'i': open_player_screen,
        'v': open_player_screen,
        't': interactUnit,
        '>': interactStairs,
        '<': interactStairs,
        '@': open_player_screen,
        # 'f1': dungeon._sundown,
        # 'f2': dungeon._sunup,
        ',': interactItem,
    }

    def processAction(x, y, key):
        if key in ("o", "c"):
            actions[key](x, y, key)
        elif key in ("a"):
            actions[key](x, y, key)
        elif key in ("<", ">"):
            actions[key](x, y, key)
        elif key in (","):
            actions[key](x, y, key)
        elif key in ("t"):
            actions[key](x, y)
        elif key in ("i", "v", "@"):
            actions[key](key)
        elif key in ("f1, f2"):
            actions[key]()
        else:
            gamelog.add('invalid command')

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

    turn = 0
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

        elif player.position_global() in calabaston.dungeon_legend.keys():
            location = calabaston.dungeon_legend[player.position_global()]

        else:
            location = ""

        term.puts(col, row + 20, "{}".format(location))

    def log_box():
        messages = gamelog.write().messages
        if messages:
            for idx in range(len(messages)):
                # offput by 1 for border and then # of lines logger is currently set at
                term.puts(
                    14 if player.height() == -1 else 1, 
                    screen_height - len(messages) + idx, messages[idx])

    def map_box():
        term.composition(False)
        dungeon.fov_calc([(player.mx, player.my, player.sight * 2)])

        for x, y, lit, ch in dungeon.output(player.mx, player.my, []):
            term.puts(x + 13, y, "[color={}]".format(lit) + ch + "[/color]")

        term.refresh()
        
    def world_legend_box():
        length, offset, height = 14, 12, 0
        world_name = surround(calabaston.name, length=length)
        selected(center(world_name, offset), height, world_name)   

        height += 1        
        # this is purely a ui enhancement. Actually entering a city is not that much different
        # than entering a dungeon/wilderness area
        if player.position_global() in calabaston.enterable_legend.keys():
            # check if player position is over a city/enterable area
            enterable_name = surround(calabaston.enterable_legend[player.position_global()], length=length)
            selected(center(enterable_name, offset), height, enterable_name)

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

    # very first thing is game logger initialized to output messages on terminal
    gamelog = GameLogger(3 if term.state(term.TK_HEIGHT) <= 25 else 4)

    # process character
    if character==None:
        # mproperly accessed new_game --> early exit
        return output(proceed=False, value="No Character Data Input")
    else:
        # unpack character tuple to create a player object
        player = Player(character)
    
    screen_width, screen_height = term.state(term.TK_WIDTH), term.state(term.TK_HEIGHT)

    # TODO: chain function so World().load() or keep as seperate functions: init() and load()?
    calabaston = World(screen_width, screen_height)
    calabaston.load(
                "./assets/worldmap.png", 
                "./assets/worldmap_territories.png",
                "./assets/worldmap_kingdoms.png")   

    proceed = True
    exit_status = None
    dungeon = None
    while proceed:
        term.clear()
        if player.height() == -1:
            if gamelog.maxlines == 2:
                gamelog.maxlines = 1
            # World View
            world_map_box()
            world_legend_box()
            log_box()
            term.refresh()

            x, y, a = key_in_world()
            if a != "Do Nothing" and a != 0:
                processWorldAction(a)

            elif (x, y) != (0, 0):
                key_process_world(x, y)

        else:
            # player is on local map level
            # world map screen size differs to local map size
            # we change the number of log lines to fit the terminal
            if gamelog.maxlines == 3:
                gamelog.maxlines = 4 if term.state(term.TK_HEIGHT) > 25 else 3

            if dungeon == None:
                # previous dungeon was unrefrenced or first time visiting local map
                player.move_height(-1)
                dungeon = calabaston.get_location(*player.position_global())
                player.move_height(1)

                if player.wz > 0:
                    # iterates down until sublevel is found
                    for i in range(player.wz):
                        dungeon = dungeon.getSublevel()

            # ui boxes
            status_box()
            log_box()
            map_box()
            
            x, y, a = key_in()

            if a:
                # non-movement action
                processAction(player.mx, player.my, a)

            else:
                # movement first action
                key_process(x, y)

    # player.dump()
    # gamelog.dumps()           
    return True
# End New Game Menu

if __name__ == "__main__":
    setup()
    setup_font('unscii-8', 8, 16)
    character = create().value
    setup_game()
    setup_font('unscii-8-thin', 8, 16)

    # setup_font('unscii-8', 8 ,8)
    new_game(character)
