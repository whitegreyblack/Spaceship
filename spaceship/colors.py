import random

# class Color:
#     def __init__(self, r=None, g=None, b=None):
#         def color():
#             return random.randint(0,255)
#         self.r = color() if r is None else r
#         self.g = color() if g is None else g
#         self.b = color() if b is None else b
#     def set(self, r=None,g=None,b=None):
#         if r is not None:
#             self.r = r
#         if g is not None:
#             self.g = g
#         if b is not None:
#             self.b = b
#     def get(self):
#         return (self.r, self.g, self.b)

class Color:

    def toRGB(self):
        hexval = str(self.h)
        return int(hexval[0:1], 16), int(hexval[2:3], 16), int(hexval[4:5], 16)

    def toHEX(self):
        return str(hex(self.r))+str(hex(self.g))+str(hex(self.b))

    def setRGB(self, r, g, b):
        '''If called set RGB then HEX'''
        self.r = r
        self.g = g
        self.b = b
        self.setHex(*self.toHEX())

    def setHEX(self, hexval):
        self.h = hexval
        self.setRGB(*self.toRGB())
    


class COLOR:
    WHITE = (250, 250, 250)
    BLACK = (0, 0, 0)
    LGREY = (200, 200, 200)
    GREY = (125, 125, 125)
    DGREY = (50, 50, 50)
    BROWN = (225, 175, 100)
    YELLOW = (250, 250, 100)

# class SHIP_COLOR:
#     wall = color(0, 128, 255).get()
#     floor = color(128, 255, 255).get()
#     hatch = color(255, 128, 0).get()
#     other = color(128, 128, 192).get()


