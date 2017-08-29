import tdl
from imports import *

WHITE = (250, 250, 250)


def array2D(x, y, v=0):
    return [[v for j in range(y)] for i in range(x)]


def tileInt(x): return x-257


def addTwo(x, y): return x+y


def subTwo(x, y): return max(x-y, 0)


def build(x, y):
    start = 16 * 16 + 2
    end = 16 * 16 + 6
    choices = [x for x in range(start, end+1)]
    world = array2D(x, y, 0)
    color = array2D(x, y, (0, 0, 0))
    for i in range(9):
        world[i][0] = random.choice(choices)
        #world[i][0] = choices[i]
        color[i][0] = (random.randint(50, 150) + i * 5,
                       random.randint(50, 150) + i * 5,
                       random.randint(50, 150) + i * 5)
    boxes = [rows[0] for rows in world[0:i+1]]
    total = sum([tileInt(x) for x in boxes])

    # plus or minus sign
    world[i+1][0] = random.choice([16*2+11, 16*2+13])
    color[i+1][0] = WHITE

    # modifier dice
    world[i+2][0] = random.choice(choices)
    color[i+2][0] = WHITE

    # left parenthesis
    world[i+3][0] = 16*2+8
    color[i+3][0] = WHITE

    # number check to format digits
    if total > 9:
        ones = total % 10
        tens = total // 10

        # tens
        world[i+4][0] = 16 * 3 + tens
        color[i+4][0] = WHITE

        # ones
        world[i+5][0] = 16 * 3 + ones
        color[i+5][0] = WHITE

        # plus or minus sign reflection
        world[i+6][0] = world[i+1][0]
        color[i+6][0] = WHITE
        # the modifier dice
        world[i+7][0] = 16 * 3 + tileInt(world[i+2][0])
        color[i+7][0] = WHITE

        # the close parenthesis
        world[i+8][0] = 16 * 2 + 9
        color[i+8][0] = WHITE

        # equal sign
        world[i+9][0] = 16 * 3 + 13
        color[i+9][0] = WHITE
        total = subTwo(total, tileInt(world[i+2][0])) if world[i+1][
                       0] == 16 * 2 + 13 else addTwo(total, tileInt(world[i+2][0]))

        if total > 9:
            ones = total % 10
            tens = total // 10
            world[i+10][0] = 16 * 3 + tens
            color[i+10][0] = WHITE
            world[i+11][0] = 16 * 3 + ones
            color[i+11][0] = WHITE
        else:
            world[i+10][0] = 16 * 3 + total
            color[i+10][0] = WHITE
    else:
        # ones
        world[i+4][0] = 16 * 3 + total
        color[i+4][0] = WHITE

        # plus or minus sign
        world[i+5][0] = world[i+1][0]
        color[i+5][0] = WHITE
        world[i+6][0] = 16 * 3 + tileInt(world[i+2][0])
        color[i+6][0] = WHITE
        world[i+7][0] = 16*2+9
        color[i+7][0] = WHITE
        world[i+8][0] = 16*3+13
        color[i+8][0] = WHITE
        total = subTwo(total, tileInt(world[i+2][0])) if world[i+1][
                       0] == 16 * 2 + 13 else addTwo(total, tileInt(world[i+2][0]))
        if total > 9:
            ones = total % 10
            tens = total // 10
            world[i+9][0] = 16 * 3 + tens
            world[i+10][0] = 16 * 3 + ones
            color[i+9][0] = WHITE
            color[i+9][0] = WHITE
            world[i+11][0] = 16 * 2 + 9
            color[i+9][0] = WHITE
        else:
            world[i+9][0] = 16 * 3 + total
            color[i+9][0] = WHITE
            world[i+10][0] = 16 * 2 + 9
            color[i+10][0] = WHITE
    return world, color

if __name__ == '__main__':
    timer = 0
    print(tileInt(16*16+2))
    W, H = 20, 10
    tdl.setFont('fonts/new16x16_gs_ro.png', greyscale=True)
    cli = tdl.init(W, H, 'cabin')
    w, c = build(W, H)
    while True:
        timer += 1
        cli.clear()
        for i in range(W):
            for j in range(H):
                cli.draw_char(i, j, w[i][j], c[i][j])
        tdl.flush()
        for e in tdl.event.get():
            if "MOUSEUP" in e.type and "LEFT" in e.button:
                print(e)
                w, c = build(W, H)
            if e.type == 'QUIT' or (e.type == 'KEYDOWN' and e.keychar == 'q'):
                print(timer)
                raise SystemExit('Exit Program')
