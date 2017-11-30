from collections import namedtuple

charmap = namedtuple("Charmap", "chars hexcode")

class WildernessCharmap:
    GRASS=charmap([",", ";", "`","\'", "\""], ("#56ab2f", "#a8e063"))
    PLAIN=charmap([".", "\"", ","], ("#F3E347", "#56ab2f"))
    TREES=charmap(["Y", "T", "f"], ("#994C00", "#994C00"))
    HILLS=charmap(["~"], ("#994C00", "#9A8478"))

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


stringify_colors = {
    'city': {
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
    'world': {
        (200, 191, 231): ("city(elven)", "&", ("#FF8844",)),
        (153, 217, 234): ("fort(dwarf)", "#", ("#FF00FF",)),
        (163, 73, 164): ("city(elven)", "&", ("#FFFF00",)),
        # (237, 28, 36): ("city(human)", "2302", ("#00fF00",)),
        (237, 28, 36): ("city(human)", "+", ("#00fF00",)),
        (136, 0, 21): ("fort(orcen)", "o", ("#FF0000",)),
        # (239, 228, 176): ("shore", "2261", ("#FFFFCC", "#FFFFE0")),
        (255, 255, 255): ("mnts(high)", "005E", ("#FFFFFF",)),
        # (195, 195, 195): ("mnts(med)", "2229", ("#C0C0C0",)),
        (195, 195, 195): ("mnts(med)", "n", ("#C0C0C0",)),

        # (127, 127, 127): ("mnts(low)", "n", ("#808080", "#A9A9A9",)),
        (127, 127, 127): ("mnts(low)", "n", ("#808080",)),

        # (185, 122, 87): ("hills", "2022", ("#C3B091", "#826644")),
        (185, 122, 87): ("hills", "2022", ("#826644",)),
        # (181, 230, 29): ("forest", "0192", ("#228B22", "#74C365")),
        (181, 230, 29): ("forest", "0192", ("#568203",)),

        # (34, 177, 76): ("dark woods", "00A5", ("#006400","#568203",)),
        (34, 177, 76): ("dark woods", "00A5", ("#006400",)),
        (255, 201, 14):("plains", ".", ("#FFBF00",)),
        (255, 127, 39): ("plains", ".", ("#FFBD22",)),
        # (255, 242, 0): ("fields", "2261", ("#FFBF00",)),
        (255, 242, 0): ("fields", "=", ("#FFBF00",)),
        (255, 174, 201): ("desert", "~", ("#F0AC82",)),
        (112, 146, 190): ("river", "~", ("#30FFFF",)),
        (63, 72, 204): ("lake", "2248", ("#3088FF",)),
        (0, 162, 232): ("deep seas", "2248", ("#3040A0",)),
        (0, 0, 0): ("dungeon", "*", ("#FF00FF",)),
    }
}


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