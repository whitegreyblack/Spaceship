import tdl
from imports import * 
from shapes import *

def generate(x, y, l):
    def randpt():
        return (random.randint(0, x-1), random.randint(0,y-1))
    yoffset = H//2
    r = [[' ' for j in range(y)] for i in range(x)]
    xoffset = 16
    boxes = []
    width = 0
    scale = 4
    xscale, yscale=2,2
    while xoffset < len(r)-16:
        if len(r)-xoffset-4 < 16:
            break
        width = random.randint(1,2)*xscale*scale
        height = random.randint(1,2)*yscale*scale
        print(width, height)
        for i in range(width):
            for j in range(height):
                try:
                    r[xoffset+i][yoffset+j] = "."
                except:
                    pass
        jump = random.randint(0, 1)
        if jump:
            for i in range(width):
                pass
        boxes.append((width,height, xoffset, width*(height*2)))
        xoffset += width + height
    woffset = 2
    wx, wy, wo, wv = boxes[random.randint(0, len(boxes)-1)]
    ww = random.randint(2,(wx-4)/4)*4
    wh = random.randint(20-wy, 20+wy//2)
    print('WW,WH',ww, wh)
    for i in range(ww):
        for j in range(wh):
            r[woffset+i+wo][yoffset+wy+j] = '.'
    # mirror on x axis
    for i in range(x):
        for j in range(y//2):
            r[i][j] = r[i][y-1-j]

    return r

def populate(x, y, l):
    r = [[0 for j in range(y+1)] for i in range(x+1)]
    rmin, rmax = 6, 18
    
    while l > 0:
        rx, ry = random.randint(0,(x/5-3)*5), random.randint(0,(y/5-3)*5)
        print(rx, ry)
        dx, dy = random.randint(1,3)*5+1, random.randint(1, 3)*5+1
        print(dx, dy)
        for i in range(dx):
            for j in range(dy):
                r[rx+i][ry+j] = 1
        l -= 1
    return r
def split(m, n):
    return (m-1)/n

def chessboard(x, y):
    r = [[0 for j in range(y)] for i in range(x)]
    xo = 1
    for i in range((x-1)/4):
        yo = 1
        for j in range((y-1)/4):
            for k in range(3):
                for l in range(3):
                    r[i*3+k+i+1][j*3+l+j+1] = 1
            yo += 1
        xo += 4
    return r
def chess(x, y):
    pass
def chess2(x, y):
    r = [[0 for j in range(y)] for i in range(x)]
    print(split(x, 7), split(y, 4))
    xo = 1
    for i in range(split(x, 7)):
        yo = 1
        for j in range(split(y, 4)):
            for k in range(6):
                for l in range(3):
                    r[i*6+k+i+1][j*3+l+j+1] = 1
            yo += 1
        xo += 7
    return r
def roomify(r):
    xo = 2
    #for i in range(split(len(r),4)):
    #    for j in range(split(len(r[0]),4)):
    #        for k in range(len(r)-4):
    #            r[k][j+1] = 1
    return r
if __name__ == "__main__":
    W, H = 161, 40
    if W % 7 != 0 or H % 4 != 0:
        exit('Not divisible by Room Dims')
    tdl.setFont('fonts/4x6.png')
    #tdl.setFont('fonts/terminal8x8_gs_ro.png')
    cli = tdl.init(W+1,H+1,'rooms')
    rooms = roomify(chess2(W+1, H+1))
    prv = None
    while True:
        cli.clear()
        for i in range(len(rooms)):
            for j in range(len(rooms[0])):
                cli.draw_char(i, j, '.' if rooms[i][j] > 0 else '#')
        tdl.flush()
        for e in tdl.event.get():
            if e.type == 'QUIT' or (e.type=='KEYDOWN' and e.keychar=='q'):
                raise SystemExit('Exit Program')
