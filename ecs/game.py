from bearlibterminal import terminal as term
from ecs.ecs import Entity, Component, Position, Render, Ai, Controller, Energy
import random

UP, DOWN, LEFT, RIGHT = term.TK_UP, term.TK_DOWN, term.TK_LEFT, term.TK_RIGHT
ESCAPE = term.TK_ESCAPE

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

def system_draw_world():
    term.puts(0, 0, world)

def system_draw_entities():
    # these are known values -- reading them off
    for position in Entity.compdict['position'].values():
        # check if theyre in the dictionary
        renderer = position.unit.get('render')
        if renderer:
            term.puts(*position.position, renderer.render)

def system_move_entities():
    def move(position, x, y):
        dx, dy = (position.x + x, position.y + y)
        # tile is floor
        if (dx, dy) in floortiles:
            # tile is empty:
            if (dx, dy) not in set(p.position for p in positions):
                position.move(x, y)

    def direction(unit):
        computer = unit.get('ai')
        if computer:
            x, y = computer.move()
        else:
            x, y = unit.get('controller').move()       
            if (x, y) == (None, None):
                return x, y, False
        return x, y, True

    proceed = True
    positions = Entity.compdict['position'].values()
    for position in positions:
        unit = position.unit
        energy = unit.get('energy')
        turns = 1
        if energy:
            turns = energy.turns
        for turn in range(turns):
            x, y, proceed = direction(unit)
            if not proceed:
                return proceed
            move(position, x, y)
    return proceed

def system_take_turn_entities():
    pass

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
    enemy.add(Ai())
    # enemy.add(Energy())

def create_player():
    Entity(components=[
        Position(*random_position()),
        Render('a', '#DD8822'),
        Controller()
    ])

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
        while proceed:
            term.clear()
            system_draw_world()
            system_draw_entities()
            term.refresh()
            proceed = system_move_entities()

if __name__ == "__main__":
    # print(tilemap(world))
    # print(random_position(floortiles))
    # print([c.__name__.lower() for c in Component.__subclasses__()])
    term.open()
    Game().run()
