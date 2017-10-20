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
from spaceship.objects import Map, Object, Character, Item, Player
from spaceship.create_character import create_character as create
from spaceship.screen_functions import center, surround, selected
from bearlibterminal import terminal as term
from spaceship.manager import UnitManager
from spaceship.gamelog import GameLogger
from random import randint, choice
from collections import namedtuple
from namedlist import namedlist
from spaceship.dungeon import build
from spaceship.setup import setup, output, setup_font
from spaceship.world import World
from time import clock

class Level: World, City, Dungeon = range(3)
class WorldView: Geo, Pol, King = range(3)

def new_game(character=None):

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
        nonlocal proceed, wview
        keydown = namedtuple("Key_Press", "x y a")
        act, x, y = 0, 0, 0
        code = term.read()
        while code in (term.TK_SHIFT, term.TK_CONTROL, term.TK_ALT):
            code = term.read()
        if code in (term.TK_CLOSE, term.TK_ESCAPE, term.TK_Q):
            proceed = False

        # map draw types
        elif code in (term.TK_P, term.TK_G, term.TK_K):
            if code == term.TK_P and wview != WorldView.Pol:
                wview = WorldView.Pol
            elif code == term.TK_G and wview != WorldView.Geo:
                wview = WorldView.Geo
            else:
                wview = WorldView.King
            act = "Do Nothing"
        
        # elif code in (term.TK_COMMA, term.TK_PERIOD):
        #     if code == term.TK_COMMA and term.state(term.TK_SHIFT):
        #         act = "exit"
        #     elif code == term.TK_PERIOD and term.state(term.TK_SHIFT):
        #         act = "enter"
        elif code in (term.TK_COMMA, term.TK_PERIOD):
            if term.state(term.TK_SHIFT):
                try:
                    act = world_key_actions[code].key
                except KeyError:
                    raise
        elif code == term.TK_Z:
            act = "Zoom"
        
        # arrow keys
        elif code in key_movement:
            x, y = key_movement[code]
        # numberpad keys
        elif code in num_movement:
            x, y = num_movement[code]
        # keyboard keys
        # elif code in key_actions:
        #     act = key_actions[code].key
        # any other key F-keys, Up/Down Pg, etc
        else:
            print("unrecognized command")
        # make sure we clear any inputs before the next action is processed
        # allows for the program to go slow enough for human playability
        while term.has_input(): 
            term.read()
        print(x, y, act)
        return keydown(x, y, act)

    def key_in():
        nonlocal proceed
        keydown = namedtuple("Key_Down", ("x", "y", "a"))
        # movement
        act, x, y = 0, 0, 0
        code = term.read()
        while code in (term.TK_SHIFT, term.TK_CONTROL, term.TK_ALT):
            code = term.read()
        if any([term.state(tk) for tk in (term.TK_SHIFT, term.TK_CONTROL, term.TK_ALT)]):
            print("CTRL | ALT | SHIFT")
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
            print("unrecognized command")
        # make sure we clear any inputs before the next action is processed
        # allows for the program to go slow enough for human playability
        while term.has_input(): 
            term.read()
        return keydown(x, y, act)

    # should change to movement process

    def onlyOne(container):
        return len(container) == 1

    def eightsquare(x, y):
        space = namedtuple("Space", ("x","y"))
        return [space(x+i,y+j) for i, j in list(num_movement.values())]

    def key_process_world(x, y):
        tx = player.wx + x
        ty = player.wy + y

        inbounds = 0 <= tx < calabaston.w and 0 <= ty < calabaston.h
        walkable = calabaston.walkable(tx, ty)

        if walkable and inbounds:
            print('Moving On Map')
            player.moveOnWorld(x, y)
            # description = calabaston.tilehasdescription(tposx, tposy)
            # if description:
            #     gamelog.add(description)
        else:
            print('Not Moving On Map')
            if blocked:
                # =============  START WALK LOG  =================================
                gamelog.add("Cannot go there")
                # ===============  END WALK LOG  =================================
            elif not inbounds:
                gamelog.add(walkBlock.format("the edge of the map"))

    def key_process(x, y):
        walkChars = {
            "+": "a door",
            "/": "a door",
            "o": "a lamp",
            "#": "a wall",
            "x": "a post",
            "~": "a river",
        }
        walkBlock = "walked into {}"
        tposx = player.mx + x
        tposy = player.my + y

        # positions = {}
        # for unit in units:
        #     positions[unit.pos()] = unit
        # unit_pos = [(unit.x, unit.y) for unit in units]
        unit_pos = []

        inbounds = 0 <= tposx < dungeon.width-1 \
            and 0 <= tposy < dungeon.height-1

        occupied = (tposx, tposy) in unit_pos

        walkable = dungeon.walkable(tposx, tposy)
        print('Walk In', walkable, inbounds)
        print('CURRENT LOCATION: ', player.mapPosition())

        # (not blocked) and (not occupied) and (inbounds)
        if walkable and inbounds:
            print('Moving on Dungeon')
            player.moveOnMap(x, y)
            print("pP:",player.mapPosition())
            if dungeon.square(tposx, tposy).items:
                gamelog.add("There is something here")
        else:
            print('Not Moving on Dungeon')
            if blocked:
                # =============  START WALK LOG  =================================
                ch = dungeon.square(tposx, tposy).char
                gamelog.add(walkBlock.format(walkChars[ch]))
                # ===============  END WALK LOG  =================================

            elif occupied:
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
                pass
            elif not inbounds:
                gamelog.add(walkBlock.format("the edge of the map"))

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
        def inventory():
            term.clear()
            for i in range(SCREEN_WIDTH):
                term.puts(i, 1, '#')
            term.puts(center(' inventory ', SCREEN_WIDTH), 1, ' Inventory ')
            col, row = 1, 3
            print(player.equipment)
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
            gamelog.add("Which direction?")
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
                openDoor(x+cx, y+cy) if opening else closeDoor(x+cx, y+cy)

        map_box()

    def interactStairs(x, y, k):
        """Allows interactions with stairs"""
        if k is ">":
            gamelog.add("Going up the stairs")
        else:
            gamelog.add("Going down the stairs")

    def enterMap():
        '''World Action:
        Logic:
            if at world level, check if there exists a map
            if exists -> enter
            else -> build the map and add it to the world
        '''
        # print('enter map')
        if player.zAxis == -1
            # print(calabaston.mapAt(*player.worldPosition()))
            # builds the map
            player.moveZAxis(1)
            if not calabaston.mapAt(*player.worldPosition()):
                # print("in legend", player.worldPosition() in calabaston.enterable_legend.keys())
                # print(player.worldPosition())
                if player.worldPosition() in calabaston.enterable_legend.keys():
                    filename = calabaston.enterable_legend[player.worldPosition()].lower().replace(' ','_')
                    filename = "./assets/maps/" + filename + ".png"
                    # print(filename)
                    try:
                        location = Map(stringify(filename), SCREEN_WIDTH, SCREEN_HEIGHT)
                    except FileNotFoundError:
                        # print('no file of that name')
                        raise
                    # basically spawn in town center
                    player.resetMapPos(location.width//2, location.height//2)

                else:
                    # print('Not important city')
                    tile = calabaston.accessTile(*player.worldPosition())
                    # print(tile.land)
                    # get options based on land tile
                    # build_options = Dungeon.build_options()
                    location = Map(build(1000)) # dungeon.build(options)
                    player.resetMapPos(*location.getExit())
                    # print('PP:',player.mapPosition())
                    # print('Exit', location.getExit())
                calabaston.add_location(location, *(player.worldPosition()))
        elif player.zAxis == 0:
            pass
            # if in city then shouldnt really have a dungeon
            # could add a basement/attic level
            # also add check to make sure not inside a building -- if in building then '<' wouldnt work
            # i mean it could work but just wouldnt zoom out to world view you know
            # if in wilderness can only '>' on a dungeon enterance
            # if in a dungeon then goes down one sublevel
        else:
            pass
            # processes all other dungeon subleves
            

    def exitMap():
        nonlocal level
        level = Level.World

    world_actions={
        '<': exitMap,
        '>': enterMap
    }
    def processWorldAction(key):
        print('IN ProcessWorldAction:', key)
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
        if key in ("o", "c"):
            actions[key](x, y, key)
        if key in (","):
            if term.state(term.TK_SHIFT):
                exitMap()
            else:
                actions[key](x, y, key)
        elif key in ("t"):
            actions[key](x, y)
        elif key in ("i"):
            actions[key]()
        elif key in ("f1, f2"):
            actions[key]()
        else:
            print("unknown command: {} @ ({}, {})".format(key, x, y))            

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
                term.puts(1, SCREEN_HEIGHT-5+idx, messages[idx])

    def map_box():
        """ Logic:
                Should first print map in gray/black
                Then print units/interactables?
                Finally light sources and player?"""
        term.composition(False)
        dungeon.fov_calc(lights+[(player.mx, player.my, player.sight)])
        for x, y, lit, ch, bkgd in list(dungeon.output(player.mx, player.my, [])):
            # ch = ch if len(str(ch)) > 1 else chr(toInt(palette[ch]))
            term.puts(x+14, y+1, "[color={}]".format(lit)+ch+"[/color]")
        term.refresh()
        
    def worldlegend_box():
        x, y = SCREEN_WIDTH-12, 1
        boxheader = "Map Legend"
        selected(center(surround(calabaston.name), 14), 1, surround(calabaston.name))   
        selected(center(boxheader, 12), 3, surround(boxheader))
        for char, color, desc, i in calabaston.worldlegend():
            term.puts(0, i*2+5, "[c={}] {}[/c] {}".format(color, char, desc))
        footer = i*2+5+3
        if player.worldPosition() in calabaston.enterable_legend.keys():
            enterable_name = surround(calabaston.enterable_legend[(player.wx, player.wy)])       
            selected(center(surround(enterable_name) if len(enterable_name) >= 12 else enterable_name, 14),
            footer,
            surround(enterable_name) if len(enterable_name) >= 12 else enterable_name)

    def worldmap_box():
        # world map header
        # selected(center(surround(calabaston.name), SCREEN_WIDTH), 0, surround(calabaston.name))
        cx = scroll(player.wx, SCREEN_WIDTH-14, calabaston.w,)
        cy = scroll(player.wy, SCREEN_HEIGHT-2, calabaston.h)
        cxe = cx+SCREEN_WIDTH-14
        cye = cy+SCREEN_HEIGHT-2

        for x, y, col, ch in list(calabaston.draw(wview, 
                                    *(player.worldPosition()), 
                                    (cx, cxe), (cy, cye))):
            term.puts(x+14, y+1, "[c={}]{}[/c]".format(col, ch))

    # if character is None then improperly accessed new_game
    # else unpack the character
    if character==None:
        return output(proceed=False, value="No Character Data Input")
    else:
        print(*character)
        player = Player(character)
    # dungeon = Map(stringify("./assets/testmap_empty.png"))
    # dungeon = Map(build())
    
    # pointer to the current view
    wview = WorldView.Geo
    calabaston = World().load(
                "./assets/worldmap.png", 
                "./assets/worldmap_territories.png",
                "./assets/worldmap_kingdoms.png")    

    # Before anything happens we create our character
    # LIMIT_FPS = 30 -- later used in sprite implementation
    blocked = []
    # dungeon = Map(stringify("./assets/testmap_colored.png"))

    # End graphics functions
    gamelog = GameLogger(4)
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
        # map = Map(parse("testmap.dat"))
        #dungeon = Map(stringify("./assets/testmap.png"))
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
    while proceed:
        term.clear()
        print('LEVEL: ', player.zAxis)
        if player.zAxis == -1:
            # World View
            worldmap_box()
            worldlegend_box()
            term.refresh()

            x, y, a = key_in_world()

            if a != "Do Nothing" and a != 0:
                processWorldAction(a)
            elif (x, y) != (0, 0):
                print('moving')
                key_process_world(x, y)
            else:
                print('do nothing')

        elif player.zAxis == 0:
            # City, Wilderness, Level 0 Dungeon
            dungeon = calabaston.map_data[player.wy][player.wx]
            status_box()
            # border()
            log_box()
            map_box()
            x, y, a = key_in()
            if a:
                processAction(player.mx, player.my, a)
            else:
                key_process(x, y)
        else:
            # dungeon = calabaston.map_data[player.wx][player]
            # for i in range(player.zAxis):
                # dungeon = dungeon.getSubLevel()
            pass

    player.dump()
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
