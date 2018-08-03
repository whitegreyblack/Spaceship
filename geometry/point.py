# Point.py
import vector

'''
Point - Position/Location in space
Vector - Displacement in space (direction)

P + P = V : Magnitude/Direction
P + V = P : Position
'''
def is_valid_iter(obj: object) -> bool:
    return isinstance(obj, (list, tuple)) and len(obj) == 2

class Point:
    '''
    Defines simple initializations 
    and operations using a pair 
    value property class

    TODO: Do we want immutable points?
    '''
    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f'Point({self._x}, {self._y})'

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __iter__(self):
        return iter((self._x, self._y))

    def __eq__(self, other):
        other_is_point = isinstance(other, Point)
        other_is_iter = is_valid_iter(other)
        if not (other_is_point or other_is_iter):
            raise ValueError
        return other == (self._x, self._y)

    def __add__(self, other):
        '''Should only be vector?'''
        other_is_vector = isinstance(other, vector.Vector)
        other_is_iter = is_valid_iter(other)

        if not (other_is_vector or other_is_iter):
            raise ValueError

        if other_is_vector:
            return Point(self.x + other.x, self.y + other.y)
        elif other_is_tuple:
            return Point(self.x + other[0], self.y + other[1])

    @property
    def x(self): 
        return self._x

    @property
    def y(self): 
        return self._y

    @classmethod
    def from_tuple(cls, pair):
        '''Helper class to create a Point from a tuple'''
        return Point(*pair)
