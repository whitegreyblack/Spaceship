from bearlibterminal import terminal as term
from maps import MAPS
from functools import lru_cache
from random import randint, choice
from time import sleep
from math import sqrt, hypot

def hexify(x):
    """Returns a single hex transformed value as a string"""
    return hex(x).split('x')[1] if x > 15 else '0'+hex(x).split('x')[1]

def hextup(x):
    """Returns a triple hex valued tuple as a string"""
    return hexify(x//randint(5,x//5))+hexify(x//randint(2,3))+hexify(x//randint(5,x//5))

def hexval(x):
    """Returns a valid ARGB hexidecimal value used as a color"""
    return "#ff"+hextup(x)

def rev_hex(x):
    """Reverses the hex value used in hexify"""
    return int(x, 16)

def dimensions(data):
    '''takes in a string map and returns a 2D list map and map dimensions'''
    data = [[col for col in row] for row in data.split('\n')]
    height = len(data)
    width = max(len(col) for col in data)
    return data, height, width

def grass(w, h):
    @lru_cache(maxsize=None)
    def distance(x, y):
        return int(hypot(x, y))
    
    @lru_cache(maxsize=None)
    def mm(x):
        return min(max(50, x), 250) 
    
    @lru_cache(maxsize=None)
    def calculate(g, v):
        return mm(g-v)
    
    @lru_cache(maxsize=None)
    def interpolate(x, y):
        return (x+y)//2

    def replace(x, y, i, j):
        _, og, _, _ = data[j][i]
        ng = calculate(og, distance(abs(x-i), abs(y-j) * factor))
        data[j][i] = (choice([",",";"]), ng if og > ng else interpolate(ng, og), i, j)

    def draw(x, y):
        i, j = x, y
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
                if randint(0, chance) == 1:
                    i -= 1
                    replace(x, y, i, j)
                if randint(0, chance) == 1:
                    i += 1     
                    replace(x, y, i, j)        
                if randint(0, chance) == 1:
                    j += 1  
                    replace(x, y, i, j)      
                if randint(0, chance) == 1:
                    j -= 1  
                    replace(x, y, i, j)      
 
                if randint(0, chance) == 1:
                    i, j = i-1, j-1
                    replace(x, y, i, j)      

                if randint(0, chance) == 1:
                    i, j = i-1, j+1
                    replace(x, y, i, j)      

                if randint(0, chance) == 1:
                    i, j = i+1, j-1
                    replace(x, y, i, j)      

                if randint(0, chance) == 1:
                    i, j = i+1, j+1
                    replace(x, y, i, j)      
            except IndexError:
                pass

    factor = 5
    chance = 8

    data = [[(".", 200, i, j) for i in range(w)] for j in range(h)]

    for k in range(50): 
        draw(
            randint(0, w), 
            randint(0, h))

    lines = []
    characters = {}

    for row in data:
        line = ""
        for c, _, _, _ in row:
            try:
                characters[c] += 1
            except KeyError:
                characters[c] = 1
            line += c
        lines.append(line)

    print("\n".join(lines))
    print(characters)
    return data

if __name__ == "__main__":
    e = hexify
    term.open()
    _, h, w = dimensions(MAPS.TOWN)
    grass(w, h)
    lines = []
    for row in grass(w, h):
        line = ""
        for ch, g, x, y in row:
            line += ch
            term.puts(x, y, f'[color={hexval(g)}]{ch}[/color]')
        lines.append(line)
    print("\n".join(lines))
    term.refresh()
    term.read()
    term.close()
