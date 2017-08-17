import tdl
from imports import *
from collections import namedtuple

WHITE = (250, 250, 250)
BLACK = (0, 0, 0)
LGREY = (200, 200, 200)
GREY = (125, 125, 125)
DGREY = (50, 50, 50)
BROWN = (225, 175, 100)
YELLOW = (250, 250, 100)
tile = namedtuple('TILE',['pos','col'])

charMap = {}
charMap['f']=47
charMap['b']=92
charMap['h']=179
charMap['v']=196
charMap['c']=9
charMap['^']=257
charMap['v']=256
charMap['<']=60
charMap['>']=62
print(charMap.keys())

class border:
    stlcorner=218
    strcorner=191
    sblcorner=192
    sbrcorner=217
    svertical=196
    shorizontal=179
def array(x, y):
    choices = [z for z in range(65, 65+27)]
    return [[[random.choice(choices), WHITE] for _ in range(y)] for _ in range(x)]

def build_menu(x, y):
    # indexes by x then y [column major]
    menu_layout = [[0 for _ in range(y)] for _ in range(x)]

    # horizontal lining
    for r in range(y):
        menu_layout[0][r] = border.shorizontal
        menu_layout[x-1][r] = border.shorizontal

    # vertical lining
    for c in range(x):
        menu_layout[c][0] = border.svertical
        menu_layout[c][y-1] = border.svertical

    # corners
    menu_layout[0][0] = border.stlcorner
    menu_layout[x-1][0] = border.strcorner
    menu_layout[0][y-1] = border.sblcorner
    menu_layout[x-1][y-1] = border.sbrcorner
    return menu_layout

def deltanorm(p1, p2):
    dp = int((p2-p1)/abs(p2-p1))
    return dp


def build_line(array, start, stop, color):
    x1, y1 = start
    x2, y2 = stop
    if max(x2, x1) - min(x2, x1) is max(y2, y1) - min(y2, y1):
        dx = deltanorm(x1, x2)
        dy = deltanorm(y1, y2)
        return [(x1+dx*d, y1+dy*d) for d in range(max(x2, x1) - min(x2, x1)+1)]
    return []

def build_background(menu):
    x, y = len(menu)-2, len(menu[0])-2 # decrement by 2 to not overwrite border? or maybe draw background first then border
    points = build_line(menu, (28, 21), (12, 37), WHITE)
    for x, y in points:
        menu[x][y] = charMap['f']
    points = build_line(menu, (44, 37), (28, 53), WHITE)
    for x, y in points:
        menu[x][y] = charMap['f']
    points = build_line(menu, (28, 21), (44, 37), WHITE)
    for x, y in points:
        menu[x][y] = charMap['b']
    points = build_line(menu, (12, 37), (28, 53), WHITE)
    for x, y in points:
        menu[x][y] = charMap['b']
    menu[28][21] = charMap['^']
    menu[28][53] = charMap['v']
    menu[44][37] = charMap['>']
    menu[12][37] = charMap['<']
    return menu

if __name__ == '__main__':
    build_line([], (28, 21), (12, 37), WHITE)
    timer = 0
    W, H = 100, 75
    tdl.setFont('fonts/new8x8_gs_ro.png', greyscale=True)
    cli = tdl.init(W,H,'menu')
    menu = build_background(build_menu(W, H))
    while True:
        timer += 1
        cli.clear()
        for i in range(W):
            for j in range(H):
                cli.draw_char(i, j, menu[i][j], WHITE if not menu[i][j] else WHITE)
        tdl.flush()
        for e in tdl.event.get():
            if "MOUSEUP" in e.type and "LEFT" in e.button:
                print(e)
            if e.type=='QUIT' or (e.type=='KEYDOWN' and e.keychar=='q'):
                print(timer)
                raise SystemExit('Exit Program')
