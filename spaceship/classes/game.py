from bearlibterminal import terminal
from re import search

class Color:
    def __init__(self, color):
        if search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):
            self.color = color
        else:
            raise ValueError("Hexcode is an invalid color")

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    @property
    def position(self):
        return self.x, self.y

    def __iadd__(self, other):
        try:
            return Point(self.x + other.x, self.y + other.y)
        except:
            return Point(self.x + other[0], self.y + other[1])

    def __isub__(self, other):
        try:
            return Point(self.x - other.x, self.y - other.y)
        except:
            return Point(self.x - other[0], self.y - other[1])

    def __eq__(self, other):
        try:        
            return self.x == other.x and self.y == other.y
        except:
            return self.x == other[0] and self.y == other[1]

class Tile:
    def __init__(self, ch, fg, bg):
        self.character = ch
        self.foreground = fg.color
        self.background = bg.color

    def freeze():
        self.background = "blue"
    
    def burn():
        self.background = "red"

    def electrify():
        self.background = "yellow"

    def poison():
        self.background = "green"

class Object:
    def __init__(self, point, tile):
        self.point = point
        self.tile = tile

    @property
    def position(self):
        return self.point.position

    @property
    def character(self):
        return self.tile.character
    
    @property
    def foreground(self):
        return self.tile.foreground
    
    @property
    def background(self):
        return self.tile.background

class Energy:
    def __init__(self):
        pass

class Unit(Object):
    def __init__(self, point, tile, energy):
        super().__init__(point, tile)
        self.energy = energy
    
    def move(self, point):
        self.point += point

    # used to be displace
    def swap(self, object):
        self.point, object.point = object.point, self.point

class Monster(Unit):
    def __init__(self, point, tile, energy):
        super().__init__(point, tile, energy)

    def take_action(self):
        if self.has_energy:
            self.use_energy()
        else:
            self.gain_energy()

class Player(Unit):
    def __init__(self, point, tile, energy):
        super().__init__(point, tile, energy)

    def take_action(self):
        if self.has_energy:
            self.use_energy()
        else:
            self.gain_energy()

class Game:
    def __init__(self, font="default"):
        self.__font = font

    def setup(self):
        terminal.open()
        terminal.set("window: size={}x{}, title='{}'".format(
            80, 25, 'Some Game'
        ))
        terminal.refresh()

    def run(self):
        self.setup()
        
        try:
            while True:
                key = terminal.read()
                if key == terminal.TK_ESCAPE or key == terminal.TK_CLOSE:
                    break
        except KeyboardInterrupt:
            pass

        finally:
            terminal.close()

if __name__ == "__main__":
    g = Game()
    g.run()