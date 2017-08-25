# -*- coding=utf-8 -*-

from bearlibterminal import terminal as term
from ctypes import c_uint32, addressof
from namedlist import namedlist
from time import time, sleep
from copy import deepcopy
import tools

limit_x, limit_y = 76, 20 # offset by -1 to account for start index 0
factor_x, factor_y = 1, 1
window_size = (limit_x+factor_x, limit_y+factor_y) # add the offset back to create window size with start index 1
player_pos = (10, 7)
movement_ratio = (factor_x, factor_y)
movement_costs = {
    term.TK_LEFT: (-1, 0),
    term.TK_RIGHT: (1, 0),
    term.TK_DOWN: (0, 1),
    term.TK_UP: (0, -1),
}
mult = [
            [1,  0,  0, -1, -1,  0,  0,  1],
            [0,  1, -1,  0,  0, -1,  1,  0],
            [0,  1,  1,  0,  0, -1, -1,  0],
            [1,  0,  0,  1, -1,  0,  0, -1]
        ]
wmap = """\
#########################################################
#....#..................................................#
#..................#.####################################
#....#........#....#......#      #...............#
#..................#......########...............#
#....#.............#.............................#
#..................###############...............#
#....#.............#             #...............#
#.............#....#             #################
#....#.............#
#..................#
#....#.............#
####################"""

wmap = """\
###########################################################
#...........#.............................................#
#...........#........#....................................#
#.....................#...................................#
#....####..............#..................................#
#.......#.......................#####################.....#
#.......#...........................................#.....#
#.......#...........##..............................#.....#
#####........#......##..........##################..#.....#
#...#...........................#................#..#.....#
#...#............#..............#................#..#.....#
#...............................#..###############..#.....#
#...............................#...................#.....#
#...............................#...................#.....#
#...............................#####################.....#
#.........................................................#
#.........................................................#
###########################################################"""

