 # -*- coding=utf-8 -*-
from typing import Tuple, Union
from namedlist import namedlist
from functools import lru_cache
from collections import namedtuple
from random import randint, choice, shuffle
from bearlibterminal import terminal as term
from spaceship.classes.monsters import Rat
from spaceship.classes.bat import Bat
from spaceship.tools import scroll

'''
The largest difference between World and City map tiles is that you can
enter any tile in a World map that is not water/mountain. Which makes 
more than 75% of the playable map enterable. Compared to city map tiles
which only allow one to five enterable locations if any. This leads to a
consideration of what kind of data structure should be used when storing
levels underneath each map.

For world maps: Use a hashmap(x, y) -> coordinate structure
	we create an empty dictionary. This dictionary stores references to
	locations reached by the player. We initialize it as empty at runtime
	since doing so reduces the amount of memory needed and the dictionary
	will build itself dynamically once the player reaches more and more 
	locations around the map.

For city maps: Use a doubly linked list structure
	we create an none variable [sublevel] which will hold a single reference
	to a location. This leads to a user's ability to iterate through top and
	sub levels by following the parent/child references in each map

TODO: seperate map and dungeon
    Map holds:
        dungeon class
        list of items
        list of units
        list of sight
        list of maps(dungeons) below it 
    World holds:
        list of maps basically a connected linked list?'

    For example
        Overworld 8x8 64 tiles
        Assume half is water so 32 tiles are land 
        Each land tile will hold an overworld map
        for each city in city/village list:
            draw a city tile on the map
            read in the city map from the string file
            these tiles will not be considered land tiles anymore
        there will also be a list of pyramid dungeons throughout the map which will have their own list of 
            dungeons
            these tiles will also not be considered land tiles
        For each land tile that is not a mountain:
            it has a chance to hold a dungeon i guess
'''

MapType = { mt: i for i, mt in enumerate('City Cave Wild World'.split()) }

