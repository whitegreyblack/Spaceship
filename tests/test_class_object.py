from .utils import spaceship
from spaceship.objects.base import Object
import math

def test_object_position():
    obj = Object(5, 5, "a", "#000000", "#ffffff")
    
    assert obj.position == (5, 5)

def test_object_distance():
    a = Object(0, 0, "a", "#000000", "#ffffff")
    b = Object(9, 9, "b", "#000000", "#ffffff")
    
    assert a.distance(b) > 0
