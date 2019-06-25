# map_configs.py

"""Holds default maps and map functions used for testing"""

# example rooms
def create_empty_room(width: int, height: int):
    room = []
    for h in range(height):
        if h in (0, height - 1):
            row = '#' * width
        else:
            row = '#' + '.' * (width - 2) + '#'
        room.append(row)
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

TEST = """
################################
#....#....#....#....#..........#
#...................#..........#
#....#....#....#....+.....#....#
#...........^.......#..........#
#....#....#....#....#..........#
################################"""[1:]

CORRIDORS = """
#########################
#.....#############.....#
#.....+...........+.....#
#.....#############.....#
#########################"""[1:]

ROOM = """
##########
#...#....#
#........#
#.....#..#
##########"""[1:]

SMALL = """
#######
#.....#
#.....#
#######"""[1:]

LONG = """
###################################################################
#...#.............................................................#
###+#.....#########################################################
#.................................................................#
###################################################################"""[1:]

LARGE = """
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
#.....<..................................................>.....#
#..........................#...................................#
#..............................................................#
#..............................................................#
#..............................................................#
################################################################"""[1:]

ROGUE = """
###################################################
##################.........########################
###############..+...................##############
###############.##.........#########.##############
#.....#########.##.........####..................##
#.....+.........##.........####..................##
#.....#########.##.........####..................##
###########.....###.......#####..................##
###########+########.....######..................##
###..........####################.#################
###..........#################......###############
###..........#################......###############
###################################################"""[1:]

BASIN = """
##########################
#......###################
#......###########.......#
#......+.........+.......#
#......#####'#####.......#
####+#######.#######+#####
##....######.#####.....###
##....######...........###
##....############.....###
##########################"""[1:]

# string maps added to config are pulled from variables() and added to list
dungeons = {
    k.lower(): v for k, v in vars().items()
        if not k.startswith('__') and isinstance(v, str)
}

if __name__ == "__main__":
    print(dungeon.keys())
