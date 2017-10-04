import random
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')

from bearlibterminal import terminal as t
from spaceship.setup import setup
from constants import GAME_SCREEN_WIDTH as width
from constants import GAME_SCREEN_HEIGHT as height

setup()

while True:
    seed = random.randint(0, 99999)
    print(seed)
    random.seed(seed)
    world = [[0 for _ in range(width)] for _ in range(height)]
    x, y = random.randint(0, width-1), random.randint(0, height-1)
    squares = 0
    percentage = int(width * height * .6)

    while squares < percentage:
        if world[y][x] == 0:
            world[y][x] = 1
            squares += 1
        x, y = random.randint(x-1, x+1), random.randint(y-1, y+1)
        x, y = max(0, min(x, width-1)), max(0, min(y, height-1))

    t.clear()
    for i in range(height):
        for j in range(width):
            t.puts(j, i, "#" if world[i][j] else "")
    t.refresh()

    code = t.read()
    while code != t.TK_ESCAPE:
        if code == t.TK_P:
            if not os.path.exists("./maps"):
                os.mkdir("./maps")
            with open("./maps/dwalk_{}.txt".format(seed), 'w') as f:
                for h in world:
                    f.write("".join(['#' if t else ' ' for t in h])+'\n')
            print("written to disk")
            break

        elif code == t.TK_R:
            t.clear()
            for i in range(height):
                for j in range(width):
                    t.puts(j, i, " " if world[i][j] else "#")
            t.refresh()

        elif code == t.TK_N:
            t.clear()
            for i in range(height):
                for j in range(width):
                    t.puts(j, i, "#" if world[i][j] else " ")
            t.refresh()

        if code == t.TK_SPACE:
            break

        code = t.read()

    if code == t.TK_ESCAPE:
        break

