# Dungeon.py
# builds a random dungeon of size MxN
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from bearlibterminal import terminal as term
from copy import deepcopy
from random import choice, choices, randint, choice
from collections import namedtuple
from tools import bresenhams
from spaceship.setup import setup_font
import math
X_MIN_ROOM_SIZE=80
X_MAX_ROOM_SIZE=100
Y_MIN_ROOM_SIZE=25
Y_MAX_ROOM_SIZE=75
X_TEMP, Y_TEMP = 80, 50
# X_TEMP, Y_TEMP = 160, 100
WALL, FLOOR = -1, 1
MULTIPLIER = 12
box = namedtuple("Box", "x1 y1 x2 y2")
point = namedtuple("Point", "x y")

def circle():
    term.open()
    term.set('window: size=160x100, cellsize=2x2')
    setup_font('Ibm_cga', 4, 4)
    dungeon = [[' ' for _ in range(X_TEMP)] for _ in range(Y_TEMP)]
    cx, cy = X_TEMP//2-1, Y_TEMP//2-1
    cr = min(cx, cy)
    print(cr)
    f = 1 - cr
    fx = 1
    fy = -2 * cr
    x = 0
    y = cr
    dungeon[cy-cr][cx] = '.'
    dungeon[cy+cr][cx] = '.'
    dungeon[cy][cx-cr] = '.'
    dungeon[cy][cx+cr] = '.'
    while x < y:
        if f >= 0: 
            y -= 1
            fy += 2
            f += fy
        x += 1
        fx += 2
        f += fx    
        dungeon[cy+y][cx+x] = '.'
        dungeon[cy+y][cx-x] = '.'
        dungeon[cy-y][cx+x] = '.'
        dungeon[cy-y][cx-x] = '.'
        dungeon[cy+x][cx+y] = '.'
        dungeon[cy+x][cx-y] = '.'
        dungeon[cy-x][cx+y] = '.'
        dungeon[cy-x][cx-y] = '.'
    for i in range(Y_TEMP):
        for j in range(X_TEMP):
            term.puts(j, i, dungeon[i][j])
    term.refresh()
    term.read()

def ellipse():
    term.open()
    term.set('window: size=160x100, cellsize=8x8')
    setup_font('Ibm_cga', 4, 4)
    dungeon = [[' ' for _ in range(X_TEMP)] for _ in range(Y_TEMP)]
    xr, yr = cx, cy = X_TEMP//2-1, Y_TEMP//2-1
    t = 0
    step = 1
    group = set()
    dungeon[cy-yr][cx] = '.'
    dungeon[cy-yr][cx] = '.'
    dungeon[cy][cx-xr] = '.'
    dungeon[cy][cx+xr] = '.'
    while t <= 360:
        x = int(round(cx + xr*math.cos(t)))
        y = int(round(cy + yr*math.sin(t)))
        if (x,y) not in group:
            dungeon[y][x] = '.'
            group.add((x,y))
        t += step    
    for i in range(Y_TEMP):
        for j in range(X_TEMP):
            term.puts(j, i, dungeon[i][j])
    term.refresh()
    term.read()

def mst(graph):
    q, p = {}, {}

    for k in graph.keys(): 
        q[k] = math.inf
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
        print(q)
    print('key pair')
    for k in p:
        print(k, p[k])
    return  p

def lpath(p1, p2):
    points = []
    xhalf = (p2.x+p1.y)//2
    yhalf = (p2.y+p1.y)//2

def distance(p1, p2):
    return math.sqrt((p2.x-p1.x)**2+(p2.y-p1.y)**2)

def intersect(b1, b2):
    return (b1.x1 <= b2.x2 and b1.x2 >= b2.x1 and 
            b1.y1 <= b2.y2 and b1.y2 >= b2.y1)

