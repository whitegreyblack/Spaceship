# -*- coding=utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.action import num_movement
from bearlibterminal import terminal as term
from PIL import Image, ImageDraw
from functools import lru_cache
from random import randint, choice
from spaceship.tools import bresenhams
from math import hypot
from copy import deepcopy
from textwrap import wrap
"""Maps file holds template functions that return randomized data maps used\
in creating procedural worlds"""

# Key-value pairs are mapped from characters to color tuples
picturfy_chars = {
    "#": (0,0,0),
    "%": (136, 0, 21),
    "o": (255, 242, 0),
    ",": (34, 177, 76),
    "+": (185, 122, 87),
    "~": (112, 146, 190),
    ".": (127, 127, 127),
    ".": (255, 255, 255),
    ":": (195, 195, 195),
}

# Key-Value pairs are tuples to tuple pertaining to color and character mapping
stringify_chars = { 
    (0, 0, 0): "#",
    (136, 0, 21): "%",
    (255, 242, 0): "o",
    (34, 177, 76): ",",
    (185, 122, 87): "+",
    (127, 127, 127): ".",
    (112, 146, 190): "~",
    (255, 255, 255): ".",
    (195, 195, 195): ":",
}

unicode_blocks_thin = {
    0: "25D9",
    1: "25D9",
    2: "25D9",
    #3: "255A",
    3: "25D9",
    4: "25D9",
    5: "2551",
    #6: "2554",
    6: "25D9",
    7: "2560",
    8: "25D9",
#   9: "255D",
    9: "25D9",
    10: "2550",
    11: "2569",
#   12: "2557",
    12: "25D9",
    13: "2562",
    14: "2566",
    15: "256C",
}

def toInt(hexval):
    return int(hexval, 16)

def picturfy(string, filename="picturfy-img.png", folder="./", debug=False):
    """Takes in a list of string lists and three positional parameters.
    Filename and folder are used to determine the output path after 
    function execution. Debug is used to print testing and terminal
    output. The inverse function to stringify and asciify"""

    mapping = string.split('\n')
    h, w = len(mapping), len(mapping[0])
    img_to_save = Image.new('RGB', (w, h))
    drawer = ImageDraw.Draw(img_to_save)

    for j in range(h):
        string_list = list(mapping[j])
        for i in range(len(string_list)):
            drawer.rectangle((i, j, i+1, j+1), picturfy_chars[string_list[i]])

    print("Saving string as {}".format(folder+filename))
    img_to_save.save(folder+filename)
    return folder+filename


def stringify(string, debug=False):
    """Takes in a file location string and a bool for debug
    to determine output. Sister function to asciify. Uses 
    only keyboard accessible characters in the map."""

    lines = []
    colors = set()

    with Image.open(string) as img:
        pixels = img.load()
        w, h = img.size

    for j in range(h):
        line = ""
        for i in range(w):
            # sometimes alpha channel is included so test for all values first
            try:
                r, g, b, _ = pixels[i, j]
            except ValueError:
                r, g, b = pixels[i, j]
            if (r, g, b) not in colors:
                colors.add((r, g, b))
            try:
                line += stringify_chars[(r, g, b)]
            except KeyError:
                print((r, g, b))
        lines.append(line)

    if debug:
        print("\n".join(lines))
        print(colors)

    return "\n".join(lines)

def asciify(string, debug=False):
    """Takes in a file location string and a debug parameter
    to determine output. Sister function to stringify. Uses
    unicode characters provided they are available in blt."""
    array = []
    colors = set()
    with Image.open(string) as img:
        pixels = img.load()
        w, h = img.size
    
    # first pass -- evaluates and transforms colors into string characters
    # second pass -- evaluates and transforms ascii characters into unicode
    for j in range(h):
        column = []
        for i in range(w):
            try:
                r, g, b, _ = pixels[i, j]
            except ValueError:
                r, g, b = pixels[i, j]
            if (r, g, b) not in colors:
                colors.add((r,g,b))
            try:
                column.append(stringify_chars[(r, g, b)])
            except KeyError:
                print((r, g, b))
        array.append(column)

    if debug:
        for i in range(h):
            print("".join(array[i]))
        print(colors)

    # return evaluate_block(lines, w, h)

    # returns a 2D array/map
    return array

