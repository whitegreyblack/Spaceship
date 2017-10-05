import random
import copy
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')

from bearlibterminal import terminal as t
from spaceship.setup import setup
width, height, size = 150, 100, 8
reverse = -1
world = None
t.open()
t.set('window: size={}x{}, cellsize={}x{}'.format(width, height, size, size))
t.set("font: ./fonts/unscii-8.ttf, size={}".format(size))
t.set("input.filter={keyboard, mouse}")

while True:
    seed = random.randint(0, 99999)
    print(seed)
    random.seed(seed)
    temp = [[-1 for _ in range(width)] for _ in range(height)]
    x, y = random.randint(0, width-1), random.randint(0, height-1)
    squares = 0
    percentage = int(width * height * .66)

    while squares < percentage:
        if temp[y][x] == -1:
            temp[y][x] = 1
            squares += 1
        x, y = random.randint(x-1, x+1), random.randint(y-1, y+1)
        x, y = max(0, min(x, width-1)), max(0, min(y, height-1))

    final = copy.deepcopy(temp)

    # remove single water tiles
    for i in range(height):
        for j in range(width):
            val = 0
            if temp[i][j] == 0:
                for ii in range(-1, 2):
                    for jj in range(-1, 2):
                        try:
                            if temp[i+ii][j+jj] == 1:
                                val += 1
                        except IndexError:
                            pass
                if val >= 7:
                    final[i][j] = 1

    t.clear()
    for i in range(height):
        for j in range(width):
            t.puts(j, i, "#" if final[i][j] else "")
    t.refresh()

    code = t.read()
    while code != t.TK_ESCAPE:
        if code == t.TK_P:
            if not os.path.exists("./maps"):
                os.mkdir("./maps")
            with open("./maps/dwalk_{}.txt".format(seed), 'w') as f:
                for h in temp:
                    f.write("".join(['#' if t else ' ' for t in h])+'\n')
            print("written to disk")
            break

        elif code == t.TK_R:
            reverse *= -1
            t.clear()
            for i in range(height):
                for j in range(width):
                    if reverse > 0:
                        t.puts(j, i, " " if final[i][j] else "#")
                    else:
                        t.puts(j, i, "#" if final[i][j] else " ")
            t.refresh()

        if code in (t.TK_SPACE, t.TK_B):
            break

        code = t.read()

    if code == t.TK_ESCAPE:
        break

    elif code == t.TK_B:
        world = final
        break