def center(box):
    return point((box.x1 + box.x2)//2, (box.y1 + box.y2)//2)

def volume(box):
    return (box.x2-box.x1) * (box.y2-box.y1)

def rotate(box):
    return list(zip(*box[::-1]))

def equal(p1, p2):
    print(p1, p2)
    try:
        return p1.x == p2.x and p1.y == p2.y
    except AttributeError:
        return center(p1) == center(p2)
    except:
        print(p1, p2)
        raise

def oob(box):
    return box.x1 < 1 or box.y1 < 1 or box.x2 >= X_TEMP-1 or box.y2 >= Y_TEMP-1

def ooe(i, j):
    h = rx = X_TEMP//2-1
    k = ry = Y_TEMP//2-1
    return ((i-h)**2)/(rx**2) + ((j-k)**2)/(ry**2) <= 1

def smooth(dungeon):
    def neighbor(x, y):
        val = 0
        wall = dungeon[x][y] == WALL
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (x, y) != (x+i, y+j):
                    if wall:
                        try:
                            if  dungeon[x+i][y+j] == FLOOR:
                                val += 1
                        except:
                            pass
                    else:
                        try:
                            if dungeon[x+i][y+j] == FLOOR:
                                val += 1
                        except:
                            pass
        if wall:
            return WALL if val < 5 else FLOOR
        else:
            return FLOOR if val > 4 else WALL
            
    newmap = deepcopy(dungeon)
    for i in range(len(dungeon)):
        for j in range(len(dungeon[0])):
            newmap[i][j] = neighbor(i, j)

    return newmap

def lpath(b1, b2):
    x1, y1 = center(b1)
    x2, y2 = center(b2)

    # check if xs are on the same axis -- returns a vertical line
    if x1 == x2 or y1 == y2:
        return bresenhams((x1, y1), (x2, y2))
    # return bresenhams((x1, y1), (x2, y2))
    # check if points are within x bounds of each other == returns the midpoint vertical line
    elif b2.x1 <= x1 < b2.x2 and b1.x1 <= x2 < b1.x2:
        x = (x1+x2)//2
        return bresenhams((x, y1), (x, y2))

    # check if points are within y bounds of each other -- returns the midpoint horizontal line
    elif b2.y1 <= y1 < b2.x2 and b1.y1 <= y2 < b2.y2:
        y = (y1+y2)//2
        return bresenhams((x1, y), (x2, y))

    else:
        slope = abs((max(y1, y2) - min(y1, y2))/((max(x1, x2) - min(x1, x2)))) <= 1.0
        short = (b1.x2 - b1.x2) + (b2.x2-b2.x1) + 1 > x2 - x1
        # low slope -- go horizontal lpath
        if slope:
            # width is short enough - make lpath else zpath
            if short:
                return bresenhams((x1, y1), (x1, y2)) \
                    + bresenhams((x1, y2), (x2, y2))
            return bresenhams((x1, y1), ((x1+x2)//2, y1)) \
                + bresenhams(((x1+x2)//2, y1), ((x1+x2)//2, y2)) \
                + bresenhams(((x1+x2)//2, y2), (x2, y2))
        # high slope -- go vertical
        else:
            if short:
                return bresenhams((x1, y1), (x2, y1)) \
                    + bresenhams((x2, y1), (x2, y2))
            return bresenhams((x1, y1), (x1, (y1+y2)//2)) \
                + bresenhams((x1, (y1+y2)//2), (x2, (y1+y2)//2)) \
                + bresenhams((x2, (y1+y2)//2), (x2, y2))
        

def build():
    term.open()
    term.set('window: size={}x{}, cellsize=4x4'.format(X_TEMP, Y_TEMP))
    setup_font('Ibm_cga', 8, 8)
    # constructor -- (-1 = impassable) start with a map of walls
    # dungeon = [[-1 for _ in range(x)] for _ in range(y)]
    dungeon = [[' ' for _ in range(X_TEMP)] for _ in range(Y_TEMP)]
    rooms, large_rooms, other_rooms = [], [], []
    graph = {}
    tries = 0

    # Expansion Algorithm
    while len(rooms) < 30 and tries < 500:
        key = choices(population=[0, 1, 2], weights=[.5,.35,.15] ,k=1)[0]
        if key == 0:
            x, y = randint(12, 18), randint(9, 15)
            px, py = randint(9, X_TEMP-9), randint(9, Y_TEMP-9)
        elif key == 1:
            x, y = randint(8, 12), randint(6, 10)
            px, py = randint(6, X_TEMP-6), randint(6, Y_TEMP-6)
        else:
            x, y = randint(4, 6), randint(3, 5)
            px, py = randint(3, X_TEMP-3), randint(3, Y_TEMP-3)

        temp = box(px-int(round(x/2)), py-int(round(y/2)), px-int(round(x/2))+x, py-int(round(y/2))+y)
        intersects = any(intersect(room, temp) for room in rooms)

        if not intersects and not oob(temp):
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
    for i in range(len(large_rooms)):
        array = {}
        for j in range(len(large_rooms)):
            array[j] = distance(center(large_rooms[i]), center(large_rooms[j]))
        graph[i] = array

    graph = mst(graph)


    # so the boxes and paths have been drawn
    # now append dimensions to the map and create a dungeon
    # floors then rooms then walls
    for r in large_rooms:
        # for y in range(r.y1, r.y2):
        #     for x in (r.x1, r.x2):
        #         dungeon[y][x] = '%'
                    
        for x in range(r.x1, r.x2):
            for y in range(r.y1, r.y2):
                dungeon[y][x] = '.'

    for k in graph:
        for x, y in lpath(large_rooms[k], large_rooms[graph[k]]):
            if dungeon[y][x] == ('%'):
                dungeon[y][x] == '+'

            if dungeon[y][x] == ' ':
                dungeon[y][x] == '#'

    for j in range(len(dungeon)):
        for i in range(len(dungeon[0])):
            term.puts(i, j, dungeon[j][i])

    
    term.refresh()
    term.read()

def draw(box):
    for i in range(box.x1, box.x2):
        for j in range(box.y1, box.y2):
            if i == box.x1 or i == box.x2-1 or j == box.y1 or j == box.y2-1:
                term.bkcolor('grey')
                char = '#'
            else:
                char = '.'
            term.puts(i, j, char)
            term.bkcolor('black')
    term.refresh()

def test_lpath():
    b1, b2 = box(0,0,5,5), box(30, 45, 35, 60)
    term.open()
    term.set('window: size=80x50, cellsize=8x8')
    term.set('font: ./fonts/Ibm_cga.ttf, size=4')
    draw(b1)
    draw(b2)
    for i, j in lpath(b1, b2):
        term.puts(i, j, 'X')
    term.refresh()
    term.read()

if __name__ == "__main__":
    build()