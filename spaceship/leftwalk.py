import tdl
from imports import *

def walk(x, y):
    pass


if __name__ == '__main__':
    W, H = 80, 40
    tdl.setFont('fonts/4x6.png')
    cli = tdl.init(W,H,'Walk')
    while True:
        cli.clear()
        tdl.flush()
        for e in tdl.event.get():
            if e.type == 'QUIT' or (e.type=='KEYDOWN' and e.keychar=='q'):
                raise SystemExit('Exit Program')