class Map:
    '''The "ABSTRACT CLASS" that should hold the functions shared across all map class types'''
    Tile = namedlist("Tile", 'char color block_mov, block_lit items light')
    mult = [
                [1,  0,  0, -1, -1,  0,  0,  1],
                [0,  1, -1,  0,  0, -1,  1,  0],
                [0,  1,  1,  0,  0, -1, -1,  0],
                [1,  0,  0,  1, -1,  0,  0, -1]
            ]

    chars_block_move = {"#", "+", "o", "x", "~", "%", "Y", "T"}
    chars_block_light = {"#", "+", "o", "%", "Y", "T"}

    def __init__(self, width, height, map_type):
        self.map_type = MapType[map_type]
        # terminal viewing dimensions
        if not hasattr(self, 'width'):
            self.width = 66
        if not hasattr(self, 'height'):
            self.height = 22
        # self.width, self.height = 66, 22
        self.__parent, self.__sublevel = None, None
        self.map_display_width = min(66, width)
        self.map_display_height = min(22, height)
        self.__units = []
        self.__items = {}

    def build(self) -> None:
        raise NotImplementedError("cannot build the base map class -- use a child map object")

    def __str__(self) -> str:
        return "{}: ({}, {})".format(self.__class__.__name__, self.width, self.height)

    def __repr__(self) -> str:
        return "\n".join("".join(row) for row in self.data)
                
    ###########################################################################
    # Level Initialization, Setup, Terraform and Evaluation                   #
    ###########################################################################
    def dimensions(self) -> None:
        '''takes in a string map and returns a 2D list map and map dimensions'''
        if hasattr(self, 'data'):
            self.height = len(self.data)
            self.width = max(len(col) for col in self.data)
        else:
            raise AttributeError("No self.data")

    def create_tile_map(self) -> None:
        '''Instantiates the tile map and fills the map with tile objects
        This function should only be called once during __init__
        '''
        self.check_data()
        self.check_chars()

        self.tilemap = []   
        for row in self.data:
            cols = []
            for char in row:
                try:
                    chars, hexcodes = self.chars[char]
                except KeyError:
                    raise KeyError("Evaluate Map: {} not in keys".format(char))

                block_mov = char in self.chars_block_move
                block_lit = char not in self.chars_block_light

                tile = self.Tile(
                    char=choice(chars),
                    color=choice(hexcodes),
                    block_mov=block_mov,
                    block_lit=block_lit,
                    items=[],
                    light=0)

                cols.append(tile)
            self.tilemap.append(cols)

    def check_data(self) -> None:
        if not hasattr(self, 'data'):
            raise AttributeError("No self.data")
    
    def check_chars(self) -> None:
        if not hasattr(self, 'chars'):
            raise AttributeError("No self.chars")
    
    def check_exists(self, attrs) -> bool:
        for attr in attrs:
            if not hasattr(self, attr):
                raise AttributeError("No self.{}".format(attr))
        return True

    ###########################################################################
    # Connected Map/Dungeon Functions and Properties                          #
    ###########################################################################
    @property
    def stairs_up(self) -> Union[Tuple[int, int], None]:
        '''Returns the position of the up stairs character on map.
        First call to the stairs will find and save the stairs position.
        Subsequent calls will returns the saved position of the stairs.
        Stairs_up will always return a position since every level has a
        parent level.
        '''
        try:
        # if hasattr(self, "__stairs_up"):
            return self.__stairs_up
        except:
            for y, row in enumerate(self.data):
                for x, char in enumerate(row):
                    if char == "<":
                        self.__stairs_up = x, y
                        return x, y

    @property
    def stairs_down(self) -> Union[Tuple[int, int], None]:
        '''Returns the position of the down stairs character on map.
        First call to stairs_down will find and save the stairs_down position.
        Subsequent calls will returns the saved position of the stairs.
        Unlike stairs_up, stairs_down has the possiblity of being None, or
        not found since the possiblity of no sublevel exists.
        '''        
        try:
            return self.__stairs_down
        except AttributeError:
            # manually look through the map to check for '>'
            for y, row in enumerate(self.data):
                for x, char in enumerate(row):
                    if char == ">":
                        self.__stairs_down = x, y
                        return x, y

    @property
    def parent(self) -> object:
        return self.__parent

    @parent.setter
    def parent(self, location) -> None:
        self.__parent = location

    @property
    def sublevel(self) -> object:
        return self.__sublevel

    @sublevel.setter
    def sublevel(self, sublevel) -> None:
        self.__sublevel = sublevel

    ###########################################################################
    #  Singular Map Functions                                                 #
    ###########################################################################
    def square(self, x, y) -> object:
        # return self.data[y][x]
        return self.tilemap[y][x]

    def within_bounds(self, x, y) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def within_generate_bounds(self, x, y):
        return 6 <= x < self.width - 6 and 2 <= y < self.width - 2

    def out_of_bounds(self, x, y) -> bool:
        return not self.within_bounds(x, y)

    def walkable(self, x, y) -> bool:
        '''Checks for bounds of map and blockable tile objects'''
        return self.within_bounds(x, y) and not self.square(x, y).block_mov

    def viewable(self, x, y) -> bool:
        '''Only acts on objects within the bounds of the map'''
        return self.within_bounds(x, y) and self.square(x, y).block_lit

    def occupied(self, x, y) -> bool:
        '''Only acts on unit objects in the map'''
        return self.within_bounds(x, y) and (x, y) in self.unit_positions

    def blocked(self, x, y) -> bool:
        '''Only acts on objects within the bounds of the map'''
        return self.out_of_bounds(x, y) or self.square(x, y).block_mov

    def is_opened_door(self, x, y) -> bool:
        '''Checks if square character is an open door'''
        return self.square(x, y).char == "/"

    def is_closed_door(self, x, y) -> bool:
        '''Checks if square character is a closed door'''
        return self.square(x,y).char == "+"

    def unblock(self, x, y) -> None:
        '''Sets the square movement block value as not blocked'''
        self.square(x, y).block_mov = False

    def reblock(self, x, y) -> None:
        '''Sets the square movement block value as blocked'''
        self.square(x, y).block_mov = True

    def open_door(self, x, y) -> None:
        '''Checks if door is closed and opens it if true'''
        if self.is_closed_door(x, y):
            self.square(x, y).char = "/"
            self.unblock(x, y)

    def close_door(self, x, y) -> None:
        '''Checks if door is open and closes it if true'''
        if self.is_opened_door(x, y):
            self.square(x, y).char = "+"
            self.reblock(x, y)

    ###########################################################################
    # Sight, Light and Color Functions                                        #
    ###########################################################################
    # Light levels depends on two factors -- discovered and visible
    #                  Discovered | Visible
    # 0 - Unexplored : False      | False
    # 1 - Unex b Vis?: False      | True -- 
    # 2 - Explored   : True       | False
    # 3 - Visible    : True       | True
    ###########################################################################
    def check_light_level(self, x, y) -> int:
        '''Gets the value of light at square specified by x and y'''
        return self.square(x, y).light

    def set_light_level(self, x, y, v) -> None:
        '''Sets the value of light at square specified by x and y'''
        if self.within_bounds(x, y):
            self.square(x, y).light = v

    def lit_reset(self) -> None:
        '''Sets all squares in the map with visible light as visited'''
        for y in range(self.height):
            for x in range(self.width):
                lighted_square = self.square(x, y).light == 2
                if lighted_square:
                    self.square(x, y).light = 1

    def path(self, p1, p2) -> list:
        '''A-star implementation that returns all possible moves'''
        node = namedtuple("Node", "df dg dh parent node")
        openlist = set()
        closelist = []
        openlist.add(node(0, 0, 0, None, p1))

        if debug:
            print("PATH: DISTANCE - {}".format(int(distance(p1, p2)*10)))

        while openlist:
            nodeq = min(sorted(openlist))
            openlist.remove(nodeq)
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (i, j) != (0, 0):
                        neighbor = nodeq.node[0]+i, nodeq.node[1]+j

                        if neighbor == p2:
                            closelist.append(nodeq)
                            return closelist

                        if not self.square(i, j).block_mov: 

                            sg = nodeq.dg + int(distance(nodeq.node, neighbor) * 10)
                            sh = int(distance(neighbor, p2) * 10)
                            sf = sg + sh

                            if any(n.node == neighbor and n.df < sf for n in openlist):
                                pass
                            elif any(n.node == neighbor and n.df < sf for n in closelist):
                                pass
                            else:
                                openlist.add(node(sf, sg, sh, nodeq.node, neighbor))

            closelist.append(nodeq)

        return closelist        

    def fov_calc_blocks(self, x, y, r) -> set:
        '''Returns all values in the map that can be seen from the position(x,y)
        with a sight radius of r
        '''
        def fov_block(cx, cy, row, start, end, radius, xx, xy, yx, yy, id):
            nonlocal vision_tiles
            if start < end:
                return

            radius_squared = radius * radius

            for j in range(row, radius + 1):

                dx, dy = -j - 1, -j
                blocked = False

                while dx <= 0:
                    dx += 1
                    X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
                    l_slope, r_slope = (dx - 0.5) / (dy + 0.5), (dx + 0.5) / (dy - 0.5)
                    
                    if start < r_slope:
                        continue
                    
                    elif end > l_slope:
                        break
                    
                    else:
                        if dx * dx + dy * dy < radius_squared:
                            if self.within_bounds(X, Y):
                                vision_tiles.add((X, Y))
                            # self.set_light_level(X, Y, 2)
                        if blocked:
                            if self.blocked(X, Y) and not self.viewable(X, Y):
                                new_start = r_slope
                                
                            else:
                                blocked = False
                                start = new_start
                        else:
                            if self.blocked(X, Y) and not self.viewable(X, Y) and j < radius:
                                blocked = True
                                fov_block(cx, cy, j + 1, start, l_slope,
                                            radius, xx, xy, yx, yy, id + 1)
                                new_start = r_slope
                if blocked:
                    break

        vision_tiles = set()
        for o in range(8):
            fov_block(x, y, 1, 1.0, 0.0, r,
                        self.mult[0][o], 
                        self.mult[1][o], 
                        self.mult[2][o], 
                        self.mult[3][o], 0)
        # return split_blocks()
        return vision_tiles

    def fov_calc(self, unit) -> None:
        '''Calls sight to calculate which tiles on the map are visible from
        the position (x, y) with a sight radius of r
        '''
        for x, y, radius in unit:
            for o in range(8):
                self.sight(x, y, 1, 1.0, 0.0, radius,
                        self.mult[0][o], 
                        self.mult[1][o], 
                        self.mult[2][o], 
                        self.mult[3][o], 0)

    def unit_fov(self, units) -> None:
        '''Calls sight to calculate which tiles on the map are visible from
        the position of the unit passed in as a parameter
        '''    
        for unit in units:
            for o in range(8):
                self.sight(*unit.local, 1, 1.0, 0.0, unit.sight,
                        self.mult[0][o], 
                        self.mult[1][o], 
                        self.mult[2][o], 
                        self.mult[3][o], 0)

    def sight(self, cx, cy, row, start, end, radius, xx, xy, yx, yy, id):
        '''Calculates all visible tiles on the map using recursive line of
        sight. All calculations are based on linear slopes and light blocking
        values found in every tile square in the map array
        '''
        if start < end:
            return

        radius_squared = radius * radius

        for j in range(row, radius + 1):

            dx, dy = -j - 1, -j
            blocked = False

            while dx <= 0:
                dx += 1
                X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
                # l_slope and r_slope store the slopes of the left and right
                # extremities of the square we're considering:
                l_slope, r_slope = (dx - 0.5) / (dy + 0.5), (dx + 0.5) / (dy - 0.5)
                
                if start < r_slope:
                    continue

                elif end > l_slope:
                    break

                else:
                    # Our light beam is touching this square; light it:
                    if dx * dx + dy * dy < radius_squared:
                        self.set_light_level(X, Y, 2)

                    if blocked:
                        # we're scanning a row of blocked squares:
                        # if self.blocked and self.viewable         - window
                        # if self.blocked and not self.viewable     - wall
                        # if not self.blocked and self.viewable     - floor
                        # if not self.blocked and not self.viewable - empty space
                        if self.blocked(X, Y) and not self.viewable(X, Y):
                        # if self.blocked(X, Y):
                            new_start = r_slope

                        else:
                            blocked = False
                            start = new_start
                    else:
                        if self.blocked(X, Y) and not self.viewable(X, Y) and j < radius:
                        # if self.blocked(X, Y) and j < radius:
                            # This is a blocking square, start a child scan:

                            blocked = True
                            self.sight(cx, cy, j + 1, start, l_slope,
                                        radius, xx, xy, yx, yy, id + 1)
                            new_start = r_slope

            # Row is scanned; do next row unless last square was blocked:
            if blocked:
                break
            
    ###########################################################################
    # Item object Functions                                                   #
    ###########################################################################
    def item_add(self, x, y, item) -> None:
        '''Adds an item object to the list of items at position (x, y)
        on the map
        '''
        self.items_at(x, y).append(item)
        
    def item_remove(self, x, y, item) -> None:
        '''Removes the item object from the list of items at position (x, y)
        on the map
        '''
        self.items_at(x, y).remove(item)

    def items_at(self, x, y) -> list:
        '''Returns a list of item objects at position (x, y) on the map.
        If no items are on the square then the list will return empty
        '''
        return self.square(x, y).items

    ###########################################################################
    # Unit object Functions                                                   #
    ###########################################################################
    @property
    def units(self) -> object:
        '''Yields all units in the unit list'''
        for unit in self.__units:
            yield unit

    @property
    def unit_positions(self) -> Tuple[int, int]:
        '''Yields all unit positions for units in the unit list'''
        for unit in self.units:
            yield unit.local
    
    def unit_ready(self) -> object:
        for unit in self.__units:
            while unit.energy.ready():
                unit.reset()
                yield unit

    def unit_at(self, x, y) -> object:
        '''Returns a unit at the given position. If the unit exists then the
        unit is returned else an empty value is returned'''
        for u in self.__units:
            if (x, y) == u.local:
                return u

    def units_add(self, units) -> None:
        '''Adds a list of units to the current unit list'''
        self.__units += units

    def unit_remove(self, unit) -> None:
        '''Removes the unit from the list of units if the unit is found'''
        try:
            self.__units.remove(unit)

        except ValueError:
            print('No unit with that value')

    def generate_units(self):
        max_units = 25
        if hasattr(self, 'spaces'):
            shuffle(self.spaces)
            for i in range(max_units):
                i, j = self.spaces[randint(0, len(self.spaces)-1)]
                unit = choice([Rat, Rat])(x=i, y=j, speed=45)
                self.__units.append(unit)
                
        else:
            raise AttributeError("Spaces has not yet been initialized")

    ###########################################################################
    # Output and Display Functions                                            #
    ###########################################################################
    def output(self, player_x, player_y):
        # detect if map is smaller than usual
        shorten_x = self.map_display_width > 66
        shorten_y = self.map_display_height > 44

        # get camera location for x coordinate
        cam_x = scroll(
            player_x, 
            self.map_display_width + (-14 if shorten_x else 0), 
            self.width)
        ext_x = cam_x + self.map_display_width + (-14 if shorten_x else 0)
        
        # get camera location for y coordinate
        cam_y = scroll(
            player_y, 
            self.map_display_height + (-6 if shorten_y else 0), 
            self.height)
        ext_y = cam_y + self.map_display_height + (-6 if shorten_y else 0)

        putstr = "[c={}]{}[/c]"
        # height should total 24/25 units
        for y in range(cam_y, ext_y):
            curstr = ""
            yieldptr = None
            # width should total 80 units
            for x in range(cam_x, ext_x):
                if (x, y) == (player_x, player_y):
                    char, color = "@", "white"
                else:
                    light_level = self.check_light_level(x, y)
                    if light_level == 2:
                        if (x, y) in self.unit_positions:
                            unit = self.unit_at(x, y)
                            char, color = unit.character, unit.foreground
                        elif self.square(x, y).items:
                            item = self.square(x, y).items[-1]
                            char, color = item.char, item.color
                        else:
                            square = self.square(x, y)
                            char, color = square.char, square.color
                    elif light_level == 1:
                        square = self.square(x, y)
                        char, color = square.char, "darkest grey"
                    else:
                        char, color = ' ', 'black'
                curstr += putstr.format(color, char)
                # yield (x - cam_x, y - cam_y, color, char)

                if not yieldptr:
                    yieldptr = (x - cam_x, y - cam_y)
                
            if yieldptr and curstr:
                yield yieldptr, curstr

        self.lit_reset()

        # stuff
                # # reset variables every iteration
                # if x == player_x and y == player_y:
                #     # Current position holds your position
                #     ch = "@"
                #     col = "white"

                # elif (x, y) in positions.keys():
                #     # Current position holds a unit
                #     lit = self.check_light_level(x, y)
                #     if lit == 2:
                #         ch = positions[(x, y)].character
                #         col = positions[(x, y)].foreground
                #     elif lit == 1:
                #         ch, col = self.square(x, y).char, 'darkest grey'
                #     else:
                #         ch, col = " ", "black"
                #         pass

                # # Current position holds an item
                # elif self.square(x, y).items:
                #     lit = self.check_light_level(x, y)
                #     if lit == 2:
                #         item = self.square(x, y).items[0]
                #         ch = item.char
                #         col = item.color
                #     elif lit == 1:
                #         ch = self.square(x, y).char
                #         col = self.square(x, y).color
                #     else:
                #         ch = self.square(x, y).char
                #         col = "darkest grey"
                #         pass

                # # # Current position holds a Lamp
                # #     elif (x, y, 10) in self.lamps:
                # #         level = ""
                # #         ch = self.square(x, y).char
                # #         col = "white"

                # # # deal with displaying traps
                # #     elif self.square(x, y).char == '^':
                # #         lit = self.lit(x, y)
                # #         if lit:
                # #             if lit == 2:
                # #                 ch = self.square(x, y).char
                # #                 col = self.square(x, y).color
                # #             else:
                # #                 ch = self.square(x, y).char
                # #                 col = Color.color('grey darkest')
                # #         else:
                # #             ch, col, bkgd = ".", "black", None

                # else:
                #     # all other environment features
                #     lit = self.check_light_level(x, y)
                #     if lit == 2:
                #         ch = self.square(x, y).char
                #         col = self.square(x, y).color
                #     elif lit == 1:
                #         ch = self.square(x, y).char
                #         col = "darkest grey"
                #     else:
                #         ch, col = " ", "black"
                #         pass
                # yield (x - cam_x, y - cam_y, col, ch)

        # print(self.tilemap[10][10])

if __name__ == "__main__":
    pass