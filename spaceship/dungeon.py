# Dungeon.py
# builds a random dungeon of size MxN
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from bearlibterminal import terminal as term
from copy import deepcopy
from random import choice, randint, shuffle
from collections import namedtuple
from tools import bresenhams
from spaceship.setup import setup_font
import math
import time
from copy import deepcopy

debug = False
X_TEMP, Y_TEMP = 78, 40
# X_TEMP, Y_TEMP = 160, 80
# X_TEMP, Y_TEMP = 80, 50
WALL, FLOOR = -1, 1
box = namedtuple("Box", "x1 y1 x2 y2")
point = namedtuple("Point", "x y")

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
        if choice([0, 1]) == 1 and q.keys():
            u = min(k for k in q.keys())
            for z in graph[u].keys():
                if z in q.keys() and 0 < graph[u][z] < q[z]: 
                    p[z] = u
                    q[z] = graph[u][z]  
    return p

def distance(p1, p2):
    try:
        return math.sqrt((p2.x-p1.x)**2+(p2.y-p1.y)**2)
    except AttributeError:
        return math.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)
    
def intersect(b1, b2):
    o = offset = 1
    return (b1.x1+o <= b2.x2 and b1.x2-o >= b2.x1 and 
            b1.y1+o <= b2.y2 and b1.y2-o >= b2.y1)

def center(box):
    return point((box.x1 + box.x2)//2, (box.y1 + box.y2)//2)

def volume(box):
    return (box.x2-box.x1) * (box.y2-box.y1)

def rotate(box):
    return list(zip(*box[::-1]))

def equal(p1, p2):
    try:
        return p1.x == p2.x and p1.y == p2.y
    except AttributeError:
        return center(p1) == center(p2)
    except:
        print(p1, p2)
        raise

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

def path(p1, p2, dungeon):
    node = namedtuple("Node", "df dg dh parent node")
    openlist = set()
    closelist = []
    openlist.add(node(0, 0, 0, None, p1))

    if debug:
        print("PATH: DISTANCE - {}".format(int(distance(p1, p2)*10)))

    while openlist:
        nodeq = min(sorted(openlist))
        openlist.remove(nodeq)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i, j) != (0, 0):
                    neighbor = nodeq.node[0]+i, nodeq.node[1]+j

                    if neighbor == p2:
                        closelist.append(nodeq)
                        return closelist

                    if dungeon[neighbor[1]][neighbor[0]] in ('.', '+'):

                        sg = nodeq.dg + int(distance(nodeq.node, neighbor) * 10)
                        sh = int(distance(neighbor, p2) * 10)
                        sf = sg + sh

                        if any(n.node == neighbor and n.df < sf for n in openlist):
                            pass
                        elif any(n.node == neighbor and n.df < sf for n in closelist):
                            pass
                        else:
                            openlist.add(node(sf, sg, sh, nodeq.node, neighbor))

        closelist.append(nodeq)

    return closelist

