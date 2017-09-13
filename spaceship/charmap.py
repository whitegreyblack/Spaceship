from collections import namedtuple

class Charmap:
    charmap = namedtuple("Charmap", "char hexcode")
    GRASS=charmap([",", ";"], ("#56ab2f", "#a8e063"))
    HOUSE=charmap(["="], ("#ffffff", "#ffffff"))
    TILES=charmap(["."], ("#808080", "#C0C0C0"))
    WALLS=charmap(["#"], ("#eacda3", "#d6ae7b"))
    WATER=charmap(["~"], ("#43C6AC", "#191654"))
    DOORS=charmap(["+"], ("#994C00", "#994C00"))
    PLANT=charmap(["|"], ("#FDFC47", "#24FE41"))
    LAMPS=charmap(["o"], ("#ffffff", "#ffffff"))
    BRICK=charmap(["%"], ("#a73737", "#7a2828"))
    ROADS=charmap([":"], ("#808080", "#C0C0C0"))
    POSTS=charmap(["x"], ("#9a8478", "#9a8478"))
    BLOCK=("#", "+", "o", "x")