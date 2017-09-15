import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')

from collections import namedtuple
from namedlist import namedlist

'''
Engine:
    base:
        length: y
        width: x
'''


Position=namedlist("Position", "x y")
Character=namedtuple("Char", "unicode character")
Color=namedtuple("Color", "format red green blue")
Tile=namedtuple("Tile", "position character color")
Square=namedlist("Square", "base block light unit item")
'''
class Light:
    self.light_map = [[]]
    self.light_list = []

    for i in light_list:
        calc_light()

class Map:
    def __init__(self, xy=None, stringdata=None):
        if not xy or stringdata:
            raise ValueError

        if x, y -> generate map
            rooms -> regular dungeon map
            dwalk -> drunkards cave walk
            towns -> generated city/town/village
            plain -> generated wilderness from map character/color as parameter -> if not exists create wilderness
            ships -> generate a spaceship interior
            
        if stringdata -> extract character
            color[character] -- color mapping for character
            block[character] -- block
            generate the map using these parameters

    def add_units(self, unit_list):
        # adds units to the map
        if hasattr(self, unit_list):
            self.unit_list.append(list)
        else:
            self.unit_list = list

    def add_items(self, item_list):
        # adds items to the map
        if hasattr(self, item_list)
            self.item_list.append(list)
        else:
            self.item_list = list
    # ^ probably refactor these into their own seperate classes


class Engine:
    '''Refactor of objects.Map since it was getting clustered'''
    # def __init__(self, x, y):
    #     #self.world=[[[Square(None, None, None, [], []) for _ in range(5)] for _ in range(x)] for _ in range(y)]
    #     pass
    def createWorld(self, width, height, layers=5):
        self.world = []
        for y in range(height):
            row = []
            for x in range(width):
                column = []
                for _ in range(layers):
                    '''Implement square types later
                    # take the block from the stringdata
                    # evaluate the block to get the character
                    # using blender apply a color to the block
                    # assign the character to the square either in ascii or unicode format
                    # from the blockables list set the value of block
                    # set the light level to unexplored -- this will be our fog of war
                    '''
                    pos = Position(x, y)
                    ch = Character(unicode=False, character='#')
                    col = Color(format='hex', red='ff', green='ff', blue='ff')
                    block = Tile(position=pos, character=ch, color=col)
                    atom = Square(base=block, block=True, light=0, unit=[], item=[])
                    column.append(atom)
                row.append(column)
            self.world.append(row)
        return self.world[0][0][0]

Engine()
print(Engine().createWorld(10,10))
