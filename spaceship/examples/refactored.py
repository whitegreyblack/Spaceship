# refactored code -- saved for future reference
'''

def circle():
    term.open()
    term.set('window: size=160x100, cellsize=2x2')
    setup_font('Ibm_cga', 4, 4)
    dungeon = [[' ' for _ in range(X_TEMP)] for _ in range(Y_TEMP)]
    cx, cy = X_TEMP//2-1, Y_TEMP//2-1
    cr = min(cx, cy)
    print(cr)
    f = 1 - cr
    fx = 1
    fy = -2 * cr
    x = 0
    y = cr
    dungeon[cy-cr][cx] = '.'
    dungeon[cy+cr][cx] = '.'
    dungeon[cy][cx-cr] = '.'
    dungeon[cy][cx+cr] = '.'
    while x < y:
        if f >= 0: 
            y -= 1
            fy += 2
            f += fy
        x += 1
        fx += 2
        f += fx    
        dungeon[cy+y][cx+x] = '.'
        dungeon[cy+y][cx-x] = '.'
        dungeon[cy-y][cx+x] = '.'
        dungeon[cy-y][cx-x] = '.'
        dungeon[cy+x][cx+y] = '.'
        dungeon[cy+x][cx-y] = '.'
        dungeon[cy-x][cx+y] = '.'
        dungeon[cy-x][cx-y] = '.'
    for i in range(Y_TEMP):
        for j in range(X_TEMP):
            term.puts(j, i, dungeon[i][j])
    term.refresh()
    term.read()

def ellipse():
    term.open()
    term.set('window: size=160x100, cellsize=8x8')
    setup_font('Ibm_cga', 4, 4)
    dungeon = [[' ' for _ in range(X_TEMP)] for _ in range(Y_TEMP)]
    xr, yr = cx, cy = X_TEMP//2-1, Y_TEMP//2-1
    t = 0
    step = 1
    group = set()
    dungeon[cy-yr][cx] = '.'
    dungeon[cy-yr][cx] = '.'
    dungeon[cy][cx-xr] = '.'
    dungeon[cy][cx+xr] = '.'
    while t <= 360:
        x = int(round(cx + xr*math.cos(t)))
        y = int(round(cy + yr*math.sin(t)))
        if (x,y) not in group:
            dungeon[y][x] = '.'
            group.add((x,y))
        t += step    
    for i in range(Y_TEMP):
        for j in range(X_TEMP):
            term.puts(j, i, dungeon[i][j])
    term.refresh()
    term.read()

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


                    then try to color according to block type
                    color the floor
                    if len(str(ch)) < 2:
                        # tile = namedlist("Tile", "char color visible walkable")
                        if isFloor(ch):
                            level = ""
                            lit = "grey"
                        if isRoads(ch):
                            ch, color, _, _ = self.tilemap[y][x]
                            level = fog_levels[lit] if not daytime else ""
                        # if ch in (".",):
                        #     #_, color, _, _ = self.stone[y][x]
                        #     #lit = "white" if lit else fog
                        #     #lit = hexone(color//2) if visible else fg_fog
                        #     level = fog_levels[lit*2] if not daytime else "darkest " 
                        #     lit = "grey" if visible else "black"
                        #     ## bkgd = "black" if not lit else bg_fog
                        if ch in (":",):
                            ch, color, _, _ = self.tilemap[y][x]
                            #lit = "white" if lit else fog
                            #lit = hexone(color//2) if visible else fg_fog
                            level = fog_levels[lit] if not daytime else "" 
                            lit =  "#9a8478" if visible else fg_fog
                            ## bkgd = "black" if not lit else bg_fog
                        # color some grasses
                        if ch in (",",";","!","`"):
                            ch, col, _, _ = self.grass[y][x]
                            #lit = hextup(color,5,2,5) if visible else fg_fog
                            # bkgd = hextup(color, 5,3,5) if lit else bg_fog
                            try:
                                level = fog_levels[lit] if not daytime else "" 
                            except IndexError:
                                print(lit)
                            lit = col if visible else fg_fog

                        # color the water
                        if ch == "~":
                            lit = choice(self.colors_water) if visible else fg_fog

                        # color the doors
                        if ch in ("+", "/",):
                            lit = "#ff994C00" if visible else fg_fog
                            # bkgd = "black"i

                        # color the lamps
                        if ch in ("o",):
                            lit = "white" if visible else fg_fog

                        # color the walls
                        if ch == "#":
                            _, color, _, _ = self.walls[y][x]
                            #lit = hexone(color) if visible else fg_fog
                            lit = color if visible else fg_fog
                            # bkgd = "grey" if lit else bg_fog
                            #lit = "white" if lit else fog
                        
                        if ch == "%":
                            _, color, _, _ = self.walls[y][x]
                            #lit = hexone(color//2) if lit else fg_fog
                            lit = color if visible else fg_fog
                            # bkgd = "grey" if lit else bg_fog
                    
                        # street border
                        if ch in ("=",):
                            lit = "dark white" if visible else fg_fog

                        if ch in ("x"):
                            lit = "#383838" if visible else fg_fog
                        
                        if ch in ("|"):
                            ch, col, _, _ = self.plant[y][x]
                            #level = fog_levels[lit//2] if lit else "darkest " 
                            
                            #lit = "yellow" if visible else fg_fog
                            level = "light "
                            lit = col if visible else fg_fog

                    else:
                        _, color, _, _ = self.walls[y][x]
                        lit = color if visible else fg_fog

                bkgd = hextup(color, 4,4,4) if lit else bg_fog
                all said and done -- return by unit block

        # if volrooms < X_TEMP * Y_TEMP * .25:
        #     x, y = randint(8, 12), randint(6, 10)
        # else:
        #     x, y = randint(4, 6), randint(3, 5)
        # ox, oy = randint(-1,2), randint(-1, 2)
        # tx, ty = X_TEMP//2-x//2, Y_TEMP//2-y//2 # <-- the upper left point of the box starts near center
        # if volrooms == 0:
        #     # center the first box
        #     room = box(tx, ty, tx+x, ty+y)
        #     rooms.append(room)
        #     for i in range(y):
        #         for j in range(x):
        #             dungeon[ty+i][tx+j] = 1
        #     volrooms += x * y

        # else:
        #     case1 = False
        #     direction = choices(population=directions, weights=distribution, k=1)[0]
        #     while True:
        #         tx, ty = tx + randint(-2,3), ty + randint(-2, 3)
        #         tx, ty = tx + direction[0] * MULTIPLIER, ty + direction[1] * MULTIPLIER
        #         temp = box(tx, ty, tx+x, ty+y)
        #         intersects = any(intersect(room, temp) for room in rooms)
        #         # only checks for out of bounds if no intersections
        #         # needs to be both free of intersectiosn and within bounds
        #         if not intersects:
        #             if not oob(temp):
        #                 rooms.append(temp)
        #                 for i in range(y):
        #                     for j in range(x):
        #                         dungeon[ty+i][tx+j] += 1
        #                 volrooms += x * y
        #                 case1 = True
        #             else:
        #                 tries += 1
        #             break
                
        #     if not case1:
        #         tx, ty = X_TEMP//2-x//2, Y_TEMP//2-y//2 # <-- the upper left point of the box starts near center
        #         while True:
        #             tx, ty = tx + randint(-2,3), ty + randint(-2, 3)        
        #             tx, ty = tx + direction[0], ty + direction[1]
        #             temp = box(tx, ty, tx+x, ty+y)
        #             intersects = any(intersect(room, temp) for room in rooms)
        #             if not intersects:
        #                 if not oob(temp):
        #                     rooms.append(temp)
        #                     for i in range(y):
        #                         for j in range(x):
        #                             dungeon[ty+i][tx+j] += 1
        #                     volrooms += x * y
        #                 else:
        #                     tries += 1
        #                 break               
    # # -- Prints only the large rooms
    # term.clear()
    # wallmap = [[0 for _ in range(X_TEMP)] for _ in range(Y_TEMP)]
    # large_rooms = set()
    # other_rooms = set()
    # for  r in rooms:
    #     inside_ellipse = ooe(*(center(r)))
    #     # long_enough = (r.x2-r.x1 >= 12 or r.y2-r.y1 >= 12)
    #     large_enough = volume(r) >= 80
    #     if large_enough:
    #         large_rooms.add((r, center(r)))
    #         term.bkcolor('dark green')
    #         for x in range(r.x1, r.x2):
    #             for y in range(r.y1, r.y2):
    #                 term.puts(x, y, '[c=grey].[/c]')
    #                 wallmap[y][x] = 2
    #         for x in range(r.x1-1, r.x2+1):
    #             wallmap[r.y1-1][x] = 1
    #             wallmap[r.y2][x] = 1
    #         for y in range(r.y1-1, r.y2+1):
    #             wallmap[y][r.x1-1] = 1
    #             wallmap[y][r.x2] = 1
    #         term.bkcolor('black')
    #     else:
    #         # save smaller rooms for later
    #         other_rooms.add((r, center(r)))
    # term.refresh()
    # term.read()
    # term.clear()
    # for i in range(len(wallmap)):
    #     for j in range(len(wallmap[0])):
    #         if wallmap[i][j] == 1:
    #             term.bkcolor('grey')
    #             char = '#'
    #         elif wallmap[i][j] == 2:
    #             char = '.'
    #         else:
    #             char = ' '
    #         term.puts(j, i, char)
    #         term.bkcolor('black')
    # term.refresh()
    # term.read()
    # term.clear()
    # # edges
    # edges = set()
    # vertices = set()
    # print(len(large_rooms))
    # for lr in large_rooms:
    #     print(lr)
    # print('creating minimum graph')
    # # create the edges
    # for room, p1 in large_rooms:
    #     term.clear()
    #     for other, p2 in large_rooms:
    #         dis = distance(p1, p2)
    #         if not equal(p1, p2):
    #             # distance ,pt-pt, rev
    #             edges.add((room, other))
    #     term.bkcolor('dark green')                  
    #     for x in range(room.x1, room.x2):
    #         for y in range(room.y1, room.y2):
    #             term.puts(x, y, '[c=grey].[/c]')

    #     term.bkcolor('black')
    # print(len(edges))
    # for e in list(edges):
    #     print('EDGE: ',e)
    #     r1, r2 = e
    #     term.bkcolor('yellow')
    #     for x, y in lpath(r1, r2):
    #         term.puts(x, y, 'X')
    # term.refresh()
    # term.read()

    # connected = set()

    # edgelist = list(edges)
    # for e in edgelist:
    #     print(e)
    # print('-------------------------\nVertices')

    # # take each individual room
    # for room, _ in large_rooms:
    #     curredges = set()
    #     # check for edges in edge list
    #     for s, e in edges:
    #         # if the edge contains itself
    #         if equal(room, s) and (s, e) not in connected and (e, s) not in connected:
    #             print('SE', s, e)
    #             curredges.add((distance(center(s), center(e)), s, e))
    #     for i in curredges:
    #         print(i)
    #     print()
    #     sortededges = sorted(list(curredges))
    #     for i in sortededges:
    #         print(i)
    #     _, r1, r2 = sortededges[0]
    #     # connected.add((r1, r2))
    #     connected.add((r2, r1))

    # print(connected)
    # print(len(connected))
    # print('-------------------------\n')
    # term.read()
    # term.clear()
    # # draw the edges first
    # for e in list(connected):
    #     r1, r2 = e
    #     term.bkcolor('yellow')
    #     for x, y in lpath(r1, r2):
    #         term.puts(x, y, 'X')

    # # draw rooms
    # for room, p1 in large_rooms:
    #     print('ROOM:', room)
    #     term.bkcolor('dark green')                  
    #     for x in range(room.x1, room.x2):
    #         for y in range(room.y1, room.y2):
    #             term.puts(x, y, '[c=grey].[/c]')
    #     term.bkcolor('black')   

"""