"""Test file to test imgpy"""
from PIL import Image
from spaceship.imgpy import picturfy, stringify
from spaceship.maps import MAPS

original = "./assets/testmap.png"

def test_stringify():
    stringify(picturfy(MAPS.TOWN)) == stringify(original, debug=True)

def test_picturfy():
    with Image.open(picturfy(MAPS.TOWN)) as img:
        with Image.open(original) as orig:
            assert img.size == orig.size
