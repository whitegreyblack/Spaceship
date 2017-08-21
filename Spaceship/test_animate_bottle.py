# coding=utf-8

from bearlibterminal import terminal as term
from ctypes import c_uint32, addressof
from namedlist import namedlist
from time import time

sprite = namedlist('Sprite', ['images', ('image', 0), ('frame', 0), ('frames', 15)])

def test_sprite():
    term.set("U+E000: ./assets/bottle_gray_01.png")
    term.set("U+E001: ./assets/bottle_gray_02.png")
    term.set("U+E002: ./assets/bottle_gray_03.png")
    bottle = sprite(images=[57344, 57345, 57346, 57345,],)
    print(bottle)
    term.clear()
    term.put(0, 1, bottle.images[bottle.image])
    term.refresh()
    proceed = True
    try:
        while proceed:
            bottle.frame += 1
            if bottle.frame > bottle.frames:
                bottle.frame = 0
                bottle.image += 1
                if bottle.image > len(bottle.images)-1:
                    bottle.image = 0
            term.clear()
            term.puts(0, 0, 'Animating a bottle\n')
            term.put(0, 1, bottle.images[bottle.image])
            term.puts(0, 4, 'Text under bottle\n')
            while proceed and term.has_input():
                term.puts(0, 5, 'Got input')
                code = term.read()
                if code in (term.TK_ESCAPE, term.TK_CLOSE):
                    term.clear()
                    term.puts(0, 1, 'Really Quit? (Y/N)')
                    term.refresh()
                    code = term.read()
                    if code in (term.TK_Y, ):
                        proceed = False
                    # proceed = False
                if term.TK_EVENT:
                    term.puts(0,5, 'Event happened')
            term.refresh()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    term.open()
    term.set("window: size=80x25, title='Animation Test'")
    test_sprite()
    term.close