def decay(dungeon, n=1000):
    """More of a fantasy concept where a pristine dungeon layout has
    exprienced years of degeneration along with decay and collapse. This
    leads to growth of fauna, broken tunnels and such. Should start with 
    a well-formed dungeon and then start decay for n turns"""
    def point_oob(i, j):
        '''Uses size of dungeon to determine out of bounds error'''
        return 0 <= i < len(dungeon[0])-1 and 0 <= j < len(dungeon)-1

    def point_oob_ext(i, j, xlim, ylim):
        '''Same as function of the same name but uses custom bounds'''
        return xlim[0] <= i < xlim[1] and ylim[0] <= j < ylim[1]

    def cellauto(i, j):
        val = 0
        # check the value of the cell
        doors = set()
        space = set()
        for ii in range(-1, 2):
            for jj in range(-1, 2):
                if (i, j) != (i+ii, j+jj):
                    if dungeon[j+jj][i+ii] == '%':
                        val += 1
                    if dungeon[j+jj][i+ii] == '+':
                        doors.add((i+ii, j+jj))
                    if dungeon[j+jj][i+ii] == ' ':
                        space.add((i+ii, j+jj))

        # turn the cell into a floor cell if surrounded by 4 walls or more
        if (val >= 4 or val <= 1) and point_oob_ext(i+ii, j+jj, (2, X_TEMP-2), (2, Y_TEMP-2)):
            # if choice([i in range(0, 2)]):
            decayed[j][i] = '.'
            floors.append((i, j))
            for di, dj in doors:
                decayed[dj][di] = '.'
                floors.append((di, dj))
            '''
            else:
                decayed[j][i] = '~'
                liquid.append((i, j))
            '''
            # make sure any free spaces bordering changed cell turn into wall tiles
            # for ii in range(-1, 2):
            #     for jj in range(-1, 2):
            #         within = point_oob_ext(i+ii, j+jj, (0, X_TEMP-1), (0, Y_TEMP-1))
            #         if within and decayed[j+jj][i+ii] == ' ':
            #             decayed[j+jj][i+ii] = '%'
            #             walls.append((i+ii, j+jj))         
            for si, sj in space:
                within = point_oob_ext(si, sj, (0, X_TEMP-1), (0, Y_TEMP-1))
                if within:
                    decayed[sj][si] = '%'
                    walls.append((si, sj))
            
            return True
        return False

    def cellpath(p1, p2):
        # creates a bsf from two points
        frontier = set()
        frontier.add((0, p1))
        camefrom = { p1:None }
        costfrom = { p1:0 }
        # print(p1, p2)
        found = False
        for j in range(len(decayed)):
            for i in range(len(decayed[0])):
                if dungeon[j][i] == '%':
                    term.puts(i, j, "[c=#ffffff]{}[/c]".format(decayed[j][i]))
                elif dungeon[j][i] == '.':
                    term.puts(i, j, "[c=#806040]{}[/c]".format(decayed[j][i]))
                elif dungeon[j][i] == '~':
                    term.puts(i, j, "[c=#0080C0]{}[/c]".format(decayed[j][i]))
                elif dungeon[j][i] == '=':
                    term.puts(i, j, "[c=#D02020]{}[/c]".format(decayed[j][i]))
                elif dungeon[j][i] == ',':
                    term.puts(i, j, "[c=#80C080]{}[/c]".format(decayed[j][i]))
                else:
                    term.puts(i, j, decayed[j][i])
        while frontier:
            current = min(sorted(frontier))
            frontier.remove(current)
            curnode = current[1]
            # print(curnode)
            i, j = curnode
            if curnode == p2:
                camefrom[neighbor] = curnode
                found = True
                break
            for ii in range(-1, 2):
                for jj in range(-1, 2):
                    ni, nj = i+ii, j+jj
                    neighbor = (ni, nj)
                    if (ii, jj) != (0, 0) and decayed[nj][ni] in ('.', '+'):
                        cost = costfrom[curnode] + distance(curnode, neighbor)
                        if neighbor not in costfrom.keys() or cost < costfrom[neighbor]:
                            costfrom[neighbor] = cost
                            priority = cost + distance(neighbor, p2)
                            frontier.add((priority, neighbor))
                            camefrom[neighbor] = curnode
            for i, j in camefrom.keys():
                term.puts(i,j,'[c=#00c0c0]/[/c]')
            term.puts(*p2, '[c=#00c0c0]/[/c]')
            term.refresh()
        if found:
            term.clear()
            for j in range(len(decayed)):
                for i in range(len(decayed[0])):
                    if dungeon[j][i] == '%':
                        term.puts(i, j, "[c=#ffffff]{}[/c]".format(decayed[j][i]))
                    elif dungeon[j][i] == '.':
                        term.puts(i, j, "[c=#806040]{}[/c]".format(decayed[j][i]))
                    elif dungeon[j][i] == '~':
                        term.puts(i, j, "[c=#0080C0]{}[/c]".format(decayed[j][i]))
                    elif dungeon[j][i] == '=':
                        term.puts(i, j, "[c=#D02020]{}[/c]".format(decayed[j][i]))
                    elif dungeon[j][i] == ',':
                        term.puts(i, j, "[c=#80C080]{}[/c]".format(decayed[j][i]))
                    else:
                        term.puts(i, j, decayed[j][i])
            start = p2
            term.puts(*p1, '[c=#00c0c0]/[/c]')
            while camefrom[start] != None:
                term.puts(*(camefrom[start]), '[c=#00c0c0]/[/c]')
                start = camefrom[start]
                term.refresh()

    walls, floors, doors, liquid, spaces, other = [], [], [], [], [], []
    decayed = deepcopy(dungeon)
    if debug:
        print("DUNGEON DIMENSIONS: {}x{}".format(len(dungeon[0]), len(dungeon)))

    # get the dungeon features
    for j in range(len(dungeon)):
        for i in range(len(dungeon[0])):
            if dungeon[j][i] == '%':
                walls.append((i, j))
            elif dungeon[j][i] == '.':
                floors.append((i, j))
            elif dungeon[j][i] == '+':
                doors.append((i, j))
            elif dungeon[j][i] == ' ':
                spaces.append((i, j))
            else:
                other.append((i, j))

    # decay of walls
    shuffle(walls)
    shuffle(floors)
    
    if debug:
        print("NUMBER OF WALLS: {}".format(len(walls)))
    
    # wallsToFloor = 0
    # while wallsToFloor <= 50:
    #     changed = cellauto(*walls[wallsToFloor%len(walls)])
    #     if changed:
    #         wallsToFloor += 1

    changed = 0
    for i in range(len(walls)):
        # decay wall
        i, j = walls[i%len(walls)]
        val = cellauto(i, j)
        if val:
            changed += 1
    
    if debug:
        print("CHANGED: {}".format(changed))

    # for i in range(len(floors)):

    # find 2nd and 3rd largest voids -> pools of water
    # space_copy = spaces
    # space_flood = {}
    # while space_copy:
    #     i, j = space_copy.pop()
    #     for k in space_flood.keys():
    #         if space_flood[k]
    # liquid = path(choice(floors), choice(floors), decayed)
    # for _, _, _, _, n in liquid:
    #     i, j = n
    #     decayed[j][i] = '~'
    # for _, _, _, _, n in liquid:
    #     i, j = n
    #     for ii in range(-2, 3):
    #         for jj in range(-2, 3):
    #             if (ii, jj) != (0, 0) and decayed[j+jj][i+ii] == '.':
    #                 decayed[j+jj][i+ii] = ','
    '''
    # leads to liquid water/lave poured out
    liquidmap = {}
    for i in range(len(liquid)):
        array = {}
        for j in range(len(liquid)):
            array[j] = distance(liquid[i], liquid[j])
        liquidmap[i] = array

    liquidmap = mst(liquidmap)

    for k in liquidmap.keys():
        for x, y in bresenhams(liquid[k], liquid[liquidmap[k]]):
            if decayed[y][x] not in ('%', ' '):
                if decayed[y][x] == '.':
                    floors.remove((x, y))
                elif decayed[y][x] == '+':
                    doors.remove((x, y))
                decayed[y][x] = '~'
                liquid.append((x, y))
            elif decayed[y][x] == '%':
                val = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if decayed[y+j][x+i] == ' ':
                            val = 1
                            break
                if val == 0:
                    walls.remove((x, y))
                    liquid.append((x, y))
                    decayed[y][x] = '~'

    # leads to growth of fauna earth vs fire elementals
    for i, j in liquid:
        for ii in range(-2, 3):
            for jj in range(-2, 3):
                if decayed[j+jj][i+ii] == '.':
                    dis = distance((i, j), (i+ii, j+jj))
                    if dis <= 1:
                        decayed[j+jj][i+ii] = ','
                    elif dis <= 2 and choice([0, 1]) == 1:
                        decayed[j+jj][i+ii] = ','
                    elif dis <= 3 and choice([-1, 0, 1]) == 1:
                        decayed[j+jj][i+ii] = ','
    '''
    return decayed

