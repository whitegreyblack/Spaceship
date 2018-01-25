import math
class Point:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"{self.__class__.__name__}: ({self.x}, {self.y})"

    def __iter__(self):
        return iter(tuple(getattr(self, var) for var in self.__slots__))

    def move(self, other):
        self.x, self.y = self + other

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

    def distance(self, other):
        if isinstance(other, tuple):
            other = Point(*other)
        midpoint = other - self
        return math.sqrt(math.pow(midpoint.x, 2) + math.pow(midpoint.y, 2))
