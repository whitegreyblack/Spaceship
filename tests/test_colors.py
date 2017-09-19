"""Colors test -- since bearlibterminal likes using hexadecimal colors we need
to test our color functions which include blend, hexify, hexone and hextup"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+"/..")
from spaceship.maps import blender
from spaceship.maps import splitter

def test_blender():
    color1 = "ff0000"
    color2 = "ffffff"
    assert color1 in str(blender((color1, color2)))
    assert color2 in str(blender((color1, color2)))
    assert len(blender((color1, color2))) == 10

def test_splitter():
    color = "#ff998877"
    assert "998877" == "".join(splitter(color))

def test_darken():
    pass