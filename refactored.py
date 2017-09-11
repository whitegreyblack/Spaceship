# refactored code -- saved for future reference
'''
def actionClose(x, y):
    def closeDoor(i, j):
        glog.add("Closed door")
        dungeon.close_door(i, j)
        dungeon.reblock(i, j)
    
    closeables = []
    for i, j in eightsquare(x, y):
        if (i, j) != (x, y):
            if dungeon.square(i, j) == "/":
                closeables.append((i, j))
    if not closeables:
        glog.add("No closeables near you")

    elif onlyOne(closeables):
        closeDoor(closeables[0][0], closeables[0][1])

    else:
        glog.add("Which direction")
        term.refresh()
        code = term.read()

        if code in key_movement:
            cx, cy = key_movement[code]
        elif code in num_movement:
            cx, cy = num_movement[code]
        else:
            return
        if (x+cx, y+cy) in closeables:
            closeDoor(x+cx, y+cy)

def actionOpen(x, y):
    def openDoor(i, j):
        glog.add("Opened door")
        dungeon.open_door(i, j)
        dungeon.unblock(i, j)

    openables = []
    for i, j in eightsquare(x, y):
        if (i, j) != (x, y):
            if dungeon.square(i, j) == "+":
                openables.append((i, j))
                
    if not openables:
        glog.add("No openables near you")

    elif onlyOne(openables):
        openDoor(openables[0][0], openables[0][1])

    else:
        glog.add("Which direction?")
        term.refresh()  
        code = term.read()

        if code in key_movement:
            cx, cy = key_movement[code]
        elif code in num_movement:
            cx, cy = num_movement[code]
        else:
            return
        if (x+cx, y+cy) in openables:
            openDoor(x+cx, y+cy)       

def world(x, y, pos=50, iterations=20):
    """Returns a more world map with forests based on the forest function below
    TODO: Color currently starts at 0 and increments by 1 everytime data is accessed -- more realistic algo?
    """
    def inc(x, y):
        _, i, _, _ = data[y][x]
        data[y][x] = (char, mm(i+1), x, y)

    def double(x, y):
        pairs.add((x,y))
        pairs.add((y,x))

    @lru_cache(maxsize=None)
    def mm(c):
        """Returns the value or predetermined value if out of bounds"""
        return min(max(0, c), 250)
    
    # random integers for picking a random point in quadrant
    quads = {
        0: (0,x//2, 0, y//3),
        1: (x//2+1, x-1, 0, y//2),
        2: (0,x//2, y//2+1, y-1),
        3: (x//2+1, x-1, y//3+1, y-1),
    }
    # explicit midpoint in each quadrant
    quad_pos = {
        0: (x//4, y//4),
        1: (x*3//4, y//4),
        2: (x//4, y*3//4),
        3: (x*3//4, y*3//4)
    }
    rotations = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1), 
    ]
    factor = 5
    chance = 10
    char = "#"
    unch = "."
    w, h = x, y
    data = table(unch, 0, x, y)
    pairs = set()
    for _ in range(10):
        quad_beg, quad_end = 0, 0
        while quad_beg == quad_end:
            quad_beg = randint(0,3)
            quad_end = randint(0,3)
        
        x0, x1, y0, y1 = quads[quad_beg]
        bx, by = randint(x0, x1), randint(y0, y1)

        x0, x1, y0, y1 = quads[quad_end]
        ex, ey = randint(x0, x1), randint(y0, y1)

        points = bresenhams((bx, by), (ex, ey))
        for x, y in points:
            inc(x, y)
            
        for point in range(0,len(points), 3):
            x, y = points[point]
            i, j = x, y
            try:
                inc(i, j)
                for _ in range(iterations):
                    for rot in rotations:
                        if randint(-chance+1, 1):
                            di, dj = rot
                            i -= di
                            j -= dj
                            inc(i, j)
            except IndexError:
                pass

    return data    

def forests(x, y, d, c, p=100, i=100):
    """Returns a list of lists with symbols and color gradient tuple"""

    @lru_cache(maxsize=None)
    def distance(x, y):
        """Returns the hypotenuse distance between two points"""
        return int(hypot(x, y))

    @lru_cache(maxsize=None)
    def mm(g, v):
        """Returns the value or predetermined value if out of bounds"""
        return min(max(50, g-v), 250)

    @lru_cache(maxsize=None)
    def mid(x, y):
        """Returns the midpoint value between two points"""
        return (x+y)//2

    def replace(x, y, i, j):
        """Evaluates the tuple in data and replaces it with a new tuple"""
        _, og, _, _ = data[j][i]
        ng = mm(og, distance(abs(x-i), abs(y-j) * factor))
        data[j][i] = (choice(c), ng if og > ng else mid(ng, og), i, j)

    factor = 3
    chance = 5
    w, h = x, y
    data = table(d, 250, x, y)

    for _ in range(p):
        x, y = randint(0, w), randint(0, h)
        i, j = x, y

        for _ in range(i):
            try:
                if randint(0, 1):
                    i -= 1
                    replace(x, y, i, j)

                if randint(0, 1):
                    i += 1
                    replace(x, y, i, j)

                if randint(0, 1):
                    j += 1
                    replace(x, y, i, j)

                if randint(0, 1):
                    j -= 1
                    replace(x, y, i, j)
        
                if randint(-chance+1, 1):
                    i, j = i-1, j-1
                    replace(x, y, i, j)

                if randint(-chance+1, 1):
                    i, j = i-1, j+1
                    replace(x, y, i, j)

                if randint(-chance+1, 1):
                    i, j = i+1, j-1
                    replace(x, y, i, j)

                if randint(-chance+1, 1):
                    i, j = i+1, j+1
                    replace(x, y, i, j)

            except IndexError:
                pass

    return data
'''
'''
class TextBox:
    def __init__(self, string):
        self.string = string

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "{}({},{})".format(
            self.__class__.__name__, self.x, self.y)


class Plane:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = x * y

    def getter(self):
        return self.x, self.y, self.size

    def update(self, x, y):
        self.x = x
        self.y = y
        self.size = x * y

    def __repr__(self):
        return "{}({},{},{})".format(
            self.__class__.__name__, self.x, self.y, self.size)

class Map(Plane):
    def __init__(self, x, y):
        super(Map, self).__init__(x, y)
        self.points = [Point(x, y) for x in self.x for y in self.y]

    def getPoint(self, x, y):
        return self.points[x][y]

    def setPoint(self, x, y, v):
        try:
            self.points[x][y] = v
        except BaseException:
            print('Unable to set value to point')

class Rectangle(Plane):
    def __init__(self, x, y, dx, dy):
        super(Rectangle, self).__init__(dx, dy)
        self.tl = Point(x, y)
        self.tr = Point(x + dx - 1, y)
        self.bl = Point(x, y + dy - 1)
        self.br = Point(x + dx - 1, y + dy - 1)

    def pts(self):
        return self.tl, self.tr, self.bl, self.br

    def ctr(self):
        return (self.tl.x + self.br.x) / 2, (self.tl.y + self.br.y) / 2

    def cross(self, other):
        return (self.tl.x <= other.br.x and self.br.x <= other.tl.x and
                self.tl.y <= other.br.y and self.br.y <= other.tl.y)

    def __repr__(self):
        return "{}({},{},{})\n({},{})\n({},{})".format(
            self.__class__.__name__, self.x, self.y, self.size,
            self.tl, self.tr, self.bl, self.br)


class Grid:
    def __init__(self, dx, dy, v):
        self.mx = dx
        self.my = dy
        self.walkable = set()
        self.map = [[v for y in range(dy)] for x in range(dx)]

    def __repr__(self):
        return "{}({},{},{})".format(
            self.__class__.__name__, self.mx, self.my, type(self.map[0][0]))


'''
'''
class Tile(Point):
    def __init__(self, x, y, blocked, block_sight):
        super(Tile, self).__init__(x, y)
        self.blocked = blocked
        self.explored = False
        self.block_sight = block_sigh if block_sight else blocked

class GameObject(Point):
    def __init__(self, x, y, char, color=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color if color else Color(0, 0, 0)

    def __repr__(self):
        return "{}({},{},{},{}".format(self.__class__.__name__,
                                       self.x, self.y, self.char, self.color)

class ImmovableObject(GameObject):
    def __init__(self, x, y, char, color=None):
        super(ImmovableObject, self).__init__(x, y, char, color)


class MovableObject(GameObject):
    def __init__(self, x, y, char, color=None):
        super(MovableObject, self).__init__(x, y, char, color)

    def move(self, dx, dy, tile):
        if tile.open:
            self.x += dx
            self.y += dy

class Tile:
    def __init__(self, blocked, sight=None):
        self.blocked = blocked
        self.sight = blocked if sight is None else sight

if __name__ == "__main__":
    # old maps script to use forests/world function
    width = 100
    height = 50
    if len(sys.argv) == 2 and sys.argv[1] == "-t":
        term.open()
        term.set("window: size={}x{}, cellsize={}x{}, title='Maps'".format(
            width, height, 8, 16
        ))
        data = world(width, height, 100, 100)
        output(data)
        for row in data:
            for c, col, i, j in row:
                col = hextup(col, 2, 1, 1) if col > 5 else hextup((col+1)*25, (col+1)*25//2, (col+1)*25//2, col+1)
                term.puts(i, j, "[color={}]{}[/color]".format(col, c))
        term.refresh()
        term.read()
    else:
        output(world(width, height//2, 100, 100))

'''