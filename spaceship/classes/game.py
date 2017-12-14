from bearlibterminal import terminal

class Point:
    def __init__(self):
        self.x, self.y = x, y

    def __iadd__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __isub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

class Tile:
    def __init__(self, ch, fg, bg):
        self.character = ch
        self.foreground = fg
        self.background = bg

class Object:
    def __init__(self, point, tile):
        self.point = point
        self.tile = tile

    def position(self):
        return x, y

    def character(self):
        return self.tile.character

    def foreground(self):
        return self.tile.foreground

    def background(self):
        return self.tile.background

class Unit(Object):
    def __init__(self, point, tile):
        super().__init__()
    
    def move(self, point):
        self.point += point

class Monster(Unit):
    def __init__(self):
        super().__init__()

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