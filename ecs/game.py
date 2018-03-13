from bearlibterminal import terminal as term
from collections import namedtuple
from ecs.ecs import (
    Entity, Component, Position, Render, Backpack, Damage, Equipment,
    Information
)
import math
import random

class Keyboard:
    UP, DOWN, LEFT, RIGHT = term.TK_UP, term.TK_DOWN, term.TK_LEFT, term.TK_RIGHT
    ESCAPE = term.TK_ESCAPE
    ARROWS = {
        term.TK_UP: (0, -1),
        term.TK_DOWN: (0, 1), 
        term.TK_LEFT: (-1, 0), 
        term.TK_RIGHT: (1, 0),
    }
    KEYPAD = {
        term.TK_KP_1: (-1, 1),
        term.TK_KP_2: (0, 1),
        term.TK_KP_3: (1, 1),
        term.TK_KP_4: (-1, 0),
        term.TK_KP_5: (0, 0),
        term.TK_KP_6: (1, 0),
        term.TK_KP_7: (-1, -1),
        term.TK_KP_8: (0, -1),
        term.TK_KP_9: (1, -1),
    }
    KEYBOARD = {
        (term.TK_COMMA, 0): "pickup",
        (term.TK_I, 0): "inventory",
        (term.TK_D, 0): "drop",
        (term.TK_E, 0): "equip",
        (term.TK_U, 0): "unequip",
    }
    MAIN_MENU = {
        term.TK_P: "pressed play",
        term.TK_E: "pressed exit",
    }

world = '''
################################################################
#....#....#....#....#..........##....#....#....#....#..........#
#...................#..........##...................#..........#
#....#....#....#..........#....##....#....#....#....#.....#....#
#..............................................................#
#....#....#....#....#................#....#....#....#..........#
#....#....#....#....#..........##....#....#....#....#..........#
#..............................................................#
#....#....#....#..........#....##....#....#....#....#.....#....#
#..............................................................#
#..............................................................#
#..............................................................#
#..............................................................#
#..............................................................#
#..............................................................#
#..............................................................#
################################################################'''[1:]

def has(entity, components=None):
    def attr(name):
        try:
            name = name.classname()
        except AttributeError:
            pass
        return hasattr(entity, name) and getattr(entity, name) is not None
    if not isinstance(components, list):
        return attr(components)
    return all(attr(component) for component in components)

def loggable(entities):
    return all(has(e, Information) for e in entities)

def is_weapon(entity):
    return has(entity, Damage)

def is_hero(entity):
    return not has(entity, Ai)

def distance(self, other):
    #return the distance to another object
    dx = other.x - self.x
    dy = other.y - self.y
    return dx ** 2 + dy ** 2

def system_draw(world, entities):
    positions = { e.position.coordinates: e.render.draw 
                    for e in sorted(entities, reverse=True) 
    }
    for j, row in enumerate(world.world):
        for i, cell in enumerate(row):
            lighted = world.lit(i, j)
            if lighted == 2:
                if (i, j) in positions.keys():
                    draw_entity((i, j), *positions[(i, j)])
                else:
                    term.puts(i, j, f"[c=#999999]{cell}[/c]")
            elif lighted == 1:
                term.puts(i, j, f"[c=#222222]{cell}[/c]")

def draw_entity(position, background, string):
    revert = False
    if background != "#000000":
        term.bkcolor(background)
        revert = True
    term.puts(*position, string)
    if revert:
        term.bkcolor('#000000')

def system_render(world, entities):
    for e in entities:
        if has(e, components=[Position, Render]):
            if world.lit(*e.position.coordinates):
                draw_entity(e.position.coordinates, *e.render.draw)

def system_alive(entites):
    return 0 in [e.eid for e in entites]

