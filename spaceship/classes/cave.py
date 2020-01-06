from collections import namedtuple
from math import inf, sqrt
from random import choice, randint, shuffle

import click
from namedlist import namedlist

from spaceship.tools import bresenhams
from spaceship.classes.map import Map
from spaceship.classes.utils import blender

box = namedtuple("Box", "x1 y1 x2 y2")
point = namedtuple("Point", "x y")
charmap = namedtuple("Charmap", "chars hexcode")

class DungeonCharmap:
    # GRASS=charmap([",", ";"], ("#56ab2f", "#a8e063"))
    GRASS=charmap([",", ";"], ("#008800", "#008800"))
    HOUSE=charmap(["="], ("#ffffff", "#ffffff"))
    TILES=charmap(["."], ("#C0C0C0", "#C0C0C0"))
    # TILES=charmap(["."], ("#404040", "#404040"))
    WALLS=charmap(["#"], ("#444444", "#656565"))
    # WATER=charmap(["~"], ("#43C6AC", "#191654"))
    WATER=charmap(["~"], ("#191654", "#191654"))
    # WATER=charmap(["~"], ("#43C6AC", "#43C6AC"))

    DOORS=charmap(["+"], ("#994C00", "#994C00"))
    # PLANT=charmap(["|"], ("#F3E347", "#24FE41"))
    PLANT=charmap(["'"], ("#ffc90e", "#ffc90e"))

    LAMPS=charmap(["o"], ("#ffffff", "#ffffff"))
    BRICK=charmap(["%"], ("#a73737", "#7a2828"))
    # ROADS=charmap([":"], ("#808080", "#994C00"))
    ROADS=charmap([":"], ("#994C00", "#994C00"))
    POSTS=charmap(["x"], ("#9a8478", "#9a8478"))
    BLOCK=charmap(["#", "+", "o", "x"],("#000000", "#ffffff"))
    LTHAN=charmap(["<"], ("#c0c0c0", "#c0c0c0"))
    GTHAN=charmap([">"], ("#c0c0c0", "#c0c0c0"))
    TRAPS=charmap(["^"], ("#c0c0c0", "#c0c0c0"))

dcm = DungeonCharmap

