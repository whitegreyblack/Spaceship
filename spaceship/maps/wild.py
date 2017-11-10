import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../../')
from spaceship.maps.base import Map
from charmap import DungeonCharmap as dcm
from charmap import WildernessCharmap as wcm
from base import blender

class Wild(Map):
    chars = {
        "grassland": {
            ".": (wcm.GRASS.chars, blender(wcm.GRASS.hexcode)),
            "T": (wcm.TREES.chars, blender(wcm.GRASS.hexcode)),
        },
        "plains": {
            ".": (".", blender(wcm.PLAIN.hexcode)),
            "T": (wcm.TREES.chars, blender(wcm.TREES.hexcode)),
        },
        "hills": {
            ".": (wcm.GRASS.chars, blender(wcm.GRASS.hexcode)),
            "~": (wcm.HILLS.chars, blender(wcm.HILLS.hexcode)),
        },
        "forest": {
            ".": ("\"", blender([wcm.GRASS.hexcode[0], wcm.TREES.hexcode[0]])),
            "T": (wcm.TREES.chars, blender(wcm.GRASS.hexcode)),
        },
        "woods": {
            ".": (wcm.GRASS.chars, blender(wcm.GRASS.hexcode)),
            "T": (wcm.TREES.chars, blender(wcm.TREES.hexcode)),            
        }
    }
    def __init__(self, map_data):
        self.map_data = map_data
    
    def build_map(self):
        pass

class Grassland:
    pass

class Forest:
    pass

class Woods:
    pass

class Hills:
    pass

class Plains:
    pass

class Mountains:
    pass

class Water:
    pass

class Swamps:
    pass

class Desert:
    pass

class Wastes:
    pass