# coding=utf-8
import random
from bearlibterminal import terminal as term
from collections import namedtuple
from ctypes import c_uint32, addressof
from namedlist import namedlist
from time import time, sleep
from sprite import Sprite

def test():
    term.set("U+E000: ./assets/bottle_gray.png")
    term.set("U+E001: ./assets/block.png, resize=32x32")

    win_width = 80
    win_height = 24

    font_width = 8
    font_height = 16

    img_width = 32
    img_height = 32

    img_offset_width = 4
    img_offset_height = 2

    total_pixels_width = win_width * font_width
    total_pixels_height = win_height * font_height

    total_sprites = total_pixels_height * total_pixels_width
    total_sprites = total_sprites // (img_width * img_height)

    print(total_sprites)
    sprites = []
    space = False
    print(total_pixels_width//img_width, total_pixels_height//img_height)
    for i in range(total_pixels_width//img_width):
        for j in range(total_pixels_height//img_height):
            if space:
                sprites.append(Sprite(images=[57345], positions=[(i*4,j*2)], offset=[0, 0]))
                space = False
            else:
                space = True
    
    # sprites.append(Sprite(images=[57345],  positions=[(0,0)], offset=[0, 0]))
    # sprites.append(Sprite(images=[57345],  positions=[(4,2)], offset=[0, 0]))
    proceed = True
    try:
        while proceed:
            term.clear()
            for sprite in sprites:
                img, px, py, off = sprite.update()
                term.put(px, py, img)
                term.refresh()
            while proceed and term.has_input():
                code = term.read()
                if code in (term.TK_ESCAPE,):
                    term.clear()
                    term.puts(0, 1, 'Really Quit? (Y/N)')
                    term.refresh()
                    code = term.read()
                    if code in (term.TK_Y, ):
                        proceed = False
                elif code in (term.TK_CLOSE,):
                    proceed = False
                    # proceed = False
                elif code not in (term.TK_CLOSE, term.TK_ESCAPE):
                    term.puts(0,5, 'Event happened')
    except KeyboardInterrupt:
        pass
                

if __name__ == "__main__":
    term.open()
    term.set("window: size=80x24, title='Animation Test'")
    test()
    term.close()