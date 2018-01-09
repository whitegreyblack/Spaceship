# main implementation of core mechanics
import shelve
from random import randint, choice
from collections import namedtuple
from namedlist import namedlist
from time import clock, sleep
from textwrap import wrap
from bearlibterminal import terminal as term

from .action import commands

from .classes.utils import hextup, hexone
from .classes.map import Map
from .classes.world import World
from .classes.wild import wilderness
from .classes.cave import Cave
from .classes.city import City
from .classes.item import Item
from .classes.player import Player

from .setup_game import setup, output, setup_font, setup_game
from .tools import bresenhams, deltanorm, movement, toInt
from .create_character import create_character as create
from .screen_functions import center, surround, selected
from .dungeon import build_terrain, build_dungeon
from .gamelog import GameLogger


# screens:
#   Main Menu
#     Continue, Options, Create Character, New Name
#   Main Game:
#     World, Local, Inventory/Backpack

class Level: Global, World, Local = -1, 0, 1
# class WorldView: Geo, Pol, King = range(3)

'''
Notes:
    x, y, a, act = key_input()
    key_action_handler(x, y, a, act):
        -> movement_handler()
        -> action_handler()
'''
def key_input():
    '''Handles keyboard input and keypress transformation
    Cases:
        Skips any pre-inputs and non-read keys
        if key read is a close command -- close early or set proceed to false
        Elif key is valid command return the command from command list with continue
        Else return invalid action tuple with continue value
    '''
    action, proceed =  tuple(None for _ in range(4)), True
    # while term.has_input():
    #     term.read()

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
            proceed = False

    try:
        # discover the command and set as current action
        action = commands[(key, shifted)]
    except KeyError:
        pass

    return action, proceed

'''
Notes:
    class Action:
        def __init__(self):
            turn_inc = True

        def action(self):
            pass
        
    def Save(Action):
        def __init__(self):
            turn_inc = False
'''

def log_box(gamelog, turns):
    # nonlocal turns
    messages = gamelog.write().messages
    if messages:
        for idx in range(len(messages)):
            # offput by 1 for border and then # of lines logger is currently set at
            term.puts(
                14 if player.height == -1 else 1, 
                screen_height - len(messages) + idx, 
                messages[idx][1])

    term.puts(1, screen_height-3, 'Turns: {:<4}'.format(turns))

def refresh(gamelog, turns, lines=[]):
    for line in lines:
        gamelog.add(line)
    term.clear()
    if player.height == -1:
        world_map_box()
    else:
        map_box()
    status_box()
    log_box(gamelog, turns)   
    term.refresh()

def enter_map(player, a, world, gamelog):
    '''Logic:
        if at world level, check if there exists a map
        if exists -> enter
        else -> build the map and add it to the world
    '''
    def determine_map(map_type):
        '''Helper function to determine wilderness map'''
        try:
            return wilderness[map_type]
        except KeyError:
            raise ValueError("Map Type Not Implemented: {}".format(map_type))

    def get_wilderness_enterance(x, y):
        '''Helper function to determine start position when entering wilderness map'''
        return (max(int(location.width * x - 1), 0), 
                max(int(location.height * y - 1), 0))

    if not world.location_exists(*player.location):
        # map does not exist yet -- create one
        if player.location in world.enterable_legend.keys():
            # map type should be a city
            fileloc = world.enterable_legend[player.location].lower().replace(' ','_')
            img_name = "./assets/maps/" + fileloc + ".png"
            cfg_name = "./assets/maps/" + fileloc + ".cfg"

            location = City(
                map_id=fileloc,
                map_img=img_name,
                map_cfg=cfg_name,
                width=term.state(term.TK_WIDTH), 
                height=term.state(term.TK_HEIGHT))

            player.position = location.width // 2, location.height // 2

        elif player.location in world.dungeon_legend.keys():
            # map type should be a cave
            location = Cave(
                width=term.state(term.TK_WIDTH),
                height=term.state(term.TK_HEIGHT),
                max_rooms=randint(15, 20))

            player.position = location.getUpStairs()

        else:
            # map type should be in the wilderness
            tile = world.square(*player.location)
            # neighbors = world.access_neighbors(*player.location)
            
            location = determine_map(tile.tile_type)(
                width=term.state(term.TK_WIDTH),
                height=term.state(term.TK_HEIGHT))

            x, y = player.get_position_on_enter()
            player.position = get_wilderness_enterance(x, y)
    
        location.addParent(world)
        world.location_create(*player.location, location)

    else:
        # location already been built -- retrieve from world map_data
        # player position is different on map enter depending on map location
        location = world.location(*player.location)
        if player.location in world.enterable_legend.keys():
            # re-enter a city
            player.position = location.width // 2, location.height // 2

        elif player.location in world.dungeon_legend.keys():
            # re-enter dungeon
            player.position = location.getUpStairs()

        else:
            # reenter a wilderness
            x, y = player.get_position_on_enter()
        
            player.position = get_wilderness_enterance(x, y)
            
    player.move_height(1)

'''
Notes:
    maybe create a class that holds all this together under a single identifier -- Engine
    so when we need to use specific actions inside the world, ie. Save() we call it like so
    Class Engine:
    def run(...): ...
    def save(...): ...

    e = Engine()
    e.run()
    e.save()

    But for now lets do this ...
'''
def save_game(player, action, world, gamelog, turns):
    gamelog.add("Save and exit game(Y/N)?")
    log_box(gamelog, turns)
    term.refresh()
    code = term.read()
    if code != term.TK_Y:
        return
    if not os.path.isdir('saves'):
        print('saved folder does not exist - creating folder: "./saves"')
        os.makedirs('saves')

    # prepare strings for file writing
    # player_hash used for same name / different character saves
    name = player.name.replace(' ', '_')
    desc = player.job + " " + str(player.level)
    file_path = './saves/{}'.format(name + "(" + str(abs(hash(desc)))) + ")"
    with shelve.open(file_path, 'n') as save_file:
        save_file['save'] = desc
        save_file['player'] = player
        save_file['world'] = world
        save_file['turns'] = turns  
    proceed = False    # logbox

