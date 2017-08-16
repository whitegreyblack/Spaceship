import sys
import tdl
from imports import *

def build(x, y):
    space = 8
    dx, dy = x/space, y/space
    for i in range(x):
        for j in range(y):
            pass

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit("Incorrect Args")
    tdl.setFont(sys.argv[1])
    W, H = 32*8, 8*8
    cli = tdl.init(W,H,'fontviewer')
    win = tdl.Window(cli, 0, 0, 32, 8)
    r = build(W,H)
    while True:
        cli.clear()
        for i in range(32):
            for j in range(8):
                cli.draw_char(i,j+32,32*j+i)
        win.draw_str(0, 5, 'Samuel | Raltdk')
        tdl.flush()
        for e in tdl.event.get():
            if e.type=='QUIT' or (e.type=='KEYDOWN' and e.keychar=='q'):
                raise SystemExit('Exit Program')
