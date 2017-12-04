import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from PIL import Image
from spaceship.maps import stringify, picturfy

"""Test file to test imgpy"""

original = "./assets/testmap.png"


# def test_map_term():
#     t.open()

# def test_map_img():
#     pass

def test_stringify():
    stringify(picturfy(stringify(original), folder="./assets/")) == stringify(original, debug=True)

def test_picturfy():
    with Image.open(picturfy(stringify(original), folder="./assets/")) as img:
        with Image.open(original) as orig:
            assert img.size == orig.size
