# -*- coding: utf-8 -*-
# utiltools : functions for 2D graphics manipulations and transformation
import math

def lambdafunc(f, x1, y1, x2, y2):
    '''Returns a tuple containing results using parameter function: useful to prevent code duplications'''
    return (f(x1, x2), f(y1, y2))

def deltanorm(p1, p2):
    '''Returns direction of line given two points'''
    return int((p2-p1)/abs(p2-p1))

def deltanorms(x1, y1, x2, y2):
    '''Returns tuple of direction of line given two points'''
    return (deltanorm(x1, x2), deltanorm(y1, y2))

def basicmap(x, y, v=0):
    '''Returns 2D list with width x, height y, and values of z'''
    return [[v for _ in range(y)] for _ in range(x)]

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
    x1, y1 = start                                                              
    x2, y2 = stop                                                               
    if max(x2, x1) - min(x2, x1) is max(y2, y1) - min(y2, y1):                  
        dx = deltanorm(x1, x2)                                                  
        dy = deltanorm(y1, y2)                                                  
        return [(x1+dx*d, y1+dy*d) for d in range(max(x2, x1) - min(x2, x1)+1)] 
    return []  

def movement(pos, change, factor, low, high):
    updated = pos + change * factor
    return updated if low < updated < high else max(low, min(updated, high))

def bresenhams(start, end):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end
    """
    
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
