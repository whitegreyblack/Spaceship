# -*- coding=utf-8 -*-
from PIL import Image, ImageDraw
from functools import lru_cache
from random import randint, choice
from math import hypot

"""Maps file holds template functions that return randomized data maps used\
in creating procedural worlds"""

# Key-value pairs are mapped from characters to color tuples
picturfy_chars = {
    "#": (0,0,0),
    ",": (34, 177, 76),
    "+": (185, 122, 87),
    "~": (112, 146, 190),
    ".": (127, 127, 127),
    ".": (255, 255, 255),

}

# Key-Value pairs are tuples to tuple pertaining to color and character mapping
stringify_chars = { 
    (0, 0, 0): ("#", "89"),
    (34, 177, 76): (",", "71"),
    (185, 122, 87): ("+", "90"),
    (127, 127, 127): (".", "72"),
    (112, 146, 190): ("~", "91"),
    (255, 255, 255): (".", "92"),
}

def picturfy(string, filename="picturfy-img.png", asciify=False, debug=False):
    '''Takes in a string map and two positional parameters to determine
    output. If asciify is specified then returns color codes reflective
    of their ascii character code else returns color based on regular
    character code. Debug is specified for testing and output viewing'''

    mapping = string.split('\n')
    h, w = len(mapping), len(mapping[0])
    img_to_save = Image.new('RGB', (w, h))
    drawer = ImageDraw.Draw(img_to_save)

    for j in range(h):
        string_list = list(mapping[j])
        for i in range(len(string_list)):
            drawer.rectangle((i, j, i+1, j+1), picturfy_chars[string_list[i]])

    img_to_save.save("assets/"+filename)
    return filename


def stringify(string, asciify=False, debug=False):
    '''Takes in a file location string and two positional parameters
    to determine output. If asciify is specified then returns ascii
    character codes for use in map construction else outputs regular
    character text. Debug is specified for testing and output viewing'''

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
            except BaseException:
                r, g, b = pixels[i, j]
            if (r, g, b) not in colors:
                colors.add((r, g, b))
            line += stringify_chars[(r, g, b)][int(asciify)]
        lines.append(line)

    if debug:
        print("\n".join(lines))
        print(colors)

    return "\n".join(lines)


def table(ch, val, x, y):
    """Returns a 2d list of lists holding a four element tuple"""
    return [[(ch, val, i, j) for i in range(x)] for j in range(y)]


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
    print("\n".join(lines), characters)


def dimensions(data):
    """Takes in a string map and returns a 2D list map and map dimensions"""
    data = [[col for col in row] for row in data.split('\n')]
    height = len(data)
    width = max(len(col) for col in data)
    return data, height, width


def world(x, y, p=50, i=100):
    pass


def gradient(x, y, d, c, p=50, i=100):
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
        _, og, _, _ = data[j % h][i % w]
        ng = mm(og, distance(abs(x-i), abs(y-j) * factor))
        data[j % h][i % w] = (choice(c), ng if og > ng else mid(ng, og), i, j)

    factor = 5
    chance = 8
    w, h = x, y
    data = table(".", 200, x, y)

    for _ in range(p):
        chance = chance
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
    land, chars = output(gradient(300, 75, 100, 100))
    print(land)
    print(chars)
