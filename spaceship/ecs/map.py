# map.py

def scroll(position, screen, worldmap):
    """
    Returns the correct starting position between two points given the size of
    the object, size of the view, and current position.
    Parameters:
        @position: current position of player 1D axis
        
        @screen  : size of the screen
        
        @worldmap: size of the map           
    """
    halfscreen = screen // 2
    if position < halfscreen:
        return 0
    elif position >= worldmap - halfscreen:
        return worldmap - screen
    else:
        return position - halfscreen

# example rooms
def create_empty_room(width: int, height: int):
    room = []
    for h in range(height):
        if h in (0, height - 1):
            room.append('#' * width)
        else:
            room.append('#' + '.' * (width - 2) + '#')
    return '\n'.join(room)

WORLD = create_empty_room(80, 25)
HALL = create_empty_room(80, 5)

DUNGEON = """
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
################################################################"""[1:]

TEST = '''
################################
#....#....#....#....#..........#
#...................#..........#
#....#....#....#....+.....#....#
#...........^.......#..........#
#....#....#....#....#..........#
################################'''[1:]


ROOM = """
##########
#...#....#
#........#
#.....#..#
##########"""[1:]


# place all maps in a dictionary to be called through single character keys
EXAMPLES = {
    'W': WORLD,
    'D': DUNGEON,
    'T': TEST,
    'R': ROOM,
    'H': HALL
}

UNSEEN, SEEN, LIGHTED = range(3)

def is_trap(tile: chr):
    return tile == '^'

