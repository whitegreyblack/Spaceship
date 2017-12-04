import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from bearlibterminal import terminal as t
from spaceship.maps.city import City
from spaceship.maps.cave import Cave

'''Test map with key handling functionality to test player input in controlled layouts'''

test_map_path = "./assets/maps/test_map.png"

def main():
    cave = Cave(66, 22)

    cave.debug_set_global_light()
    for x, y, char, col in cave.output():
        pass


if __name__ == "__main__":
    main()