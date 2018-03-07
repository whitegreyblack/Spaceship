from bearlibterminal import terminal as term
from ecs.ecs import Entity, Position, Render
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
mapx, mapy = len(world.split()[0]), len(world.split())

def system_draw_world():
    term.puts(0, 0, world)

def system_draw_entities():
    # these are known values -- reading them off
    for position in Entity.compdict['position'].values():
        # check if theyre in the dictionary
        renderer = position.unit.get('render')
        if renderer:
            term.puts(*position.position, renderer.render)

class Game():
    def __init__(self):
        self.player = Entity(components=[
            Position(random.randint(1, mapx - 1), 
                     random.randint(1, mapy - 1)),
            Render('@', '#DD8822')
        ])
        self.enemy = Entity(components=[
            Position(random.randint(1, mapx - 1),
                     random.randint(1, mapy - 1)),
            Render('g', '#008800'),
        ])
    def run(self):
        while True:
            term.clear()
            system_draw_world()
            system_draw_entities()
            term.refresh()

            key = term.read()
            if key == ESCAPE:
                break

if __name__ == "__main__":
    term.open()
    Game().run()
