from .utils import spaceship
from spaceship.classes.game import Point, Tile, Object, Unit, Monster, Game, Color
import math

def test_point_creation():
    p = Point(2, 3)
    assert p.position == (2, 3)

def test_point_addition():
    p = Point(2, 3)
    p += Point(3, 4)

    assert p.position == (5, 7)

def test_point_addition():
    p = Point(2, 3)
    p -= Point(2, 3)

    assert p.position == (0, 0)

def test_points_addition():
    import functools, random
    pass
    
def test_object_position():
    obj = Object(Point(5, 6), Tile('@', Color('#888888'), Color('#040404')))
    assert obj.position == (5, 6)
    assert obj.position == Point(5, 6)

def test_object_character():
    obj = Object(Point(5, 6), Tile('@', Color('#888888'), Color('#040404')))
    assert obj.character == '@'

def test_object_foreground():
    obj = Object(Point(5, 6), Tile('@', Color('#888888'), Color('#040404')))
    assert obj.foreground == "#888888"

def test_object_background():
    obj = Object(Point(5, 6), Tile('@', Color('#888888'), Color('#040404')))
    assert obj.background == "#040404"