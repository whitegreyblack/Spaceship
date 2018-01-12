from collections import namedtuple

charmap = namedtuple("Charmap", "chars hexcode")

item_chars = ('%', '[', ')')
unit_chars = ('@', 'o', 'r', 'b', 'R', "v", "V", "B", "G", "I", "S")

class WildernessCharmap:
    GRASS=charmap([",", ";", "`","\'", "\""], ("#56ab2f", "#a8e063"))
    PLAIN=charmap([".", "\"", ","], ("#F3E347", "#56ab2f"))
    TREES=charmap(["Y", "T", "f"], ("#994C00", "#994C00"))
    HILLS=charmap(["~"], ("#994C00", "#9A8478"))

class DungeonCharmap:
    GRASS=charmap([",", ";"], ("#56ab2f", "#a8e063"))
    HOUSE=charmap(["="], ("#ffffff", "#ffffff"))
    TILES=charmap(["."], ("#C0C0C0", "#C0C0C0"))
    # TILES=charmap(["."], ("#404040", "#404040"))
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

class WorldCharmap:
    CITY = ""
    FORT = ""
    TOWN = ""
    HOLD = ""
    HILLS = ""
    PLAINS = ""
    DUNGEONS = ""
    MOUNTAINS = ""
    GRASSLANDS = ""
    TREES_SOUTH = "" 
    TREES_NORTH = ""


stringify_colors = {
    'city': {
        'string': {
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
        },
    },
    'world': {
        'string': {
            (200, 191, 231): "&",
            (153, 217, 234): "#",
            (163, 73, 164): "&",
            (237, 28, 36): "+",
            (136, 0, 21): "o",
            (255, 255, 255): "^",
            (195, 195, 195): "A",
            (127, 127, 127): "A",
            (185, 122, 87): "~",
            (181, 230, 29): "T",
            (34, 177, 76): "T",
            (255, 201, 14): ".",
            (255, 127, 39): ".",
            (255, 242, 0): "X",
            (255, 174, 201): "%",
            (112, 146, 190): "~",
            (63, 72, 204): "-",
            (0, 162, 232): "=",
            (0, 0, 0): "*",
        },
        'tile': {
            '&': 'city',
            '#': 'fort',
            '+': 'town',
            'o': 'hold',
            '^': 'mountain',
            '~': 'hills',
            'T': 'forest',
            '.': 'plains',
            '"': 'grassland',
            '*': 'dungeon',
        }
    }
}

'''
Light levels depends on two factors -- discovered and visible
                     Discovered | Visible
    0 - Unexplored : False      | False
    1 - Unex b Vis?: False      | True -- 
    2 - Explored   : True       | False
    3 - Visible    : True       | True
'''