class Map:
    FULL_VISIBLE = 2 # tiles currently in view
    HALF_VISIBLE = 1 # tiles previously seen but now out of view
    NONE_VISIBLE = 0 # tiles not yet seen and currently undiscovered

    # octants used in field-of-view calculations
    mult = [
            [1,  0,  0, -1, -1,  0,  0,  1],
            [0,  1, -1,  0,  0, -1,  1,  0],
            [0,  1,  1,  0,  0, -1, -1,  0],
            [1,  0,  0,  1, -1,  0,  0, -1]
        ]

    def __init__(self, world: str):
        """Initializes world variables, light, and walkable spaces"""
         # keep raw string in case we need to rebuild
        self.world_raw = world
        self.world = [[c for c in r] for r in world.split('\n')]
        self.height = len(self.world)
        self.width = len(self.world[0])

        # iterates through each position in the map to get floor tiles
        self.floors = set(
            (i, j) 
            for j in range(self.height - 1)
                for i in range(self.width - 1)
                    if self.world[j][i] == '.'
        )

        # create another 2d list to keep track of visiblilty/light levels
        self.init_light()

    def init_light(self):
        """
        Creates a 2d list of lists of size world where each value to 0 or light
        level of NONE_VISIBLE.
        """
        self.light = [[0 for c in r] for r in self.world]

    def reset_light(self):
        """
        Recreates a 2d list of lists of size world and sets each value to 1
        or light level of HALF_VISIBLE if previous light value was 1 or 2
        else the value is kept as 0.
        """
        self.light = [[1 if c >= 1 else 0 for c in r] for r in self.light]

    @property
    def lighted(self) -> set:
        """Returns all positions on map that are not blocked and lit"""
        for y in range(self.height):
            for x in range(self.width):
                if self.lit(x, y) == 2:
                    yield x, y, self.square(x, y)

    def tiles(self) -> set:
        """Returns all positions and characters on the map"""
        for y in range(height):
            for x in range(width):
                yield x, y, self.square(x, y)

    def view(self, player, width=None, height=None) -> set:
        if not width:
            width = self.width

        if not height:
            height = self.height

        for y in range(height):
            for x in range(width):
                l = self.lit(x,  y)
                c = self.square(x, y)
                if l == 2:
                    if c == '#':
                        c = f"[color=#876543]{c}[/color]"
                    else:
                        c = f"[color=#AAAAAA]{c}[/color]"
                    yield x, y, c
                elif l == 1:
                    c = f"[color=#444444]{c}[/color]"
                    yield x, y, c

    def square(self, x: int, y: int):
        '''Returns tile information at target coordinates'''
        return self.world[y][x]

    def affects(self, unit: object):
        """Does things to units depending on their position in the map"""
        tile = self.square(*unit.position)
        if is_trap(tile):
            unit.stats.health -= 1
            return f'You step on a trap. You take damage ({unit.stats.health+1}->{unit.stats.health}).'

    def blocked(self, x: int, y: int):
        return (not 0 <= x < self.width or not 0 <= y < self.height
                or self.world[y][x] in ("#", '+'))
 
    def lit(self, x: int, y: int) -> int:
        '''Returns light level of tile at target coordinates'''
        return self.light[y][x]

    def set_lit(self, x: int, y: int):
        '''Light level at target coordinates is set to maximum value'''
        if 0 <= x < self.width and 0 <= y < self.height:
            self.light[y][x] = LIGHTED

    def do_fov(self, x: int , y: int, radius: int):
        '''Calculate lit squares from the given location and radius'''
        self.reset_light()
        self.set_lit(x, y)
        for oct in range(8):
            self._cast_light(x, y, 1, 1.0, 0.0, radius,
                             self.mult[0][oct], self.mult[1][oct],
                             self.mult[2][oct], self.mult[3][oct])

    def _cast_light(self, cx, cy, row, start, end, radius, xx, xy, yx, yy):
        '''Recursive lightcasting function'''
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

    def output(self, ux, uy, sw, sh):
        """
        ux, uy: position of current unit being centered
        sw, sh: dimensions of the view window
        """
        # determine if there is a need to resize the current map
        mw, mh = min(self.width, sw), min(self.height, sh)
        shorten_x = mw > sw
        shorten_y = mh > sh

        print(mw, mh, shorten_x, shorten_y)

        short_mw = mw + (-sw if shorten_x else 0)
        short_mh = mh + (-sh if shorten_y else 0) 

        print(short_mw, short_mh)

        cam_x = scroll(ux, short_mw, self.width)
        cam_y = scroll(uy, short_mh, self.height)
        ext_x = cam_x + short_mw
        ext_y = cam_y + short_mh

        print(cam_x, cam_y, ext_x, ext_y)

        for y in range(cam_y, ext_y):
            for x in range(cam_x, ext_x):
                l = self.lit(x,  y)
                c = self.square(x, y)
                if l == self.FULL_VISIBLE:
                    if c == '#':
                        c = f"[color=#876543]{c}[/color]"
                    else:
                        c = f"[color=#AAAAAA]{c}[/color]"
                    yield x - cam_x, y - cam_y, c
                elif l == self.HALF_VISIBLE:
                    c = f"[color=#444444]{c}[/color]"
                    yield x - cam_x, y - cam_y, c

if __name__ == "__main__":
    "Implement example program using curses"
    import curses
    from collections import namedtuple

    instructions = {
        curses.KEY_DOWN: (1, 0),
        curses.KEY_UP: (-1, 0),
        curses.KEY_LEFT: (0, -1),
        curses.KEY_RIGHT: (0, 1),
        49: (-1, 1),
        50: (0, 1),
        51: (1, 1),
        52: (-1, 0),
        53: (0, 0),
        54: (1, 0),
        55: (-1, -1),
        56: (0, -1),
        57: (1, -1)
    }

    def example(screen):
        curses.curs_set(0)
        position = namedtuple("Position", "x y")
        player = position(40, 12)
        m = Map(WORLD)

        m.do_fov(*player, 25)
        for x, y, c in m.lighted:
            if x > 79 or y > 23:
                continue
            screen.addch(y, x, c)
        screen.addch(player.y, player.x, '@')
        screen.refresh()
        while True:
            ch = screen.getch()
            if ch == 27 or ch == ord('q'):
                break

            move = instructions.get(ch, None)
            if move:
                player = position(*(sum(p) for p in zip(player, move)))

            print(player)
            m.do_fov(*player, 25)
            for x, y, c in m.lighted:
                if x > 79 or y > 23:
                    continue
                screen.addch(y, x, c)
            screen.addch(player.y, player.x, '@')
            screen.addstr(23, 0, str(ch))

    curses.wrapper(example)