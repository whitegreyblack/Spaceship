import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../../')
from spaceship.maps.base import Map
from spaceship.maps.utils import blender
from PIL import Image
from collections import namedtuple
from spaceship.maps.charmap import DungeonCharmap as dcm
from spaceship.maps.charmap import WildernessCharmap as wcm
from random import shuffle, choice, randint

class World(Map):
    chars = {
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
    def __init__(self, map_img):
        self.map_img = map_img
        self.parse_img()
        super().__init__(self.width, self.height, self.__class__.__name__)


    def parse_img(self):
        """Takes in a file location string to create map object"""
        stringify_chars = {
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
            (255, 242, 0): "=",
            (255, 174, 201): "%",
            (112, 146, 190): "~",
            (63, 72, 204): "=",
            (0, 162, 232): "#",
            (0, 0, 0): "*",
        }  

        self.data = []
        self.spaces = []

        try:
            with Image.open(self.map_img) as img:
                pixels = img.load()
                self.width, self.height = img.size
        except FileNotFoundError:
            raise FileNotFoundError("Cannot find file for stringify: {}".format(self.map_img))

        for j in range(self.height):
            line = ""
            for i in range(self.width):
                # sometimes alpha channel is included so test for all values first
                try:
                    r, g, b, _ = pixels[i, j]
                except ValueError:
                    r, g, b = pixels[i, j]
                try:
                    char = stringify_chars[(r, g, b)]
                    if char in (".", ":", ",", "="):
                        self.spaces.append((i, j))
                    line += char
                except KeyError:
                    print((r, g, b))
            self.data.append(line)

if __name__ == "__main__":
    w = World("./assets/worldmap.png")
    for j in w.data:
        print(j)