class Cave(Map):
    chars = {
        ".": (dcm.TILES.chars, blender(dcm.TILES.hexcode)),
        ",": (dcm.GRASS.chars, blender(dcm.GRASS.hexcode)),
        "#": (dcm.WALLS.chars, blender(dcm.WALLS.hexcode)),
        "~": (dcm.WATER.chars, blender(dcm.WATER.hexcode)),
        "+": (dcm.DOORS.chars, blender(dcm.DOORS.hexcode)),
        "x": (dcm.POSTS.chars, blender(dcm.POSTS.hexcode)), 
        "|": (dcm.PLANT.chars, blender(dcm.PLANT.hexcode)),
        "o": (dcm.LAMPS.chars, blender(dcm.LAMPS.hexcode)),
        ":": (dcm.ROADS.chars, blender(dcm.ROADS.hexcode)),
        "=": (dcm.HOUSE.chars, blender(dcm.HOUSE.hexcode)),
        " ": (' ', '#000000'),
        "%": (dcm.WALLS.chars, blender(dcm.WALLS.hexcode)),
        "^": (dcm.WALLS.chars, blender(dcm.WALLS.hexcode)),
        "<": (dcm.LTHAN.chars, blender(dcm.LTHAN.hexcode)),
        ">": (dcm.GTHAN.chars, blender(dcm.GTHAN.hexcode)),
        "^": (dcm.TRAPS.chars, blender(dcm.TRAPS.hexcode)),
    }
    def __init__(self, width=66, height=22, generate=True, rot=0, max_rooms=8, levels=3):
        # builds a raw data map with given inputs
        super().__init__(width, height, self.__class__.__name__)
        self.levels = levels
        self.build(rot, max_rooms)
        self.create_tile_map()        

        if generate:
            self.generate_units()
        
    def build(self, rot=0, max_rooms=15):
        """
            Places rooms in a box of size width by height and applies rot if
            is not 0 and returns the box to be parsed as a dungeon
        """
        def mst(graph):
            """
                Minimum spanning tree
            """
            q, p = {}, {}

            for k in graph.keys(): 
                q[k] = inf
                p[k] = 0

            q[0] = 0
            p[0] = [0]
            
            while q:
                u = min(k for k in q.keys())
                for z in graph[u].keys():
                    if z in q.keys() and 0 < graph[u][z] < q[z]: 
                        p[z] = [u]
                        q[z] = graph[u][z]

                q.pop(u)

                if choice([0, 1]) == 1 and q.keys():
                    u = min(k for k in q.keys())
                    for z in graph[u].keys():
                        if z in q.keys() and 0 < graph[u][z] < q[z]: 
                            p[z] = [u]
                            q[z] = graph[u][z]  
            return p

        def lpath(b1, b2):
            x1, y1 = center(b1)
            x2, y2 = center(b2)

            # check if xs are on the same axis -- returns a vertical line
            if x1 == x2 or y1 == y2:
                return bresenhams((x1, y1), (x2, y2))

            # check if points are within x bounds of each other == returns the midpoint vertical line
            elif b2.x1 <= x1 < b2.x2 and b1.x1 <= x2 < b1.x2:
                x = (x1+x2)//2
                return bresenhams((x, y1), (x, y2))

            # check if points are within y bounds of each other -- returns the midpoint horizontal line
            elif b2.y1 <= y1 < b2.x2 and b1.y1 <= y2 < b2.y2:
                y = (y1+y2)//2
                return bresenhams((x1, y), (x2, y))

            else:
                # we check the slope value between two boxes to plan the path
                slope = abs((max(y1, y2) - min(y1, y2))/((max(x1, x2) - min(x1, x2)))) <= 1.0
            
                # low slope -- go horizontal
                if slope:
                    # width is short enough - make else zpath
                    return bresenhams((x1, y1), (x1, y2)) \
                        + bresenhams((x1, y2), (x2, y2))

                # high slope -- go vertical
                else:
                    return bresenhams((x1, y1), (x2, y1)) \
                        + bresenhams((x2, y1), (x2, y2))

        def box_oob(box):
            return box.x1 < 0 or box.y1 < 0 or \
                box.x2 >= self.width-1 or box.y2 >= self.height - 1

        def intersect(b1, b2):
            o = offset = 1
            return (b1.x1+o <= b2.x2 and b1.x2-o >= b2.x1 and 
                    b1.y1+o <= b2.y2 and b1.y2-o >= b2.y1)

        def distance(p1, p2):
            try:
                x, y = p2.x - p1.x, p2.y - p1.y

            except AttributeError:
                x, y = p2[0] - p1[0], p2[1] - p1[1]
                
            finally:
                return sqrt(x ** 2 + y ** 2)

        def volume(box):
            return (box.x2-box.x1) * (box.y2-box.y1)

        def center(box):
            return point((box.x1 + box.x2)//2, (box.y1 + box.y2)//2)

        dungeon = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        rooms, large_rooms, other_rooms = [], [], []
        self.spaces = []
        graph = {}
        tries = 0

        # Expansion Algorithm
        key_range = 3 if self.height <= 25 else 4
        while len(rooms) < max_rooms and tries < 3000:
            key = choice([i for i in range(-1, key_range)])

            if key == 4:
                x, y = randint(16, 20), randint(12, 16)
                px, py = randint(9, self.width - 9), randint(7, self.height - 7)
            elif key >= 2:
                x, y = randint(12, 16), randint(8, 12)
                px, py = randint(x // 2, self.width - x // 2), randint(y // 2, self.height - y // 2)
            elif key >= 0:
                x, y = randint(8, 12), randint(4, 6)
                px, py = randint(x // 2, self.width - x // 2), randint(y // 2, self.height - y // 2)
            else:
                x, y = randint(6, 8), randint(3, 4)
                px, py = randint(x // 2, self.width - x // 2), randint(y // 2, self.height - y // 2)

            # if randint(0, 3):
            #     x, y = y, x
            #     px, py = py, px

            temp = box(
                px - int(round(x / 2)), 
                py - int(round(y / 2)), 
                px - int(round(x / 2)) + x, 
                py - int(round(y / 2)) + y
            )

            # check for out of bounds error first -- makes for filtering easier and does not check
            # intersections with temp and other rooms due to first failure -- thus faster looping 
            if not box_oob(temp) and not any(intersect(room, temp) for room in rooms):
                rooms.append(temp)
            else:
                tries += 1

        # update large rooms
        for r in rooms:
            if volume(r) >= 60:
                large_rooms.append(r)
            else:
                other_rooms.append(r)

        # create a graph and build mst
        for i in range(len(rooms)):
            array = {}
            for j in range(len(rooms)):
                array[j] = distance(center(rooms[i]), center(rooms[j]))
            graph[i] = array

        # build a mst graph between rooms
        graph = mst(graph)

        # randomly choose rooms to join with
        m = max(graph.keys())
        pairs = {
            (i, j) for i in range(m) for j in range(m-1)
        }
        paired = {
           (k, v[0]) 
                for k, v in graph.items()
        }
        pairs.difference_update(paired)
        for i in range(len(graph.keys()) // 2):
            a, b = pairs.pop()
            graph[a].append(b)

        # =========================================================================
        # basically these steps draw the rooms onto a tilemap
        # anything before is pre rendering (drawing)
        # anything after is post rendering 
        # =========================================================================

        # so the boxes and paths have been rendered
        # now append dimensions to the map and create a dungeon
        # floors then rooms then walls

        # drawing rooms
        floor = []
        for r in rooms:
            for x in range(r.x1, r.x2+1):
                for y in range(r.y1, r.y2+1):
                    dungeon[y][x] = '.'
                    floor.append((x, y))

                for y in (r.y1, r.y2):
                    dungeon[y][x] = '%'

            for y in range(r.y1, r.y2+1):
                for x in (r.x1, r.x2):
                    dungeon[y][x] = '%'

        # draw paths/hallways
        paths = []
        for k, vs in graph.items():
            for v in vs:
                for x, y in lpath(rooms[k], rooms[v]):
                    dungeon[y][x] = '#'
                    paths.append((x, y))

        # draw doors
        doors = []
        for i, j in paths:
            if dungeon[j][i] == '#':
                hwalls = (dungeon[j][i+1] == '%' and dungeon[j][i-1] == '%')
                vwalls = (dungeon[j+1][i] == '%' and dungeon[j-1][i] == '%')
                if hwalls or vwalls:
                    doors.append((i, j))

        for i, j in doors:
            skip = False
            for ii in range(-1, 2):
                for jj in range(-1, 2):
                    if dungeon[j+jj][i+ii] == '+':
                        skip = True
            if not skip and choice([0, 1]):
                dungeon[j][i] = '+'
            else:
                dungeon[j][i] = '.'
            paths.remove((i, j))

        for i, j in paths:
            if dungeon[j][i] == '#':
                for ii in range(-1, 2):
                    for jj in range(-1, 2):
                        if dungeon[j+jj][i+ii] == ' ':
                            dungeon[j+jj][i+ii] = '%'
                dungeon[j][i] = '.'

        floor_clear = []
        for i, j in floor:
            val = 0
            for ii in range(-1, 2):
                for jj in range(-1, 2):
                    if dungeon[j+jj][i+ii] == '.':
                        val += 1
            if val == 9:
                floor_clear.append((i, j))

        # TODO: REMOVE TRAPS UNTIL TRAPS CAN BE IMPLEMENTED -- CURRENT ERRROR IS TRAPS IS HIDDEN UNTIL STEPPED ON
        # traps = []
        # for i in range(3):
        #     i, j = choice(floor_clear)
        #     floor_clear.remove((i, j))
        #     dungeon[j][i] = '^'

        upStairs, downStairs = choice(floor_clear), choice(floor_clear)

        while distance(upStairs, downStairs) <= 15:
            upStairs, downStairs = choice(floor_clear), choice(floor_clear)

        # remove upstairs from floors and replace char
        floor_clear.remove(upStairs)
        ui, uj = upStairs
        dungeon[uj][ui] = '<'

        # remove downstairs from floors and replace char
        if randint(0, 5):
            floor_clear.remove(downStairs)
            di, dj = downStairs
            dungeon[dj][di] = '>'

        # the output is more for debugging
        if rot > 0:
            dungeon = decay(dungeon, n=rot)

        self.data = dungeon

        # get all spaces avaialable
        for i in range(self.width):
            for j in range(self.height):
                if dungeon[j][i] == ".":
                    self.spaces.append((i, j))
        
    def current_level():
        return self.levels
    

@click.command()
@click.option('--width', default=58, help="width of cave")
@click.option('--height', default=17, help="height of cave")
@click.option('--runs', default=1, help="number of generated caves")
def cli(width, height, runs):
    for _ in range(runs):
        print(repr(Cave(width, height, False)))

if __name__ == "__main__":
    cli()
