# coding=utf-8
import random
from bearlibterminal import terminal as term
from collections import namedtuple
from ctypes import c_uint32, addressof
from namedlist import namedlist
from time import time
from sprite import Sprite

def test():
    term.set("U+E000: ./assets/bottle_gray.png")

    win_width = 80
    win_height = 24

    font_width = 8
    font_height = 16

    total_pixels_width = win_width * font_width
    total_pixels_height = win_height * font_height

    img_width = 32
    img_height = 32

    total_sprites = total_pixels_height * total_pixels_width
    total_sprites = total_sprites//(img_width*img_height)

    print(total_sprites)
    sprites = []
    for i in range(total_pixels_width//img_width):
        for j in range(total_pixels_height//img_height):
            sprites.append(Sprite(
                                images=[57344],
                                positions=[(0,0)],
                                offset=[i*3, j*3]))

    proceed = True
    try:
        while proceed:
            term.clear()
            for sprite in sprites:
                img, px, py, off = sprite.update()
                term.put(px+off[0], py+off[1], img)
            term.refresh()
            while proceed and term.has_input():
                code = term.read()
                if code in (term.TK_ESCAPE,):
                    term.clear()
                    term.put(0, 1, 'Really Quit? (Y/N)')
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