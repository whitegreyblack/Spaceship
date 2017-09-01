# -*- coding=utf-8 -*-
from bearlibterminal import terminal as term
from functools import lru_cache
from random import randint
from time import sleep
from math import sqrt, hypot

"""Maps file holds template functions that return randomized data maps used\
in creating procedural worlds"""

def table(ch, val, x, y):
    """Returns a 2d list of lists holding a four element tuple"""
    return [[(ch, val, i, j) for i in range(x)] for j in range(y)]


def hexify(x):
    """Returns a single hex transformed value as a string"""
    return hex(x).split('x')[1] if x > 15 else '0'+hex(x).split('x')[1]


def hextup(x, a, b, c):
    """Returns a triple hex valued tuple as ARGB hex string"""
    return "#ff" \
            + hexify(x//a) \
            + hexify(x//b) \
            + hexify(x//c)


def hexone(x):
    return "#ff" +  hexify(x)*3

def output(data):
    lines = []
    characters = {}

    for row in data:
        line = ""
        for c, _, _, _ in row:
            try:
                characters[c] += 1
            except KeyError:
                characters[c] = 1
            line += c
        lines.append(line)

    return "\n".join(lines), characters 

def dimensions(data):
    """Takes in a string map and returns a 2D list map and map dimensions"""
    data = [[col for col in row] for row in data.split('\n')]
    height = len(data)
    width = max(len(col) for col in data)
    return data, height, width

def world(x, y, p=50, i=100):
    pass

def gradient(x, y, p=50, i=100):
    """Returns a list of lists with symbols and color gradient tuple"""

    @lru_cache(maxsize=None)
    def distance(x, y):
        """Returns the hypotenuse distance between two points"""
        return int(hypot(x, y))
    

    @lru_cache(maxsize=None)
    def mm(g,v):
        """Returns the value or predetermined value if out of bounds"""
        return min(max(50, g-v), 250) 
    
    
    @lru_cache(maxsize=None)
    def mid(x, y):
        """Returns the midpoint value between two points"""
        return (x+y)//2

    def replace(x, y, i, j):
        """Evaluates the tuple in data and replaces it with a new tuple"""
        _, og, _, _ = data[j%h][i%w]
        ng = mm(og, distance(abs(x-i), abs(y-j) * factor))
        data[j%h][i%w] = ("#", ng if og > ng else mid(ng, og), i, j)        

    factor = 5
    chance = 8
    w, h = x, y
    data = table(".", 200, x, y)

    for _ in range(p):
        chance = chance
        x, y = randint(0, w), randint(0, h)
        i, j = x, y

        for _ in range(i):
            try:
                if randint(0, 1):
                    i -= 1
                    replace(x, y, i, j)

                if randint(0, 1):
                    i += 1     
                    replace(x, y, i, j)  

                if randint(0, 1):
                    j += 1  
                    replace(x, y, i, j)   

                if randint(0, 1):
                    j -= 1  
                    replace(x, y, i, j)      
                if randint(-chance+1, 1):
                    i, j = i-1, j-1
                    replace(x, y, i, j)      

                if randint(-chance+1, 1):
                    i, j = i-1, j+1
                    replace(x, y, i, j)      

                if randint(-chance+1, 1):
                    i, j = i+1, j-1
                    replace(x, y, i, j)      

                if randint(-chance+1, 1):
                    i, j = i+1, j+1
                    replace(x, y, i, j)    

            except IndexError:
                pass

    return data

if __name__ == "__main__":
    land, chars = output(gradient(300, 75, 100, 100))
    print(land)
    print(chars)