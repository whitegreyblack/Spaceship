from bearlibterminal import terminal as term
from maps import MAPS

dungeon = MAPS.TEST
fov_radius = 10
class Map:
    mult = [
                [1,  0,  0, -1, -1,  0,  0,  1],
                [0,  1, -1,  0,  0, -1,  1,  0],
                [0,  1,  1,  0,  0, -1, -1,  0],
                [1,  0,  0,  1, -1,  0,  0, -1]
            ]
    def __init__(self, data):
        print('init')
        self.data, self.height, self.width = self.dimensions(data)     
        self.light = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.flag = 0

    def dimensions(self, data):
        '''takes in a string map and returns a 2D list map and map dimensions'''
        data = [[col for col in row] for row in data.split('\n')]
        height = len(data)
        width = max(len(col) for col in data)
        return data, height, width

    def square(self, x, y):
        return self.data[y][x]

    def blocked(self, x, y):
        return (x < 0 or y < 0 or x >= self.width or y >= self.height or self.data[y][x] == "#")

    def lit(self, x, y):
        return self.light[y][x] == self.flag
    
    def set_lit(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.light[y][x] = self.flag

    def fov_calc(self, x, y, radius):
        self.flag += 1
        for o in range(8):
            self.sight(x, y, 1, 1.0, 0.0, radius, self.mult[0][o], self.mult[1][o], self.mult[2][o], self.mult[3][o], 0)

    def sight(self, cx, cy, row, start, end, radius, xx, xy, yx, yy, id):
        if start < end:
            return

        radius_squared = radius * radius

        for j in range(row, radius+1):
            dx, dy = -j-1, -j
            blocked = False
            while dx <= 0:
                dx += 1
                X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
                l_slope, r_slope = (dx-0.5)/(dy+0.5), (dx+0.5)/(dy-0.5)
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
                            self.sight(cx, cy, j+1, start, l_slope,
                                             radius, xx, xy, yx, yy, id+1)
                            new_start = r_slope
            # Row is scanned; do next row unless last square was blocked:
            if blocked:
                break

    def output(self, X, Y):
        for x in range(self.width):
            for y in range(self.height):
                if self.lit(x, y):
                    lit = "white"
                else:
                    lit = "grey"
                if x == X and y == Y:
                    ch = "@"
                    lit = "white"
                else:
                    ch = self.square(x, y)
                term.puts(x, y, "[color={}]{}[/color]".format(lit,ch))
        term.refresh()

movement_costs = {
    term.TK_LEFT: (-1, 0),
    term.TK_RIGHT: (1, 0),
    term.TK_DOWN: (0, 1),
    term.TK_UP: (0, -1),
}
def movement(pos, change, factor, low, high):
    '''takes in a 1d axis position and change parameters and returns a new position'''
    updated = pos + change * factor
    return updated if low < updated < high else max(low, min(updated, high))
if __name__ == "__main__":
    term.open()
    px, py = 36, 13
    map = Map(dungeon)

    proceed=True
    while proceed:
        map.fov_calc(px, py, fov_radius)
        map.output(px, py)
        while proceed and term.has_input():
            term.puts(21, 5, 'Got input')
            code = term.read()
            if code in (term.TK_ESCAPE, term.TK_CLOSE):
                term.clear()
                term.puts(10, 6, 'Really Quit? (Y/N)')
                term.refresh()
                code = term.read()
                if code in (term.TK_Y,):
                    proceed = False
            elif code is term.TK_C and term.state(term.TK_CONTROL):
                term.clear()
                term.puts(10, 6, 'Really Quit? (Y/N)')
                term.refresh()
                code = term.read()
                if code in (term.TK_Y,):
                    proceed = False
            elif code in movement_costs.keys():
                x, y = movement_costs[code]
                px, py = px+x, py+y
    import time