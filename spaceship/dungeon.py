# Dungeon.py
# builds a random dungeon of size MxN

from bearlibterminal import terminal as term
from copy import deepcopy
from random import choice, choices, randint
from tools import bresenhams
X_MIN_ROOM_SIZE=80
X_MAX_ROOM_SIZE=100
Y_MIN_ROOM_SIZE=25
Y_MAX_ROOM_SIZE=75
X_TEMP, Y_TEMP = 80, 25
WALL, FLOOR = -1, 1
def build(x, y):
    # constructor -- (-1 = impassable) start with a map of walls
    # dungeon = [[-1 for _ in range(x)] for _ in range(y)]
    dungeon = [[0 for _ in range(X_TEMP)] for _ in range(Y_TEMP)]
    for i in range(0, 22, 4):
        for j in range(0, 73, 7):
            if choice([0, 1, 1, 1]):
                for ii in range(choice([3,4])):
                    for jj in range(choice([5,6])):
                        try:
                            dungeon[i+ii+1][j+jj+1] = 1
                        except:
                            pass
    return dungeon

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

def draw(dungeon):
    term.open()
    for i in range(len(dungeon)):
        for j in range(len(dungeon[0])):
            term.puts(j, i, '.' if dungeon[i][j]==1 else '#')
    term.refresh()
    term.read()
if __name__ == "__main__":
    draw(build(0,0))