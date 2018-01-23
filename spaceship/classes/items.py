from spaceship.classes.item import Item, Weapon, Armor, Ring, Food, Shoes, Potion

itemlist = {
    # TODO -- implement ranged weapons
    # TODO -- implement readable items: scrolls, tomes

    # -------------------------------------------------
    # (Armor\()(\"[a-z ]*\", )(\"[\[\']\", )(\"[a-z]*\", )(\"[a-z]*\", )(\()
    # $1\n\t\t\tname=$2\n\t\t\tchar=$3\n\t\t\tcolor=$4\n\t\t\teffects=$5
    # -------------------------------------------------


    "horned helmet": 
        Armor(
            name="horned helmet", 
            char="[", 
            color="grey", 
            placement="head", 
            effects=(
                ("dv", 1), ("str", 1),
            )),

    "metal helmet": 
        Armor(
            name="metal helmet", 
            char="[", 
            color="grey", 
            placement="head", 
            effects=(
                ("dv", 2), ("str", 1),
            )),

    "leather cap": 
        Armor(
            name="leather cap", 
            char="[", 
            color="grey", 
            placement="head", 
            effects=(
                ("dv", 1),
            )),

    "cloth hood": 
        Armor(
			name="cloth hood", 
			char="[", 
			color="grey", 
			placement="head", 
            effects=(
                ("dv", 1),
            )),

    "gold necklace": 
        Armor(
			name="gold necklace", 
			char="'", 
			color="yellow", 
			placement="neck", 
            effects=(
                ("cha", 2),
            )),

    "holy symbol": 
        Armor(
			name="holy symbol", 
			char="'", 
			color="white", 
			placement="neck",             
            effects=(
                ("wis", 2),
            )),

    "whistle": 
        Armor(
            name="whistle", 
            char="'", 
            color="grey", 
            placement="neck", 
            effects=None),

    "amulet of power": 
        Armor(
			name="amulet of power", 
			char="'", 
			color="red", 
			placement="neck", 
            effects=(
                ("str", 2),
            )),

    "elven chainmail": 
        Armor(
			name="elven chainmail", 
			char="[", 
			color="blue", 
			placement="body", 
            effects=(
                ("dv", 4), ("mr", -3),
            )),

    "metal armor": 
        Armor(
			name="metal armor", 
			char="[", 
			color="grey", 
			placement="body", 
            effects=(
                ("dv", 3), ("mr", -3),
            )),  

    "thick fur coat": 
        Armor(
			name="thick fur coat", 
			char="[", 
			color="grey", 
			placement="body", 
            effects=(
                ("dv", 2),
            )),

    "light robe": 
        Armor(
			name="light robe", 
			char="[", 
			color="grey", 
			placement="body", 
            effects=(
                ("dv", 1),
            )),
            
    "heavy cloak":  
        Armor(
			name="heavy cloak", 
			char="[", 
			color="grey", 
			placement="body", 
            effects=(
                ("dv", 1), ("mr", 2),
            )),

    "leather armor": 
        Armor(
			name="leather armor", 
			char="[", 
			color="grey", 
			placement="body", 
            effects=(
                ("dv", 1), ("mr", 2),
            )),

    "thick fur bracers": 
        Armor(
			name="thick fur bracers", 
			char="~", 
			color="grey", 
			placement="body", 
            effects=(
                ("dv", 1),
            )),

    "leather bracers": 
        Armor(
			name="leather bracers", 
			char="[", 
			color="grey", 
			placement="body", 
            effects=(
                ("dv", 2), ("mr", 1),
            )),

    "cloth gloves": 
        Armor(
			name="cloth gloves", 
			char="[", 
			color="grey", 
			placement="body", 
            effects=(
                ("mr", 1),
            )),

    "leather gloves": 
        Armor(
			name="leather gloves", 
			char="[", 
			color="grey", 
			placement="body", 
            effects=(
                ("dv", 1), ("mr", 2),
            )),
    
    "rope belt": 
        Armor(
			name="rope belt", 
			char="[", 
			color="green", 
            placement="waist",
			effects=(
                ("dv", 0), ("mr", 1),
            )),

    "common pants": 
        Armor(
			name="common pants", 
			char="[", 
			color="green", 
            placement="legs",
			effects=(
                ("dv", 0), ("mr", 1),
            )),

    # -- WEAPONS -- 
    "long spear": 
        Weapon(
			name="long spear", 
            char="(", 
            color="grey", 
            effects=(
                ("acc", 2), ("dmg", (2, 9)),
            ), 
            hands=2),

    "silver sword": 
        Weapon(
			name="silver sword", 
            char="(", 
            color="grey", 
            effects=(
                ("acc", 2), ("dmg", (3, 7)),
            ), 
            hands=1),

    "battle axe": 
        Weapon(
			name="battle axe", 
            char="(", 
            color="grey", 
            effects=(
                ("acc", -1), ("dmg",  (6, 10)),
            ), 
            hands=2),

    "copper pick": 
        Weapon(
			name="copper pick", 
            char="(", 
            color="grey", 
            effects=(
                ("acc", -2), ("dmg",  (3, 5)),
            ), 
            hands=2),

    "mithril dagger": 
        Weapon(
			name="mithril dagger", 
            char="(", 
            color="grey", 
            effects=(
                ("acc", 1), ("dmg", (2, 4)),
            ), 
            hands=1),

    "broadsword": 
        Weapon(
			name="broadsword", 
            char="(", 
            color="grey", 
            effects=(
                ("acc", 0), ("dmg", (4, 8)),
            ), 
            hands=2),

    "long sword": 
        Weapon(
			name="long sword", 
            char="(", 
            color="grey", effects=(
                ("acc", 1), ("dmg", (5, 7)),
            ), 
            hands=2),

    "medium shield": 
        Weapon(
			name="medium shield", 
            char="[", 
            color="grey", 
            effects=(
                ("dv", 2),
            ), 
            hands=1),

    "small shield": 
        Weapon(
			name="small shield", 
            char="[", 
            color="grey", 
            effects=(
                ("dv", 1),
            ), 
            hands=1),

    "mace": 
        Weapon(
			name="mace", 
            char="(", 
            color="grey", 
            effects=(
                ("acc", -2), ("dmg", (3, 6))
            ), 
            hands=1),

    "warhammer": 
        Weapon(
			name="warhammer", 
            char="(", 
            color="dark green", 
            effects=(
                ("acc", -3), ("dmg", (8, 15)),
            ), 
            hands=2),

    "wooden staff": 
        Weapon(
			name="wooden staff", 
            char="(", 
            color="grey", 
            effects=(
                ("acc", 3), ("dmg", (3, 5)),
            ), 
            hands=2),

    # "quarterstaff": Weapon("quarterstaff", 
    #     "(", "grey", 2, -1, (4, 9)),
    # short bow,

    # -- RINGS --

    # "ring of regen": None,
    # "ring of protection": None,
    # "ring of resistance": None,
    # "ring of darkness": None,
    # "storm ring": None,

    "ring of light": 
        Ring(
            name="ring of light", 
            char="=", 
            color="white", 
            effects=(("wis", 1),)),

    "ring of chaos": 
        Ring(
            name="ring of chaos", 
            char="=", 
            color="dark red", 
            effects=(
                ("str", 3), ("con", 3), ("dex", 3), 
                ("int", 3), ("wis", 3), ("cha", 3),
            )),

    "ring of ice": 
        Ring(
            name="ring of ice", 
            char="=", 
            color="light blue", 
            effects=(
                ("hp", 10),
            )),

    "ring of fire": 
        Ring(
            name="ring of fire", 
            char="=", 
            color="dark red", 
            effects=(
                ("dmg", 3),
            )),

    "ring of water": 
        Ring(
            name="ring of water", 
            char="=", 
            color="dark blue", 
            effects=(
                ("sp", 10),
            )),

    "ring of lightning": 
        Ring(
            name="ring of lightning", 
            char="=", 
            color="yellow", 
            effects=(
                ("wis", 2),
            )),

    "ring of earth": 
        Ring(
            name="ring of earth", 
            char="=", 
            color="dark green", 
            effects=(
                ("str", 1),
            )),

    "ring of nature": 
        Ring(
            name="ring of nature", 
            char="=", 
            color="green", 
            effects=(
                ("wis", 1),
            )),

    "ring of power": 
        Ring(
            name="ring of power", 
            char="=", 
            color="red", 
            effects=(
                ("str", 2), ("dex", 1),
            )),
    
    # -- PANTS --
    "leather belt": 
        Armor(
            name="leather belt", 
            char="[", 
            color="green", 
            placement="waist", 
            effects=(
                ("dv", 1),
            )),


    # -- Shoes --
    "leather boots": 
        Shoes(
            name="leather boots", 
            char="[", 
            color="green", 
            effects=(
                ("dv", 1),
            )),

    "metal boots": 
        Shoes(
			name="metal boots", 
			char="[", 
			color="grey", 
			effects=(
                ("str", 1), ("dv", 0), ("mr", -2),
            )),

    "sandals": 
        Shoes(
			name="sandals", 
			char="[", 
			color="green", 
			effects=(
                ("dv", 0), ("mr", 0),
            )),
    # tome, spellbook, scrolls

    # -- Consumables --
    "small health potion": 
        Potion(
            name="small health potion", 
            char="!", 
            color="light red", 
            effects=(
                ('heal', 5),
            )),

    "small mana potion": 
        Potion(
            name="small mana potion", 
            char="!", 
            color="light blue", 
            effects=(
                ("gain", 5),
            )),

    # "medium health potion": Potion("medium health potion", "!", "red", 20),
    # "large health potion": Potion("large health potion", "!", "red", 30),
    # "small shield potion": Potion("small shield potion", "!", "blue", 10),

    "berry": 
        Food(
            name="berry", 
            char="%", 
            color="blue", 
            effects=(
                ("hr", 1),
            ), 
            turns=3),
}

def convert(item):
    try:
        item = itemlist[item]
    except KeyError:
        pass
    except TypeError:
        pass    
    return item

def get_all_items():
    for key in itemlist.keys():
        print(itemlist[key])
        print(itemlist[key].__repr__())
        print()
    print(len(itemlist))

if __name__ == "__main__":
    get_all_items()
