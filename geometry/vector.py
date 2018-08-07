# Vector.py
import point

class Vector:
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __str__(self):
        return repr(self)
        
    def __repr__(self):
        return f'Vector({self._x}, {self._y})'
    
    def __init__(self, x, y):
        self._x = x
        self._y = y
    
    def __iter__(self):
        return iter((self.x, self.y))
        
    def __eq__(self, other):
        if not isinstance(other, Vector):
            raise ValueError
            
        return other == (self.x, self.y)
        
    def __add__(self, other):
        '''Should return a point: Point + Vector = `Point'''
        other_is_point = isinstance(other, point.Point)
        other_is_tuple = isinstance(other, (list, tuple)) and len(other) == 2
        
        if not (other_is_point or other_is_tuple):
            raise ValueError

        if other_is_point:
            return point.Point(self.x + other.x, self.y + other.y)
        elif other_is_tuple:
            return point.Point(self.x + other[0], self.y + other[1])

if __name__ == "__main__":
    print(__file__)
