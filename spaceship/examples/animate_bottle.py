# coding=utf-8
import random
from bearlibterminal import terminal as term
from collections import namedtuple
from namedlist import namedlist

movement_costs = {
    term.TK_LEFT: (-1, 0),
    term.TK_RIGHT: (1, 0),
    term.TK_DOWN: (0, 1),
    term.TK_UP: (0, -1),
}
sprite_list = namedlist( 'Sprite_List', [
                                         ('sprites', []),
                                         ('positions', []),
                                        ])
sprite = namedlist('Sprite', [
                              ('images', []),
                              ('positions', []),
                              ('image', 0),
                              ('position', 0),
                              ('frame', 0),
                              ('frames', 8),
                              ('speed', 0),
                              ('delay', 0),
                              ('offsets', [0, 0])
                             ])
font_width = 8
font_height = 16
block_cost = 16

def convert(images, positions):
    '''returns a sprite objec'''
    return sprite(images=images, positions=positions)

def make_bottle(): return sprite(images=[57344], positions=[(0,0), (0,-1), (0,-2), (0,-1), (0, 0), (0, 1), (0, 2), (0, 1)], frame=random.randint(0, 7))
def make_shield(): return sprite(images=[57345], positions=[(0,0)])
def make_boots(): return sprite(images=[57346], positions=[(0,0), (0,-1), (0,-2), (0,-1), (0, 0), (0, 1), (0, 2), (0, 1)], frame=random.randint(0,7))

def random_position(width, height, dx, dy):
    return namedtuple('Position', [('x', random.randint(0, width//dx-dx)), ('y', random.randint(0, height//dy-dy))])

def test_sprite():
    term.set("U+E000: ./assets/bottle_gray_black_01.png, resize=32x32")
    term.set("U+E001: ./assets/shield.png, resize=32x32")
    term.set("U+E002: ./assets/boots.png, resize=32x32")
    term.set("U+E003: ./assets/border.png, resize=64x64")

    # [57344, 57345, 57346, 57345,]
    bottles = sprite_list(
        sprites=[make_boots(), make_bottle()],
        positions=[(38, 6), (42, 6)])

    print(len(bottles))
    bottles.sprites.append(make_boots())
    bottles.positions.append((10, 10))
    print(len(bottles))
    term.clear()
    term.put(0, 0, 57347)
    for index in range(len(bottles)):
        bottle = bottles.sprites[index]
        x, y = bottles.positions[index]
        print(bottle, (x, y))
        term.put(x, y, bottle.images[bottle.image])
    term.refresh()
    proceed = True
    dx = 0
    try:
        while proceed:
            term.clear()
            term.put(0, 0, 57347)

            for index in range(len(bottles)):
                term.layer(index)
                bottle = bottles.sprites[index]
                x, y = bottles.positions[index]
                bottle.frame += 1
                if bottle.frame > bottle.frames:
                    bottle.frame = 0
                    bottle.image += 1
                    bottle.position += 1
                    if bottle.image > len(bottle.images)-1:
                        bottle.image = 0
                    if bottle.position > len(bottle.positions)-1:
                        bottle.position = 0
                dx, dy = bottle.positions[bottle.position]
                term.put_ext(x, y, dx, dy, bottle.images[bottle.image])
                
            while proceed and term.has_input():
                code = term.read()
                if code in (term.TK_ESCAPE,):
                    term.clear()
                    term.puts(0, 1, 'Really Quit? (Y/N)')
                    term.refresh()
                    code = term.read()
                    if code in (term.TK_Y, ):
                        proceed = False
                elif code in (term.
                TK_CLOSE,):
                    proceed = False
                    # proceed = False
                elif code in (term.TK_UP, term.TK_DOWN, term.TK_LEFT, term.TK_RIGHT,):
                    term.puts(0,6, 'Movement Event')
                    mx, my = movement_costs[code]
                    bottle.offsets[0] += mx * block_cost
                    bottle.offsets[1] += my * block_cost
                elif code not in (term.TK_CLOSE, term.TK_ESCAPE):
                    term.puts(0,5, 'Event happened')
            term.refresh()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    term.open()
    term.set("window: size=80x25, title='Animation Test'")
    test_sprite()
    term.close
