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
X_TEMP, Y_TEMP = 160, 100
WALL, FLOOR = -1, 1

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

def build():
    term.open()
    term.set('window: size={}x{}, cellsize=4x4'.format(X_TEMP, Y_TEMP))
    setup_font('Ibm_cga', 8, 8)
    # constructor -- (-1 = impassable) start with a map of walls
    # dungeon = [[-1 for _ in range(x)] for _ in range(y)]
    dungeon = [[0 for _ in range(X_TEMP)] for _ in range(Y_TEMP)]
    volrooms = 0
    rooms = []
    tries = 0
    directions = [
        [1, 0], [-1, 0], [0,  1], [0, -1], 
        [1, 1], [1, -1], [-1, 1], [-1,-1],
        [1, 2], [1, -2], [-1, 2], [-1,-2],
        [2, 1], [-2, 1], [2, -1], [-2,-1]]
    distribution = [
        .5, .5, .5, .5, 
        .25, .25, .25, .25, 
        .125, .125, .125, .125, 
        .125, .125, .125, .125
        ]
    while volrooms < X_TEMP * Y_TEMP * .85 and tries < 300:
        # for i in range(len(dungeon)):
        #     for j in range(len(dungeon[0])):
        #         if dungeon[i][j] == 1:
        #             term.bkcolor('blue')
        #         elif dungeon[i][j] == 2:
        #             term.bkcolor('green')
        #         elif dungeon[i][j] == 3:
        #              term.bkcolor('red')
        #         term.puts(j, i, '[c=grey]'+('.' if dungeon[i][j] > 0 else '#')+'[/c]')
        #         term.bkcolor('black')
        #         if j % 10 == 0:
        #             term.puts(j, 0, "{}".format(j//10))
        #     if i % 10 == 0:
        #         term.puts(0, i, "{}".format(i//10))
        # term.refresh()
        x, y = randint(5, 12), randint(5, 12)
        ox, oy = randint(-1,2), randint(-1, 2)
        tx, ty = X_TEMP//2-x//2, Y_TEMP//2-y//2 # <-- the upper left point of the box starts near center
        if volrooms == 0:
            # center the first box
            room = box(tx, ty, tx+x, ty+y)
            rooms.append(room)
            for i in range(y):
                for j in range(x):
                    dungeon[ty+i][tx+j] = 1
            volrooms += x * y

        else:
            case1 = False
            direction = choices(population=directions, weights=distribution, k=1)[0]
            while True:
                tx, ty = tx + randint(-2,3), ty + randint(-2, 3)
                tx, ty = tx + direction[0], ty + direction[1]
                temp = box(tx, ty, tx+x, ty+y)
                intersects = any(intersect(room, temp) for room in rooms)
                # only checks for out of bounds if no intersections
                # needs to be both free of intersectiosn and within bounds
                if not intersects:
                    if not oob(temp):
                        rooms.append(temp)
                        for i in range(y):
                            for j in range(x):
                                dungeon[ty+i][tx+j] += 1
                        volrooms += x * y
                        case1 = True
                    else:
                        tries += 1
                    break
                
            if not case1:
                tx, ty = X_TEMP//2-x//2, Y_TEMP//2-y//2 # <-- the upper left point of the box starts near center
                while True:
                    tx, ty = tx + randint(-2,3), ty + randint(-2, 3)        
                    tx, ty = tx + direction[0], ty + direction[1]
                    temp = box(tx, ty, tx+x, ty+y)
                    intersects = any(intersect(room, temp) for room in rooms)
                    if not intersects:
                        if not oob(temp):
                            rooms.append(temp)
                            for i in range(y):
                                for j in range(x):
                                    dungeon[ty+i][tx+j] += 1
                            volrooms += x * y
                        else:
                            tries += 1
                        break                

    print('-------------------------\nBOXES:')
    for r in rooms:
        print(r)
    print('-------------------------')

    # -- Seperates boxes inside vs outside ellipse
    term.read()
    term.clear()
    for  r in rooms:
        for x in range(r.x1, r.x2):
            for y in range(r.y1, r.y2):
                if ooe(*(center(r))):
                    # (r.x2-r.x1 >= 12 or r.y2-r.y1 >= 12)    
                    if volume(r) >= 85:
                        term.bkcolor('dark green')
                    else:
                        term.bkcolor('dark blue')
                else:
                    term.bkcolor('dark red')
                term.puts(x, y, '[c=grey].[/c]')
            term.bkcolor('black')
    term.refresh()
    term.read()
    # -- Prints only the large rooms
    term.clear()
    wallmap = [[0 for _ in range(X_TEMP)] for _ in range(Y_TEMP)]
    large_rooms = set()
    other_rooms = set()
    for  r in rooms:
        inside_ellipse = ooe(*(center(r)))
        # long_enough = (r.x2-r.x1 >= 12 or r.y2-r.y1 >= 12)
        large_enough = volume(r) >= 85
        if large_enough:
            large_rooms.add((r, center(r)))
            term.bkcolor('dark green')
            for x in range(r.x1, r.x2):
                for y in range(r.y1, r.y2):
                    term.puts(x, y, '[c=grey].[/c]')
                    wallmap[y][x] = 2
            for x in range(r.x1-1, r.x2+1):
                wallmap[r.y1-1][x] = 1
                wallmap[r.y2][x] = 1
            for y in range(r.y1-1, r.y2+1):
                wallmap[y][r.x1-1] = 1
                wallmap[y][r.x2] = 1
            term.bkcolor('black')
        else:
            # save smaller rooms for later
            other_rooms.add((r, center(r)))
    term.refresh()
    term.read()
    term.clear()
    for i in range(len(wallmap)):
        for j in range(len(wallmap[0])):
            if wallmap[i][j] == 1:
                term.bkcolor('grey')
                char = '#'
            elif wallmap[i][j] == 2:
                char = '.'
            else:
                char = ' '
            term.puts(j, i, char)
            term.bkcolor('black')
    term.refresh()
    term.read()
    term.clear()
    # edges
    edges = set()
    vertices = set()
    print('creating minimum graph')
    # create the edges
    for room, p1 in large_rooms:
        for other, p2 in large_rooms:
            dis = distance(p1, p2)
            if p1 != p2 and (p1 in vertices and p2 in vertices):
                # distance ,pt-pt, rev
                edges.add((dis, (p1, p2), (p2, p1)))
                vertices.add(p1)
                vertices.add(p2)

    #     # print('checking breshams')
    # for room, p1 in large_rooms:
    #     for other, p2 in large_rooms:
    #         if p1 != p2:
    #             edges.add((distance(p1, p2), (p1, p2), (p2, p1)))
    #             term.bkcolor('yellow')
    #             for x, y in bresenhams(p1, p2):
    #                 term.puts(x, y, 'X')
    #     term.bkcolor('dark green')                  
    #     for x in range(room.x1, room.x2):
    #         for y in range(room.y1, room.y2):
    #             term.puts(x, y, '[c=grey].[/c]')
    #     term.bkcolor('black')
    # term.refresh()
    # # print(edges)
    # for i in sorted(edges):
    #     print(i)
    # term.read()
    # while True:


if __name__ == "__main__":
    build()
    # circle()
    # print(intersect(box(36, 16, 45, 25), box(37, 8, 43, 14)))
    # print(intersect(box(37, 8, 43, 14), box(36, 16, 45, 25)))
    # print(intersect(box(35, 16, 45, 22), box(35,9, 44, 15)))
    # print(intersect(box(37, 8, 44, 16), box(35, 8, 44, 17)))
    # print(oob(box(-1, 0, 1, 1)))
    # print(oob(box(0, 0, 1, 1)))
    # print(oob(box(0, 0, 79, 25)))
    # print(oob(box(0, 0, 80, 24)))
    # print(oob(box(0, 0, 79, 24)))