actions={
    0: {
        '>': enter_map,
        # '@': open_player_screen,
        # 'i': open_player_screen,
        # 'v': open_player_screen,
        'S': save_game,
    },
    # 1: {
    #     '>': interactStairs,
    #     '<': interactStairs,
    #     'a': attackUnit,
    #     'o': interactDoor,
    #     'c': interactDoor,
    #     't': interactUnit,
    #     ',': interactItem,
    #     '@': open_player_screen,
    #     'i': open_player_screen,
    #     'v': open_player_screen,
    # },
}

def process_action(action, player, world, gamelog, turns):
    turn_inc = 0
    ''' 
    Player class should return a height method and position method
    Position method should return position based on height
    So height would be independent and position would be depenedent on height
    try:
        if player.height == Level.World:
            actions[max(0, min(player.height, 1)][action](*player.position, action)
    except KeyError
    '''
    try:
    #     if player.height == Level.World:
    #         actions[max(0, min(player.height, 1))][action](player.wx, player.wy, action)
    #     else:
    #         actions[max(0, min(player.height, 1))][action](player.x, player.y, action)
    # except TypeError:
        # if player.height == Level.World:
        #     actions[max(0, min(player.height, 0))][action](player, action, world, gamelog)
        # else:
        actions[max(0, min(player.height, 1))][action](player, 
                                                       action, 
                                                       world, 
                                                       gamelog)
    except TypeError:
        actions[max(0, min(player.height, 1))][action](player, 
                                                       action, 
                                                       world, 
                                                       gamelog, 
                                                       turns)
    except KeyError:
        gamelog.add("'{}' is not a valid command".format(action))

def process_movement(x, y, player, world, gamelog):
    turn_inc = 0
    if  player.height == Level.World:
        if (x, y) == (0, 0):
            gamelog.add("You wait in the area")
            turn_inc = True
        else:
            tx = player.wx + x
            ty = player.wy + y

            if world.walkable(tx, ty):
                player.save_location()
                player.travel(x, y)
                turn_inc = True
            else:
                travel_error = "You cannot travel there"
                gamelog.add(travel_error)
    else:
        if (x, y) == (0, 0):
            gamelog.add("You rest for a while")
            turn_inc = True
        else:
            tx = player.x + x
            ty = player.y + y

            if world.walkable(tx, ty):
                if not world.occupied(tx, ty):
                    player.move(x, y)
                    if world.square(tx, ty).items and randint(0, 5):
                        pass_item_messages = [
                            "You pass by an item.",
                            "There is something here."
                            "Your feet touches an object."
                        ]
                        item_message = randint(0, len(pass_item_messages) - 1)
                        gamelog.add(
                            pass_item_messages[item_message])
                    turn_inc = True
                else:
                    unit = world.get_unit(tx, ty)
                    if unit.friendly:
                        unit.move(-x, -y)
                        player.move(x, y)
                        log = "You switch places with the {}".format(
                            unit.race)
                        gamelog.add(log)
                    else:
                        chance = player.calculate_attack_chance()
                        if chance == 0:
                            log = "You try attacking the {} but miss".format(
                                unit.race)
                            gamelog.add(log)
                        else:
                            damage = player.calculate_attack_damage()
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
                            gamelog.add(log)
                            term.refresh()

                            if unit.cur_health < 1:
                                player.gain_exp(unit.xp)
                                log += "You have killed the {}! ".format(
                                                                    unit.race)
                                log += "You gain {} exp".format(unit.xp)
                                gamelog.add(log)
                                term.refresh()

                                if player.check_exp():
                                    log = "You level up. "
                                    log += "You are now level {}. ".format(
                                        self.player.level)
                                    log += "You feel much stronger."
                                    gamelog.add(log)
                                    term.refresh()
                                item = unit.drops()

                                if item:
                                    world.square(*unit.position).items.append(
                                                                        item)
                                    gamelog.add("The {} has dropped {}".format(
                                                                    unit.race, 
                                                                    item.name))

                                world.remove_unit(unit)

                            else:
                                log += "The {} has {} health left".format(
                                    unit.race, 
                                    max(0, unit.cur_health))
                                gamelog.add(log)
                                term.puts(tx + 13, ty + 1, '[c=red]*[/c]')
                                term.refresh()

                    turn_inc = True
            else:
                if world.out_of_bounds(tx, ty):
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
                    ch = world.square(tx, ty).char
                    if ch == "~":
                        gamelog.add("You cannot swim")
                    else:
                        gamelog.add("You walk into {}".format(walkChars[ch]))
                        term.puts(tx + 13, ty + 1, '[c=red]X[/c]')
                term.refresh()

def process_handler(x, y, k, key, player, world, gamelog, turns):
    '''Checks actions linearly by case:
    (1) processes non-movement action
        Actions not in movement groupings
    (2) processes movement action
        Keyboard shortcut action grouping
    (3) If action teplate is empty:
        Return skip-action command
    '''
    if k is not None:
        process_action(k, player, world, gamelog, turns)
    elif all(z is not None for z in [x, y]):
        process_movement(x, y, player, world, gamelog)
    else:
        return 'skipped-turn'

def onlyOne(container):
    return len(container) == 1

def eightsquare(x, y):
    squares = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    space = namedtuple("Space", ("x","y"))
    for i, j in squares:
        yield space(x + i, y + j)

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

