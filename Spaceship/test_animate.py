# coding=utf-8

from bearlibterminal import terminal as term
from ctypes import c_uint32, addressof
from namedlist import namedlist
from time import time

sprite = namedlist('Sprite', [('images', []), ('positions', ()), ('image', 0), ('frame', 0), ('frames', 15)])

def test_sprite():
    term.set("U+E000: ./imgs/dknight1.png")
    term.set("U+E001: ./imgs/dknight2.png")
    term.set("U+E002: ./imgs/dknight3.png")
    knight = sprite(images=[57344, 57345, 57346],)
    print(knight)
    term.clear()
    term.put(0, 1, knight.images[knight.image])
    term.refresh()
    proceed = True
    try:
        while proceed:
            knight.frame += 1
            if term.TK_EVENT:
                term.puts(0,5, 'Event happened')
            if knight.frame > knight.frames:
                knight.frame = 0
                knight.image += 1
                if knight.image > len(knight.images)-1:
                    knight.image = 0
            term.clear()
            term.puts(0, 0, 'Animating a knight\n')
            term.put(0, 1, knight.images[knight.image])
            term.puts(0, 5, 'Text under knight\n')
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
            term.refresh()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    term.open()
    term.set("window: size=80x25, title='Animation Test'")
    test_sprite()
    term.close