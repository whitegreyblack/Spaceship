import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship import tools
import math


"""Test file for spaceship/tools.py"""


string = """\
aaaaaaaaaa
aaaaaaaaa
aaaaaaaa
aaaaaaaaaaa
aaaaaaaaa"""


def test_lamdafunc():
    value = tools.lambdafunc(min, 0, 1)
    assert value == 0

    value = tools.lambdafunc(max, 0, 1)
    assert value == 1

def test_deltanorm():
    value = tools.deltanorm(0, 1)
    assert value == 1

    value = tools.deltanorm(1, 0)
    assert value == -1


def test_deltanorms():
    value = tools.deltanorms(0, 1, 1, 0)
    assert value == (1, -1)

    value = tools.deltanorms(1, 0, 0, 1)
    assert value == (-1, 1)


def test_basicmap():
    map2d = tools.basicmap(4, 4)
    assert len(map2d) == 4
    assert len(map2d) == 4
    assert sum(map(sum, map2d)) == 0

    map2d = tools.basicmap(4, 4, 4)
    assert len(map2d) == 4
    assert len(map2d) == 4
    assert sum(map(sum, map2d)) == 4*4*4


def test_distance():
    d = tools.distance(0, 1, 3, 0)
    x, y = tools.absdistances(0, 1, 3, 0)
    assert d == math.sqrt(x**2+y**2)


def test_absdistance():
    distance = tools.absdistance(0, 1)
    assert distance == 1
    distance = tools.absdistance(-1, 1)
    assert distance == 2
    distance = tools.absdistance(-2, 0)
    assert distance == 2


def test_absdistances():
    distances = tools.absdistances(0, 1, 3, 0)
    assert distances == (3, 1)


def test_maxmindistance():
    distance = tools.maxmindistance(0, 1)
    assert distance == 1
    distance = tools.maxmindistance(-1, 1)
    assert distance == 2
    distance = tools.maxmindistance(-2, 0)
    assert distance == 2


def test_maxmindistances():
    distances = tools.maxmindistances(0, 1, 3, 0)
    assert distances == (3, 1)
    distanceA = tools.maxmindistances(0, 1, 3, 0)
    distanceB = tools.maxmindistances(3, 0, 0, 1)
    assert distanceA == distanceB


def test_line():
    start = (0, 0)
    stop = (3, 3)
    line_points = tools.line(start, stop)
    assert len(line_points) == 4
    assert line_points == [(0, 0), (1, 1), (2, 2), (3, 3)]

    start = (0, 0)
    stop = (3, 2)
    line_points = tools.line(start, stop)
    assert len(line_points) == 0
    assert line_points == []


def test_movement():
    high, low = 10, 0
    position, change, factor = 5, 1, 2
    assert low < tools.movement(position, change, factor, low, high) < high
    position, change = 1, -1
    assert tools.movement(position, change, factor, low, high) == low
    position, change = 9, 1
    assert tools.movement(position, change, factor, low, high) == high


def test_dimensions():
    smap, height, width = tools.dimensions(string)
    print(string)
    assert height == 5
    assert width == 11
