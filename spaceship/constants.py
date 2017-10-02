'''Constants used in main and other modules -- equivalent to globals'''
MENU_SCREEN_WIDTH, MENU_SCREEN_HEIGHT = 80, 25
MENU_FONT_WIDTH, MENU_FONT_HEIGHT = 8, 16

GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT = 80, 50
GAME_FONT_WIDTH, GAME_FONT_HEIGHT = 8, 8

FOV_RADIUS = 25

# CHARACTER MENU GLOBALS
CM_TITLE = 1
CM_SUBTITLE = 2
CM_BORDER_WIDTH = 80
CM_BORDER_HEIGHT = ()
CM_COLUMN_WIDTH = 12
CM_COLUMN_START = 1, 15, 27
CM_FOOTER_HEIGHT = 22

# OPTION MENU GLOBALS
OPT_TITLE = 1
OPT_BORDER_WIDTH = 80
OPT_BORDER_HEIGHT = (2, 24)

# ITEM CONSTANTS
ITEM_DROP_RATE=0 # drop rate from monsters in dungeons
ITEM_FIND_RATE=0 # chances item spawns in dungeon
ITEM_PREREVEAL=0 # basically pre identification rate 

# ROOM CONSTANTS
ROOM_MIN_PLACE=0
ROOM_MAX_PLACE=0
ROOM_HALL_SIZE=2
ROOM_DOOR_RATE=0

GAME_TITLE_VERSION="v 0.0.4"
GAME_TITLE_WIDTH=46
GAME_TITLE_HEIGHT=6
GAME_TITLE=''' \
 ___                           _     _       
/  _\_ __   __ _  ___ ___  ___| |__ (_)_ __  
\  \| '_ \ / _` |/ __/ _ \/ __| '_ \| | '_ \ 
_\  \ |_) | (_| | (_|  __/\__ \ | | | | |_) |
\___/ .__/ \__,_|\___\___||___/_| |_|_| .__/ 
    |_|                               |_|    
'''[1:]