def dwalk_lake(x, y):
    pass

def build_terrain(width, height, tiletype, entropy=0, buildopts=None):
    if buildopts:
        rocks = None
        water = None
        trees = None
    
    if tiletype == "plains":
        vegatation = .33
        num_trees = 10
        terrain = [["." for _ in range(width)] for _ in range(height)]

        # for sure at least 3 trees
        for t in range(3):
             terrain[randint(0, height-1)][randint(0, width-1)] = "T"

        for t in range(num_trees-3):
            terrain[randint(0, height-1)][randint(0, width-1)] = "T"
            stop_chance = randint(0, num_trees-t)
            if stop_chance == 0:
                break

        return terrain

    if tiletype == "grassland":
        num_trees = 100
        terrain = [["." for _ in range(width)] for _ in range(height)]
        
        # for sure at least 3 trees
        for t in range(3):
             terrain[randint(0, height-1)][randint(0, width-1)] = "T"

        for t in range(num_trees-3):
            terrain[randint(0, height-1)][randint(0, width-1)] = "T"
            stop_chance = randint(0, num_trees-t)
            if stop_chance == 0:
                break

        return terrain 

    elif tiletype == "hills":
        num_trees = 10
        vege_chars = (".", "~")
        terrain = [[choice(vege_chars) for _ in range(width)] for _ in range(height)]
                
        # for t in range(num_trees):
        #     terrain[randint(0, height-1)][randint(0, width-1)] = "T"
        #     stop_chance = randint(0, num_trees-t)
        #     if stop_chance == 0:
        #         break

        return terrain

    elif tiletype == 'woods' or tiletype == 'forest':
        num_trees = 200
        terrain = [[choice(".") for _ in range(width)] for _ in range(height)]
                
        for t in range(num_trees):
            terrain[randint(0, height-1)][randint(0, width-1)] = "T"
            stop_chance = randint(0, num_trees)
            if stop_chance == 0:
                break

        return terrain
        
    elif tiletype == 'fields':
        # ALGO: BSP seperates areas into 'fields' which then contain a couple of rectangles and
        #       the largest one or two rectangles become fields while the next two become houses
        #       all other rectangles become plain tiles
        # Maybe a bezier curve could be used to add a river that flows between the fields
        # Even add a chance for river to split within the map
        pass
    else:
        print(tiletype)
        raise ValueError("Tiletype not implemented")

