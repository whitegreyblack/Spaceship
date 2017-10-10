# Dungeon.py
# builds a random dungeon of size MxN
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from bearlibterminal import terminal as term
from copy import deepcopy
from random import choice, choices, randint
from collections import namedtuple
from tools import bresenhams
from spaceship.setup import setup_font
X_MIN_ROOM_SIZE=80
X_MAX_ROOM_SIZE=100
Y_MIN_ROOM_SIZE=25
Y_MAX_ROOM_SIZE=75
X_TEMP, Y_TEMP = 80, 50
WALL, FLOOR = -1, 1

box = namedtuple("BOX", "x1 y1 x2 y2")

def intersect(b1, b2):
    return (b1.x1 <= b2.x2 and b1.x2 >= b2.x1 and 
            b1.y1 <= b2.y2 and b1.y2 >= b2.y1)

def rotate(box):
    return list(zip(*box[::-1]))

def oob(box):
    return box.x1 < 0 or box.y1 < 0 or box.x2 >= 80 or box.y2 >= 50

def build():
    term.open()
    term.set('window: size=80x50')
    setup_font('Ibm_cga', 8, 8)
    # constructor -- (-1 = impassable) start with a map of walls
    # dungeon = [[-1 for _ in range(x)] for _ in range(y)]
    dungeon = [[0 for _ in range(X_TEMP)] for _ in range(Y_TEMP)]
    numrooms = 0
    rooms = []
    while numrooms < 25:
        for i in range(len(dungeon)):
            for j in range(len(dungeon[0])):
                if dungeon[i][j] == 1:
                    term.bkcolor('blue')
                elif dungeon[i][j] == 2:
                    term.bkcolor('green')
                elif dungeon[i][j] == 3:
                     term.bkcolor('red')
                term.puts(j, i, '[c=grey]'+('.' if dungeon[i][j] > 0 else '#')+'[/c]')
                term.bkcolor('black')
                if j % 10 == 0:
                    term.puts(j, 0, "{}".format(j//10))
            if i % 10 == 0:
                term.puts(0, i, "{}".format(i//10))
           
        term.refresh()
        # key = term.read()
        # if key in (term.TK_ESCAPE, term.TK_CLOSE):
        #     break
        # else:
        x, y = randint(4, 12), randint(4, 12)
        tx, ty = X_TEMP//2-x//2, Y_TEMP//2-y//2 # <-- the upper left point of the box starts near center
        if numrooms == 0:
            # center the first box
            print('Box{} : {}x{} start @ {}x{}'.format(numrooms+1, x, y, tx, ty))
            room = box(X_TEMP//2-x//2, Y_TEMP//2-y//2, tx+x, ty+y)
            rooms.append(room)
            print('found a spot at {}x{}'.format(tx, ty))
            print(room)
            for i in range(y):
                for j in range(x):
                    dungeon[Y_TEMP//2-y//2+i][X_TEMP//2-x//2+j] = 1
            numrooms += 1

        else:
            case1 = False
            directions = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1],[1, 2],[1, -2],[-1, 2],[-1,-2]]
            direction = directions[randint(0, len(directions)-1)]
            room = None
            print('Box{} : {}x{} start @ {}x{}'.format(numrooms+1, x, y, tx, ty))
            
            while True:
                tx, ty = tx + direction[0], ty + direction[1]
                temp = box(tx, ty, tx+x, ty+y)

                intersects = any(intersect(room, temp) for room in rooms)
                
                # only checks for out of bounds if no intersections
                # needs to be both free of intersectiosn and within bounds
                if not intersects:
                    if not oob(temp):
                        rooms.append(temp)
                        print(temp)
                        for i in range(y):
                            for j in range(x):
                                dungeon[ty+i][tx+j] += 1
                        numrooms += 1
                    break
                

                # while intersects:
                #     tx, ty = tx + direction[0], ty + direction[1]
                #     temp = box(tx, ty, tx+x, ty+y)
                #     for room, i in zip(rooms, range(len(rooms))):
                #         print('Comparing ({}){} and {} | {}'.format(i, room, temp, not intersect(room, temp)))
                #         if not intersect(room, temp):
                #             print('found a spot at {}x{}'.format(tx, ty))
                #             intersects = False
                #             room = temp
                #             break
                #     if oob(temp):
                #         break
                # if not intersects and not oob(room):
                #     rooms.append(room)
                #     print(room)
                #     for i in range(y):
                #         for j in range(x):
                #             dungeon[ty+i][tx+j] += 1
                #     numrooms += 1
                #     case1 = True
                
                # # tries a second time with rotate box
                # if not case1:
                #     print('Trying rotation')
                #     x, y, = y, x
                #     tx, ty = X_TEMP//2-x//2, Y_TEMP//2-y//2
                #     print('Box{} : {}x{} start @ {}x{}'.format(numrooms+1, x, y, tx, ty))

                #     while intersects:
                #         tx, ty = tx + direction[0], ty + direction[1]
                #         temp = box(tx, ty, tx+x, ty+y)
                #         for room in rooms:
                #             if not intersect(room, temp):
                #                 print('found a spot at {}x{}'.format(tx, ty))
                #                 intersects = False
                #                 room = temp
                #         if oob(temp):
                #             break
                #     if not intersects and not oob(room):
                #         rooms.append(room)
                #         print(room)
                #         for i in range(y):
                #             for j in range(x):
                #                 dungeon[ty+i][tx+j] += 1
                #         numrooms += 1
    print('-------------------------\nBOXES:')
    for r in rooms:
        print(r)
    print('-------------------------')
    term.read()



                    

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


if __name__ == "__main__":
    build()
    # print(intersect(box(36, 16, 45, 25), box(37, 8, 43, 14)))
    # print(intersect(box(37, 8, 43, 14), box(36, 16, 45, 25)))
    # print(intersect(box(35, 16, 45, 22), box(35,9, 44, 15)))
    # print(intersect(box(37, 8, 44, 16), box(35, 8, 44, 17)))
    # print(oob(box(-1, 0, 1, 1)))
    # print(oob(box(0, 0, 1, 1)))
    # print(oob(box(0, 0, 79, 25)))
    # print(oob(box(0, 0, 80, 24)))
    # print(oob(box(0, 0, 79, 24)))