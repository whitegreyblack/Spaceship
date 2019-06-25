# map.py

"""
Base map class. Other classes override methods implemented here.
"""

def scroll(position, screen, worldmap):
    """
    Returns the correct starting position between two points given the size of
    the object, size of the view, and current position.
    Parameters:
        position : current position of player 1D axis
        screen   : size of the screen
        worldmap : size of the map
    """
    halfscreen = screen // 2
    if position < halfscreen:
        return 0
    elif position >= worldmap - halfscreen:
        return worldmap - screen
    else:
        return position - halfscreen

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
        """
        Initializes world variables, light, and walkable spaces
        """
         # keep raw string in case we need to rebuild
        self._world = world
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

    def square(self, x: int, y: int):
        """
        Returns tile information at target coordinates
        """
        return self.world[y][x]

    def affects(self, unit: object):
        """
        Does things to units depending on their position in the map
        """
        tile = self.square(*unit.position)
        if is_trap(tile):
            old_health = unit.stats.health
            unit.stats.health -= 1
            new_health = unit.stats.health
            return f'You step on a trap. You take damage ({old_health}->{new_health}).'

    def is_blocked(self, x: int, y: int) -> bool:
        """
        Returns value indicating if position on map is blocked
        """
        x_bounds = 0 <= x < self.width
        y_bounds = 0 <= y < self.height
        unblocked = self.square(x, y) not in ("#", "+")
        return not all((x_bounds, y_bounds, unblocked))
 
    def is_trap(self, x: int, y: int):
        return self.square(x, y) == '^'

    def is_wall(self, x: int, y: int):
        return self.square(x, y) == '#'

    def is_door(self, x: int, y: int):
        return self.square(x, y) in ('+', '/')

    def open_door(self, x: int, y: int):
        if self.is_door(x, y) and self.square(x, y) == '+':
            self.world[y][x] = '/'
    
    def close_door(self, x: int, y:int):
        if self.is_door(x, y) and self.square(x, y) == '/':
            self.world[y][x] = '+'
        
    def lit(self, x: int, y: int) -> int:
        """
        Returns light level of tile at target coordinates
        """
        return self.light[y][x]

    def set_lit(self, x: int, y: int):
        """Light level at target coordinates is set to maximum value"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.light[y][x] = self.FULL_VISIBLE

    def do_fov(self, x: int , y: int, radius: int):
        """Calculate lit squares from the given location and radius"""
        self.reset_light()
        self.set_lit(x, y)
        for oct in range(8):
            self._cast_light(
                cx=x, 
                cy=y, 
                row=1, 
                start=1.0, 
                end=0.0, 
                radius=radius,
                xx=self.mult[0][oct], 
                xy=self.mult[1][oct],
                yx=self.mult[2][oct], 
                yy=self.mult[3][oct]
            )

    def _cast_light(self, cx, cy, row, start, end, radius, xx, xy, yx, yy):
        """Recursive lightcasting function"""
        if start < end:
            return
        radius_squared = radius * radius
        for j in range(row, radius + 1):
            dx, dy = -j-1, -j
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
                    if dx * dx + dy * dy < radius_squared:
                        self.set_lit(X, Y)
                    if blocked:
                        # we're scanning a row of blocked squares:
                        if self.is_blocked(X, Y):
                            new_start = r_slope
                            continue
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if self.is_blocked(X, Y) and j < radius:
                            # This is a blocking square, start a child scan:
                            blocked = True
                            self._cast_light(
                                cx, cy, j + 1, start, l_slope,
                                radius, xx, xy, yx, yy
                            )
                            new_start = r_slope
            # Row is scanned; do next row unless last square was blocked:
            if blocked:
                break

    @property
    def lighted_tiles(self) -> (int, int, str, int):
        """
        Returns all positions on map that are not blocked and lit
        """
        for y in range(self.height):
            for x in range(self.width):
                l = self.lit(x, y)
                if l > 0:
                    yield x, y, self.square(x, y), l

    @property
    def tiles(self) -> (int, int, str, int):
        """
        Returns all positions and characters on the map
        """
        if not width:
            width = self.width
        if not height:
            height = self.height
        for y in range(self.height):
            for x in range(self.width):
                l = self.lit(x, y)
                c = self.square(x, y)
                yield x, y, c, l


if __name__ == "__main__":
    print("Usage: py -m maps -m map")