def evaluate_blocks(data, w, h, array=False):
    """Helper function for asciify which returns the same sized map
    but with the indices holding unicode character codes"""
    def evalValue(x, y):
        bit_value=0
        increment=1
        debug=11
        for i, j in ((0,-1), (1,0), (0,1), (-1, 0)):
                try:
                    char = data[y+j][x+i]
                except IndexError:
                    char = ""
                if char in ("#", "o", "+"):
                    bit_value += increment
                increment *= 2
        return bit_value

    unicodes = deepcopy(data)
    for i in range(h):
        for j in range(w):
            if data[i][j] == "#":
                unicodes[i][j] = toInt(unicode_blocks_thin[evalValue(j, i)])
    return unicodes

def table(ch, val, x, y):
    """Returns a 2d list of lists holding a four element tuple"""
    return [[(ch, val, i, j) for i in range(x)] for j in range(y)]


def blender(hex1, hex2, n=10):
    """blender holds color transformation functions
    TODO: probably should move this to another file
    Up to user to decide whether color is valid"""
    def splitter(c):
        c = c.replace("#", "")
        if len(c) > 8:
            c = c[2::]
        return wrap(c,2)
    
    def transform(c):
        # for i in c:
        #   integer = int(i, 16)
        return [int(i, 16) for i in c]

    def blend(ca, cb, n, i):
        value = abs(ca-cb)
        value /= n
        value *= i+1
        value = round(value)
        value = hex(min(ca,cb)+value)
        value = value.replace("0x", "")
        #value = hex(((abs(ca-cb)//n))*i).replace("0x", "")
        return value

    def mash(color):
        return "#ff"+"".join(map(lambda x: "0"+str(x) if len(str(x)) < 2 else str(x), color))

    colorA = transform(splitter(hex1))
    colorB = transform(splitter(hex2))
    colorS = [mash(splitter(hex2.replace("#","")))]

    for i in range(n-2):
        color=[]
        for j in range(3):
            color.append(blend(colorA[j], colorB[j], n, i))
        colorS.append(mash(color))
    colorS.append(mash(splitter(hex1.replace("#",""))))
    return colorS

def gradient(hex1, hex2, n):
    pass

def hexify(x):
    """Returns a single hex transformed value as a string"""
    return hex(x).split('x')[1] if x > 15 else '0' + hex(x).split('x')[1]


