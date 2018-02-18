import math
class Point:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"{self.__class__.__name__}: ({self.x}, {self.y})"

    def __iter__(self):
        return iter(tuple(getattr(self, var) for var in self.__slots__))

    def __add__(self, other):
        try:
            x, y = self.x + other.x, self.y + other.y
        except AttributeError:
            x, y = self.x + other[0], self.y + other[1]
        finally:
            return Point(x, y)

    def __sub__(self, other):
        try:
            x, y = self.x - other.x, self.y - other.y
        except:
            x, y = self.x - other[0], self.y - other[1]
        finally:
            return Point(x, y)

    def __eq__(self, other):
        return (self.x, self.y) == other

    def __hash__(self):
        return hash((self.x, self.y))

    def move(self, other):
        self.x, self.y = self + other

    def distance(self, other):
        if isinstance(other, tuple):
            other = Point(*other)
        midpoint = other - self
        return math.sqrt(math.pow(midpoint.x, 2) + math.pow(midpoint.y, 2))

def spaces(point, exclusive=True):
    '''Returns a list of spaces in a 8 space grid with the center (pos 5)
    returned if exclusive is set as false or excluded if set as true.
    '''
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if (dx, dy) == (0, 0) and exclusive:
                continue
            else:
                yield point + Point(dx, dy)