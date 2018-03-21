# map.py

WORLD = '''
################################################################
#....#....#....#....#..........##....#....#....#....#..........#
#...................#..........##...................#..........#
#....#....#....#..........#....##....#....#....#....#.....#....#
#..............................................................#
#....#....#....#....#................#....#....#....#..........#
#....#....#....#....#..........##....#....#....#....#..........#
#..............................................................#
#....#....#....#..........#....##....#....#....#....#.....#....#
#..............................................................#
#..............................................................#
#..............................................................#
#..............................................................#
#..............................................................#
#..............................................................#
#..............................................................#
################################################################'''[1:]

class Map:
    mult = [
            [1,  0,  0, -1, -1,  0,  0,  1],
            [0,  1, -1,  0,  0, -1,  1,  0],
            [0,  1,  1,  0,  0, -1, -1,  0],
            [1,  0,  0,  1, -1,  0,  0, -1]
        ]
    def __init__(self, world:str):
        self.world = [[c for c in r] for r in world.split('\n')]
        self.height = len(self.world)
        self.width = len(self.world[0])
        self.floors = set((i, j) for j in range(self.height - 1)
                                 for i in range(self.width - 1)
                                 if self.world[j][i] == '.')
        self.init_light()

    def init_light(self):
        self.light = [[0 for c in r] for r in self.world]

    def reset_light(self):
        self.light = [[1 if c >= 1 else 0 for c in r] for r in self.light]

    @property
    def lighted(self) -> set:
        return {
            (x, y) for y in range(self.height) for x in range(self.width)
                   if self.square(x, y) == '.' and self.lit(x, y) == 2
        }

    def square(self, x, y):
        return self.world[y][x]

    def blocked(self, x, y):
        return (not 0 <= x < self.width or not 0 <= y < self.height
                or self.world[y][x] in ("#", '+'))
                
    def lit(self, x, y):
        return self.light[y][x]

    def set_lit(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.light[y][x] = 2

    def do_fov(self, x, y, radius):
        "Calculate lit squares from the given location and radius"
        self.reset_light()
        self.set_lit(x, y)
        for oct in range(8):
            self._cast_light(x, y, 1, 1.0, 0.0, radius,
                             self.mult[0][oct], self.mult[1][oct],
                             self.mult[2][oct], self.mult[3][oct])

    def _cast_light(self, cx, cy, row, start, end, radius, xx, xy, yx, yy):
        "Recursive lightcasting function"
        if start < end:
            return
        radius_squared = radius*radius
        for j in range(row, radius + 1):
            dx, dy = -j - 1, -j
            blocked = False
            while dx <= 0:
                dx += 1
                # Translate the dx, dy coordinates into map coordinates:
                X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
                # l_slope and r_slope store the slopes of the left and right
                # extremities of the square we're considering:
                l_slope = (dx - 0.5) / (dy + 0.5)
                r_slope = (dx + 0.5) / (dy - 0.5)
                if start < r_slope:
                    continue
                elif end > l_slope:
                    break
                else:
                    # Our light beam is touching this square; light it:
                    if dx*dx + dy*dy < radius_squared:
                        self.set_lit(X, Y)
                    if blocked:
                        # we're scanning a row of blocked squares:
                        if self.blocked(X, Y):
                            new_start = r_slope
                            continue
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if self.blocked(X, Y) and j < radius:
                            # This is a blocking square, start a child scan:
                            blocked = True
                            self._cast_light(cx, cy, j + 1, start, l_slope,
                                             radius, xx, xy, yx, yy)
                            new_start = r_slope
            # Row is scanned; do next row unless last square was blocked:
            if blocked:
                break