def system_action(entities, floortiles, lightedtiles):
    def get_input():
        a, (x, y) = None, (0, 0)
        key = term.read()
        shifted = term.state(term.TK_SHIFT)
        notexit = key != Keyboard.ESCAPE
        notarrows = key not in Keyboard.ARROWS.keys()
        notkeypad = key not in Keyboard.KEYPAD.keys()
        notkeyboard = (key, shifted) not in Keyboard.KEYBOARD.keys()

        while notexit and notarrows and notkeypad and notkeyboard:
            key = term.read()
            shifted = term.state(term.TK_SHIFT)

            notexit = key != Keyboard.ESCAPE
            notarrows = key not in Keyboard.ARROWS.keys()
            notkeypad = key not in Keyboard.KEYPAD.keys()
            notkeyboard = (key, shifted) not in Keyboard.KEYBOARD.keys()

        # we finally get the right key value after parsing invalid keys
        if key == Keyboard.ESCAPE:
            x, y, = None, None
        elif key in Keyboard.ARROWS.keys():
            x, y = Keyboard.ARROWS[key]
        elif key in Keyboard.KEYPAD.keys():
            x, y = Keyboard.KEYPAD[key]
        elif (key, shifted) in Keyboard.KEYBOARD.keys():
            a = Keyboard.KEYBOARD[(key, shifted)]
        return a, x, y

    def take_turn():
        a, (x, y) = None, (0, 0)
        if has(entity, components='ai'):
            # hero = [e for e in entities if e.eid == 0]
            # if entity.position.coordinates in lightedtiles:
            #     pass
                    
            # notmonster = [e for e in entities 
            #     if has(e, Position) and not has(e, Ai) and 
            #         distance(entity, e) == 2]
            # if any(distance(e) == 2 for e in notmonster):
            # Don't care about monsters -- they do whatever
            # the return value will always be a directional x, y value
            x, y = random.randint(-1, 1), random.randint(-1, 1)
        else:
            # a :- action variable if action is chosen
            a, x, y = get_input()
            # on escape inputs -- early exit
            if (x, y) == (None, None):
                return None, x, y, False
        return a, x, y, True

    def move(entity, x, y):
        entity.position.x += x
        entity.position.y += y

    recompute = False
    proceed = True
    for entity in entities:
        # print(repr(entity))
        # needs these two components to move -- dead entities don't move
        if has(entity, 'moveable') and not has(entity, 'delete'):
            if loggable((entity,)) and not has(entity, 'ai'): 
                print(f"{entity.information.name()} takes his turn")
            print(f"{entity.information.name()}, {entity.delete if has(entity, 'delete') else False}")
            a, x, y, proceed = take_turn()
            if not proceed:
                break
            if a:
                if a == "pickup":
                    for e in entities: 
                        if not has(e, 'moveable'):
                            e.position = None
                            entity.backpack.append(e)
                            for i in entity.backpack:
                                print(i, is_weapon(i))
                                if is_weapon(i):
                                    print(i, repr(i.damage))
                            e.delete = True
                elif a == "inventory":
                    print(entity.backpack)
                    for i in entity.backpack:
                        print(has(i, Position))
                elif a == "drop":
                    item = entity.backpack.pop()
                    item.position = Position(*entity.position.coordinates)
                    item.delete = False
                    entities.append(item)         
                elif a == "equip":
                    if len(entity.backpack) == 1:
                        item = entity.backpack.pop()
                        if not entity.equipment.left_hand:
                            print("current damage:", entity.equipment.left_hand)
                            print("equipping left hand with item")
                            entity.equipment.left_hand = item.damage
                            print("current damage:", entity.equipment.left_hand)
                        elif not entity.equipment.right_hand:
                            print("current damage:", entity.equipment.right_hand)
                            print("equipping right hand with item")  
                            entity.equipment.right_hand = item.damage
                            print("current damage:", entity.equipment.right_hand)
                        else:
                            print("Both hands are full")
                            entity.backpack.append(item)
                        entity.equipment.left_hand
                elif a == "unequip":
                    item = None
                    if has(entity.equipment, 'left_hand') and entity.equipment.left_hand:
                        print("Unequipping left hand")
                        item = entity.equipment.left_hand
                        entity.equipment.left_hand = Damage("1d6", Damage.PHYSICAL)
                    elif has(entity.equipment, 'right_hand') and entity.equipment.right_hand:
                        item = entity.equipment.right_hand
                        entity.equipment.right_hand = Damage("1d6", Damage.PHYSICAL)
                    else:
                        print("Both hands are empty")
                    if item:
                        entity.backpack.append(item)
                continue

            recompute = True
            dx, dy = entity.position.x + x, entity.position.y + y
            # tile is floor
            if (dx, dy) in floortiles:
                positions = set(e.position.coordinates for e in entities
                                if has(e, 'position') and not has(e, 'delete'))
                if (dx, dy) not in positions:
                    # nothing here -- move
                    move(entity, x, y)
                else:
                    other = None
                    # find the other entity on the occupied position
                    for e in entities:
                        if entity != e and e.position.coordinates == (dx, dy):
                            # will only be one movable on this tile -- delete
                            if has(e, 'moveable'):
                                other = e
                    # couldn't find the entity, just move and exit
                    if not other:
                        move(entity, x, y)
                        print('moved')
                        continue

                    elif loggable(entities=(entity, other)):
                        attacker = entity.information.name()
                        defender = other.information.name()
                        if has(entity, Equipment):
                            damage = entity.equipment.left_hand.deal
                            damage += entity.equipment.right_hand.deal
                            damages = [0 for _ in range(2)]
                            for dt, dmg in damage:
                                damages[dt] += dmg
                            print(f"{attacker} dealt {sum(damages)} damage to the {defender}")
                        print(f"{attacker} has killed the {defender}")

                        # if has(entity, Damage):
                        #     dmg = entity.damage.deal
                        #     print(f"{attacker} deals {dmg} damage to {defender}")
                    other.delete = True
                    print(f"{other.information.name()} will be deleted: {other.delete}")
        # print(repr(entity), list(entity.components))
    return proceed, recompute

