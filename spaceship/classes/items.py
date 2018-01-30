from spaceship.classes.item import Item, Food, Potion
from collections import namedtuple

item = namedtuple('Item', 'char color item_type placement hands bonuses effects')
stats = namedtuple('Stats', 'stat abbr value')
itemlist = {
    # TODO -- implement ranged weapons
    # TODO -- implement readable "items": scrolls, tomes

    # -------------------------------------------------
    # (item\()(\"[a-z ]*\", )(\"[\[\']\", )(\"[a-z]*\", )(\"[a-z]*\", )(\()
    # $1\n\t\t\"tname": $2\n\t\t\"tchar": $3\n\t\t\"tcolor": $4\n\t\t\"teffects": $5
    # -------------------------------------------------

    "horned helmet": 
        item(char="[", 
             color="grey", 
             item_type="helmet",
             placement="head", 
             hands=None,
             bonuses=(
                stats("defensive value", "mr", 1), 
                stats("strength", "str", 1),
             ),
             effects=None),

    "metal helmet": 
        item(char="[", 
             color="grey", 
             item_type="helmet",
             placement="head", 
             hands=None,
             bonuses=(
                stats("defensive value", "dv", 2), 
                stats("strength", "str", 1),
             ),
             effects=None),

#     "leather cap": 
#         item( 
#             char="[", 
#             color="grey", 
#             item_type="helmet",
#             placement="head", 
#             effects=(
#                 ("dv", 1),
#             )),

#     "cloth hood": 
#         item(
# 			char="[", 
# 			color="grey", 
#             item_type="helmet",
# 			placement="head", 
#             effects=(
#                 ("dv", 1),
#             )),

#     "gold necklace": 
#         item(
# 			char="'", 
# 			color="yellow", 
#             item_type="necklace",
# 			placement="neck", 
#             effects=(
#                 ("cha", 2),
#             )),

#     "holy symbol": 
#         item(
# 			char="'", 
# 			color="white",             
#             item_type="necklace",
# 			placement="neck",             
#             effects=(
#                 ("wis", 2),
#             )),

#     "whistle": 
#         item( 
#             char="'", 
#             color="grey", 
#             item_type="necklace",
#             placement="neck", 
#             effects=None),

#     "amulet of power": 
#         item(
# 			char="'", 
# 			color="red", 
#             item_type="necklace",
# 			placement="neck", 
#             effects=(
#                 ("str", 2),
#             )),

#     "elven chainmail": 
#         item(
# 			char="[", 
# 			color="blue", 
#             item_type="armor",
# 			placement="body", 
#             effects=(
#                 ("dv", 4), ("mr", -3),
#             )),

#     "metal armor": 
#         item(
# 			char="[", 
# 			color="grey", 
#             item_type="armor",
# 			placement="body", 
#             effects=(
#                 ("dv", 3), ("mr", -3),
#             )),  

    # "thick fur coat": 
    #     item(char="[", 
	# 		 color="grey", 
    #          item_type="armor",
	# 		 placement="body", 
    #          effects=(
    #             ("dv", 2),
    #          ),
    #          hands=None),

#     "light robe": 
#         item(
# 			char="[", 
# 			color="grey", 
#             item_type="armor",
# 			placement="body", 
#             effects=(
#                 ("dv", 1),
#             )),
            
#     "heavy cloak":  
#         item(
# 			char="[", 
# 			color="grey", 
#             item_type="armor",
# 			placement="body", 
#             effects=(
#                 ("dv", 1), ("mr", 2),
#             )),

#     "leather armor": 
#         item(
# 			char="[", 
# 			color="grey", 
#             item_type="armor",
# 			placement="body", 
#             effects=(
#                 ("dv", 1), ("mr", 2),
#             )),

    # "thick fur bracers": 
    #     item(char="~", 
	# 		 color="grey", 
    #          item_type="hands",
	# 		 placement="body", 
    #          effects=(
    #             ("dv", 1),
    #          ),
    #          hands=None),

#     "leather bracers": 
#         item(
# 			 
# 			char="[", 
# 			color="grey", 
#             item_type="hands",
# 			placement="body", 
#             effects=(
#                 ("dv", 2), ("mr", 1),
#             )),

#     "cloth gloves": 
#         item(
# 			 
# 			char="[", 
# 			color="grey", 
#             item_type="hands",
# 			placement="body", 
#             effects=(
#                 ("mr", 1),
#             )),

#     "leather gloves": 
#         item(
# 			 
# 			char="[", 
# 			color="grey", 
#             item_type="hands",
# 			placement="body", 
#             effects=(
#                 ("dv", 1), ("mr", 2),
#             )),
    
#     "rope belt": 
#         item(
# 			 
# 			char="[", 
# 			color="green", 
#             item_type="belt",
#             placement="waist",
# 			effects=(
#                 ("dv", 0), ("mr", 1),
#             )),

#    "leather belt": 
#         item( 
#             char="[", 
#             color="red",
#             item_type="belt",
#             placement="waist",
#             effects=(
#                 ("dv", 1),
#             )),

#     "common pants": 
#         item(
# 			 
# 			char="[", 
# 			color="green", 
#             item_type="pants",
#             placement="legs",
# 			effects=(
#                 ("dv", 0), ("mr", 1),
#             )),

#     # -- Shoes --
#     "leather boots": 
#         item( 
#             char="[", 
#             color="green", 
#             item_type="shoes",
#             placement="feet",
#             effects=(
#                 ("dv", 1),
#             )),

#     "metal boots": 
#         item(
# 			 
# 			char="[", 
# 			color="grey", 
#             item_type="shoes",
#             placement="feet",
# 			effects=(
#                 ("str", 1), ("dv", 0), ("mr", -2),
#             )),

#     "sandals": 
#         item(
# 			 
# 			char="[", 
# 			color="green", 
#             item_type="shoes",
#             placement="feet",
# 			effects=(
#                 ("dv", 0), ("mr", 0),
#             )),

#     # -- WEAPONS -- 
#     "long spear": {			 
#         char="(", 
#         color="grey", 
#         item_type="weapon",
#         placement={"hand_left", "hand_right"},
#         effects=(
#             ("acc", 2), ("dmg", (2, 9)),
#         ), 
#         "hands": 2
#     },

#     "silver sword": {			 
#         char="(", 
#         color="grey", 
#         item_type="weapon",
#         placement={"hand_left", "hand_right"},
#         effects=(
#             ("acc", 2), ("dmg", (3, 7)),
#         ), 
#         "hands": 1
#     },

#     "battle axe": { 
#         char="(", 
#         color="grey", 
#         item_type="weapon",
#         placement={"hand_left", "hand_right"},
#         effects=(
#             ("acc", -1), ("dmg",  (6, 10)),
#         ), 
#         "hands": 2),
#     }

#     "copper pick": 
#         item(
# 			 
#             char="(", 
#             color="grey", 
#             item_type="weapon",
#             placement={"hand_left", "hand_right"},
#             effects=(
#                 ("acc", -2), ("dmg",  (3, 5)),
#             ), 
#             "hands": 2),

#     "mithril dagger": 
#         {			
# 			 
#             char="(", 
#             color="grey", 
#             item_type="weapon",
#             placement={"hand_left", "hand_right"},
#             effects=(
#                 ("acc", 1), ("dmg", (2, 4)),
#             ), 
#             "hands": 1
# 		},

#     "broadsword": 
#         {			
# 			 
#             char="(", 
#             color="grey", 
#             item_type="weapon",
#             placement={"hand_left", "hand_right"},
#             effects=(
#                 ("acc", 0), ("dmg", (4, 8)),
#             ), 
#             "hands": 2
# 		},

#     "long sword": 
#         {			
# 			 
#             char="(", 
#             color="grey", 
#             item_type="weapon",
#             placement={"hand_left", "hand_right"},
#             effects=(
#                 ("acc", 1), ("dmg", (5, 7)),
#             ), 
#             "hands": 2
# 		},

#     "medium shield": 
#         item(
# 			 
#             char="[", 
#             color="grey", 
#             item_type="weapon",
#             placement={"hand_left", "hand_right"},
#             effects=(
#                 ("dv", 2),
#             ), 
#             "hands": 1),

#     "small shield": 
#         item(
# 			 
#             char="[", 
#             color="grey", 
#             item_type="weapon",
#             placement={"hand_left", "hand_right"},
#             effects=(
#                 ("dv", 1),
#             ), 
#             "hands": 1),

#     "mace": 
#         item(
# 			 
#             char="(", 
#             color="grey", 
#             item_type="weapon",
#             placement={"hand_left", "hand_right"},
#             effects=(
#                 ("acc", -2), ("dmg", (3, 6))
#             ), 
#             "hands": 1),

#     "warhammer": 
#         item(
# 			 
#             char="(", 
#             color="dark green",
#             item_type="weapon",
#             placement={"hand_left", "hand_right"},
#             effects=(("acc", -3), ("dmg", (8, 15)),), 
#             "hands": 2),
# difference between written attribute name vs logical attribute name
    # "wooden staff": 
    #     item(char="(", 
    #          color="grey", 
    #          item_type="weapon",
    #          placement={"hand_left", "hand_right"},
    #          effects=(
    #             ("acc", 3), 
    #             ("dmg", (3, 5)),
    #          ), 
    #          hands=2),

#     "quarterstaff": 
#         {			 
#             char="(", 
#             color="grey", 
#             item_type="weapon",
#             placement={"hand_left", "hand_right"},
#             effects=(
#                 ("acc", 2), ("dmg", (4, 7))
#             ),
#             "hands": 2
# 		},

#     # short bow,

#     # -- RINGS --

#     # "ring of regen": None,
    # "ring of protection": 
    #     item(char="=", 
    #          color="white", 
    #          item_type="ring",
    #          placement={"ring_left", "ring_right"},
    #          effects=(("dv", 2),),
    #          hands=None),

#     # "ring of resistance": None,
#     # "ring of darkness": None,
#     # "storm ring": None,

#     "ring of light": 
#         {			 
#             char=": ", 
#             color="white", 
#             item_type="ring",
#             placement={"ring_left", "ring_right"},
#             effects=(("wis", 1),)
# 		},

#     "ring of chaos": 
#         {			 
#             char=": ", 
#             color="dark red", 
#             item_type="ring",
#             placement={"ring_left", "ring_right"},
#             effects=(
#                 ("str", 3), ("con", 3), ("dex", 3), 
#                 ("int", 3), ("wis", 3), ("cha", 3),
#             )
# 		},

#     "ring of ice": 
#         {			 
#             char=": ", 
#             color="light blue", 
#             item_type="ring",
#             placement={"ring_left", "ring_right"},
#             effects=(
#                 ("hp", 10),
#             )
# 		},

#     "ring of fire": 
#         			 
#             char=": ", 
#             color="dark red",
#             item_type="ring",
#             placement={"ring_left", "ring_right"},
#             effects=(
#                 ("dmg", 3),
#             )
# 		},

#     "ring of water": 
#         {			 
#             char=": ", 
#             color="dark blue", 
#             item_type="ring",
#             placement={"ring_left", "ring_right"},
#             effects=(
#                 ("sp", 10),
#             )
# 		},

#     "ring of lightning": 
#         {			 
#             char=": ", 
#             color="yellow", 
#             item_type="ring",
#             placement={"ring_left", "ring_right"},
#             effects=(
#                 ("wis", 2),
#             )
# 		},

#     "ring of earth": 
#             char=": ", 
#             color="dark green", 
#             item_type="ring",
#             placement={"ring_left", "ring_right"},
#             effects=(
#                 ("str", 1),
#             )

    # "ring of nature": 
    #     item(char="=", 
    #          color="green", 
    #          item_type="ring",
    #          placement={"ring_left", "ring_right"},
    #          effects=(
    #             ("wis", 1),
    #          ),
    #          hands=1)
#   "ring of whater":
#       item(ch, col, itype, placement)
#
#
#     "ring of power": 
#         
#             char=": ", 
#             color="red", 
#             item_type="ring",
#             placement={"ring_left", "ring_right"},
#             effects=(
#                 ("str", 2), ("dex", 1),
#             )
    
#     # -- PANTS --
#     "leather belt": 
#         item( 
#             char="[", 
#             color="green", 
#             placement="waist", 
#             effects=(
#                 ("dv", 1),
#             )),


#     # -- item --
#     "leather boots": 
#         item( 
#             char="[", 
#             color="green", 
#             effects=(
#                 ("dv", 1),
#             )),

#     "metal boots": 
#         item(
# 			char="[", 
# 			color="grey", 
# 			effects=(
#                 ("str", 1), ("dv", 0), ("mr", -2),
#             )),

#     "sandals": 
#         item(
# 			char="[", 
# 			color="green", 
# 			effects=(
#                 ("dv", 0), ("mr", 0),
#             )),
#     # tome, spellbook, scrolls

#     # -- Consumables --
#     "small health potion": 
#         Potion( 
#             char="!", 
#             color="light red", 
#             effects=(
#                 ('heal', 5),
#             )),

#     "small mana potion": 
#         Potion( 
#             char="!", 
#             color="light blue", 
#             effects=(
#                 ("gain", 5),
#             )),

#     # "medium health potion": Potion("medium health potion", "!", "red", 20),
#     # "large health potion": Potion("large health potion", "!", "red", 30),
#     # "small shield potion": Potion("small shield potion", "!", "blue", 10),

#     "berry": 
#         Food( 
#             char="%", 
#             color="blue", 
#             effects=(
#                 ("hr", 1),
#             ), 
#             "turns": 3),
}

def build(item_name):
    if isinstance(item_name, str) and item_name in itemlist.keys():
        print(itemlist[item_name])
        return Item(item_name, *itemlist[item_name])
    else:
        return item_name
    
def get_all_items():
    for key in itemlist.keys():
        print(itemlist[key].__repr__())
    print(len(itemlist))

if __name__ == "__main__":
    get_all_items()
