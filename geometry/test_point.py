# test_point.py
from point import Point

def test_init():
	p = Point(3, 4)
	assert p.x == 3
	assert p.y == 4
	
def test_init_tuple():
	p = Point.from_tuple((3, 2))
	assert p.x == 3
	assert p.y == 2

def test_eq():
	p = Point(4, 3)
	assert p == (4, 3)