"""Colors test -- since bearlibterminal likes using hexadecimal colors we need
to test our color functions which include blend, hexify, hexone and hextup"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+"/..")
from spaceship.maps import blend

def test_blend():
    color1 = "ff0000"
    color2 = "ffffff"
    assert str(blend(color1, color2)) == "#ff777777"