def interactItem(x, y, key):
        print('interactItem')
        nonlocal turns
        def pickItem():
            item = dungeon.square(x, y).items.pop()
            player.inventory.append(item)
            gamelog.add("You pick up a {}".format(item.name))
        
        if key == ",": # pickup
            print('picking up')
            # if player.backpack.full():
            if len(player.inventory) >= 25:
                # earlly exit
                gamelog.add("Backpack is full")
                return

            items = dungeon.square(x, y).items
            if items:
                # if len(items) == 1:
                #     pickItem()
                pickItem()
                # TODO                
                # else:
                #     glog.add("opening pick up menu")
                #     pick_menu(items)
            else:
                gamelog.add("Nothing to pick up")
        turn_inc = True

def attackUnit(x, y, k):
    nonlocal turns
    def attack(x, y):
        unit = dungeon.get_unit(x, y)
        log = "You attack the {}. ".format(unit.race)
        unit.cur_health -= 1           
        log += "The {} has {} health left. ".format(unit.race, unit.cur_health)
        if dungeon.maptype == "city":
            dungeon.reduce_unit_relationships(100)
            # dungeon.reduce_relationship(100)
            log += "Your relationship with {} has decreased by {} ".format(
                dungeon.map_name, 100)
        for l in wrap(log, width=screen_width):
            gamelog.add(l)

        # if unit.r is not "human": # condition should be more complex
        if unit.cur_health < 1:
            gamelog.add("You have killed the {}! You gain 15 exp".format(unit.race))
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

    turn_inc = True

def interactUnit(x, y, action):
    """Allows talking with other units"""
    def talkUnit(x, y):
        unit = dungeon.get_unit(x, y)
        gamelog.add(unit.talk())
        refresh()

    print("talking")
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
        try:
            cx, cy, a, act = commands[(code, term.state(term.TK_SHIFT))]
            if act == "move" and (x+cx, y+cy) in interactables:
                talkUnit(x+cx, y+cy) 
        except:
            raise
            return

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
        refresh()

        code = term.read()
        try:
            cx, cy, a, act = commands[(code, term.state(term.TK_SHIFT))]
            if act == "move" and (x+cx, y+cy) in reachables:
                openDoor(x+cx, y+cy) if key is 'o' else closeDoor(x+cx, y+cy)            
        except:
            raise
            return

    turn_inc = True

def interactStairs(x, y, k):
    nonlocal dungeon
    """Allows interactions with stairs"""

    if k == ">":  
        #  differentiate going up versus down
        if player.position == dungeon.getDownStairs():                

            if not dungeon.hasSublevel():
                sublevel = Cave(
                    width=term.state(term.TK_WIDTH),
                    height=term.state(term.TK_HEIGHT),
                    max_rooms=randint(15, 20))

                sublevel.addParent(dungeon)
                dungeon.addSublevel(sublevel)

            dungeon = dungeon.getSublevel()
            player.move_height(1)
            player.position = dungeon.getUpStairs()

        else:
            gamelog.add('You cannot go downstairs without stairs.')
            
    else:
        print(dungeon.map_type)
        # map at the location exists -- determine type of map
        if player.location in calabaston.enterable_legend.keys():
            # check if you're in a city
            player.move_height(-1)
            dungeon = dungeon.getParent()

        # elif calabaston.is_wilderness(*player.location):
        elif calabaston.location_is(*player.location, 2):
            # check for wilderness type map
            player.move_height(-1)
            dungeon = dungeon.getParent()

        elif player.position == dungeon.getUpStairs():
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
            player.position = (0, 0)

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

    term.puts(col, row + 7, "HP:  {:>6}".format("{}/{}".format(player.cur_health, player.max_health)))
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
    if player.location in calabaston.enterable_legend.keys():
        location = calabaston.enterable_legend[player.location]
        term.bkcolor('grey')
        term.puts(0, 0, ' ' * screen_width)
        term.bkcolor('black')
        term.puts(center(surround(location), screen_width), 0, surround(location))

    elif player.location in calabaston.dungeon_legend.keys():
        location = calabaston.dungeon_legend[player.location]

    else:
        location = ""

    term.puts(col, row + 20, "{}".format(location))

def map_box():
    def calc_sight():
        dungeon.fov_calc([(player.x, player.y, player.sight * 2 if calabaston.location_is(*player.location, 1) else player.sight)])
    
    def output_map():
        for x, y, lit, ch in dungeon.output(player.x, player.y):
            term.puts(x + 13, y + 1, "[color={}]".format(lit) + ch + "[/color]")

    calc_sight()
    output_map()

def world_legend_box():
    length, offset, height = 14, 12, 0
    world_name = surround(calabaston.map_name, length=length)
    selected(center(world_name, offset), height, world_name)   

    height += 1        
    # this is purely a ui enhancement. Actually entering a city is not that much different
    # than entering a dungeon/wilderness area
    if player.location in calabaston.enterable_legend.keys():
        # check if player position is over a city/enterable area
        city_name = calabaston.enterable_legend[player.location]
        enterable_name = surround(city_name, length=length)
        selected(center(enterable_name, offset), height, enterable_name)
        # try:
        #     gamelog.add(calabaston.city_descriptions[city_name])
        # except:
        #     gamelog.add("\n\n")

    elif player.location in calabaston.dungeon_legend.keys():
        # check if player position is over a dungeon position
        dungeon_name = surround(calabaston.dungeon_legend[player.location], length=length)
        selected(center(dungeon_name, offset), height, dungeon_name)

    else:
        # Add land types to the overworld ui
        landtype = surround(calabaston.landtype(*player.location), length=length)
        selected(center(landtype, offset), height, landtype)
        

    for char, color, desc, i in calabaston.legend():
        # finally print the lengend with character and description
        term.puts(0, height + i + 2, "[c={}] {}[/c] {}".format(color, char, desc))

