# coding=utf-8

from bearlibterminal import terminal as term
from ctypes import c_uint32, addressof
from namedlist import namedlist
from time import time

sprite = namedlist('Sprite', ['images', ('image', 0), ('frame', 0), ('frames', 15)])



'''
class sprite:
    def __init__(self, images):
        self.images=images
        self.index=0
    def update(self):
        self.index+=1
        if self.index > len(self.images):
            self.index = 0
        return self.images[self.index]
'''

def test_sprite():
    term.set("U+E000: ./imgs/dknight1.png")
    term.set("U+E001: ./imgs/dknight2.png")
    term.set("U+E002: ./imgs/dknight3.png")
    knight = sprite(images=[57344, 57345, 57346],)
    print(knight)
    term.clear()
    term.put(0, 1, knight.images[knight.image])
    term.refresh()
    try:
        while True:
            knight.frame += 1
            if knight.frame > knight.frames:
                knight.frame = 0
                knight.image += 1
                if knight.image > len(knight.images)-1:
                    knight.image = 0
            term.clear()
            term.puts(0, 0, 'Animating a knight\n')
            term.put(0, 1, knight.images[knight.image])
            term.puts(0, 5, 'Text under knight\n')
            term.refresh()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    term.open()
    term.set("window: size=80x25, title='Animation Test'")
    test_sprite()
    term.close