if world:
    exempt = (127, 191, 247, 239, 223, 254, 253, 251)
    removes = (1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 16, 17, 18, 20, 21, 24, 32, 33, 34, 35, 36, 38, 
        40, 42, 48, 50, 51, 54, 64, 65, 66, 68, 69, 72, 80, 81, 84, 85, 96, 98, 99, 
        102, 127, 128, 129, 132, 136, 137, 138, 140, 141, 144, 148, 152, 153, 160, 164, 168, 170, 192, 
        200, 204, 216)
    values = {
        (-1, -1): 1,
        (-1,  0): 2,
        (-1,  1): 4,
        ( 0, -1): 128,
        ( 0,  1): 8,
        ( 1, -1): 64,
        ( 1,  0): 32,
        ( 1,  1): 16,
    }
    # reverses the world if reverse is true
    if reverse > 0:
        for i in range(height):
            for j in range(width):
                if world[i][j] == 1:
                    world[i][j] = -1
                else:
                    world[i][j] = 1

    # first pass to differentiate land and water
    # Adds bit values to the world 
    temp = copy.deepcopy(world)
    for i in range(height):
        for j in range(width):
            num = 0
            val = 0
            if temp[i][j] == 1:
                for ii in range(-1, 2): 
                    for jj in range(-1, 2):
                        if (ii, jj) != (0, 0):
                            try:
                                if temp[i+ii][j+jj] == 1:
                                    val += values[(ii, jj)]
                            except IndexError:
                                val += values[(ii, jj)]
                if val not in removes:
                    world[i][j] = val

                # else:
                #     world[i][j] = 0
            # considered water
            else:
                for ii in range(-1, 2):
                    for jj in range(-1, 2):
                        if (ii, jj) != (0, 0):
                            try:
                                val += temp[i+ii][j+jj]
                            except IndexError:
                                pass

                # all tiles around center tile is water
                # so make it into a deep water tile
                if val <= 100:
                    world[i][j] = -1
                # elif num == 6:


    # # second pass -- creates forest and really deep water
    # temp = copy.deepcopy(world)
    # for i in range(height):
    #     for j in range(width):
    #         num = 0
    #         val = 0
    #         if temp[i][j] == 255:
    #             for ii in range(-2, 3): 
    #                 for jj in range(-2, 3):
    #                     if (ii, jj) != (0, 0):
    #                         try:
    #                             if temp[i+ii][j+jj] == 255:
    #                                 val += 1
    #                             num += 1
    #                         except IndexError:
    #                             pass
                
    #             # surrounded by alot of really high features
    #             if val >= num:
    #                 world[i][j] = 256  

    #         # deep water
    #         if temp[i][j] == -1:
    #             for ii in range(-3, 4):
    #                 for jj in range(-3, 4):
    #                     if (ii, jj) != (0, 0):
    #                         try:
    #                             if temp[i+ii][j+jj] == -1:
    #                                 val += 1
    #                             num += 1
    #                         except IndexError:
    #                             pass
    #             if val == num:
    #                 world[i][j] = -2

    # # third pass adds mountains
    # temp = copy.deepcopy(world)
    # for i in range(height):
    #     for j in range(width):
    #         num = 0
    #         val = 0
    #         if temp[i][j] >= 255:
    #             for ii in range(-5, 6): 
    #                 for jj in range(-5, 6):
    #                     if (ii, jj) != (0, 0):
    #                         try:
    #                             if temp[i+ii][j+jj] == 256:
    #                                 val += 1
    #                             num += 1
    #                         except IndexError:
    #                             pass
    #             if val == num:
    #                 world[i][j] = 257

    # blend them all together:
    # temp = copy.deepcopy(world)
    # for i in range(height):
    #     for j in range(width):
    #         num = 0
    #         val = 0
    #         if temp[i][j] >= 255:
    #             for ii in range(-1, 2):
    #                 for jj in range(-1, 2):
    #                     try:
    #                         val += temp[i+ii][j+jj]
    #                         num += 1
    #                     except:
    #                         pass
    #             world[i][j] = val//num


    t.clear()
    '''
    # colors
    #c2b280 # sand
    #1e932d # light green
    #4da83b # dark green
    #14351a # forest green
    #05267b # deep ocean
    #1e3f7b # dark blue
    #40a4df # light blue
    '''
    # for i in range(height*2//3, height):
    #     print(1.0-(i/height/3), i/(height)/3)

    for i in range(height):
        for j in range(width):
            if world[i][j] in exempt:
                    char = "[c=#f4c875]#[/c]" 
            elif world[i][j] > 0:
                if world[i][j] == 257:
                    char = "[c=#c0c0c0]^[/c]"
                elif world[i][j] == 256:
                    if i < height*2//3:
                        char = "[c=#14351a]#[/c]"  
                    elif height*2//3 <= i < height:
                        char = "[c={}]#[/c]".format(random.choices(['#14351a', '#f4c875'], weights=[1.0-(i/(height)), i/(height)], k=1)[0])
                elif world[i][j] == 255:
                    if i < height*2//3:
                        char = "[c=#1e932d]#[/c]"
                    else:
                        char = "[c=#f4c875]#[/c]" 
                else:
                    char = "[c=#c2b280]#[/c]"
            else:
                if world[i][j] == 0:
                    char = "[c=#05267b]=[/c]"

                elif world[i][j] == -1:
                    char = "[c=#40a4df]=[/c]"
                else:
                    char = "[c=#1e3f7b]=[/c]"

            t.puts(j, i, char)
    t.refresh()
    
    code = t.read()
    while code in (t.TK_MOUSE_MOVE, t.TK_SHIFT, t.TK_ALT, t.TK_MOUSE_SCROLL):
        code = t.read()

    while True:
        if code == t.TK_R:
            t.clear()
            for i in range(height):
                for j in range(width):
                    t.puts(j, i, "#" if temp[i][j] else " ")
            t.refresh()
        
        elif code == t.TK_B:
            t.clear()
            for i in range(height):
                for j in range(width):
                    if world[i][j] in exempt:
                        char = "[c=#82d435]#[/c]"
                    elif world[i][j] > 0:
                        if world[i][j] == 257:
                            char = "[c=#c0c0c0]^[/c]"
                        elif world[i][j] == 256:
                            char = "[c=#14351a]#[/c]"  
                        elif world[i][j] == 255:
                            char = "[c=#1e932d]#[/c]"
                        else:
                            char = "[c=#c2b280]#[/c]"
                    else:
                        if world[i][j] == 0:
                            char = "[c=#40a4df]=[/c]"
                        elif world[i][j] == -1:
                            char = "[c=#1e3f7b]=[/c]"
                        else:
                            char = "[c=#05267b]=[/c]"
                    t.puts(j, i, char)
            t.refresh()

        elif code == t.TK_MOUSE_LEFT:
            print(t.state(t.TK_MOUSE_Y), t.state(t.TK_MOUSE_X), world[t.state(t.TK_MOUSE_Y)][t.state(t.TK_MOUSE_X)])

        else:
            break
        code = t.read()
        while code in (t.TK_MOUSE_MOVE, t.TK_SHIFT, t.TK_ALT, t.TK_MOUSE_SCROLL):
            code = t.read()