def system_remove(entities):
    # return [e for e in entities if not has(e, Delete)]
    remove = [e for e in entities if has(e, 'delete') and e.delete]
    for e in remove:
        try:
            print(f"Deleting: {e.information.name()}")
        except:
            print(f"Deleting item: {e.eid}")
        entities.remove(e)
    return entities

# -- helper functions -- 
def random_position(entities, floortiles):
    tiles = list(floortiles)
    random.shuffle(tiles)
    for e in entities:
        if has(e, 'moveable'):
            tiles.remove(e.position.coordinates)
    tile = tiles.pop()
    return tile

def create_player(entities, floors):
    # color -> class type
    # race/name
    # backpack stuff
    entities.append(Entity(components=[
        Position(*random_position(entities, floors)),
        Information(title="Hero", race="Human"),
        Render('a', '#DD8822', '#000088'),
        ('moveable', True),
        ('backpack', []),
        Equipment(Damage(("1d6", Damage.PHYSICAL)), 
                  Damage(("1d6", Damage.PHYSICAL))),
    ])) 

def create_enemy(entities, floors):
    if random.randint(0, 1):
        entities.append(Entity(components=[
            Position(*random_position(entities, floors)),
            Information(race="goblin"),
            Render('g', '#008800'),
            ('moveable', True),
            ('ai', True),
        ]))
    else:
        entities.append(Entity(components=[
            Position(*random_position(entities, floors)),   
            Information(race="rat"),
            Render('r', '#664422'),
            ('moveable', True),
            ('ai', True),
        ]))

def create_weapon(entities, floors):
    entities.append(Entity(components=[
        Render('[[', '#00AAAA'),
        Position(*random_position(entities, floors)),
        Damage(("1d6", Damage.PHYSICAL)),
    ]))

class Tile:
    def __init__(self, ttype):
        self.ttype = ttype
    def walkable(self): return self.ttype

WALL, FLOOR, OPEN_DOOR, CLOSED_DOOR = [Tile(i) for i in range(4)]

class Result:
    def __init__(self):
        self.events = []
        self.proceed = False

    @property
    def refresh(self) -> bool:
        return self.proceed or bool(self.events)

Event = namedtuple('Event', 'string position')
# class Event:
#     def __init__(self, string, position):
#         self.string = string
#         self.position = position

