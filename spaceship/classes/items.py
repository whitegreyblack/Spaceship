from spaceship.classes.item import Item, Item, Item, Food, Item, Potion

itemlist "":  {
    # TODO -- implement ranged weapons
    # TODO -- implement readable "items": scrolls, tomes

    # -------------------------------------------------
    # (Item\()(\"[a-z ]*\", )(\"[\[\']\", )(\"[a-z]*\", )(\"[a-z]*\", )(\()
    # $1\n\t\t\"tname": $2\n\t\t\"tchar": $3\n\t\t\"tcolor": $4\n\t\t\"teffects": $5
    # -------------------------------------------------

    "horned helmet""": {
        "name": "horned helmet", 
        "char": "[", 
        "color": "grey", 
        "item_type": "helmet",
        "placement": "head", 
        "effects": (
            ("dv", 1), ("str", 1),
        )),
    }

    "metal helmet""": 
        Item(
            "name": "metal helmet", 
            "char": "[", 
            "color": "grey", 
            "item_type": "helmet",
            "placement": "head", 
            "effects": (
                ("dv", 2), ("str", 1),
            )),

    "leather cap""": 
        Item(
            "name": "leather cap", 
            "char": "[", 
            "color": "grey", 
            "item_type": "helmet",
            "placement": "head", 
            "effects": (
                ("dv", 1),
            )),

    "cloth hood""": 
        Item(
			"name": "cloth hood", 
			"char": "[", 
			"color": "grey", 
            "item_type": "helmet",
			"placement": "head", 
            "effects": (
                ("dv", 1),
            )),

    "gold necklace""": 
        Item(
			"name": "gold necklace", 
			"char": "'", 
			"color": "yellow", 
            "item_type": "necklace",
			"placement": "neck", 
            "effects": (
                ("cha", 2),
            )),

    "holy symbol""": 
        Item(
			"name": "holy symbol", 
			"char": "'", 
			"color": "white",             
            "item_type": "necklace",
			"placement": "neck",             
            "effects": (
                ("wis", 2),
            )),

    "whistle""": 
        Item(
            "name": "whistle", 
            "char": "'", 
            "color": "grey", 
            "item_type": "necklace",
            "placement": "neck", 
            "effects": None),

    "amulet of power""": 
        Item(
			"name": "amulet of power", 
			"char": "'", 
			"color": "red", 
            "item_type": "necklace",
			"placement": "neck", 
            "effects": (
                ("str", 2),
            )),

    "elven chainmail""": 
        Item(
			"name": "elven chainmail", 
			"char": "[", 
			"color": "blue", 
            "item_type": "armor",
			"placement": "body", 
            "effects": (
                ("dv", 4), ("mr", -3),
            )),

    "metal armor""": 
        Item(
			"name": "metal armor", 
			"char": "[", 
			"color": "grey", 
            "item_type": "armor",
			"placement": "body", 
            "effects": (
                ("dv", 3), ("mr", -3),
            )),  

    "thick fur coat""": 
        Item(
			"name": "thick fur coat", 
			"char": "[", 
			"color": "grey", 
            "item_type": "armor",
			"placement": "body", 
            "effects": (
                ("dv", 2),
            )),

    "light robe""": 
        Item(
			"name": "light robe", 
			"char": "[", 
			"color": "grey", 
            "item_type": "armor",
			"placement": "body", 
            "effects": (
                ("dv", 1),
            )),
            
    "heavy cloak""":  
        Item(
			"name": "heavy cloak", 
			"char": "[", 
			"color": "grey", 
            "item_type": "armor",
			"placement": "body", 
            "effects": (
                ("dv", 1), ("mr", 2),
            )),

    "leather armor""": 
        Item(
			"name": "leather armor", 
			"char": "[", 
			"color": "grey", 
            "item_type": "armor",
			"placement": "body", 
            "effects": (
                ("dv", 1), ("mr", 2),
            )),

    "thick fur bracers""": 
        Item(
			"name": "thick fur bracers", 
			"char": "~", 
			"color": "grey", 
            "item_type": "hands",
			"placement": "body", 
            "effects": (
                ("dv", 1),
            )),

    "leather bracers""": 
        Item(
			"name": "leather bracers", 
			"char": "[", 
			"color": "grey", 
            "item_type": "hands",
			"placement": "body", 
            "effects": (
                ("dv", 2), ("mr", 1),
            )),

    "cloth gloves""": 
        Item(
			"name": "cloth gloves", 
			"char": "[", 
			"color": "grey", 
            "item_type": "hands",
			"placement": "body", 
            "effects": (
                ("mr", 1),
            )),

    "leather gloves""": 
        Item(
			"name": "leather gloves", 
			"char": "[", 
			"color": "grey", 
            "item_type": "hands",
			"placement": "body", 
            "effects": (
                ("dv", 1), ("mr", 2),
            )),
    
    "rope belt""": 
        Item(
			"name": "rope belt", 
			"char": "[", 
			"color": "green", 
            "item_type": "belt",
            "placement": "waist",
			"effects": (
                ("dv", 0), ("mr", 1),
            )),

   "leather belt""": 
        Item(
            "name": "leather belt", 
            "char": "[", 
            "color": "red",
            "item_type": "belt",
            "placement": "waist",
            "effects": (
                ("dv", 1),
            )),

    "common pants""": 
        Item(
			"name": "common pants", 
			"char": "[", 
			"color": "green", 
            "item_type": "pants",
            "placement": "legs",
			"effects": (
                ("dv", 0), ("mr", 1),
            )),

    # -- Shoes --
    "leather boots""": 
        Item(
            "name": "leather boots", 
            "char": "[", 
            "color": "green", 
            "item_type": "shoes",
            "placement": "feet",
            "effects": (
                ("dv", 1),
            )),

    "metal boots""": 
        Item(
			"name": "metal boots", 
			"char": "[", 
			"color": "grey", 
            "item_type": "shoes",
            "placement": "feet",
			"effects": (
                ("str", 1), ("dv", 0), ("mr", -2),
            )),

    "sandals""": 
        Item(
			"name": "sandals", 
			"char": "[", 
			"color": "green", 
            "item_type": "shoes",
            "placement": "feet",
			"effects": (
                ("dv", 0), ("mr", 0),
            )),

    # -- WEAPONS -- 
    "long spear""": {			
        "name": "long spear", 
        "char": "(", 
        "color": "grey", 
        "item_type": "weapon",
        "placement": {"hand_left", "hand_right"},
        "effects": (
            ("acc", 2), ("dmg", (2, 9)),
        ), 
        "hands": 2
    },

    "silver sword""": {			
        "name": "silver sword", 
        "char": "(", 
        "color": "grey", 
        "item_type": "weapon",
        "placement": {"hand_left", "hand_right"},
        "effects": (
            ("acc", 2), ("dmg", (3, 7)),
        ), 
        "hands": 1
    },

    "battle axe""": {
        "name": "battle axe", 
        "char": "(", 
        "color": "grey", 
        "item_type": "weapon",
        "placement": {"hand_left", "hand_right"},
        "effects": (
            ("acc", -1), ("dmg",  (6, 10)),
        ), 
        "hands": 2),
    }

    "copper pick""": 
        Item(
			"name": "copper pick", 
            "char": "(", 
            "color": "grey", 
            "item_type": "weapon",
            "placement": {"hand_left", "hand_right"},
            "effects": (
                ("acc", -2), ("dmg",  (3, 5)),
            ), 
            "hands": 2),

    "mithril dagger""": 
        {			
			"name": "mithril dagger", 
            "char": "(", 
            "color": "grey", 
            "item_type": "weapon",
            "placement": {"hand_left", "hand_right"},
            "effects": (
                ("acc", 1), ("dmg", (2, 4)),
            ), 
            "hands": 1
		},

    "broadsword""": 
        {			
			"name": "broadsword", 
            "char": "(", 
            "color": "grey", 
            "item_type": "weapon",
            "placement": {"hand_left", "hand_right"},
            "effects": (
                ("acc", 0), ("dmg", (4, 8)),
            ), 
            "hands": 2
		},

    "long sword""": 
        {			
			"name": "long sword", 
            "char": "(", 
            "color": "grey", 
            "item_type": "weapon",
            "placement": {"hand_left", "hand_right"},
            "effects": (
                ("acc", 1), ("dmg", (5, 7)),
            ), 
            "hands": 2
		},

    "medium shield""": 
        Item(
			"name": "medium shield", 
            "char": "[", 
            "color": "grey", 
            "item_type": "weapon",
            "placement": {"hand_left", "hand_right"},
            "effects": (
                ("dv", 2),
            ), 
            "hands": 1),

    "small shield""": 
        Item(
			"name": "small shield", 
            "char": "[", 
            "color": "grey", 
            "item_type": "weapon",
            "placement": {"hand_left", "hand_right"},
            "effects": (
                ("dv", 1),
            ), 
            "hands": 1),

    "mace""": 
        Item(
			"name": "mace", 
            "char": "(", 
            "color": "grey", 
            "item_type": "weapon",
            "placement": {"hand_left", "hand_right"},
            "effects": (
                ("acc", -2), ("dmg", (3, 6))
            ), 
            "hands": 1),

    "warhammer""": 
        Item(
			"name": "warhammer", 
            "char": "(", 
            "color": "dark green",
            "item_type": "weapon",
            "placement": {"hand_left", "hand_right"},
            "effects": (
                ("acc", -3), ("dmg", (8, 15)),
            ), 
            "hands": 2),

    "wooden staff""": 
        {			
			"name": "wooden staff", 
            "char": "(", 
            "color": "grey", 
            "item_type": "weapon",
            "placement": {"hand_left", "hand_right"},
            "effects": (
                ("acc", 3), ("dmg", (3, 5)),
            ), 
            "hands": 2
		},

    "quarterstaff""": 
        {			
            "name": "quarterstaff", 
            "char": "(", 
            "color": "grey", 
            "item_type": "weapon",
            "placement": {"hand_left", "hand_right"},
            "effects": (
                ("acc", 2), ("dmg", (4, 7))
            ),
            "hands": 2
		},

    # short bow,

    # -- RINGS --

    # "ring of regen""": None,
    "ring of protection""":         
        {			
            "name": "ring of protection", 
            "char": "grey", 
            "color": "white", 
            "item_type": "ring",
            "placement": {"ring_left", "ring_right"},
            "effects": (("dv", 2),)
		},

    # "ring of resistance""": None,
    # "ring of darkness""": None,
    # "storm ring""": None,

    "ring of light""": 
        {			
            "name": "ring of light", 
            "char": """: ", 
            "color": "white", 
            "item_type": "ring",
            "placement": {"ring_left", "ring_right"},
            "effects": (("wis", 1),)
		},

    "ring of chaos""": 
        {			
            "name": "ring of chaos", 
            "char": """: ", 
            "color": "dark red", 
            "item_type": "ring",
            "placement": {"ring_left", "ring_right"},
            "effects": (
                ("str", 3), ("con", 3), ("dex", 3), 
                ("int", 3), ("wis", 3), ("cha", 3),
            )
		},

    "ring of ice""": 
        {			
            "name": "ring of ice", 
            "char": """: ", 
            "color": "light blue", 
            "item_type": "ring",
            "placement": {"ring_left", "ring_right"},
            "effects": (
                ("hp", 10),
            )
		},

    "ring of fire""": 
        {
			
            "name": "ring of fire", 
            "char": """: ", 
            "color": "dark red",
            "item_type": "ring",
            "placement": {"ring_left", "ring_right"},
            "effects": (
                ("dmg", 3),
            )
		},

    "ring of water""": 
        {			
            "name": "ring of water", 
            "char": """: ", 
            "color": "dark blue", 
            "item_type": "ring",
            "placement": {"ring_left", "ring_right"},
            "effects": (
                ("sp", 10),
            )
		},

    "ring of lightning""": 
        {			
            "name": "ring of lightning", 
            "char": """: ", 
            "color": "yellow", 
            "item_type": "ring",
            "placement": {"ring_left", "ring_right"},
            "effects": (
                ("wis", 2),
            )
		},

    "ring of earth""": 
        {			
            "name": "ring of earth", 
            "char": """: ", 
            "color": "dark green", 
            "item_type": "ring",
            "placement": {"ring_left", "ring_right"},
            "effects": (
                ("str", 1),
            )
		},

    "ring of nature""": 
        {			
            "name": "ring of nature", 
            "char": """: ", 
            "color": "green", 
            "item_type": "ring",
            "placement": {"ring_left", "ring_right"},
            "effects": (
                ("wis", 1),
            )
		},

    "ring of power""": 
        {			
            "name": "ring of power", 
            "char": """: ", 
            "color": "red", 
            "item_type": "ring",
            "placement": {"ring_left", "ring_right"},
            "effects": (
                ("str", 2), ("dex", 1),
            )
		},
    
    # -- PANTS --
    "leather belt""": 
        Item(
            "name": "leather belt", 
            "char": "[", 
            "color": "green", 
            "placement": "waist", 
            "effects": (
                ("dv", 1),
            )),


    # -- Item --
    "leather boots""": 
        Item(
            "name": "leather boots", 
            "char": "[", 
            "color": "green", 
            "effects": (
                ("dv", 1),
            )),

    "metal boots""": 
        Item(
			"name": "metal boots", 
			"char": "[", 
			"color": "grey", 
			"effects": (
                ("str", 1), ("dv", 0), ("mr", -2),
            )),

    "sandals""": 
        Item(
			"name": "sandals", 
			"char": "[", 
			"color": "green", 
			"effects": (
                ("dv", 0), ("mr", 0),
            )),
    # tome, spellbook, scrolls

    # -- Consumables --
    "small health potion""": 
        Potion(
            "name": "small health potion", 
            "char": "!", 
            "color": "light red", 
            "effects": (
                ('heal', 5),
            )),

    "small mana potion""": 
        Potion(
            "name": "small mana potion", 
            "char": "!", 
            "color": "light blue", 
            "effects": (
                ("gain", 5),
            )),

    # "medium health potion""": Potion("medium health potion", "!", "red", 20),
    # "large health potion""": Potion("large health potion", "!", "red", 30),
    # "small shield potion""": Potion("small shield potion", "!", "blue", 10),

    "berry""": 
        Food(
            "name": "berry", 
            "char": "%", 
            "color": "blue", 
            "effects": (
                ("hr", 1),
            ), 
            "turns": 3),
}

def convert(item)"":
    "try":
        item "":  itemlist[item]
    except KeyE"rror":
        pass
    except TypeE"rror":
        pass    
    return item

def get_all_items()"":
    for key in itemlist.keys()"":
        print(itemlist[key])
        print(itemlist[key].__repr__())
        print()
    print(len(itemlist))

if __name__ "": "":  "__main__""":
    get_all_items()
