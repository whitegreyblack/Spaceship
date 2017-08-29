# -*- coding=utf-8 -*-

from bearlibterminal import terminal as term
from namedlist import namedlist
from objects import Map
from maps import MAPS
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
wmap = MAPS.DUNGEON

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
                            x = tools.movement(x, dx, fx, 1, 79)
                            y = tools.movement(y, dy, fy, 2, 23)
                            if (x, y) in blockables or (x, y) in units:
                                x, y = tx, ty
                                stop = True
                            elif (tx, ty) == (x, y):
                                stop = True
                            tx, ty = x, y
                    else:
                        x = tools.movement(x, dx, fx, 1, 79)
                        y = tools.movement(y, dy, fy, 1, 23)
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
