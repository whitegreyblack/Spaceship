from bearlibterminal import terminal as term
from ecs.ecs import Entity, Position, Render, Ai, Controller
import random

UP, DOWN, LEFT, RIGHT = term.TK_UP, term.TK_DOWN, term.TK_LEFT, term.TK_RIGHT
ESCAPE = term.TK_ESCAPE

world = '''
################################################################
#....#....#....#....#..........##....#....#....#....#..........#
#...................#..........##...................#..........#
#....#....#....#....+.....#....##....#....#....#....+.....#....#
#...................#...............................#..........#
#....#....#....#....#..........##....#....#....#....#..........#
#....#....#....#....#..........##....#....#....#....#..........#
#...................#...............................#..........#
#....#....#....#....+.....#....##....#....#....#....+.....#....#
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
    print(Entity.compdict['position'])
    for position in Entity.compdict['position'].values():
        computer = position.unit.get('ai')
        if computer:
            x, y = computer.move()
        else:
            x, y = position.unit.get('controller').move()            
            if (x, y) == (None, None):
                return False

        if (position.x + x, position.y + y) in floortiles:
            position.move(x, y)
    return True

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
        self.player = Entity(components=[
            Position(random.randint(1, mapx - 1), 
                     random.randint(1, mapy - 1)),
            Render('a', '#DD8822'),
            Controller()
        ])
        self.enemy = Entity(components=[
            Position(random.randint(1, mapx - 1),
                     random.randint(1, mapy - 1)),
            Render('g', '#008800'),
            Ai(),
        ])
        # self.entities = [self.player, self.enemy]

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
    term.open()
    Game().run()
