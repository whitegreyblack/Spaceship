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
