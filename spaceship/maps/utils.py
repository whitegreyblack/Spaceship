 # -*- coding=utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../../')
from bearlibterminal import terminal as term
from PIL import Image, ImageDraw
from functools import lru_cache
from random import randint, choice, shuffle
from spaceship.tools import bresenhams
from math import hypot
from copy import deepcopy
from textwrap import wrap
from namedlist import namedlist
from collections import namedtuple
from spaceship.maps.charmap import DungeonCharmap as dcm
from spaceship.maps.charmap import WildernessCharmap as wcm
from spaceship.tools import scroll
from spaceship.units.monsters import Rat, Bat

"""Maps file holds template functions that return randomized data maps used\
in creating procedural worlds"""

# Key-value pairs are mapped from characters to color tuples
# used when converting maps into color images
picturfy_chars = {
    "#": (0,0,0),
    "%": (136, 0, 21),
    "o": (255, 242, 0),
    ",": (34, 177, 76),
    "+": (185, 122, 87),
    "=": (112, 146, 190),
    ".": (127, 127, 127),
    ".": (255, 255, 255),
    ":": (195, 195, 195),
    "~": (0, 162, 232),
    "|": (241, 203, 88),
    "x": (98, 81, 43),
}

# Key-Value pairs are tuples to tuple pertaining to color and character mapping
# used in converting colored images into string maps
stringify_chars = { 
    (0, 0, 0): "#",
    (136, 0, 21): "%",
    (255, 242, 0): "=",
    (34, 177, 76): ",",
    (185, 122, 87): "+",
    (127, 127, 127): ".",
    (112, 146, 190): "=",   
    (153, 217, 234): "=",
    (255, 255, 255): ".",
    (195, 195, 195): ":",
    (241, 203, 88): "|",
    (255, 201, 14): "|",
    (0, 162, 232): "~",
    (98, 81, 43): "x",
    (239, 228, 176): ",",
}

stringify_world = {
    (112, 146, 190): "=",
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

    print("Saving string as {}".format(folder + filename))
    img_to_save.save(folder + filename)
    return folder + filename

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
    return [[(choice(ch), choice(val), i, j) for i in range(x)] for j in range(y)]

def splitter(c):
    '''Returns a sequence derived from a hexcode'''
    c = c.replace("#", "")
    if len(c) >= 8:
        c = c[2::]
    return wrap(c,2)

def blender(hexes, n=10):
    """blender holds color transformation functions
    TODO: probably should move this to another file
    Up to user to decide whether color is valid"""
    hex1, hex2 = hexes
    
    def transform(c):
        # for i in c:
        #   integer = int(i, 16)
        return [int(i, 16) for i in c]

    def blend(ca, cb, n, i):
        value = ca - cb
        value /= n
        value *= i
        value = round(value)
        value = hex(cb+value)
        value = value.replace("0x", "")
        #value = hex(((abs(ca-cb)//n))*i).replace("0x", "")
        return value

    def mash(color):
        return "#ff"+"".join(map(lambda x: "0"+str(x) if len(str(x)) < 2 else str(x), color))

    colorA = transform(splitter(hex2))
    colorB = transform(splitter(hex1))
    colorS = [mash(splitter(hex1.replace("#","")))]

    for i in range(n-2):
        color=[]
        for j in range(3):
            color.append(blend(colorA[j], colorB[j], n-2, i))
        colorS.append(mash(color))

    colorS.append(mash(splitter(hex2.replace("#",""))))
    
    return colorS

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


# copy from objects.maps.dimensions() but takes in array as positional
def dimensions(data, array=False):
    """Takes in a string map and returns a 2D list map and map dimensions"""
    if not array:
        data = [[col for col in row] for row in data.split('\n')]
    height = len(data)
    width = max(len(col) for col in data)
    return data, height, width

def gradient(x, y, characters, colors):
    """Returns a more realistic map color gradient"""
    return table(characters, blender(colors), x, y)