def build_dungeon(width, height, rot=0):
    '''Places rooms in a box of size width by height and applies rot if
    is not 0 and returns the box to be parsed as a dungeon'''

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
            box.x2 >= width-1 or box.y2 >= height-1

    print("BUILD DUNGEON: {}x{}".format(width, height))
    dungeon = [[' ' for _ in range(width)] for _ in range(height)]
    rooms, large_rooms, other_rooms = [], [], []
    graph = {}
    tries = 0

    # Expansion Algorithm
    while len(rooms) < 25 and tries < 2000:
        key = choice([i for i in range(-1, 4)])

        if key == 4:
            x, y = randint(16, 24), randint(12, 18)
            px, py = randint(9, width-9), randint(9, height-9)
        elif key >= 2:
            x, y = randint(12, 16), randint(8, 12)
            px, py = randint(x//2, width-x//2), randint(y//2, height-y//2)
        elif key >= 0:
            x, y = randint(8, 12), randint(4, 6)
            px, py = randint(x//2, width-x//2), randint(y//2, height-y//2)
        else:
            x, y = randint(6, 8), randint(3, 4)
            px, py = randint(x//2, width-x//2), randint(y//2, height-y//2)

        temp = box(px-int(round(x/2)), py-int(round(y/2)), px-int(round(x/2))+x, py-int(round(y/2))+y)
        intersects = any(intersect(room, temp) for room in rooms)

        if not intersects and not box_oob(temp):
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

    traps = []
    for i in range(3):
        i, j = choice(floor_clear)
        floor_clear.remove((i, j))
        dungeon[j][i] = '^'

    upStairs, downStairs = choice(floor_clear), choice(floor_clear)
    while distance(upStairs, downStairs) <= 15:
        upStairs, downStairs = choice(floor_clear), choice(floor_clear)

    # remove upstairs from floors and replace char
    floor_clear.remove(upStairs)
    ui, uj = upStairs
    dungeon[uj][ui] = '<'

    # remove downstairs from floors and replace char
    floor_clear.remove(downStairs)
    di, dj = downStairs
    dungeon[dj][di] = '>'

    # i, j = choice(floor_clear)
    # floor_clear.remove((i, j))
    # dungeon[j][i] = '>'

    # i, j = choice(floor_clear)
    # floor_clear.remove((i, j))
    # dungeon[j][i] = '<'

    # for j in range(len(dungeon)):
    #     for i in range(len(dungeon[0])):
    #         if dungeon[j][i] == '%':
    #             term.puts(i, j, "[c=#ffffff]{}[/c]".format(dungeon[j][i]))
    #         elif dungeon[j][i] == '.':
    #             term.puts(i, j, "[c=#808080]{}[/c]".format(dungeon[j][i]))
    #         else:
    #             term.puts(i, j, dungeon[j][i])

    # term.refresh()
    # term.read()

    # create backstory
    backstory = ""

    # the output is more for debugging
    print("Rooms:", len(rooms))

    if rot:
        dungeon = decay(dungeon, n=rot)

    return dungeon

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

def test_dungeon():
    dungeon = build(2000)
    x, y = 0, 0

    for j in range(len(dungeon)):
        for i in range(len(dungeon[0])):
            if dungeon[j][i] == '<':
                x, y = i, j

    for j in range(len(dungeon)):
        for i in range(len(dungeon[0])):
            if dungeon[j][i] == '%':
                term.puts(i, j, "[c=#ffffff]{}[/c]".format(dungeon[j][i]))
            elif dungeon[j][i] == '+':
                term.puts(i, j, "[c=#602020]{}[/c]".format(dungeon[j][i]))
            elif dungeon[j][i] == '.':
                term.puts(i, j, "[c=#806040]{}[/c]".format(dungeon[j][i]))
            elif dungeon[j][i] == '~':
                term.puts(i, j, "[c=#0080C0]{}[/c]".format(dungeon[j][i]))
            elif dungeon[j][i] == '=':
                term.puts(i, j, "[c=#D02020]{}[/c]".format(dungeon[j][i]))
            elif dungeon[j][i] == ',':
                term.puts(i, j, "[c=#80C080]{}[/c]".format(dungeon[j][i]))
            else:
                term.puts(i, j, dungeon[j][i])
            
    term.puts(x, y, '[c=#00C0C0]@[/c]')

    # River runs red
    # rx1, rx2 = 0, 0
    # ry1, ry2 = 0, 0
    # while rx1 == rx2 and abs(rx1-rx2) < X_TEMP//4:
    #     rx1, ry1 = randint(0, X_TEMP), 0
    #     rx2, ry2 = randint(0, X_TEMP), Y_TEMP-1
    # term.puts(rx1, ry1, "[c=#0080C0]~[/c]")
    # if randint(-2, 2) > 0:
    #     for i in range(-3, 4):
    #         for i,j in bresenhams((rx1+i,ry1), (rx2+i, ry2)):
    #             term.puts(i, j, "[c=#0080C0]~[/c]")
    #     term.puts(rx2, ry2, "[c=#0080C0]~[/c]")
    term.refresh()
    term.read()
        


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
    term.open()
    term.set('window: size={}x{}, cellsize=4x4'.format(X_TEMP, Y_TEMP))
    setup_font('Ibm_cga', 8, 8)
    test_dungeon()
