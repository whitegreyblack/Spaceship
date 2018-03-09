from bearlibterminal import terminal as term
from collections import namedtuple
from ecs.ecs import (
    Entity, Component, Position, Render, Ai, COMPONENTS, Delete
)
import random

UP, DOWN, LEFT, RIGHT = term.TK_UP, term.TK_DOWN, term.TK_LEFT, term.TK_RIGHT
ESCAPE = term.TK_ESCAPE
directions = {
    term.TK_UP: (0, -1),
    term.TK_DOWN: (0, 1), 
    term.TK_LEFT: (-1, 0), 
    term.TK_RIGHT: (1, 0),
}
world = '''
################################################################
#....#....#....#....#..........##....#....#....#....#..........#
#...................#..........##...................#..........#
#....#....#....#..........#....##....#....#....#....+.....#....#
#...................................................#..........#
#....#....#....#....#................#....#....#....#..........#
#....#....#....#....#..........##....#....#....#....#..........#
#...................................................#..........#
#....#....#....#..........#....##....#....#....#....+.....#....#
#...................#..........##...................#..........#
#....#....#....#....#..........##....#....#....#....#..........#
################################################################
'''[1:]
def has(entity, components=None):
    if not isinstance(components, list):
        return hasattr(entity, components.name())
    return all(hasattr(entity, component.name()) for component in components)

def system_draw(world):
    for j, row in enumerate(world):
        for i, cell in enumerate(row):
            term.puts(i, j, cell)

def draw_entity(position, background, string):
    revert = False
    if background != "#000000":
        term.bkcolor(background)
        revert = True
    term.puts(*position, string)
    if revert:
        term.bkcolor('#000000')

def system_render(entities):
    for e in entities:
        if has(e, components=[Position, Render]):
            draw_entity(e.position.position, *e.render.render)

def system_alive(entites):
    return 0 in [e.eid for e in entites]

def system_action(entities, floortiles):
    def get_input():
        key = term.read()
        while key != ESCAPE and key not in directions.keys():
            key = term.read()
        if key == ESCAPE:
            return None, None
        return directions.get(key, (0, 0))

    def direction():
        if has(entity, components=[Ai]):
            # Don't care about monsters -- they do whatever
            x, y = random.randint(-1, 1), random.randint(-1, 1)
        else:
            x, y = get_input()   
            if (x, y) == (None, None):
                return x, y, False
        return x, y, True

    recompute = False
    proceed = True
    for entity in entities:
        if has(entity, Position) and not has(entity, Delete):
            x, y, proceed = direction()
            if not proceed:
                break
            dx, dy = entity.position.x + x, entity.position.y + y
            # tile is floor
            if (dx, dy) in floortiles:
                if (dx, dy) not in set(e.position.position for e in entities):
                    entity.position.x += x
                    entity.position.y += y
                    recompute = True
                else:
                    other = None
                    for e in entities:
                        if entity != e and e.position.position == (dx, dy):
                            e.delete = Delete()
    return proceed, recompute

def system_remove(entities):
    # return [e for e in entities if not has(e, Delete)]
    remove = [e for e in entities if has(e, Delete)]
    for e in remove:
        entities.remove(e)
    return entities

# -- helper functions -- 
def random_position(floortiles, entities):
    tiles = set(floortiles)
    for e in entities:
        if has(e, [Position]):
            tiles.remove(e.position.position)
    return tiles.pop()

def create_player(entities, floors):
    entities.append(Entity(components=[
        Position(*random_position(floors, entities)),
        Render('a', '#DD8822', '#000088'),
    ]))

def create_enemy(entities, floors):
    entities.append(Entity(components=[
        Render(*random.choice((('g', '#008800'), ('r', '#664422')))),
        Position(*random_position(floors, entities)),
        Ai(),
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

class Game:
    def __init__(self, world:str):
        # world variables
        self.world = [[c for c in r] for r in world.split('\n')]
        self.height = len(self.world) - 1
        self.width = len(self.world[0]) - 1        
        self.floors = set((i, j) for j in range(self.height)
                                 for i in range(self.width)
                                 if self.world[j][i] == '.')

        # entities -- game objects
        self.eindex = 0     
        self.entities = []   
        create_player(self.entities, self.floors)
        for i in range(random.randint(3, 5)):
            create_enemy(self.entities, self.floors)

    def run(self):
        proceed = True
        fov_recalc = True
        while proceed:
            if fov_recalc:
                term.clear()                
                system_draw(self.world)
                system_render(self.entities)
                term.refresh()
            # read write
            proceed, fov_recalc = system_action(self.entities, self.floors)
            self.entites = system_remove(self.entities)
            # check player alive
            if not system_alive(self.entites):
                term.clear()
                term.puts(0, 0,'You died')
                term.refresh()
                term.read()
                break

    @property
    def entity(self):
        return self.entities[self.eindex]

if __name__ == "__main__":
    # print(tilemap(world))
    # print(random_position(floortiles))
    # print([c.__name__.lower() for c in Component.__subclasses__()])
    # for i in range(5):
    #     create_player()
    # for i in range(3):
    #     print(random_position())
    term.open()
    g = Game(world)
    g.run()
    # print(COMPONENTS)
    # print(Entity.compdict)
    # import os
    # import psutil
    # process = psutil.Process(os.getpid())
    # print(process.memory_info().rss)