def world_map_box():
    '''Displays the world map tiles in the terminal'''
    screen_off_x, screen_off_y = 14, 0
    calabaston.fov_calc([(player.wx, player.wy, player.sight * 2)])
    
    for x, y, col, ch in calabaston.output(*(player.location)):
        term.puts(
            x + screen_off_x, 
            y + screen_off_y, 
            "[c={}]{}[/c]".format(col, ch))

def new_game(character=None, world=None, turns=0):
    # Unused:
        # def save_game(x, y, action):
        #     nonlocal proceed

        #     gamelog.add("Save and exit game? (Y/N)")
        #     log_box()
        #     term.refresh()
        #     code = term.read()
        #     if code != term.TK_Y:
        #         return

        #     if not os.path.isdir('saves'):
        #         print('saved folder does not exist - creating folder: "./saves"')
        #         os.makedirs('saves')

        #     # prepare strings for file writing -- player_hash used for same name/different character saves
        #     name = player.name.replace(' ', '_')
        #     desc = player.job + " " + str(player.level)
        #     with shelve.open('./saves/{}'.format(name + "(" + str(abs(hash(desc)))) + ")", 'n') as save_file:
        #         save_file['save'] = desc
        #         save_file['player'] = player
        #         save_file['world'] = calabaston
        #         save_file['turns'] = turns  
        #     proceed = False

        # def refresh(gamelog, turns, lines=[]):
        #     for line in lines:
        #         gamelog.add(line)
        #     term.clear()
        #     if player.height == -1:
        #         world_map_box()
        #     else:
        #         map_box()
        #     status_box()
        #     log_box(gamelog, turns)   
        #     term.refresh()

        # END SETUP TOOLS
        # -----------------------------------------------------------------------------------------------------------------#
        # Keyboard input
        # def onlyOne(container):
        #     return len(container) == 1

        # def eightsquare(x, y):
        #     squares = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        #     space = namedtuple("Space", ("x","y"))
        #     for i, j in squares:
        #         yield space(x + i, y + j)
            # return [space(x+i,y+j) for i, j in list(num_movement.values())]

        # def process_movement(x, y):
        #     nonlocal player, turn_inc
        #     if  player.height == Level.World:
        #         if (x, y) == (0, 0):
        #             gamelog.add("You wait in the area")
        #             turn_inc = True
        #         else:
        #             tx = player.wx + x
        #             ty = player.wy + y

        #             if calabaston.walkable(tx, ty):
        #                 player.save_location()
        #                 player.travel(x, y)
        #                 turn_inc = True
        #             else:
        #                 travel_error = "You cannot travel there"
        #                 gamelog.add(travel_error)
        #     else:
        #         if (x, y) == (0, 0):
        #             gamelog.add("You rest for a while")
        #             turn_inc = True
        #         else:
        #             tx = player.x + x
        #             ty = player.y + y

        #             if dungeon.walkable(tx, ty):
        #                 if not dungeon.occupied(tx, ty):
        #                     player.move(x, y)
        #                     if dungeon.square(tx, ty).items and randint(0, 5):
        #                         pass_item_messages = [
        #                             "You pass by an item.",
        #                             "There is something here."
        #                             "Your feet touches an object."
        #                         ]
        #                         gamelog.add(pass_item_messages[randint(0, len(pass_item_messages)-1)])
        #                     turn_inc = True
        #                 else:
        #                     unit = dungeon.get_unit(tx, ty)
        #                     if unit.friendly:
        #                         unit.move(-x, -y)
        #                         player.move(x, y)
        #                         gamelog.add("You switch places with the {}".format(unit.race))
        #                     else:
        #                         chance = player.calculate_attack_chance()
        #                         if chance == 0:
        #                             gamelog.add("You try attacking the {} but miss".format(unit.race))

        #                         else:
        #                             damage = player.calculate_attack_damage() * (2 if chance == 2 else 1)
        #                             unit.cur_health -= damage
        #                             log = "You{}attack the {} for {} damage. ".format(
        #                                 " crit and " if chance == 2 else " ", unit.race, damage)
        #                             log += "The {} has {} health left. ".format(unit.race, max(unit.cur_health, 0))
        #                             gamelog.add(log)

        #                             if unit.cur_health < 1:
        #                                 log += "You have killed the {}! You gain {} exp".format(unit.race, unit.xp)
        #                                 gamelog.add(log)
        #                                 player.gain_exp(unit.xp)

        #                                 if player.check_exp():
        #                                     gamelog.add("You level up. You are now level {}".format(player.level))
        #                                     gamelog.add("You feel much stronger")

        #                                 item = unit.drops()

        #                                 if item:
        #                                     dungeon.square(*unit.position).items.append(item)
        #                                     gamelog.add("The {} has dropped {}".format(unit.race, item.name))

        #                                 dungeon.remove_unit(unit)

        #                             else:
        #                                 log += "The {} has {} health left".format(
        #                                     unit.race, 
        #                                     max(unit.cur_health, 0))
        #                                 gamelog.add(log)

        #                                 term.puts(tx + 13, ty + 1, '[c=red]*[/c]')
        #                                 term.refresh()
        #                     turn_inc = True
        #             else:
        #                 if dungeon.out_of_bounds(tx, ty):
        #                     gamelog.add("You reached the edge of the map")

        #                 else:
        #                     walkChars = {
        #                         "+": "a door",
        #                         "/": "a door",
        #                         "o": "a lamp",
        #                         "#": "a wall",
        #                         "x": "a post",
        #                         "~": "a river",
        #                         "T": "a tree",
        #                         "f": "a tree",
        #                         "Y": "a tree",
        #                         "%": "a wall",
        #                     }
        #                     ch = dungeon.square(tx, ty).char

        #                     if ch == "~":
        #                         gamelog.add("You cannot swim")
        #                     else:
        #                         gamelog.add("You walk into {}".format(
        #                             walkChars[ch]))
        #                         term.puts(tx + 13, ty + 1, '[c=red]X[/c]')
        #                         term.refresh()

        # def open_player_screen(x, y, key):
        #     '''Game function to handle player equipment and inventory'''
        #     def profile():
        #         '''Handles player profile screen'''
        #         term.clear()

        #         for i in range(screen_width):
        #             term.puts(i, 1, '#')
        #         term.puts(center('profile  ', screen_width), 1, ' Profile ')

        #         for colnum, column in enumerate(list(player.get_profile())):
        #             term.puts(col + (20 * colnum), row, column)

        #     def inventory():
        #         '''Handles inventory screen'''
        #         term.clear()

        #         # title backpack
        #         for i in range(screen_width):
        #             term.puts(i, 1, '#')
        #         term.puts(center('backpack  ', screen_width), 1, ' Backpack ')

        #         for index, item in player.get_inventory():
        #             letter = chr(ord('a') + index) + ". "
        #             item_desc = item.__str__() if item else ""

        #             term.puts(
        #                 col,
        #                 row + index * (2 if screen_height > 25 else 1),
        #                 letter + item_desc)

        #     def equipment():
        #         '''Handles equipment screen'''
        #         term.clear()

        #         for i in range(screen_width):
        #             term.puts(i, 1, '#')

        #         term.puts(center(' inventory ', screen_width), 1, ' Inventory ')
                
        #         for index, part, item in player.get_equipment():
        #             letter = chr(ord('a') + index)
        #             body_part = ".  {:<10}: ".format(part)
        #             item_desc = item.__str__() if item else ""

        #             term.puts(
        #                 col,
        #                 row + index * (2 if screen_height > 25 else 1),
        #                 letter + body_part + item_desc)

            # col, row = 1, 3
            # playscreen = False
            # current_screen = key
            # current_range = 0
            # while True:
            #     term.clear()

            #     if current_screen == "i":
            #         equipment()
            #     elif current_screen == "v":
            #         inventory()
            #     else:
            #         profile()

            #     term.refresh()
            #     code = term.read()

            #     if code in (term.TK_ESCAPE,):
            #         if current_screen == 1:
            #             current_screen = 0
            #         else:
            #             break

            #     elif code == term.TK_I:
            #         current_screen = 'i'

            #     elif code == term.TK_V:
            #         # V goes to inventory screen
            #         current_screen = 'v'
                
            #     elif code == term.TK_2 and term.state(term.TK_SHIFT):
            #         # @ goes to profile
            #         current_screen = '@'

            #     elif code == term.TK_UP:
            #         if current_range > 0: current_range -= 1

            #     elif code == term.TK_DOWN:
            #         if current_range < 10: current_range += 1

            # term.clear()

        # def interactItem(x, y, key):
        #     print('interactItem')
        #     nonlocal turns
        #     def pickItem():
        #         item = dungeon.square(x, y).items.pop()
        #         player.inventory.append(item)
        #         gamelog.add("You pick up a {}".format(item.name))
            
        #     if key == ",": # pickup
        #         print('picking up')
        #         # if player.backpack.full():
        #         if len(player.inventory) >= 25:
        #             # earlly exit
        #             gamelog.add("Backpack is full")
        #             return

        #         items = dungeon.square(x, y).items
        #         if items:
        #             # if len(items) == 1:
        #             #     pickItem()
        #             pickItem()
        #             # TODO                
        #             # else:
        #             #     glog.add("opening pick up menu")
        #             #     pick_menu(items)
        #         else:
        #             gamelog.add("Nothing to pick up")
        #     turn_inc = True

        # def attackUnit(x, y, k):
        #     nonlocal turns
        #     def attack(x, y):
        #         unit = dungeon.get_unit(x, y)
        #         log = "You attack the {}. ".format(unit.race)
        #         unit.cur_health -= 1           
        #         log += "The {} has {} health left. ".format(unit.race, unit.cur_health)
        #         if dungeon.maptype == "city":
        #             dungeon.reduce_unit_relationships(100)
        #             # dungeon.reduce_relationship(100)
        #             log += "Your relationship with {} has decreased by {} ".format(
        #                 dungeon.map_name, 100)
        #         for l in wrap(log, width=screen_width):
        #             gamelog.add(l)

        #         # if unit.r is not "human": # condition should be more complex
        #         if unit.cur_health < 1:
        #             gamelog.add("You have killed the {}! You gain 15 exp".format(unit.race))
        #             dungeon.remove_unit(unit)

        #     attackables = []
        #     for i, j in eightsquare(x, y):
        #         if (i, j) != (x, y) and dungeon.get_unit(i, j):
        #             attackables.append((i, j))
            
        #     if not attackables:
        #         gamelog.add("Nothing you can attack. You want to punch the floor?")
            
        #     elif onlyOne(attackables):
        #         attack(*attackables.pop())

        #     else:
        #         gamelog.add("Who do you want to attack?")
        #         code = term.read()
        #         if code in key_movement:
        #             cx, cy = key_movement[code]
        #         elif code in num_movement:
        #             cx, cy = num_movement[code]
        #         else:
        #             return
        #         if (x+cx, y+cy) in attackables:
        #             attack(x + cx, y + cy)

        #     turn_inc = True

        # def interactUnit(x, y, action):
        #     """Allows talking with other units"""
        #     def talkUnit(x, y):
        #         unit = dungeon.get_unit(x, y)
        #         gamelog.add(unit.talk())
        #         refresh()

        #     print("talking")
        #     interactables = []
        #     for i, j in eightsquare(x, y):
        #         # dungeon.has_unit(i, j) -> returns true or false if unit is on the square
        #         if (i, j) != (x, y) and dungeon.get_unit(i, j):
        #             interactables.append((i, j))

        #     # no interactables
        #     if not interactables:
        #         gamelog.add("No one to talk with")

        #     # only one interactable
        #     elif onlyOne(interactables):
        #         # i, j = interactables.pop()
        #         talkUnit(*interactables.pop())

        #     # many interactables
        #     else:
        #         gamelog.add("Which direction?")   
        #         refresh()
        #         code = term.read()
        #         try:
        #             cx, cy, a, act = commands[(code, term.state(term.TK_SHIFT))]
        #             if act == "move" and (x+cx, y+cy) in interactables:
        #                 talkUnit(x+cx, y+cy) 
        #         except:
        #             raise
        #             return

        # def interactDoor(x, y, key):
        #     """Allows interaction with doors"""
        #     nonlocal turns
        #     def openDoor(i, j):
        #         gamelog.add("Opened door")
        #         dungeon.open_door(i, j)
        #         dungeon.unblock(i, j)

        #     def closeDoor(i, j):
        #         gamelog.add("Closed door")
        #         dungeon.close_door(i, j)
        #         dungeon.reblock(i, j)

        #     char = "+" if key is "o" else "/"

        #     reachables = []
        #     for i, j in eightsquare(x, y):
        #         if (i, j) != (x, y):
        #             isSquare = 0
        #             try:
        #                 isSquare = dungeon.square(i, j).char is char
        #             except IndexError:
        #                 gamelog.add("out of bounds ({},{})".format(i, j))
        #             if isSquare:
        #                 reachables.append((i, j))

        #     if not reachables:
        #         gamelog.add("No {} near you".format("openables" if key is "o" else "closeables"))
            
        #     elif onlyOne(reachables):
        #         i, j = reachables.pop()
        #         openDoor(i, j) if key is "o" else closeDoor(i, j)

        #     else:
        #         gamelog.add("There is more than one door near you. Which direction?")
        #         refresh()

        #         code = term.read()
        #         try:
        #             cx, cy, a, act = commands[(code, term.state(term.TK_SHIFT))]
        #             if act == "move" and (x+cx, y+cy) in reachables:
        #                 openDoor(x+cx, y+cy) if key is 'o' else closeDoor(x+cx, y+cy)            
        #         except:
        #             raise
        #             return

        #     turn_inc = True

        # def interactStairs(x, y, k):
        #     nonlocal dungeon
        #     """Allows interactions with stairs"""

        #     if k == ">":  
        #         #  differentiate going up versus down
        #         if player.position == dungeon.getDownStairs():                

        #             if not dungeon.hasSublevel():
        #                 sublevel = Cave(
        #                     width=term.state(term.TK_WIDTH),
        #                     height=term.state(term.TK_HEIGHT),
        #                     max_rooms=randint(15, 20))

        #                 sublevel.addParent(dungeon)
        #                 dungeon.addSublevel(sublevel)

        #             dungeon = dungeon.getSublevel()
        #             player.move_height(1)
        #             player.position = dungeon.getUpStairs()

        #         else:
        #             gamelog.add('You cannot go downstairs without stairs.')
                    
        #     else:
        #         print(dungeon.map_type)
        #         # map at the location exists -- determine type of map
        #         if player.location in calabaston.enterable_legend.keys():
        #             # check if you're in a city
        #             player.move_height(-1)
        #             dungeon = dungeon.getParent()

        #         # elif calabaston.is_wilderness(*player.location):
        #         elif calabaston.location_is(*player.location, 2):
        #             # check for wilderness type map
        #             player.move_height(-1)
        #             dungeon = dungeon.getParent()

        #         elif player.position == dungeon.getUpStairs():
        #             # check if you're in a dungeon
        #             # dungeon will have parent -- need to differentiate between
        #             # world and first level dungeon
        #             player.move_height(-1)
        #             dungeon = dungeon.getParent()

        #         else:
        #             gamelog.add('You cannot go upstairs without stairs.')

        #         if isinstance(dungeon, World):
        #             # we unrefrence the dungeon only if it is at level 0
        #             dungeon = None
        #             player.position = (0, 0)

        # def enter_map(x, y, a):
        #     '''Logic:
        #         if at world level, check if there exists a map
        #         if exists -> enter
        #         else -> build the map and add it to the world
        #     '''
        #     def determine_map(map_type):
        #         '''Helper function to determine wilderness map'''
        #         try:
        #             return wilderness[map_type]
        #         except KeyError:
        #             raise ValueError("Map Type Not Implemented: {}".format(map_type))

        #     def get_wilderness_enterance(x, y):
        #         '''Helper function to determine start position when entering wilderness map'''
        #         return (max(int(location.width * x - 1), 0), 
        #                 max(int(location.height * y - 1), 0))

        #     if not calabaston.location_exists(*player.location):
        #         # map does not exist yet -- create one
        #         if player.location in calabaston.enterable_legend.keys():
        #             # map type should be a city
        #             fileloc = calabaston.enterable_legend[player.location].lower().replace(' ','_')
        #             img_name = "./assets/maps/" + fileloc + ".png"
        #             cfg_name = "./assets/maps/" + fileloc + ".cfg"

        #             location = City(
        #                 map_id=fileloc,
        #                 map_img=img_name,
        #                 map_cfg=cfg_name,
        #                 width=term.state(term.TK_WIDTH), 
        #                 height=term.state(term.TK_HEIGHT))

        #             player.position = location.width // 2, location.height // 2

        #         elif player.location in calabaston.dungeon_legend.keys():
        #             # map type should be a cave
        #             location = Cave(
        #                 width=term.state(term.TK_WIDTH),
        #                 height=term.state(term.TK_HEIGHT),
        #                 max_rooms=randint(15, 20))

        #             player.position = location.getUpStairs()

        #         else:
        #             # map type should be in the wilderness
        #             tile = calabaston.square(*player.location)
        #             # neighbors = calabaston.access_neighbors(*player.location)
                    
        #             location = determine_map(tile.tile_type)(
        #                 width=term.state(term.TK_WIDTH),
        #                 height=term.state(term.TK_HEIGHT))

        #             x, y = player.get_position_on_enter()
        #             player.position = get_wilderness_enterance(x, y)
            
        #         location.addParent(calabaston)
        #         calabaston.location_create(*player.location, location)

        #     else:
        #         # location already been built -- retrieve from world map_data
        #         # player position is different on map enter depending on map location
        #         location = calabaston.location(*player.location)
        #         if player.location in calabaston.enterable_legend.keys():
        #             # re-enter a city
        #             player.position = location.width // 2, location.height // 2

        #         elif player.location in calabaston.dungeon_legend.keys():
        #             # re-enter dungeon
        #             player.position = location.getUpStairs()

        #         else:
        #             # reenter a wilderness
        #             x, y = player.get_position_on_enter()
                
        #             player.position = get_wilderness_enterance(x, y)
                    
        #     player.move_height(1)

        # def process_action(action):
        #     print('action', action)
        #     nonlocal turns
        #     ''' 
        #     Player class should return a height method and position method
        #     Position method should return position based on height
        #     So height would be independent and position would be depenedent on height
        #     try:
        #         if player.height == Level.World:
        #             actions[max(0, min(player.height, 1)][action](*player.position, action)
        #     except KeyError
        #     '''
        #     try:
        #         if player.height == Level.World:
        #             actions[max(0, min(player.height, 1))][action](player.wx, player.wy, action)
        #         else:
        #             actions[max(0, min(player.height, 1))][action](player.x, player.y, action)
        #     # except TypeError:
        #     #     if player.height == Level.World:
        #     #         actions[max(0, min(player.height, 1))][action](player.wx, player.wy, action, gamelog)
        #     #     else:
        #     #         actions[max(0, min(player.height, 1))][action](player.x, player.y, action, gamelog)
        #     except KeyError:
        #         gamelog.add("'{}' is not a valid command".format(action))
        # End Keyboard Functions
        # ---------------------------------------------------------------------------------------------------------------------#
        # Graphic functions

        # def graphics(integer: int) -> None:
        #     def toBin(n):
        #         return list(bin(n).replace('0b'))
        #     if not 0 < integer < 8:
        #         raise ValueError("Must be within 0-7")

        # def border():
        #     # status border
        #     border_line =  "[color=dark #9a8478]"+chr(toInt("25E6"))+"[/color]"

        #     # y axis
        #     for i in range(0, 80, 2):
        #         if i < 20:
        #             term.puts(screen_width - 20 + i, 0, border_line)
        #             term.puts(screen_width - 20 + i, 10, border_line)
        #         if i < 60:
        #             term.puts(i, screen_height - 6, border_line)
        #         term.puts(i, screen_height - 1, border_line)
            
        #     # x axis
        #     for j in range(35):
        #         if j < 6:
        #             term.puts(0, screen_height - 6 + j, border_line)
        #         term.puts(screen_width - 20, j, border_line)
        #         term.puts(screen_width - 1, j, border_line)

        # def status_box():
        #     col, row = 1, 2
        #     term.puts(col, row - 1, player.name)
        #     term.puts(col, row + 0, player.gender)
        #     term.puts(col, row + 1, player.race)
        #     term.puts(col, row + 2, player.job)

        #     term.puts(col, row + 4, "LVL: {:>6}".format(player.level))
        #     term.puts(col, row + 5, "EXP: {:>6}".format("{}/{}".format(player.exp, player.advexp)))

        #     term.puts(col, row + 7, "HP:  {:>6}".format("{}/{}".format(player.cur_health, player.max_health)))
        #     term.puts(col, row + 8, "MP:  {:>6}".format("{}/{}".format(player.mp, player.total_mp)))
        #     term.puts(col, row + 9, "SP:  {:>6}".format(player.sp))

        #     term.puts(col, row + 11, "STR: {:>6}".format(player.str)) 
        #     term.puts(col, row + 12, "CON: {:>6}".format(player.con))
        #     term.puts(col, row + 13, "DEX: {:>6}".format(player.dex))
        #     term.puts(col, row + 14, "INT: {:>6}".format(player.int))
        #     term.puts(col, row + 15, "WIS: {:>6}".format(player.wis))
        #     term.puts(col, row + 16, "CHA: {:>6}".format(player.cha))

        #     term.puts(col, row + 18, "GOLD:{:>6}".format(player.gold))

        #     # sets the location name at the bottom of the status bar
        #     if player.location in calabaston.enterable_legend.keys():
        #         location = calabaston.enterable_legend[player.location]
        #         term.bkcolor('grey')
        #         term.puts(0, 0, ' ' * screen_width)
        #         term.bkcolor('black')
        #         term.puts(center(surround(location), screen_width), 0, surround(location))

        #     elif player.location in calabaston.dungeon_legend.keys():
        #         location = calabaston.dungeon_legend[player.location]

        #     else:
        #         location = ""

        #     term.puts(col, row + 20, "{}".format(location))

        # def log_box():
        #     nonlocal turns
        #     messages = gamelog.write().messages
        #     if messages:
        #         for idx in range(len(messages)):
        #             # offput by 1 for border and then # of lines logger is currently set at
        #             term.puts(
        #                 14 if player.height == -1 else 1, 
        #                 screen_height - len(messages) + idx, 
        #                 messages[idx][1])

        #     term.puts(1, screen_height-3, 'Turns: {:<4}'.format(turns))

        # def map_box():
        #     def calc_sight():
        #         dungeon.fov_calc([(player.x, player.y, player.sight * 2 if calabaston.location_is(*player.location, 1) else player.sight)])
            
        #     def output_map():
        #         for x, y, lit, ch in dungeon.output(player.x, player.y):
        #             term.puts(x + 13, y + 1, "[color={}]".format(lit) + ch + "[/color]")

        #     calc_sight()
        #     output_map()

        # def world_legend_box():
        #     length, offset, height = 14, 12, 0
        #     world_name = surround(calabaston.map_name, length=length)
        #     selected(center(world_name, offset), height, world_name)   

        #     height += 1        
        #     # this is purely a ui enhancement. Actually entering a city is not that much different
        #     # than entering a dungeon/wilderness area
        #     if player.location in calabaston.enterable_legend.keys():
        #         # check if player position is over a city/enterable area
        #         city_name = calabaston.enterable_legend[player.location]
        #         enterable_name = surround(city_name, length=length)
        #         selected(center(enterable_name, offset), height, enterable_name)
        #         # try:
        #         #     gamelog.add(calabaston.city_descriptions[city_name])
        #         # except:
        #         #     gamelog.add("\n\n")

        #     elif player.location in calabaston.dungeon_legend.keys():
        #         # check if player position is over a dungeon position
        #         dungeon_name = surround(calabaston.dungeon_legend[player.location], length=length)
        #         selected(center(dungeon_name, offset), height, dungeon_name)

        #     else:
        #         # Add land types to the overworld ui
        #         landtype = surround(calabaston.landtype(*player.location), length=length)
        #         selected(center(landtype, offset), height, landtype)
                

        #     for char, color, desc, i in calabaston.legend():
        #         # finally print the lengend with character and description
        #         term.puts(0, height + i + 2, "[c={}] {}[/c] {}".format(color, char, desc))

        # def world_map_box():
        #     '''Displays the world map tiles in the terminal'''
        #     screen_off_x, screen_off_y = 14, 0
        #     calabaston.fov_calc([(player.wx, player.wy, player.sight * 2)])
            
        #     for x, y, col, ch in calabaston.output(*(player.location)):
        #         term.puts(
        #             x + screen_off_x, 
        #             y + screen_off_y, 
        #             "[c={}]{}[/c]".format(col, ch))

        # screen_width, screen_height = term.state(term.TK_WIDTH), term.state(term.TK_HEIGHT)
    
    # very first thing is game logger initialized to output messages on terminal
    # gamelog = GameLogger(3 if term.state(term.TK_HEIGHT) <= 25 else 4)

    # process character
    if not character:
        # improperly accessed new_game --> early exit
        return output(proceed=False, value="No Character Data Input")

    if not world:
        # unpack character tuple to create a player object
        player = Player(character)
        print(player.energy.speed)
        # create the world from scratch
        # TODO: chain function so World().load() or keep as seperate functions: init() and load()?
        # calabaston = World(screen_width, screen_height)
        # calabaston.load(
        #             "./assets/worldmap.png", 
        #             "./assets/worldmap_territories.png",
        #             "./assets/worldmap_kingdoms.png")   

        calabaston = World(
            "Calabaston",
            "./assets/worldmap.png"
        )

    else:
        # coming from a save file -- player object already defined
        player = character

        # coming from a save file -- world already definied
        calabaston = world    

        # coming from a save file -- turns already defined
        turns = turns

    turn_inc = False
    proceed = True
    dungeon = None
    current_map = None
    player_waiting = False
    '''
    while True:
        clear()
        render()
        refresh()
        
        for unit in unitlist:
            unit.take_turn
    '''
    while proceed and player.cur_health:
        term.clear()
        '''
        Maybe make ui the same for overworld and dungeons to make the loop easier?
        '''
        if player.height == Level.World:
            gamelog.maxlines = 2
            world_map_box()
            world_legend_box()
            log_box(gamelog, turns)
        else:
            gamelog.maxlines = 4 if term.state(term.TK_HEIGHT) > 25 else 2  
            if dungeon == None:
                dungeon = calabaston.location(*player.location)
                
                if player.height == 0:
                    for i in range(player.height):
                        dungeon = dungeon.getSublevel()
                        
            map_box()
            status_box()
            log_box(gamelog, turns)
        term.refresh()

        # check if turn was used to signal npc actor actions
        turn_inc = False
        # action flag if has enough energy
        do_action = False        

        if player.height != Level.World: # not in overworld
            if dungeon.map_type == 1:
                # action, proceed = key_input()
                # process_handler(*action, player, dungeon, gamelog)
                do_action = True

            elif dungeon.map_type == 0:
                if player.energy.ready():
                    # action, proceed = key_input()
                    # process_handler(*action, player, dungeon. gamelog)
                    player.energy.reset()
                    do_action = True

                else:
                    player.energy.gain_energy()
                    turn_inc = True
        else:
            do_action = True
            # action, proceed = key_input()
            # process_handler(*action, player, calabaston)

        if not proceed:
            '''check if player pressed exit before processing units'''
            break          
    
        if do_action:
            action, proceed = key_input()
            process_handler(*action, player, calabaston, gamelog)

        # checks 3 conditions on whether ai takes turn or not
        # 1. player took a valid turn in which ai takes turn
        # 2. player in a level with actual monsters
        # 3. dungeon player is using exists
        if turn_inc:
            if player.height != Level.World and dungeon:
                for unit in dungeon.units:
                    if unit.energy.ready():
                        positions = dungeon.fov_calc_blocks(unit.x, unit.y, unit.sight)
                        tiles = {position: dungeon.square(*position) for position in positions}
                        units = {u.position: u for u in dungeon.units if u != unit}
                        unit.acts(player, tiles, units)
                        if player.cur_health <= 0:
                            return
                        unit.energy.reset()
                    else:
                        unit.energy.gain_energy()         
                # dungeon.handle_units(player)           
                    
    # player.dump()
    # gamelog.dumps()
    if not proceed:
        return "Safe Exit"
    else:
        term.clear()
        term.puts(center('You Died', len('you died')), 0, surround('You Died'))
        term.refresh()
        term.read()
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
