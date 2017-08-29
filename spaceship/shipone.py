import tdl
from imports import *
from objects import *
from colors import wall, hatch, floor, other

def build(x, y):
    fc = 3
    bc = 16 * 13+11
    c = [[(0,0,0) for j in range(y)] for i in range(x)]
    s = [['4' for j in range(y)] for i in range(x)]
    r = [
            Rectangle(1,9,9,5),
            Rectangle(9,5,9,9),
            Rectangle(9,13,9,5),
            Rectangle(17,5,9,5),
            Rectangle(17,13,9,5),
            Rectangle(25,1,9,9),
            Rectangle(33,1,9,9),
            Rectangle(25,13,9,9),
            Rectangle(33,13,9,5),
            Rectangle(37,9,9,5),
        ]
    d = [
            Point(9, 11),
            Point(11,13),
            Point(17,15),
            Point(17, 7),
            Point(25,15),
            Point(25, 7),
            Point(33, 3),
            Point(33,15),
            Point(39,13),
            Point(39, 9),
            Point(45,11),
        ]
    cor = []
    for i in range(random.randint(20, 30)):
        ''' some stars '''
        sx, sy = random.randint(0,x-1), random.randint(0,y-1)
        s[sx][sy] = '*'
        c[sx][sy] = (250, 250, 250)
    for room in r:
        ''' flood fill with wall color '''
        for i in range(room.x):
            for j in range(room.y):
                x, y = room.tl.x, room.tl.y
                if i == 0 or i == room.x-1:
                    s[x+i-1][y+j-1] = bc
                if j == 0 or j == room.y-1:
                    s[x+i-1][y+j-1] = bc
                c[x+i-1][y+j-1] = wall
        ''' flood fill inside room with floor color '''
        for i in range(room.x-2):
            for j in range(room.y-2):
                x, y = room.tl.x, room.tl.y
                s[x+i][y+j] = '.'
                c[x+i][y+j] = floor
        ''' add corners to list '''
        cor.extend([room.tl, room.tr, room.bl, room.br])
    cor = list(set(cor))
    for corner in cor:
        ''' modify corners of spaceship '''
        x, y = corner.x, corner.y
        s[x-1][y-1] = bc
        c[x-1][y-1] = wall
    for door in d:
        ''' modify hatches and doors '''
        x, y = door.x, door.y
        s[x-1][y-1] = bc
        c[x-1][y-1] = hatch
    colors = [floor, wall, other, hatch]
    for i in range(4):
        ''' sampling of tiles and colors '''
        s[i][0] = 16*15+15
        c[i][0] = colors[i]
        s[i][1] = fc
        c[i][1] = colors[i]
    return s,c

if __name__ == '__main__':
    W, H = 45, 21
    tdl.setFont('fonts/terminal16x16_gs_ro.png', greyscale=True)
    cli = tdl.init(W,H,'shipone')
    s,c = build(W, H)
    while True:
        cli.clear()
        for i in range(W):
            for j in range(H):
                cli.draw_char(i, j, s[i][j], c[i][j])
        cli.draw_char(9, 11, '@')
        tdl.flush()
        for e in tdl.event.get():
            if e.type=='QUIT' or (e.type=='KEYDOWN' and e.keychar=='q'):
                raise SystemExit('Exit Program')
