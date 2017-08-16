import tdl
from imports import *

def array2D(x, y, v=0):
    return [[0 for j in range(y)] for i in range(x)]

def build(x, y):
    wall_in = 16 * 16
    wall_out = 16 * 16 + 1
    world = array2D(x, y, 0)
    color = array2D(x, y, (0,0,0))
    for i in range(2):
        world[i][0] = random.choice([wall_in, wall_out])
        color[i][0] = (250,250,250)
    return world, color
if __name__ == '__main__':
    W, H = 20, 10
    tdl.setFont('fonts/new16x16_gs_ro.png', greyscale=True)
    cli = tdl.init(W,H,'cabin')
    w, c = build(W,H)
    while True:
	cli.clear()
        for i in range(W):
            for j in range(H):
                cli.draw_char(i, j, w[i][j], c[i][j])
	tdl.flush()
	for e in tdl.event.get():
	    if e.type=='QUIT' or (e.type=='KEYDOWN' and e.keychar=='q'):
	        raise SystemExit('Exit Program')