class Map:
    def __init__(self, data):
        self.data, self.height, self.width = self.dimensions(data)     
        self.light = [[0 for _ in self.width] for _ in self.height]
        self.flag = 0

    def dimensions(self, data):
        '''takes in a string map and returns a 2D list map and map dimensions'''
        data = [[col for col in row] for row in data.split('\n')]
        height = len(data)
        width = max(len(col) for col in data)
        return data, height, width

    def square(self, x, y):
        return self.data[y][x]

    def blocked(self, x, y):
        return (x < 0 or y < 0 or x >= self.width or y >= self.height or self.data[y][x] == "#")

    def lit(self, x, y):
        return self.light[y][x] == self.flag
    
    def set_lit(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.light[y][x] == self.flag

    def fov_calc(self, x, y, radius):
        self.flag += 1
        for o in range(8):
            self.sight(x, y, 1, 1.0, 0.0, radius, mult[0][o], mult[1][o], mult[2][o], mult[3][o], 0)

    def sight(self, cx, cy, row, start, end, radius, xx, xy, yx, yy, id):
        if start < end:
            return

        radius_squared = radius * radius

        for j in range(row, radius+1):
            dx, dy = -j-1, -j
            blocked = False
            while dx <= 0:
                dx += 0
                X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
                l_slope, r_slope = (dx-0.5)/(dy+0.5), (dx+0.5)/(dy-0.5)
                if start < r_slope:
                    continue
                elif end > l_slope:
                    break
                else:
                    # Our light beam is touching this square; light it:
                    if dx*dx + dy*dy < radius_squared:
                        self.set_lit(X, Y)
                    if blocked:
                        # we're scanning a row of blocked squares:
                        if self.blocked(X, Y):
                            new_start = r_slope
                            continue
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if self.blocked(X, Y) and j < radius:
                            # This is a blocking square, start a child scan:
                            blocked = True
                            self.sight(cx, cy, j+1, start, l_slope,
                                             radius, xx, xy, yx, yy, id+1)
                            new_start = r_slope
            # Row is scanned; do next row unless last square was blocked:
            if blocked:
                break

    def output(self):
        print(self.light)
        return self.light

def movement(pos, change, factor, low, high):
    '''takes in a 1d axis position and change parameters and returns a new position'''
    updated = pos + change * factor
    return updated if low < updated < high else max(low, min(updated, high))

def sight(x, y, r):
    def lightable():
        pass
    def light(v, x, y, row, start, end, radius, xx, xy, yx, yy):
        if start < end:
            return
        r_sq = radius*radius
        for j in range(row, radius+1):
            dx ,dy = -j-1, -1
            blocked = False
            while dx <= 0:
                dx += 1
                X, Y = x + dx * xx + dy * xy, y + dx * yx + dy * yy
                l_slope, r_slope = (dx-0.5)/(dy+0.5), (dx+0.5)/(dy-0.5)
                if start < r_slope:
                    continue
                elif end > l_slope:
                    break
                else:
                    if dx*dx + dy*dy < r_sq:
                        v.add((X,Y))
                    if blocked:
                        pass
    visible = set()
    visible.add((x,y))
    for region in range(len(mult)):
        light(visible, x, y, 1, 1.0, 0.0, r, mult[0][region], mult[1][region], mult[2][region], mult[3][region])


def test_map():
    global player_pos
    term.set("U+E003: ./assets/cursor03_small.png")
    term.clear()
    term.refresh()
    proceed = True
    blockables =[]
    units = []
    positions = []
    # this is by row
    copwmap = [[col for col in row] for row in wmap.split('\n')]
    #blockables = [(5,4), (5, 9), (14, 4), (14, 9)]
    for i in range(len(copwmap)):
        for j in range(len(copwmap[i])):
            positions.append((j, i))
            if copwmap[i][j] == "#":
                # reverse index due to row-major from split()
                blockables.append((j, i))
    try: # remove once game is running up and smooth -- no need for fast exit
        while proceed:
            term.clear()
            term.puts(limit_x, 0, 'Animating a map\n')
            term.color("grey")
            #term.puts(0, 0, wmap)
            # for x,y in positions:
            #     if (x,y) in blockables:
            #         term.puts(x, y, '#')
            #for  in blockables
            term.color("white")
            # reverse the indices to account for appending order
            #for j, i in blockables:
            #j, i = blockables[5]
            x, y = player_pos

            # for j, i in positions:
            #     if tools.distance(x, y, j, i) <= 10:
            #         points = tools.bresenhams((x, y), (j, i))
            #         for px, py in points:
            #             term.puts(px, py, copwmap[py][px])
            #             if (px, py) in blockables:
            #                 break
                        # elsee
                        #     term.puts(px, py, copwmap[py][px])
            term.puts(5,10, '[color=orange]r[/color]')
            units.append((5,10))
            term.puts(x, y, '[color=white]@[/color]')
            '''
            # Keyboard input -- currently handles:
                Exitting: [ESC]|[CLOSE][CTRL-C] -- [Y/N]
                Movement: [UP][DOWN][LEFT][RIGHT]
                Abilitys: [T][S
            '''
            while proceed and term.has_input():
                term.puts(21, 5, 'Got input')
                code = term.read()
                if code in (term.TK_ESCAPE, term.TK_CLOSE):
                    term.clear()
                    term.puts(10, 6, 'Really Quit? (Y/N)')
                    term.refresh()
                    code = term.read()
                    if code in (term.TK_Y,):
                        proceed = False
                elif code is term.TK_C and term.state(term.TK_CONTROL):
                    term.clear()
                    term.puts(10, 6, 'Really Quit? (Y/N)')
                    term.refresh()
                    code = term.read()
                    if code in (term.TK_Y,):
                        proceed = False
                elif code in movement_costs.keys():
                    tx, ty = x, y
                    dx, dy = movement_costs[code]
                    fx, fy = movement_ratio
                    if term.state(term.TK_SHIFT):
                        # px, py = x, y
                        term.puts(21, 6, 'Pressed Shift') 
                        stop = False
                        while not stop:
                            x = movement(x, dx, fx, 1, 79) 
                            y = movement(y, dy, fy, 2, 23)
                            if (x, y) in blockables or (x, y) in units:
                                x, y = tx, ty
                                stop = True
                            elif (tx, ty) == (x, y):
                                stop = True
                            tx, ty = x, y
                    else:
                        x = movement(x, dx, fx, 1, 79)
                        y = movement(y, dy, fy, 1, 23)
                        if (x, y) in blockables or (x, y) in units:
                            x, y = tx, ty
                    player_pos = (x, y)
                elif code in (term.TK_T,):
                    term.puts(21, 7, 'talking')
                elif code in (term.TK_S,):
                    term.puts(21, 7, 'stealing')
                else:
                    term.puts(0,6, 'other input')
            term.refresh()
    except KeyboardInterrupt:
        pass
    finally:
        term.close()

if __name__ == "__main__":
    term.open()
    x, y = window_size
    term.set("window: size={}x{}, title='Animation Test'".format(x, y))
    test_map()
    term.close