class Map:
    mult = [
            [1,  0,  0, -1, -1,  0,  0,  1],
            [0,  1, -1,  0,  0, -1,  1,  0],
            [0,  1,  1,  0,  0, -1, -1,  0],
            [1,  0,  0,  1, -1,  0,  0, -1]
        ]
    def __init__(self, world:str):
        self.world = [[c for c in r] for r in world.split('\n')]
        self.height = len(self.world)
        self.width = len(self.world[0])
        self.floors = set((i, j) for j in range(self.height - 1)
                                 for i in range(self.width - 1)
                                 if self.world[j][i] == '.')
        self.init_light()

    def init_light(self):
        self.light = [[0 for c in r] for r in self.world]

    def reset_light(self):
        self.light = [[1 if c >= 1 else 0 for c in r] for r in self.light]

    @property
    def lighted(self) -> set:
        return {
            (x, y) for y in range(self.height) for x in range(self.width)
                   if self.square(x, y) == '.' and self.lit(x, y) == 2
        }

    def square(self, x, y):
        return self.world[y][x]

    def blocked(self, x, y):
        return (not 0 <= x < self.width or not 0 <= y < self.height
                or self.world[y][x] in ("#", '+'))
                
    def lit(self, x, y):
        return self.light[y][x]

    def set_lit(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.light[y][x] = 2

    def do_fov(self, x, y, radius):
        "Calculate lit squares from the given location and radius"
        self.set_lit(x, y)
        self.visit = 0
        for oct in range(8):
            self._cast_light(x, y, 1, 1.0, 0.0, radius,
                             self.mult[0][oct], self.mult[1][oct],
                             self.mult[2][oct], self.mult[3][oct], 0)

    def _cast_light(self, cx, cy, row, start, end, radius, xx, xy, yx, yy, id):
        "Recursive lightcasting function"
        if start < end:
            return
        radius_squared = radius*radius
        for j in range(row, radius + 1):
            dx, dy = -j - 1, -j
            blocked = False
            while dx <= 0:
                dx += 1
                # Translate the dx, dy coordinates into map coordinates:
                X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
                self.visit += 1
                # l_slope and r_slope store the slopes of the left and right
                # extremities of the square we're considering:
                l_slope = (dx - 0.5) / (dy + 0.5)
                r_slope = (dx + 0.5) / (dy - 0.5)
                if start < r_slope:
                    continue
                elif end > l_slope:
                    break
                else:
                    # Our light beam is touching this square; light it:
                    if dx*dx + dy*dy < radius_squared:
                        self.set_lit(X, Y)
                    if blocked:
                        # we're scanning a row of blocked squares:
                        if self.blocked(X, Y):
                            new_start = r_slope
                            continue
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if self.blocked(X, Y) and j < radius:
                            # This is a blocking square, start a child scan:
                            blocked = True
                            self._cast_light(cx, cy, j+1, start, l_slope,
                                             radius, xx, xy, yx, yy, id+1)
                            new_start = r_slope
            # Row is scanned; do next row unless last square was blocked:
            if blocked:
                break

def draw_main_menu():
    term.clear()
    term.puts(0, 0, "Play Game")
    term.puts(0, 1, "Exit")
    term.refresh()

    key = term.read()
    while key not in Keyboard.MAIN_MENU.keys():
        key = term.read()

    term.clear()
    return Keyboard.MAIN_MENU[key]

class Game:
    def __init__(self, world:str):
        # world variables
        self.dungeon = Map(world)

        # entities -- game objects
        self.eindex = 0     
        self.entities = []   
        create_player(self.entities, self.dungeon.floors)
        for i in range(random.randint(3, 5)):
            create_enemy(self.entities, self.dungeon.floors)
        # for i in range(3):
        create_weapon(self.entities, self.dungeon.floors)

    def run(self):
        proceed = True
        fov_recalc = True
        while proceed and system_alive(self.entities):
            if fov_recalc:
                term.clear()               
                self.dungeon.reset_light()
                self.dungeon.do_fov(*self.entities[0].position.coordinates, 15)
                system_draw(self.dungeon, self.entities)
                # system_render(self.dungeon, self.entities)
                term.refresh()

            # read write -- if user presses exit here then quit next loop?
            proceed, fov_recalc = system_action(self.entities, 
                                                self.dungeon.floors,
                                                self.dungeon.lighted)

            self.entities = system_remove(self.entities)
            
        # check player alive
        else:
            term.puts(0, 24,'You died')
            term.refresh()
            term.read()
            


if __name__ == "__main__":
    # print(tilemap(world))
    # print(random_position(floortiles))
    # print([c.__name__.lower() for c in Component.__subclasses__()])
    # for i in range(5):
    #     create_player()
    # for i in range(3):
    #     print(random_position())
    term.open()
    if draw_main_menu() == "pressed play":
        g = Game(world)
        g.run()
    # term.close()
    # print(COMPONENTS)
    # print(Entity.compdict)
    # import os
    # import psutil
    # process = psutil.Process(os.getpid())
    # print(process.memory_info().rss)