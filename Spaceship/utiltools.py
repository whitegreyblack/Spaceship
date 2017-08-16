# utiltools : functions for 2D graphics manipulations and transformation

def deltanorm(p1, p2):
    '''Returns direction of line given two points'''
    return int((p2-p1)/abs(p2-p1))

def deltanorm(x1, y1, x2, y2)
    '''Returns tuple of direction of line given two points'''
    return (deltanorm(x1, x2), deltanorm(y1, y2))

def basicmap(x, y, v=0):
    '''Returns 2D list with width x, height y, and values of z'''
    return [[0 for _ in range(y)] for _ in range(x)]
