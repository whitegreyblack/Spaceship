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
entities = set()

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

def system_move_entities():
    def get_input():
        key = term.read()
        while key != ESCAPE and key not in directions.keys():
            key = term.read()
        if key == ESCAPE:
            return None, None
        return directions.get(key, (0, 0))

    def move():
        dx, dy = (position.x + x, position.y + y)
        # tile is floor
        if (dx, dy) in floortiles:
            # tile is empty:
            if (dx, dy) not in set(p.position for p in positions):
                position.move(x, y)
                recompute = True
            # elif position.unit.has('damage') and 

    def direction():
        computer = unit.get('ai')
        if computer:
            # Don't care about monsters -- they do whatever
            x, y = random.randint(-1, 1), random.randint(-1, 1)

        else:
            x, y = get_input()   
            if (x, y) == (None, None):
                return x, y, False
        return x, y, True

    recompute = False
    proceed = True
    positions = Entity.compdict['position'].values()
    for position in positions:
        unit = position.unit
        energy = unit.get('energy')
        turns = 1
        if energy:
            turns = energy.turns
        for turn in range(turns):
            # haven't moved yet -- just seeing which action to take
            # allows for early exit if user entered ESCAPE
            x, y, proceed = direction()
            if not proceed:
                # return proceed, recompute
                break
            # determines moving, staying, or attacking
            dx, dy = (position.x + x, position.y + y)
            # tile is floor
            if (dx, dy) in floortiles:
                # tile is empty:
                if (dx, dy) not in set(p.position for p in positions):
                    position.x += x
                    position.y += y
                    recompute = True        
        if not proceed:
            break
    return proceed, recompute

def random_position():
    tiles = set(floortiles)
    for p in Entity.compdict['position'].values():
        tiles.remove(p.position)
    return tiles.pop()

def create_enemy():
    enemy = Entity()
    # determine type of enemy
    enemy.add(Render(*random.choice((('g', '#008800'), ('r', '#664422')))))
    # determine position
    enemy.add(Position(*random_position()))
    # add a component class telling systems this is an npc/monster
    enemy.add(Ai())
    entities.add(enemy)

def create_player():
    entities.add(Entity(components=[
        Position(*random_position()),
        Render('a', '#DD8822', '#000088'),
    ]))

def tilemap(world):
    return [[c for c in r] for r in world.split('\n')]

def floors(world):
    return set((i, j ) for j, r in enumerate(world) 
                        for i, c in enumerate(r)
                         if c == '.')

worldmap = tilemap(world)
floortiles = floors(worldmap)
mapx, mapy = len(world.split()[0]) - 1, len(world.split()) - 1

class Game():
    def __init__(self):
        create_player()
        for _ in range(random.randint(3, 8)):
            create_enemy()

    def run(self):
        proceed = True
        fov_recalc = True
        while proceed:
            term.clear()
            system_draw_world()
            # system_draw_entities()
            system_render_by_entity()
            term.refresh()
            proceed, fov_recalc = system_move_entities()

if __name__ == "__main__":
    # print(tilemap(world))
    # print(random_position(floortiles))
    # print([c.__name__.lower() for c in Component.__subclasses__()])
    term.open()
    Game().run()
    # print(COMPONENTS)
    # print(Entity.compdict)