from collections import namedtuple

charmap = namedtuple("Charmap", "chars hexcode")

class WildernessCharmap:
    GRASS=charmap([",", ";", "`","\""], ("#56ab2f", "#a8e063"))
    TREES=charmap(["Y", "T", "f"], ("#994C00", "#994C00"))

class DungeonCharmap:
    GRASS=charmap([",", ";"], ("#56ab2f", "#a8e063"))
    HOUSE=charmap(["="], ("#ffffff", "#ffffff"))
    TILES=charmap(["."], ("#808080", "#C0C0C0"))
    WALLS=charmap(["#"], ("#656565", "#656565"))
    WATER=charmap(["~"], ("#43C6AC", "#191654"))
    DOORS=charmap(["+"], ("#994C00", "#994C00"))
    PLANT=charmap(["|"], ("#F3E347", "#24FE41"))
    LAMPS=charmap(["o"], ("#ffffff", "#ffffff"))
    BRICK=charmap(["%"], ("#a73737", "#7a2828"))
    ROADS=charmap([":"], ("#808080", "#994C00"))
    POSTS=charmap(["x"], ("#9a8478", "#9a8478"))
    BLOCK=charmap(["#", "+", "o", "x"],("#000000", "#ffffff"))
    LTHAN=charmap(["<"], ("#c0c0c0", "#c0c0c0"))
    GTHAN=charmap([">"], ("#c0c0c0", "#c0c0c0"))
    TRAPS=charmap(["^"], ("#c0c0c0", "#c0c0c0"))

class Light:
    '''Light levels depends on two factors -- discovered and visible
                     Discovered | Visible
    0 - Unexplored : False      | False
    1 - Unex b Vis?: False      | True -- 
    2 - Explored   : True       | False
    3 - Visible    : True       | True

    lightlevel = namedtuple("Light", "UNEXPLORED EXPLORED VISIBLE"'''
    pass

color = namedtuple("Color", "r g b")