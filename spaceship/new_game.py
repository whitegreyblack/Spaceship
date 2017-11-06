# main implementation of core mechanics
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.action import key_movement, num_movement, key_actions, action, keypress, world_key_actions
from spaceship.constants import FOV_RADIUS
from spaceship.constants import GAME_SCREEN_WIDTH as SCREEN_WIDTH
from spaceship.constants import GAME_SCREEN_HEIGHT as SCREEN_HEIGHT
from spaceship.setup import setup_game
from spaceship.tools import bresenhams, deltanorm, movement
from spaceship.maps import stringify, hextup, hexone, toInt
from spaceship.objects import Map, Object, Character, Item
from spaceship.player import Player
from spaceship.create_character import create_character as create
from spaceship.screen_functions import center, surround, selected
from bearlibterminal import terminal as term
from spaceship.manager import UnitManager
from spaceship.gamelog import GameLogger
from random import randint, choice
from collections import namedtuple
from namedlist import namedlist
from spaceship.dungeon import buildTerrain, buildDungeon
from spaceship.setup import setup, output, setup_font
from spaceship.world import World
from time import clock

class Level: World, City, Dungeon = range(3)
class WorldView: Geo, Pol, King = range(3)

debug = False

def new_game(character=None):

    def refresh(lines=[]):
        for line in lines:
            gamelog.add(line)
        term.clear()
        # border()
        map_box()
        status_box()
        log_box()
        term.refresh()

    # END SETUP TOOLS
    # ---------------------------------------------------------------------------------------------------------------------#
    # Keyboard input

    def key_in_world():
        '''Key processing while player in overworld'''
        nonlocal proceed, wview
        keydown = namedtuple("Key_Press", "x y a")
        act, x, y = 0, 0, 0
        code = term.read()

        while code in (term.TK_SHIFT, term.TK_CONTROL, term.TK_ALT):
            code = term.read()
        if code in (term.TK_CLOSE, term.TK_ESCAPE, term.TK_Q):
            proceed = False

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
        elif code in (term.TK_COMMA, term.TK_PERIOD):
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
            if debug:
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
        nonlocal proceed
        keydown = namedtuple("Key_Down", ("x", "y", "a"))
        # movement
        act, x, y = 0, 0, 0
        code = term.read()
        while code in (term.TK_SHIFT, term.TK_CONTROL, term.TK_ALT):
            code = term.read()
        if any([term.state(tk) for tk in (term.TK_SHIFT, term.TK_CONTROL, term.TK_ALT)]):
            if debug:
                gamelog.add("CTRL | ALT | SHIFT")
        if code in (term.TK_ESCAPE, term.TK_CLOSE):
            gamelog.dumps()
            proceed = False

        # arrow keys
        elif code in key_movement:
            x, y = key_movement[code]
        # numberpad keys
        elif code in num_movement:
            x, y = num_movement[code]
        # keyboard keys
        elif code in key_actions:
            act = key_actions[code].key
        # any other key F-keys, Up/Down Pg, etc
        else:
            if debug:
                gamelog.add("[KEY_IN]: unrecognized command")
        # make sure we clear any inputs before the next action is processed
        # allows for the program to go slow enough for human playability
        while term.has_input(): 
            term.read()
        return keydown(x, y, act)

    # try creating a general purpose key input function that is called by both
    # world and map functions
    def key_input():
        nonlocal proceed, wview
        return

    def onlyOne(container):
        return len(container) == 1

    def eightsquare(x, y):
        space = namedtuple("Space", ("x","y"))
        return [space(x+i,y+j) for i, j in list(num_movement.values())]

    def key_process_world(x, y):
        walkBlock = "walked into {}"
        tx = player.wx + x
        ty = player.wy + y

        # inbounds = 0 <= tx < calabaston.w and 0 <= ty < calabaston.h
        walkable = calabaston.walkable(tx, ty)

        if walkable:
            if debug:
                gamelog.add('[KEY_PROCESS_WORLD]:\n\tMOVING ON WORLD MAP')

            player.saveWorldPos()

            if debug:
                gamelog.add("\tSAVED LAST WORLD POSITION")

            player.moveOnWorld(x, y)
            # description = calabaston.tilehasdescription(tposx, tposy)
            # if description:
            #     gamelog.add(description)
        else:
            # Individually log the specific reason
            if debug:
                gamelog.add('\tNOT MOVING ON WORLD MAP')
            # if blocked:
                # =============  START WALK LOG  =================================
                # gamelog.add("Cannot go there {}, {}".format(tx, ty))
                # ===============  END WALK LOG  =================================
            # elif not inbounds:
            #     gamelog.add(walkBlock.format("the edge of the map"))
            #     print("cannot go there", tx, ty)
            
            if not walkable and debug:
                gamelog.add("\tNOT WALKABLE: GW,GH: {},{}, PX,PY: {},{}".format(
                    calabaston.w,
                    calabaston.h,
                    tx, ty
                ))
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
        }
        walkBlock = "walked into {}"
        tposx = player.mx + x
        tposy = player.my + y

        # positions = {}
        # for unit in units:
        #     positions[unit.pos()] = unit
        # unit_pos = [(unit.x, unit.y) for unit in units]

        # 3 variables involved in walking
        # OUT-OF-BOUNDS -- is player within the map?
        # WALKABLE -- is the tile a walkable tile?
        # BLOCKEd -- is the tile blocked?
        unit_pos = []

        # inbounds = 0 <= tposx < dungeon.width \
        #     and 0 <= tposy < dungeon.height
        if debug:
            gamelog.add("[KEY PROCESS]:\n\tDUNGEON BOUNDS: DW, DH: {}, {} PX, PY: {} {}".format(
                dungeon.width, 
                dungeon.height, 
                tposx, 
                tposy))

        occupied = (tposx, tposy) in unit_pos
        # walkable = not dungeon.blocked(tposx, tposy)
        walkable = dungeon.walkable(tposx, tposy)

        if debug:
            gamelog.print_on()
            gamelog.add('\tWALKABLE: {}'.format(walkable))
            gamelog.print_off()

        if debug:
            gamelog.add('\tCURRENT LOCATION: {}'.format(player.mapPosition()))

        # (not blocked) and (not occupied) and (inbounds)
        if walkable:
            if debug:
                gamelog.add('\tMOVING IN DUNGEON')

            player.saveMapPos()

            if debug:
                gamelog.add("\tSAVED LAST MAP POSITION")

            player.moveOnMap(x, y)

            if debug:
                gamelog.add("\tPLAYER POSITION - {}".format(player.mapPosition()))

            if dungeon.square(tposx, tposy).items:
                gamelog.add("There is something here")

        else:
            if debug:
                gamelog.add('\tNOT MOVING IN DUNGEON BECAUSE: ')

            # elif occupied:
                # ============= START COMBAT LOG =================================
                # unit = positions[(tposx, tposy)]
                # if unit.r is not "human": # condition should be more complex
                #     unit.h -= 1
                #     gamelog.add("You attack the {}".format(unit.name))
                #     gamelog.add("The {} has {} left".format(unit.name, unit.h))
                #     if unit.h < 1:
                #         gamelog.add("You have killed the {}! You gain 15 exp".format(unit.name))
                #         units.remove(unit)
                # =============== END COMBAD LOG =================================
                # else:
                #     gamelog.add(walkBlock.format(unit.r))
                # pass

            if not walkable:
                # =============  START WALK LOG  =================================
                # find out if it was due to out of bounds error or block error
                if debug:
                    gamelog.add("\t\tNOT WALKABLE")
                if dungeon.out_of_bounds(tposx, tposy):
                    gamelog.add("Reached the edge of the map")
                else:
                    ch = dungeon.square(tposx, tposy).char
                    if ch == "~":
                        gamelog.add('you cannot swim')
                    else:
                        gamelog.add(walkBlock.format(walkChars[ch]))
                # ===============  END WALK LOG  =================================


            # elif not inbounds:
            #     gamelog.add(walkBlock.format("the edge of the map"))

        # refresh units
    #     units = list(filter(lambda u: u.h > 0, units))

    #     for unit in units:
    # #     if unit.c != "grey":
    #         x, y = 0, 0
    #         if randint(0, 1):
    #             x, y = num_movement[choice(list(num_movement.keys()))]
    #         try:
    #             blocked = blockables[unit.y+y][unit.x+x]
    #         except:
    #             blocked = False
    #         occupied = (unit.x + x, unit.y + y) in unit_pos or (unit.x+x, unit.y+y) == (player.x, player.y)
    #         outofbounds = 0 <= unit.x + x < len(blockables[0]) and 0 <= unit.y + y < len(blockables)
    #         if not (blocked or occupied or not outofbounds):
    #             unit.move(x, y)
        
    #     um.build()

    inventory_list = [
        "Head       : ", 
        "Neck       : ", 
        "Body       : ", 
        "Arms       : ",
        'Hands      : ', 
        "Left hand  : ",
        "Right hand : ", 
        "Left ring  : ",
        "Right ring : ",
        "Waist      : ",
        "Legs       : ",
        "Feet       : ",
    ]

    def openInventory():
        def backback():
            term.clear()
            for i in range(SCREEN_WIDTH):
                term.puts(i, 1, '#')
            term.puts(center('backback  ', SCREEN_WIDTH), 1, ' Backpack ')
            
        def inventory():
            term.clear()
            for i in range(SCREEN_WIDTH):
                term.puts(i, 1, '#')
            term.puts(center(' inventory ', SCREEN_WIDTH), 1, ' Inventory ')
            col, row = 1, 3
            gamelog.add("EQ: {}".format(*player.equipment))
            for i, l, e in zip(range(len(inventory_list)), inventory_list, player.equipment):
                term.puts(col, row+i*2, chr(ord('a')+i)+'. '+ l+(e if isinstance(e, str) else ''))
        debug=False
        if debug:
            gamelog.add("opening inventory")

        playscreen = False

        current_range = 0
        while True:
            term.clear()
            # border()
            # status_box()
            # log_box()
            # term.puts(2, 0, "[color=white]Inventory")
            inventory()
            term.refresh()
            code = term.read()
            if code in (term.TK_ESCAPE, term.TK_I,):
                break
            elif code == term.TK_V:
                # this is where our backback will be accessed
                pass
            elif code == term.TK_UP:
                if current_range > 0: current_range -= 1
            elif code == term.TK_DOWN:
                if current_range < 10: current_range += 1
        if debug:
            gamelog.add("Closing inventoryy")
        term.clear()

    def interactUnit(x, y):
        """Allows talking with other units"""
        def talkUnit(x, y):
            gamelog.add(um.talkTo(x, y))
            refresh()

        interactables = []
        for i, j in eightsquare(x, y):
            # dungeon.has_unit(i, j) -> returns true or false if unit is on the square
            if (i, j) != (x, y) and um.unitat(i, j):
                interactables.append((i, j))

        # no interactables
        if not interactables:
            gamelog.add("No one to talk with")

        # only one interactable
        elif onlyOne(interactables):
            i, j = interactables.pop()
            talkUnit(i, j)

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

    def interactItem(x, y, i):
        def pickItem():
            item = dungeon.square(x, y).items.pop()
            player.backpack.add_item(item)
            gamelog.add("You pick up a {}".format(item.name))
        
        if i == ",": # pickup
            if player.backpack.full():
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
                glog.add("Nothing to pick up")
                refresh()

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
        if debug:
            gamelog.add("[INTERACTSTAIRS]:")

        # first seperate logic by action take to differentiate going up versus down
        if k is ">": # and player.mapPosition() == dungeon.get
            if debug:
                gamelog.add("TRYING TO GO DOWN STAIRS")
            
            if player.mapPosition() == dungeon.getDownStairs():
                if debug:
                    gamelog.add('\tPLAYER STANDING ON STAIRS LEADING DOWN')
                
                if not dungeon.hasSublevel():
                    x = player.wx
                    y = player.wy
                    z = player.wz
                    t = "dungeon"
                    v = str(x) + str(y) + str(z) + t
                    
                    if debug:
                        gamelog.add("\tHASH: {}".format(hash(v)))
                    
                    sublevel = Map(buildDungeon(), "dungeon", hash(v))
                    
                    if debug:
                        print('\tSUBLEVEL ID: {}'.format(sublevel.map_id))
                    
                    sublevel.addParent(dungeon)
                    dungeon.addSublevel(sublevel)

                dungeon = dungeon.getSublevel()
                player.moveZAxis(1)
                player.resetMapPos(*dungeon.getUpStairs())

            else:
                gamelog.add('\tPLAYER NOT STANDING ON STAIRS LEADING DOWN')

        else:
            gamelog.add("\tTRYING TO GO UP STAIRS")

            # check if you're in a city
            if player.worldPosition() in calabaston.enterable_legend.keys():
                if debug:
                    gamelog.add('\tPLAYER IN CITY MAP')
                    gamelog.add('\tPLAYER MOVES FREELY IN CITY')

                player.moveZAxis(-1)

                if debug:
                    gamelog.add("\tCHECKING PARENT")

                dungeon = dungeon.getParent()

                if debug:
                    gamelog.add("\tPARENT ID: {}".format(dungeon.map_id))

            elif calabaston.is_wilderness(*player.worldPosition()):
                
                gamelog.add('\tPLAYER IS IN WILDERNESS\nPLAYER CAN EXIT MAP ANYWHERE')
                player.moveZAxis(-1)
                dungeon = dungeon.getParent()

            # check if you're in a dungeon
            elif player.mapPosition() == dungeon.getUpStairs():
                if debug:
                    gamelog.add('\tPLAYER STANDING ON STAIRS LEADING UP')

                # dungeon will have parent -- need to differentiate between
                # world and first level dungeon
                if debug:
                    gamelog.add("\tGOING UP STAIRS")

                player.moveZAxis(-1)

                if debug:
                    gamelog.add("\tZAXIS AFTER GOING UP STAIRS: {}".format(player.wz))
                    gamelog.add("\tCHECKING PARENT")
                
                dungeon = dungeon.getParent()

                if debug:
                    gamelog.add("\tPARENT ID: {}".format(dungeon.map_id))
                # if isinstance(dungeon, World):
                #     dungeon = None
                #     player.resetMapPos(0, 0)
            else:
                if debug:
                    gamelog.add('\tPLAYER NOT STANDING ON STAIRS LEADING UP')

            if debug:
                gamelog.add('\tCHECKING IF PARENT IS OVERWORLD')

            if isinstance(dungeon, World):
                if debug:
                    gamelog.add('\tPARENT IS OVERWORLD -- DESTROYING DUNGEON REFERENCE')

                dungeon = None
                player.resetMapPos(0, 0)

            else:
                if debug:
                    gamelog.add('\tPARENT IS NOT OVERWORLD -- DUNGEON REFERENCE STILL EXISTS')
                
    def enter_map():
        '''World Action:
        Logic:
            if at world level, check if there exists a map
            if exists -> enter
            else -> build the map and add it to the world
        '''
        if debug:
            gamelog.add('[ENTER MAP]:')

        if player.wz == -1:
            if debug:
                gamelog.add("\tCalabaston has map: {}".format(calabaston.mapAt(*player.worldPosition())))
                gamelog.add("\tPlayer @ {},{}".format(*player.worldPosition()))

            # builds the map
            player.moveZAxis(1)

            # check for non existance at map at player's world position
            if not calabaston.mapAt(*player.worldPosition()):
                # print("in legend", player.worldPosition() in calabaston.enterable_legend.keys())
                # print(player.worldPosition())
                # entering a city location
                if player.worldPosition() in calabaston.enterable_legend.keys():
                    fileloc = calabaston.enterable_legend[player.worldPosition()].lower().replace(' ','_')
                    filename = "./assets/maps/" + fileloc + ".png"
                    # print(filename)
                    try:
                        x = player.wx
                        y = player.wy
                        z = player.wz
                        t = 'city'
                        v = str(x) + str(y) + str(z) + t
                        
                        if debug:
                            gamelog.add('CITY HASH ID: {}'.format(hash(v)))

                        location = Map(stringify(filename), "city", hash(v), SCREEN_WIDTH, SCREEN_HEIGHT)
                    except FileNotFoundError:
                        # print('no file of that name')
                        raise FileNotFoundError("Map for {} not yet implemented".format(fileloc))
                    # basically spawn in town center
                    player.resetMapPos(location.width//2, location.height//2)

                else:
                    # print('Not important city')
                    tile = calabaston.accessTile(*player.worldPosition())
                    
                    if debug:
                        gamelog.add("TILE TYPE: {}".format(tile.land))
                    
                    # get options based on land tile
                    # build_options = Dungeon.build_options()
                    wilderness = tile.land in ("plains", "dark woods", "hills", "forest", "desert")
                    
                    x = player.wx
                    y = player.wy
                    z = player.wz
                    t = 'wilderness'
                    v = str(x) + str(y) + str(z) + t

                    if wilderness:
                        neighbors = calabaston.accessTileNeighbors(*player.worldPosition())
                    
                        location = Map(
                            buildTerrain(tile.land, buildopts=neighbors), 
                            tile.land,
                            mapid=hash(v))
                    
                        x, y = player.getWorldPosOnEnter()
                        x = max(int(location.width * x - 1), 0)
                        y = max(int(location.height * y - 1), 0)
                        
                        if debug:
                            gamelog.add("location w,h {}, {}".format(location.width, location.height))
                        
                        player.resetMapPos(x, y)
                    
                    # Build a dungeon tile
                    else:
                        location = Map(
                            buildDungeon(1000), 
                            tile.land,
                            mapid=hash(v)) # dungeon.build(options)
                    
                        player.resetMapPos(*location.getUpStairs())
                    
                    if debug:
                        gamelog.add("\tLocation Exit : {}".format(location.getUpStairs()))
                        gamelog.add("\tLocation Enter: {}".format(location.getDownStairs()))
                    # print('PP:',player.mapPosition())
                    # print('Exit', location.getExit())

                location.addParent(calabaston)
                calabaston.add_location(location, *(player.worldPosition()))

            else:
                # re-enter city
                if debug:
                    gamelog.add("PLAYER POSITION ON WORLD {}, {}".format(
                        *player.worldPosition()))
                
                if player.worldPosition() in calabaston.enterable_legend.keys():
                    location = calabaston.get_location(*player.worldPosition())
                    player.resetMapPos(location.width//2, location.height//2)

                else:
                    location = calabaston.get_location(*player.worldPosition())
                    
                    # reenter a wilderness
                    if location.maptype in ("plains", "dark woods", "hills", "forest", "desert"):
                        x, y = player.getWorldPosOnEnter()
                        x = int((location.width-1) * x)
                        y = int((location.height-1) * y)
                        player.resetMapPos(x, y)
                    
                    # reenter a dungeon:
                    else:
                        player.resetMapPos(*calabaston.get_location(*player.worldPosition()).getUpStairs())
            
        # probably in a dungeon
        elif player.wz == 0:
            gamelog.add("Map Level 0")
            player.moveZAxis(1)
            if player.mapPosition() == dungeon.getEntrance():
                gamelog.add('ill allow it -- move down')
                pass
            else:
                gamelog.add("cannot enter on current tile")

            # if in city then shouldnt really have a dungeon
            # could add a basement/attic level
            # also add check to make sure not inside a building -- if in building then '<' wouldnt work
            # i mean it could work but just wouldnt zoom out to world view you know
            # if in wilderness can only '>' on a dungeon enterance
            # if in a dungeon then goes down one sublevel
        elif player.wz > 0:
            gamelog.add('at level 0 -- trying sublevel')
        
            # processes all other dungeon subleves
        
        else:
            gamelog.add('no enter_map action')
            pass

    world_actions={
        # '<': exit_map,
        '>': enter_map
    }
    def processWorldAction(key):
        if debug:
            print('[PROCESS WORLD ACTION]: key - {}'.format(key))
        if key == ">":
            world_actions[key]()

    actions={
        'o': interactDoor,
        'c': interactDoor,
        'i': openInventory,
        't': interactUnit,
        '>': interactStairs,
        '<': interactStairs,
        # 'f1': dungeon._sundown,
        # 'f2': dungeon._sunup,
        ',': interactItem,
    }

    def processAction(x, y, key):
        # gamelog.add("[PROCESS ACTION]: KEY - {}".format(key))
        if key in ("o", "c"):
            actions[key](x, y, key)
        elif key in ("<"):
            if debug:
                gamelog.add('[PROCESS ACTION]: EXIT')
            actions[key](x, y, key)
        elif key in (">"):
            gamelog.add('enter')
            actions[key](x, y, key)
        elif key in ("t"):
            actions[key](x, y)
        elif key in ("i"):
            actions[key]()
        elif key in ("f1, f2"):
            actions[key]()
        else:
            if debug:
                gamelog.add("[PROCESS ACTION]: UNKNOWN COMMAND - {} @ ({}, {})".format(key, x, y))            
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
                term.puts(SCREEN_WIDTH-20+i, 0, border_line)
                term.puts(SCREEN_WIDTH-20+i, 10, border_line)
            if i < 60:
                term.puts(i, SCREEN_HEIGHT-6, border_line)
            term.puts(i, SCREEN_HEIGHT-1, border_line)
        
        # x axis
        for j in range(35):
            if j < 6:
                term.puts(0, SCREEN_HEIGHT-6+j, border_line)
            term.puts(SCREEN_WIDTH-20, j, border_line)
            term.puts(SCREEN_WIDTH-1, j, border_line)

    turn = 0
    def status_box():
        col, row = 0, 2
        term.puts(col, row+0, player.name)
        term.puts(col, row+1, player.gender + " " + player.race)
        term.puts(col, row+2, player.job)

        term.puts(col, row+4, "LVL: {:>6}".format(player.level))
        term.puts(col, row+5, "EXP: {:>6}".format("{}/{}".format(player.exp, player.advexp)))

        term.puts(col, row+7, "HP:  {:>6}".format("{}/{}".format(player.hp, player.total_hp)))
        term.puts(col, row+8, "MP:  {:>6}".format("{}/{}".format(player.mp, player.total_mp)))
        term.puts(col, row+9, "SP:  {:>6}".format(player.sp))

        term.puts(col, row+11, "STR: {:>6}".format(player.str)) 
        term.puts(col, row+12, "CON: {:>6}".format(player.con))
        term.puts(col, row+13, "DEX: {:>6}".format(player.dex))
        term.puts(col, row+14, "INT: {:>6}".format(player.int))
        term.puts(col, row+15, "WIS: {:>6}".format(player.wis))
        term.puts(col, row+16, "CHA: {:>6}".format(player.cha))

        term.puts(col, row+18, "GOLD:{:>6}".format(player.gold))

    def log_box():
        messages = gamelog.write().messages
        if messages:
            for idx in range(len(messages)):
                term.puts(1, SCREEN_HEIGHT- gamelog.maxlines + idx, messages[idx])

    def map_box():
        """ Logic:
                Should first print map in gray/black
                Then print units/interactables?
                Finally light sources and player?"""
        term.composition(False)
        dungeon.fov_calc(lights+[(player.mx, player.my, player.sight)])
        for x, y, lit, ch, bkgd in dungeon.output(player.mx, player.my, []):
            # ch = ch if len(str(ch)) > 1 else chr(toInt(palette[ch]))
            term.puts(x + 14, y + 1, "[color={}]".format(lit) + ch + "[/color]")
        term.refresh()
        
    def worldlegend_box():
        x, y = SCREEN_WIDTH-12, 1
        boxheader = "Map Legend"
        selected(center(surround(calabaston.name), 14), 1, surround(calabaston.name))   
        selected(center(boxheader, 12), 3, surround(boxheader))
        for char, color, desc, i in calabaston.worldlegend():
            term.puts(0, i + 4, "[c={}] {}[/c] {}".format(color, char, desc))
        footer = i + 5 + 3

        # check if player position is over a city/enterable area
        # this is purely a ui enhancement. Actually entering a city is not that much different
        # than entering a dungeon/wilderness area
        if player.worldPosition() in calabaston.enterable_legend.keys():
            enterable_name = surround(calabaston.enterable_legend[(player.wx, player.wy)])       
            selected(
                center(surround(enterable_name) if len(enterable_name) <= 12 else enterable_name, 12),
                footer,
                surround(enterable_name) if len(enterable_name) <= 12 else enterable_name)

        # check if player position is over a dungeon position
        elif player.worldPosition() in calabaston.dungeon_legend.keys():
            dungeon_name = surround(calabaston.dungeon_legend[player.worldPosition()])
            selected(
                center(surround(dungeon_name) if len(dungeon_name) <= 12 else dungeon_name, 12),
                footer,
                surround(dungeon_name) if len(dungeon_name) <= 12 else dungeon_name)
        footer += 1

        # Add land types to the overworld ui
        landtype = calabaston.get_landtype(*player.worldPosition())
        if landtype:
            selected(
                center(surround(landtype), 12),
                footer,
                surround(landtype))
        

    def worldmap_box():
        '''Displays the world map tiles in the terminal'''
        def scroll(position, screen, worldmap):
            '''
            @position: current position of player 1D axis
            
            @screen  : size of the screen
            
            @worldmap: size of the map           
            '''
            halfscreen = screen//2
            # less than half the screen - nothing
            if position < halfscreen:
                return 0
            elif position >= worldmap - halfscreen:
                return worldmap - screen
            else:
                return position - halfscreen

        # world map header and variables used in calculating screen box
        # selected(center(surround(calabaston.name), SCREEN_WIDTH), 0, surround(calabaston.name))
        SCREEN_WIDTH_OFFSET = 14 # save 14 tiles on left side of screen to display map information
        SCREEN_HEIGHT_OFFSET = 2 # save two tiles to create horizonatal bars on top and bottom
        TOTAL_MAP_WIDTH = SCREEN_WIDTH - SCREEN_WIDTH_OFFSET    # keeping these variables explicit
        TOTAL_MAP_HEIGHT = SCREEN_HEIGHT - SCREEN_HEIGHT_OFFSET # so we dont have to calculate again
        cx = scroll(player.wx, TOTAL_MAP_WIDTH, calabaston.w,)
        cy = scroll(player.wy, TOTAL_MAP_HEIGHT, calabaston.h)
        cxe = cx+TOTAL_MAP_WIDTH
        cye = cy+TOTAL_MAP_HEIGHT

        for x, y, col, ch in calabaston.draw(wview, 
                                    *(player.worldPosition()), 
                                    (cx, cxe), (cy, cye)):
            term.puts(x + 14, y + 1, "[c={}]{}[/c]".format(col, ch))

    # very first thing is game logger initialized to output messages on terminal
    # gamelog = GameLogger(4, ptt=True)
    gamelog = GameLogger(4)

    # if character is None then improperly accessed new_game
    # else unpack the character
    if character==None:
        return output(proceed=False, value="No Character Data Input")
    else:
        # gamelog.add("[SETUP]: CHARACTER - {}".format(*character))
        player = Player(character)
    
    # pointer to the current view
    wview = WorldView.Geo
    calabaston = World()
    calabaston.load(
                "./assets/worldmap.png", 
                "./assets/worldmap_territories.png",
                "./assets/worldmap_kingdoms.png")   
    # Before anything happens we create our character
    # LIMIT_FPS = 30 -- later used in sprite implementation
    blocked = []

    # End graphics functions
    # global game variables
    #MAP_WIDTH, MAP_HEIGHT = 24, 48

    MAP_FACTOR = 2
    COLOR_DARK_WALL = term.color_from_argb(128, 0, 0, 100)
    COLOR_DARK_GROUND = term.color_from_argb(128, 50, 50, 150)
    #px, py = SCREEN_WIDTH//2, SCREEN_HEIGHT//2
    wpx, wpy = player.worldPosition()
    # dpx, dpy = dungeon.start_position()

    # blanks
        #px, py = 0, 0
        # units = Map.appendUnitList("./unitlist/test_map_colored.png")
        # um = UnitManager()
        # ======================================================================================
        # player = Player(character, dpx, dpy)
        # ======================================================================================
        # player.inventory[0] = "sword"
        # rat = Object("rat", dpx-5, dpy, 'r', c='#904040', r="monster")
        # rat.message = "I am a rat"
        # rat2 = Object("rat", 85, 29, 'R', r="monster")
        # rat2.message = "I am a big rat"
        # npc = Object("v1", dpx+1, dpy, '@', 'orange')
        # npc1 = Object("v2", 5, 15, '@', 'orange')
        # npc2 = Object("v3", 0, 56, '@', 'orange')
        # guard3 = Object("v4", 63, 31, '@', 'orange')
        # guard1 = Object("v5", 64, 32, "@", 'orange')
        # guard2 = Object("v6", 63, 37, "@", 'orange')
        # guard4 = Object("v7", 64, 37, '@', 'orange')
        # units = [npc, guard1, guard2, guard3, guard4, npc1, npc2, rat, rat2]
        # units = [npc, rat]
        # um.add(units)
        # print(um._positions.keys())
        # dungeon.add_item(87, 31, Item("sword", "(", "grey"))

    proceed = True
    # lr = 5
    lights = []
    dungeon = None
    while proceed:
        # gamelog.add('-' * 30)
        # gamelog.add('[MAIN GAME LOOP]:')
        term.clear()
        # gamelog.add('\tWORLD PLAYER LEVEL - {}'.format(player.wz))
        # player is on overworld level == -1
        if player.wz == -1:

            # World View
            worldmap_box()
            worldlegend_box()
            term.refresh()

            x, y, a = key_in_world()
            # gamelog.add('\tACTION - {} {} {}'.format(x, y, a))
            if a != "Do Nothing" and a != 0:
                processWorldAction(a)
            elif (x, y) != (0, 0):
                # gamelog.add('\tNOT MOVING')
                key_process_world(x, y)
            # else:
                # gamelog.add('\tDOING NOTHING')
                # pass

        # player is on local map level >= 0
        else:
            # gamelog.add('\tPLAYER IN LOCAL MAP')
            # gamelog.add('\tPLAYER WORLD POSITION: {}'.format(player.worldPosition()))
            # City, Wilderness, Level 0 Dungeon
            if dungeon == None:
                dungeon = calabaston.get_location(*player.worldPosition())

                if debug:
                    gamelog.add('\tMAP ID: {}, {}'.format(
                        dungeon.maptype,
                        dungeon.map_id
                    ))

                if player.wz > 0:
                    for i in range(player.wz):
                        dungeon = dungeon.getSublevel()
            status_box()
            # border()
            log_box()
            map_box()
            x, y, a = key_in()
            if a:
                processAction(player.mx, player.my, a)
            else:
                key_process(x, y)

    # player.dump()
    # gamelog.dumps()   
    return False
# End New Game Menu

if __name__ == "__main__":
    setup()
    setup_font('unscii-8', 8, 16)
    character = create().value
    setup_game()
    setup_font('unscii-8-thin', 8, 16)

    # setup_font('unscii-8', 8 ,8)
    new_game(character)