def hextup(x, a, b, c):
    """Returns a triple hex valued tuple as ARGB hex string"""
    return "#ff" \
        + hexify(x//a) \
        + hexify(x//b) \
        + hexify(x//c)


def hexone(x):
    return "#ff" + hexify(x) * 3


def output(data):
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


def dimensions(data, array=False):
    """Takes in a string map and returns a 2D list map and map dimensions"""
    if not array:
        data = [[col for col in row] for row in data.split('\n')]
    height = len(data)
    width = max(len(col) for col in data)
    return data, height, width

def world(x, y, pos=50, iterations=20):
    """Returns a more realistic world map of size (X, y)
    TODO: Color currently starts at 0 and increments by 1 everytime data is accessed -- more realistic algo?
    """
    def inc(x, y):
        _, i, _, _ = data[y][x]
        data[y][x] = (char, mm(i+1), x, y)

    def double(x, y):
        pairs.add((x,y))
        pairs.add((y,x))

    @lru_cache(maxsize=None)
    def mm(c):
        """Returns the value or predetermined value if out of bounds"""
        return min(max(0, c), 250)
    
    # random integers for picking a random point in quadrant
    quads = {
        0: (0,x//2, 0, y//3),
        1: (x//2+1, x-1, 0, y//2),
        2: (0,x//2, y//2+1, y-1),
        3: (x//2+1, x-1, y//3+1, y-1),
    }
    # explicit midpoint in each quadrant
    quad_pos = {
        0: (x//4, y//4),
        1: (x*3//4, y//4),
        2: (x//4, y*3//4),
        3: (x*3//4, y*3//4)
    }
    rotations = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1), 
    ]
    factor = 5
    chance = 10
    char = "#"
    unch = "."
    w, h = x, y
    data = table(unch, 0, x, y)
    pairs = set()
    for _ in range(10):
        quad_beg, quad_end = 0, 0
        while quad_beg == quad_end:
            quad_beg = randint(0,3)
            quad_end = randint(0,3)
        
        x0, x1, y0, y1 = quads[quad_beg]
        bx, by = randint(x0, x1), randint(y0, y1)

        x0, x1, y0, y1 = quads[quad_end]
        ex, ey = randint(x0, x1), randint(y0, y1)

        points = bresenhams((bx, by), (ex, ey))
        for x, y in points:
            inc(x, y)
            
        for point in range(0,len(points), 3):
            x, y = points[point]
            i, j = x, y
            try:
                inc(i, j)
                for _ in range(iterations):
                    for rot in rotations:
                        if randint(-chance+1, 1):
                            di, dj = rot
                            i -= di
                            j -= dj
                            inc(i, j)
            except IndexError:
                pass

    return data    

def forests(x, y, d, c, p=100, i=100):
    """Returns a list of lists with symbols and color gradient tuple"""

    @lru_cache(maxsize=None)
    def distance(x, y):
        """Returns the hypotenuse distance between two points"""
        return int(hypot(x, y))

    @lru_cache(maxsize=None)
    def mm(g, v):
        """Returns the value or predetermined value if out of bounds"""
        return min(max(50, g-v), 250)

    @lru_cache(maxsize=None)
    def mid(x, y):
        """Returns the midpoint value between two points"""
        return (x+y)//2

    def replace(x, y, i, j):
        """Evaluates the tuple in data and replaces it with a new tuple"""
        _, og, _, _ = data[j][i]
        ng = mm(og, distance(abs(x-i), abs(y-j) * factor))
        data[j][i] = (choice(c), ng if og > ng else mid(ng, og), i, j)

    factor = 3
    chance = 5
    w, h = x, y
    data = table(d, 250, x, y)

    for _ in range(p):
        x, y = randint(0, w), randint(0, h)
        i, j = x, y

        for _ in range(i):
            try:
                if randint(0, 1):
                    i -= 1
                    replace(x, y, i, j)

                if randint(0, 1):
                    i += 1
                    replace(x, y, i, j)

                if randint(0, 1):
                    j += 1
                    replace(x, y, i, j)

                if randint(0, 1):
                    j -= 1
                    replace(x, y, i, j)
        
                if randint(-chance+1, 1):
                    i, j = i-1, j-1
                    replace(x, y, i, j)

                if randint(-chance+1, 1):
                    i, j = i-1, j+1
                    replace(x, y, i, j)

                if randint(-chance+1, 1):
                    i, j = i+1, j-1
                    replace(x, y, i, j)

                if randint(-chance+1, 1):
                    i, j = i+1, j+1
                    replace(x, y, i, j)

            except IndexError:
                pass

    return data


if __name__ == "__main__":
    width = 100
    height = 50
    if len(sys.argv) == 2 and sys.argv[1] == "-t":
        term.open()
        term.set("window: size={}x{}, cellsize={}x{}, title='Maps'".format(
            width, height, 8, 16
        ))
        data = world(width, height, 100, 100)
        output(data)
        for row in data:
            for c, col, i, j in row:
                col = hextup(col, 2, 1, 1) if col > 5 else hextup((col+1)*25, (col+1)*25//2, (col+1)*25//2, col+1)
                term.puts(i, j, "[color={}]{}[/color]".format(col, c))
        term.refresh()
        term.read()
    else:
        output(world(width, height//2, 100, 100))
