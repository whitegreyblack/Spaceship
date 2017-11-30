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
    def __init__(self, map_img):
        pass

if __name__ == "__main__":
    w = World("./spaceship/assets/worldmap.png")