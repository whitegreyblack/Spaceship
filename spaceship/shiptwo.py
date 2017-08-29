import tdl
from imports import *

def build():
    pass


if __name__ == '__main__':
    W, H = 100, 50
    tdl.setFont('fonts/arial12x12.png')
    cli = tdl.init(W,H,'shiptwo')
    while True:
    cli.clear()
    tdl.flush()
    for e in tdl.event.get():
        if e.type=='QUIT' or (e.type=='KEYDOWN' and e.keychar=='q'):
            raise SystemExit('Exit Program')
