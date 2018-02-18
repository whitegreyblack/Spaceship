from spaceship.classes.object import Point, Object
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
    obj = Object(5, 6, '@', '#888888', '#040404')
    assert obj.local == (5, 6)
    assert obj.local == Point(5, 6)

def test_object_character():
    obj = Object(5, 6, '@', '#888888', '#040404')
    assert obj.character == '@'

def test_object_foreground():
    obj = Object(5, 6, '@', '#888888', '#040404')
    assert obj.foreground == "#888888"

def test_object_background():
    obj = Object(5, 6, '@', '#888888', '#040404')
    assert obj.background == "#040404"