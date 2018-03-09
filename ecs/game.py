from bearlibterminal import terminal as term
from ecs.ecs import (
    Entity, Component, Position, Render, Ai, COMPONENTS
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
def has(entity, components:list=None):
    return all(hasattr(entity, component) for component in components)

def system_draw_world():
    term.puts(0, 0, world)

def draw_entity(position, background, string):
    revert = False
    if background != "#000000":
        term.bkcolor(background)
        revert = True
    term.puts(*position, string)
    if revert:
        term.bkcolor('#000000')
        
def system_draw_entities():
    for position in Component.get('position').values():
        renderer = position.unit.get('render')
        if renderer:
            draw_entity(position.position, *renderer.render)

def system_render_by_entity():
    for e in entities:
        flags = Position.FLAG | Render.FLAG
        if e.FLAG & flags == flags:
            draw_entity(e.get('position').position, *e.get('render').render)

def system_render():
    for e in entities:
        if has(e, components=[Position.name(), Render.name()]):
            draw_entity(e.position.position, *e.render.render)

def system_move_entities():
    def get_input():
        key = term.read()
        while key != ESCAPE and key not in directions.keys():
            key = term.read()
        if key == ESCAPE:
            return None, None
        return directions.get(key, (0, 0))

    def move():
        dx, dy = (e.position.x + x, e.position.y + y)
        # tile is floor
        if (dx, dy) in floortiles:
            # tile is empty:
            if (dx, dy) not in set(e.position.position for e in positions):
                position.move(x, y)
                recompute = True
            # elif position.unit.has('damage') and 

    def direction():
        # computer = unit.get('ai')
        # if computer:
        if has(e, components=[Ai.name()]):
            # Don't care about monsters -- they do whatever
            x, y = random.randint(-1, 1), random.randint(-1, 1)
        else:
            x, y = get_input()   
            if (x, y) == (None, None):
                return x, y, False
        return x, y, True

    recompute = False
    proceed = True
    for e in entities:
        if has(e, components=[Position.name()]):
            x, y, proceed = direction()
            if not proceed:
                break
            dx, dy = e.position.x + x, e.position.y + y
            if (dx, dy) in floortiles:
                if (dx, dy) not in set(e.position.position for e in entities):
                    e.position.x += x
                    e.position.y += y
                    recompute = True
    return proceed, recompute

def random_position(floortiles, entities):
    tiles = set(floortiles)
    for e in entities:
        if has(e, [Position.name()]):
            tiles.remove(e.position.position)
    return tiles.pop()

def create_player(floors, entities):
    entities.append(Entity(components=[
        Position(*random_position(floors, entities)),
        Render('a', '#DD8822', '#000088'),
    ]))
    return entities

def create_enemy(floors, entities):
    return Entity(components=[
        Render(*random.choice((('g', '#008800'), ('r', '#664422')))),
        Position(*random_position()),
        Ai(),
    ])

class Tile:
    def __init__(self, ttype):
        self.ttype = ttype
    def walkable(self): return self.ttype
WALL, FLOOR, OPEN_DOOR, CLOSED_DOOR = [Tile(i) for i in range(4)]

class Game():
    def __init__(self, world:str):
        # world variables
        self.world = [[c for c in r] for r in world.split('\n')]
        self.width = len(self.world) - 1
        self.height = len(self.world[0]) - 1
        self.floors = set((i, j) for j, r in enumerate(world) 
                                 for i, c in enumerate(r)
                                 if c == '.')

        # entities -- game objects
        self.eindex = 0        
        self.entities = create_player(self.floors, [])

        # for _ in range(random.randint(3, 8)):
        #     create_enemy()

    # def run(self):
    #     proceed = True
    #     fov_recalc = True
    #     while proceed:
    #         term.clear()
    #         system_draw_world()
    #         # system_draw_entities()
    #         # system_render_by_entity()
    #         system_render()
    #         term.refresh()
    #         proceed, fov_recalc = system_move_entities()

    @property
    def entity(self):
        return self.entities[self.index]

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
    
    # print(COMPONENTS)
    # print(Entity.compdict)
    # import os
    # import psutil
    # process = psutil.Process(os.getpid())
    # print(process.memory_info().rss)