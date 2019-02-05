"""space.py: creates an arbitrary object space and prints to term"""

import random
import copy

size = (80, 25)

def random_matrix(w, h, v=(0, 1)):
    """Builds a matrix of width, height with values passed in"""
    rchoice = random.choice
    return [[rchoice(v) for _ in range(w)] for _ in range(h)]

def probability_matrix(w, h, v=(0, 1), p=(55, 45)):
    """Creates a matrix based on values and probabilities for each value"""
    assert sum(p) == 100
    rchoices = random.choices
    return [[rchoices(v, p).pop() for _ in range(w)] for _ in range(h)]

def evaluate_matrix(m):
    print(f"Matrix(width: {len(m)} height: {len(m[0])})")
    env = [0, 0]
    for row in m:
        for cell in row:
            env[cell] = env[cell] + 1
    print(f"Floors: {env[0]}")
    print(f"Walls: {env[1]}")
    print(f"ratio: floor {env[0]/sum(env):.2f}, wall {env[1]/sum(env):.2f}")

def randpoint(x):
    """Shorter function name than randint. Exclusive of x."""
    return random.randint(0, x-1)

def eight_square():
    """Yields x, y values indicating cardinal directions on a grid"""
    for x in range(-1, 2):
        for y in range(-1 ,2):
            if (x, y) != (0, 0):
                yield x, y

def caves(width, height):
    """Uses cellular automata to build the space"""
    pass

def cavern(width, height, passes=2):
    """Uses cellular automata to build the space"""
    # smoothing algo
    # every floor cell with with fewer than 4 adjacent floor cells becomes a wall
    # every wall cell with six or more adjacent wall cells becomes a floor
    
    m = probability_matrix(width, height)
    n = copy.deepcopy(m)
    
    for _ in range(passes):
        print()
        matrix_to_term(m)
        evaluate_matrix(m)
        
        # iterate through each neighbor
        for j, row in enumerate(m):
            for i, col in enumerate(row):
                v = 0
                t = 0
                # floor
                for x, y in eight_square():
                    # check bounds before moving on
                    xb = 0 <= i + x < width
                    yb = 0 <= j + y < height
                    if not (xb and yb):
                        continue
                    c = m[j+y][i+x]
                    t += 1
                    # spot on map is a floor(0) or wall(1)
                    if m[j][i] == 0:
                        v += c == 0
                    else:
                        v += c == 1
                if m[j][i] == 0:
                    if t < 7 or (t == 8 and v > 7): # t<7|(t=8&&v>5)
                        n[j][i] = 1
                else:
                    if t < 8:
                        continue
                    elif t == 8 and v < 6:
                        n[j][i] = 0

        m, n = n, copy.deepcopy(n)
    return m

def islands(width, height):
    """Uses diamond square to build the space"""
    pass

def blocks(width, height):
    """Uses bsp"""
    pass

def convert_int_to_char(ch):
    """Given a value of 0 and 1, returns a wall or floor char"""
    return '#' if ch else '.'

def matrix_to_term(m):
    """Prettier printing for 2d lists"""
    change = convert_int_to_char
    for row in m:
        print(''.join(change(c) for c in row))

if __name__ == "__main__":
    m = cavern(80, 25, 12)
    matrix_to_term(m)
    # after random build. Fill non-travelable islands
    # def fill(m):
    #     1. flood fill by island into a set
    #     2. take largest island set.
    #     3. remove all other islands.
    #     note: if largest island only contains < half the number
    #           of floors available. Then add the second largest set
    #           of islands until it does become >= half the number of
    #           floors available.
