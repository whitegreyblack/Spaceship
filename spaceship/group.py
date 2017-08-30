from bearlibterminal import terminal as term
from maps import MAPS
from objects import Map
from functools import lru_cache
from random import randint
from time import sleep
from math import sqrt, hypot
def forest(w, h):
    def draw(x, y):
        i, j = x, y
        for k in range(100):
            n = randint(1,4)
            e = randint(1,4)
            w = randint(1,4)
            s = randint(1,4)
            try:
                if n == 1:
                    i -= 1; data[j][i] = ('T', i, j)
                if s == 1:
                    i += 1
                    data[j][i] = ('T', i, j)
                if e == 1:
                    j += 1
                    data[j][i] = ('T', i, j)
                if w == 1:
                    j -= 1
                    data[j][i] = ('T', i ,j)
            except:
                pass
    data = [[('.', x, y) for x in range(w)] for y in range(h)]
    for i in range(randint(10, 15)):
        x = randint(0,w)
        y = randint(0,h)
        draw(x, y)
    return data  

def hexify(x):
    return hex(x).split('x')[1] if x > 15 else '0'+hex(x).split('x')[1]

def rev_hex(x):
    return int(x, 16)

def stones(w, h):
    @lru_cache(maxsize=None)
    def distance(x, y):
        return int(hypot(x, y))

    def mm(x):
        return min(max(25, x), 250) 

    def calculate(g, v):
        return mm(g-v)

    def interpolate(x, y):
        return (x+y)//2

    def draw(x, y):
        i, j = x, y
        factor = 5
        chance = 8
        for k in range(100):
            n = randint(0, chance)
            e = randint(0, chance)
            w = randint(0, chance)
            s = randint(0, chance)
            nw = randint(0, chance)
            ne = randint(0, chance)
            sw = randint(0, chance)
            se = randint(0, chance)
            try:
                if n == 1:
                    i -= 1
                    _, og, _, _ = data[j][i]
                    ng = calculate(og, distance(abs(x-i), abs(y-j) * factor))
                    data[j][i] = ("#", ng if og > ng else interpolate(ng, og), i, j)                
                if s == 1:
                    i += 1
                    _, og, _, _ = data[j][i]
                    ng = calculate(og, distance(abs(x-i), abs(y-j) * factor))
                    data[j][i] = ("#", ng if og > ng else interpolate(ng, og), i, j)
                if e == 1:
                    j += 1
                    _, og, _, _ = data[j][i]
                    ng = calculate(og, distance(abs(x-i), abs(y-j) * factor))
                    data[j][i] = ("#", ng if og > ng else interpolate(ng, og), i, j)
                if w == 1:
                    j -= 1
                    _, og, _, _ = data[j][i]
                    ng = calculate(og, distance(abs(x-i), abs(y-j) * factor))
                    data[j][i] = ("#", ng if og > ng else interpolate(ng, og), i, j)
                if nw == 1:
                    i -= 1
                    j -= 1
                    _, og, _, _ = data[j][i]
                    ng = calculate(og, distance(abs(x-i), abs(y-j) * factor))
                    data[j][i] = ("#", ng if og > ng else interpolate(ng, og), i, j)
                if ne == 1:
                    i -= 1
                    j += 1
                    _, og, _, _ = data[j][i]
                    ng = calculate(og, distance(abs(x-i), abs(y-j) * factor))
                    data[j][i] = ("#", ng if og > ng else interpolate(ng, og), i, j)
                if sw == 1:
                    i += 1
                    j -= 1
                    _, og, _, _ = data[j][i]
                    ng = calculate(og, distance(abs(x-i), abs(y-j) * factor))
                    data[j][i] = ("#", ng if og > ng else interpolate(ng, og), i, j)
                if se == 1:
                    i += 1
                    j += 1
                    _, og, _, _ = data[j][i]
                    ng = calculate(og, distance(abs(x-i), abs(y-j) * factor))
                    data[j][i] = ("#", ng if og > ng else interpolate(ng, og), i, j)
            except:
                pass
    data = [[(".", 200, x, y) for x in range(w)] for y in range(h)]
    for k in range(50): 
        x = randint(0, w)
        y = randint(0, h)
        draw(x, y)
    return data

if __name__ == "__main__":
    e = hexify
    term.open()
    _, h, w = Map.dimensions(MAPS.TOWN)
    lines = []
    for row in stones(w, h):
        line = ""
        for ch, g, x, y in row:
            line += ch
            term.puts(x, y, f'[color={"#ff"+e(g)*3}]{ch}[/color]')
        lines.append(line)
    print("\n".join(lines))
    term.refresh()
    term.read()
    term.close()
