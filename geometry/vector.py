# Vector.py
import point

class Vector:
	def __str__(self):
		return repr(self)
		
	def __repr__(self):
		return f'Vector({self._x}, {self._y})'
	
	def __init__(self, x, y):
		self._x = x
		self._y = y
	
	def __iter__(self):
		return iter((self._x, self._y))
		
	def __eq__(self, other):
		if not isinstance(other, Vector):
			raise ValueError
			
		return other == (self._x, self.y)
		
	def __add__(self, other):
		other_is_point = isinstance(other, point.Point)
		other_is_tuple = isinstance(other, (list, tuple)) and len(other) == 2
		
		if not (other_is_point):
			pass

if __name__ == "__main__":
	print(__file__)