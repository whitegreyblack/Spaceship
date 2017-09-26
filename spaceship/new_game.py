# main implementation of core mechanics
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.action import key_movement, num_movement, key_actions, action, keypress
from spaceship.constants import SCREEN_HEIGHT, SCREEN_WIDTH, FOV_RADIUS
from spaceship.tools import bresenhams, deltanorm, movement
from spaceship.maps import stringify, hextup, hexone, toInt
from spaceship.objects import Map, Object, Character, Item
from bearlibterminal import terminal as term
from spaceship.manager import UnitManager
from spaceship.gamelog import GameLogger
from random import randint, choice
from collections import namedtuple
from namedlist import namedlist
from spaceship.setup import setup
from time import clock

def new_game(player, name):
    print(name, player)
    dungeon = Map(stringify("./assets/testmap_colored.png"))

    def refresh(lines=[]):
        for line in lines:
            gamelog.add(line)
        term.clear()
        border()
        map_box()
        status_box()
        log_box()
        term.refresh()
    # END SETUP TOOLS
    # ---------------------------------------------------------------------------------------------------------------------#
    # Keyboard input


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
    walkChars = {
        "+": "a door",
        "/": "a door",
        "o": "a lamp",
        "#": "a wall",
        "x": "a post",
        "~": "a river",
    }
    walkBlock = "walked into {}"

    def onlyOne(container):
        return len(container) == 1

    def eightsquare(x, y):
        space = namedtuple("Space", ("x","y"))
        return [space(x+i,y+j) for i, j in list(num_movement.values())]

    def key_process(x, y, blockables, units):
        tposx = player.x + x
        tposy = player.y + y
        positions = {}
        for unit in units:
            positions[unit.pos()] = unit
        unit_pos = [(unit.x, unit.y) for unit in units]

        outofbounds = 0 <= tposx < len(blockables[0]) \
            and 0 <= tposy < len(blockables)

        occupied = (tposx, tposy) in unit_pos

        try:
            blocked = blockables[tposy][tposx]
            ch = dungeon.square(tposx, tposy).char
        except BaseException:
            blocked = False


        # (not blocked) and (not occupied) and (inbounds)
        if not (blocked or occupied or not outofbounds):
            player.move(x, y)
            if dungeon.square(tposx, tposy).items:
                gamelog.add("There is something here")
        else:
            if blocked:
                gamelog.add(walkBlock.format(walkChars[ch]))
                # if ch == "+":
                #     gamelog.add(walkBlock.format("a door"))
                # if ch == "#":
                #     gamelog.add(walkBlock.format("a wall"))
                    # gamelog.add(f"{player.x+x}, {player.y+y}")
            elif occupied:
                # ============= START COMBAT LOG =================================
                unit = positions[(tposx, tposy)]
                if unit.r is not "human": # condition should be more complex
                    unit.h -= 1
                    gamelog.add("You attack the {}".format(unit.name))
                    gamelog.add("The {} has {} left".format(unit.name, unit.h))
                    if unit.h < 1:
                        gamelog.add("You have killed the {}".format(unit.name))
                # =============== END COMBAD LOG =================================
                else:
                    gamelog.add(walkBlock.format(unit.r))
            elif outofbounds:
                gamelog.add(walkBlock.format("the edge of the map"))

        # refresh units
        units = list(filter(lambda u: u.h > 0, units))

        for unit in units:
    #     if unit.c != "grey":
            x, y = 0, 0
            if randint(0, 1):
                x, y = num_movement[choice(list(num_movement.keys()))]
            try:
                blocked = blockables[unit.y+y][unit.x+x]
            except:
                blocked = False
            occupied = (unit.x + x, unit.y + y) in unit_pos or (unit.x+x, unit.y+y) == (player.x, player.y)
            outofbounds = 0 <= unit.x + x < len(blockables[0]) and 0 <= unit.y + y < len(blockables)
            if not (blocked or occupied or not outofbounds):
                unit.move(x, y)
        
        um.build()

    inventory_list = [
        "head       :", 
        "neck       :", 
        "body       :", 
        "back       :", 
        "left hand  :",
        "right hand :", 
        "waist      :",
        "legs       :",
        "feet       :",
        "token      :",
    ]
    def openInventory():
        debug=False
        if debug:
            gamelog.add("opening inventory")
        playscreen = False

        current_range = 0
        while True:
            term.clear()
            border()
            status_box()
            log_box()
            term.puts(2, 0, "[color=white]Inventory")
            for i in range(10):
                if i == 3 and player.inventory[0]:
                    term.puts(2, i+2, inventory_list[i] + " " + str(player.inventory[0].slot))
                term.puts(2, i+2, inventory_list[i])
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

    def interactDoor(x, y, k):
        """Allows interaction with doors"""
        def openDoor(i, j):
            gamelog.add("Opened door")
            dungeon.open_door(i, j)
            dungeon.unblock(i, j)

        def closeDoor(i, j):
            gamelog.add("Closed door")
            dungeon.close_door(i, j)
            dungeon.reblock(i, j)

        opening = k is "o"
        char = "+" if opening else "/"

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
            gamelog.add("No {} near you".format("openables" if opening else "closeables"))
        
        elif onlyOne(reachables):
            i, j = reachables.pop()
            openDoor(i, j) if opening else closeDoor(i, j)

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

    actions={
        'o': interactDoor,
        'c': interactDoor,
        'i': openInventory,
        't': interactUnit,
        'f1': dungeon._sundown,
        'f2': dungeon._sunup,
        ',': interactItem,
    }

    def processAction(x, y, key):
        if key in ("o", "c", ","):
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
        term.puts(61, 1, "[color=red]HP[/color]: {}".format(player.h))
        term.puts(61, 3, "[color=blue]MP[/color]: {}".format(player.m))
        term.puts(61, 5, "[color=green]SP[/color]: {}".format(player.s))
        term.puts(61, 7, "[color=yellow]{}[/color]".format('day' if dungeon._sun() else 'night'))
        term.puts(61, 9, "[color=orange]{}[/color]".format(turn))

    def inventory_box():
        term.puts(61, 11, "{}".format(player.inventory[0].slot))

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
        dungeon.fov_calc(lights+[(player.x, player.y, player.l)])
        for x, y, lit, ch, bkgd in list(dungeon.output(player.x, player.y, units)):
            # term.bkcolor(bgkd)
            if len(str(ch)) < 2:
                term.puts(x, y, "[color={}]{}[/color]".format(lit, ch))
            else:
                try:
                    if ch == 57389:
                        term.bkcolor(bkgd if bkgd else "black")
                        term.puts(x, y, "[color={}]{}[/color]".format(lit, ch))
                    else:
                        term.bkcolor(bkgd if bkgd else "black")
                        term.puts(x, y, "[color={}]".format(lit)+chr(toInt(ch))+"[/color]")
                except:
                    print(lit, ch, bkgd)
                    raise
        term.refresh()
    # Before anything happens we create our character
    # LIMIT_FPS = 30 -- later used in sprite implementation
    blocked = []
    dungeon = Map(stringify("./assets/testmap_colored.png"))

    # End graphics functions
    gamelog = GameLogger(4)
    # global game variables
    #MAP_WIDTH, MAP_HEIGHT = 24, 48

    MAP_FACTOR = 2
    COLOR_DARK_WALL = term.color_from_argb(128, 0, 0, 100)
    COLOR_DARK_GROUND = term.color_from_argb(128, 50, 50, 150)
    #px, py = SCREEN_WIDTH//2, SCREEN_HEIGHT//2
    px, py = 86, 30
    #px, py = 0, 0
    # units = Map.appendUnitList("./unitlist/test_map_colored.png")
    # map = Map(parse("testmap.dat"))
    #dungeon = Map(stringify("./assets/testmap.png"))
    um = UnitManager()
    player = Character("player", px, py, '@')
    player.inventory[0] = "sword"
    rat = Object("rat", 85, 30, 'r', r="monster")
    rat.message = "I am a rat"
    rat2 = Object("rat", 85, 29, 'R', r="monster")
    rat2.message = "I am a big rat"
    npc = Object("v1", 7, 7, '@', 'orange')
    npc1 = Object("v2", 5, 15, '@', 'orange')
    npc2 = Object("v3", 0, 56, '@', 'orange')
    guard3 = Object("v4", 63, 31, '@', 'orange')
    guard1 = Object("v5", 64, 32, "@", 'orange')
    guard2 = Object("v6", 63, 37, "@", 'orange')
    guard4 = Object("v7", 64, 37, '@', 'orange')
    units = [npc, guard1, guard2, guard3, guard4, npc1, npc2, rat, rat2]
    um.add(units)
    print(um._positions.keys())
    dungeon.add_item(87, 31, Item("sword", "(", "grey"))
    proceed = True
    lr = 5
    lights = [(121, 39, 10)]
    while proceed:
        term.clear()
        status_box()
        border()
        log_box()
        inventory_box()
        map_box()
        x, y, a = key_in()
        if a:
            processAction(player.x, player.y, a)
        else:
            key_process(x, y, dungeon.block, units)

    player.dump()
    return False
# End New Game Menu

if __name__ == "__main__":
    setup()
    new_game(None, None)
