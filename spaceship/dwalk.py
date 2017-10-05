import random
import copy
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')

from bearlibterminal import terminal as t
from spaceship.setup import setup
width, height = 40, 25
reverse = -1
world = None
t.open()
t.set('window: size={}x{}, cellsize={}x{}'.format(width, height, 16, 16))
t.set("font: ./fonts/unscii-8.ttf, size=16")
t.set("input.filter={keyboard, mouse}")

while True:
    seed = random.randint(0, 99999)
    print(seed)
    random.seed(seed)
    temp = [[0 for _ in range(width)] for _ in range(height)]
    x, y = random.randint(0, width-1), random.randint(0, height-1)
    squares = 0
    percentage = int(width * height * .66)

    while squares < percentage:
        if temp[y][x] == 0:
            temp[y][x] = 1
            squares += 1
        x, y = random.randint(x-1, x+1), random.randint(y-1, y+1)
        x, y = max(0, min(x, width-1)), max(0, min(y, height-1))

    final = copy.deepcopy(temp)

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
                if val == 8:
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
        40, 42, 48, 50, 64, 65, 66, 68, 69, 72, 80, 81, 84, 85, 96, 98, 
        127, 128, 129, 132, 136, 137, 138, 140, 144, 148, 152, 160, 164, 168, 170, 192, 200)
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

    if reverse > 0:
        for i in range(height):
            for j in range(width):
                if world[i][j] == 1:
                    world[i][j] = 0
                else:
                    world[i][j] = 1
                    
    temp = copy.deepcopy(world)
    flood = copy.deepcopy(world)
    for i in range(height):
        for j in range(width):
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
                else:
                    world[i][j] = 0
    t.clear()
    '''
    # colors
    c2b280 # sand
    1e932d # light green
    4da83b # dark green
    '''
    for i in range(height):
        for j in range(width):
            char = "[c=#82d435]#[/c]" if world[i][j] in exempt \
              else "[c=#c2b280]#[/c]" if world[i][j] != 255 \
              else "[c=#1e932d]#[/c]"
            t.puts(j, i, char if world[i][j] else "[c=#1e3f7b]=[/c]")
    t.refresh()
    
    code = t.read()
    while code in (t.TK_MOUSE_MOVE,):
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
                    char = "[c=#82d435]#[/c]" if world[i][j] in exempt \
                    else "[c=#c2b280]#[/c]" if world[i][j] != 255 \
                    else "[c=#1e932d]#[/c]"
                    t.puts(j, i, char if world[i][j] else "[c=#1e3f7b]=[/c]")
            t.refresh()
        elif code == t.TK_MOUSE_LEFT:
            t.puts(0, height-1, "{}x{}={}".format(t.state(t.TK_MOUSE_X), t.state(t.TK_MOUSE_Y),world[i][j]))
            t.refresh()

        else:
            break
        code = t.read()
        while code in (t.TK_MOUSE_MOVE,):
            code = t.read()