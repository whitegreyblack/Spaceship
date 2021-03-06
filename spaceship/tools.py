# -*- coding: utf-8 -*-
# utiltools : functions for 2D graphics manipulations and transformation
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')

import math

# TODO: Move these into more generalized files

def lambdatrue(f, *args, **kwargs):
    return f(*args, **kwargs)

def lambdafunc(f, x, y):
    return f(x, y)

def lambdafunctwice(f, x1, y1, x2, y2):
    '''Returns a tuple containing results using parameter function'''
    return (f(x1, x2), f(y1, y2))


def deltanorm(p1, p2):
    '''Returns direction of line given two points'''
    return int((p2 - p1) / abs(p2 - p1))


def deltanorms(x1, y1, x2, y2):
    '''Returns tuple of direction of line given two points'''
    return (deltanorm(x1, x2), deltanorm(y1, y2))


def basicmap(x, y, v=0):
    '''Returns 2D list with width x, height y, and values of z'''
    return [[v for _ in range(y)] for _ in range(x)]


def distance(x1, y1, x2, y2):
    '''Returns a float that represents distance between two points'''
    return math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))


def absdistance(p1, p2):
    '''Returns the distance between two points'''
    return abs(p1 - p2)


def absdistances(x1, y1, x2, y2):
    '''Returns a tuple of distances for x, y'''
    return (absdistance(x1, x2), absdistance(y1, y2))


def maxmindistance(p1, p2):
    '''Returns the distance between two points'''
    return max(p1, p2) - min(p1, p2)


def maxmindistances(x1, y1, x2, y2):
    '''Returns a tuple of distances for x, y'''
    return (maxmindistance(x1, x2), maxmindistance(y1, y2))


def line(start, stop):
    '''Naive Line algorithm -- produces a list of tuples from start to end'''
    x1, y1 = start
    x2, y2 = stop
    if max(x2, x1) - min(x2, x1) is max(y2, y1) - min(y2, y1):
        dx = deltanorm(x1, x2)
        dy = deltanorm(y1, y2)
        return [(x1 + dx * d, y1 + dy * d)
                for d in range(max(x2, x1) - min(x2, x1) + 1)]
    return []


def movement(pos, change, factor, low, high):
    '''takes a 1d position and change parameters and returns a new position'''
    updated = pos + change * factor
    return updated if low < updated < high else max(low, min(updated, high))


def dimensions(string):
    '''takes in a string map and returns a 2D list map and map dimensions'''
    string_map = [[col for col in row] for row in string.split('\n')]
    height = len(string_map)
    width = max(len(col) for col in string_map)
    return string_map, height, width


def bresenhams(start, end):
    """Bresenham's Line Algo -- returns list of tuples from start and end"""

    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points

def scroll(position, screen, worldmap):
    '''
    @position: current position of player 1D axis
    
    @screen  : size of the screen
    
    @worldmap: size of the map           
    '''
    halfscreen = screen//2
    # less than half the screen - nothing
    if position < halfscreen:
        return 0
    elif position >= worldmap - halfscreen:
        return worldmap - screen
    else:
        return position - halfscreen

def toInt(hexval):
    try:
        return int(hexval, 16)
    except TypeError:
        print("TOINT ERROR:", hexval)
        raise
