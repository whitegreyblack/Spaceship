from imports import *
import tdl
class Camera:
    def __init__(self, x, y, dx, dy, lx, ly):
        self.x = x
        self.y = y
        self.w = dx
        self.h = dy
        self.mx = lx
        self.my = ly
    
def movement_handler():
    pass
def exit_handler():
    pass
if __name__ == "__main__":
    CAM_W, CAM_H = 40,20
    MAP_W, MAP_H = 45, 25
    tdl.setFont('fonts/terminal8x8_gs_ro.png', greyscale=True)
    cli = tdl.init(CAM_W,CAM_H, 'scroll')
    world = [[i*j+1 if j==i else 0 for j in range(MAP_H)] for i in range(MAP_W)]
    for i in range(MAP_W):
        world[i][MAP_H-1] = 2
        world[i][0] = 2
    for j in range(MAP_H):
        world[0][j] = 2
        world[MAP_W-1][j]=2
    CAM_X1, CAM_Y1 = 0, 0
    ## 0 <= camy2 < map_w - cam_w
    ## cam_w <= camy2 < map_w
    CAM_X2, CAM_Y2 = CAM_W, CAM_H
    px, py = 0,0
    while True:
        cli.clear()
        for i in range(CAM_W):
            for j in range(CAM_H):
                try:
                    cli.draw_char(i, j, '.' if not world[CAM_X1+i][CAM_Y1+j] else 'o')
                except:
                    print(CAM_X1+i, CAM_Y1+j)
                    exit()
        cli.draw_char(px, py, '@')
        tdl.flush()
        for e in tdl.event.get():
            if e.type=='QUIT' or (e.type=='KEYDOWN' and e.keychar=='q'):
                raise SystemExit('ExitProgram')
            if e.type=='KEYDOWN' and e.keychar=='DOWN':
                in_cam = py+1 < CAM_Y1+CAM_H
                in_map = CAM_Y1+CAM_H-1 < MAP_H
                
            if e.type=='KEYDOWN' and e.keychar=='UP':
                if py > 0:
                    py -= 1
                #if CAM_Y1 > 0:
                #    CAM_Y1 -= 1
                '''
            if e.type=='KEYDOWN' and e.keychar=='LEFT':
                if CAM_X1 > 0:
                    CAM_X1 -= 1
            if e.type=='KEYDOWN' and e.keychar=='RIGHT':
                if CAM_X1+CAM_W < MAP_W:
                    CAM_X1 += 1
                    '''
