import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from PIL import Image
from spaceship.imgpy import picturfy, stringify
from spaceship.maps import MAPS

"""Test file to test imgpy"""

original = "./assets/testmap.png"


def test_stringify():
    stringify(picturfy(MAPS.TOWN)) == stringify(original, debug=True)


def test_picturfy():
    with Image.open(picturfy(MAPS.TOWN)) as img:
        with Image.open(original) as orig:
            assert img.size == orig.size
