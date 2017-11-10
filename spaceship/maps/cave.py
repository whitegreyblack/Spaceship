import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../../')
from spaceship.maps.base import Map
from collections import namedtuple
from namedlist import namedlist
from charmap import DungeonCharmap as dcm
from charmap import WildernessCharmap as wcm
from random import choice, randint
from math import sqrt, inf
from base import blender
from spaceship.tools import bresenhams

box = namedtuple("Box", "x1 y1 x2 y2")
point = namedtuple("Point", "x y")

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
    def __init__(self, width, height, rot=0, max_rooms=15):
        # builds a raw data map with given inputs
        self.width, self.height = width, height
        self.build(rot, max_rooms)

    def build(self, rot=0, max_rooms=15):
        '''Places rooms in a box of size width by height and applies rot if
        is not 0 and returns the box to be parsed as a dungeon'''
        def mst(graph):
            q, p = {}, {}

            for k in graph.keys(): 
                q[k] = inf
                p[k] = 0

            q[0] = 0
            p[0] = 0
            
            while q:
                u = min(k for k in q.keys())
                for z in graph[u].keys():
                    if z in q.keys() and 0 < graph[u][z] < q[z]: 
                        p[z] = u
                        q[z] = graph[u][z]
                q.pop(u)
                if choice([0, 1]) == 1 and q.keys():
                    u = min(k for k in q.keys())
                    for z in graph[u].keys():
                        if z in q.keys() and 0 < graph[u][z] < q[z]: 
                            p[z] = u
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
                return sqrt((p2.x-p1.x)**2+(p2.y-p1.y)**2)
            except AttributeError:
                return sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)

        def volume(box):
            return (box.x2-box.x1) * (box.y2-box.y1)

        def center(box):
            return point((box.x1 + box.x2)//2, (box.y1 + box.y2)//2)

        dungeon = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        rooms, large_rooms, other_rooms = [], [], []
        graph = {}
        tries = 0

        # Expansion Algorithm
        key_range = 3 if self.height <= 25 else 4
        while len(rooms) < max_rooms and tries < 2000:
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

            if randint(0, 3):
                x, y = y, x
                px, py = py, px

            temp = box(
                    px - int(round(x / 2)), 
                    py - int(round(y / 2)), 
                    px - int(round(x / 2)) + x, 
                    py - int(round(y / 2)) + y)

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

        # =========================================================================
        # basically these steps draw the rooms onto a tilemap
        # anything before is pre rendering (drawing)
        # anything after is post rendering 
        # =========================================================================

        # so the boxes and paths have been rendered
        # now append dimensions to the map and create a dungeon
        # floors then rooms then walls

        floor = []
        # drawing rooms
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
        for k in graph.keys():
            for x, y in lpath(rooms[k], rooms[graph[k]]):
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


if __name__ == "__main__":
    cave = Cave(66, 22)
    print(cave.__repr__())
    print(cave)