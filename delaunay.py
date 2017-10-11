# Delauny, Python module for convex polygon triangulation
from math import sqrt
from collections import namedtuple
from namedlist import namedlist

point = namedlist("Point", "x y id")
edge = namedlist("Edge", "p1 p2")

def quatCross(a, b, c):
    p = (a+b+c)*(a+b-c)*(a-b+c)*(-a+b+c)
    return sqrt(p)

def crossProduct(p1, p2, p3):
    x1, x2 = p2.x-p1.x, p3.x-p2.x
    y1, y2 = p2.y-p1.y, p3.y-p2.y
    return x1 * y2 - y1 * x2

def isFlatAngle(p1, p2, p3);
    return crossProduct(p1, p2, p3) == 0

def edgeEq(a, b):
    return a.p1 == b.p1 and a.p2 == b.p2
