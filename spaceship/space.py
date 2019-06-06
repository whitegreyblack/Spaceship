# space.py

"""
Creates an arbitrary object space and prints to term
"""

import click
import colorama
import copy
import random

VALLEY = 0
HILL = 1

def matrix(w, h, v=0):
    return [[v for _ in range(w)] for _ in range(h)]

def random_matrix(w, h, v=(0, 1)):
    """
    Builds a matrix of width, height with values passed in
    """
    rchoice = random.choice
    return [[rchoice(v) for _ in range(w)] for _ in range(h)]

def probability_matrix(w, h, v=(0, 1), p=(55, 45)):
    """
    Creates a matrix based on values and probabilities for each value
    """
    assert sum(p) == 100
    rchoices = random.choices
    return [[rchoices(v, p).pop() for _ in range(w)] for _ in range(h)]

def evaluate_matrix(i, m, t):
    """
    Analyzes given matrix and outputs information based on analysis
    """
    # holds number of specific land types corresponding with 0 or 1.
    env = [0, 0]
    for row in m:
        for cell in row:
            env[cell] += 1
    print(f"""\n
Iteration: {i}
Using: {t}
Matrix(width: {len(m)} height: {len(m[0])})
Floors: {env[0]}
Walls: {env[1]}
ratio: floor {env[0]/sum(env):.2f}, wall {env[1]/sum(env):.2f}"""[1:])

def randpoint(x):
    """
    Shorter function name than randint. Exclusive of x.
    """
    return random.randint(0, x-1)

def eight_square():
    """
    Yields x, y values indicating cardinal directions on a grid
    """
    for x in range(-1, 2):
        for y in range(-1 ,2):
            if (x, y) != (0, 0):
                yield x, y

def transform_lake(square, neighbors, hills):
    """
    Counts number of neighbors and landtypes around the current square and
    modifies value of the cell
    """
    if neighbors == 8 and square is HILL and hills < 4:
        return VALLEY
    elif neighbors == 8 and square is VALLEY and hills > 4:
        return HILL
    elif neighbors < 8:
        return HILL
    return square

def transform_cave(square, neighbors, hills):
    """
    Counts number of neighbors and landtypes around the current square and
    modifies value of cell
    """
    # t<7|(t=8&&v>5) 
    if neighbors == 8 and square is HILL and hills < 4:
        return VALLEY
    elif neighbors == 8 and square is VALLEY and hills > 4:
        return HILL
    elif neighbors < 8:
        return HILL
    return square

def remove_islands(m):
    group_map = copy.deepcopy(m)
    group = 0
    groups = []
    for j, row in enumerate(m):
        for i, col in enumerate(row):
            pass
    matrix_to_term(group_map, string=to_string, colored=False)

def generate(width, height, transform, passes=2):
    """
    Uses cellular automata and smooting to build the map

    TODO: maybe add a stop parameter so that when the map reaches a certain 
          percentage of hills or valleys then the loop stops early.
          or if the % of hills or valleys do not change between two iterations
          then we can stop early too then.
    """
    
    # initial map plus copy
    m = probability_matrix(width, height)
    n = copy.deepcopy(m)
    
    for loop in range(passes):
        # matrix_to_term(m)
        # evaluate_matrix(loop+1, m, transform)
        
        if loop % 2:
            transform = transformers.get('lake')
        else:
            transform = transformers.get('cave')

        # iterate through each neighbor
        for j, row in enumerate(m):
            for i, col in enumerate(row):
                square = m[j][i]
                hills = 0
                neighbors = 0
                # will iterate cardinal coordinates except for 0, 0
                coordinates = eight_square()
                for x, y in list(coordinates):
                    # check bounds before moving on
                    xb = 0 <= i + x < width
                    yb = 0 <= j + y < height
                    if not (xb and yb):
                        continue
                    neighbor = m[j+y][i+x]
                    neighbors += 1
                    # depending on whether the current cell is a hill
                    # calculate the number of opposite types of lands
                    # surrounding the cell.
                    hills += int(neighbor == HILL)
                n[j][i] = transform(square, neighbors, hills)
        m = copy.deepcopy(n)
    return m

def convert_int_to_string(value, colored=False):
    """
    Returns a character based on value passed in
    """
    if not colored:
        return '#' if value else '.'
    if value:
        return colorama.Fore.GREEN + '#' + colorama.Style.RESET_ALL
    else:
        return colorama.Fore.BLUE + '.' + colorama.Style.RESET_ALL

def to_string(value, colored=False):
    return value

def matrix_to_term(m, string, colored=False):
    """
    Prettier printing for 2d lists
    """
    rows = []
    for row in m:
        rows.append(''.join(string(i, colored) for i in row))
    print('\n'.join(rows))


transformers = {
    'lake': transform_lake,
    'cave': transform_cave
}

@click.command()
@click.option('-w', '--width', 'width', default=80)
@click.option('-h', '--height', 'height', default=25)
@click.option('-t', '--type', 'maptype', default='lake')
@click.option('-p', '--passes', 'passes', default='2')
@click.option('-c', '--color', 'color', is_flag=True, default=False)
def main(width, height, passes, maptype, color):
    if color:
        colorama.init()
    transformer = transformers.get(maptype, transformers['lake'])
    world = generate(width, height, transformer, int(passes))
    matrix_to_term(world, convert_int_to_string, color)

if __name__ == "__main__":
    main()

