from spaceship.classes.item import Item, Weapon, Armor, Ring, Food, Shoes, Potion

itemlist = {
    # TODO -- implement shields
    # TODO -- implement ranged weapons
    # TODO -- implement readable items: scrolls, tomes
    "horned helmet": 
        Armor(
            name="horned helmet", 
            char="[", 
            color="grey", 
            placement="head", 
            effects=(("dv", 1), ("str", 1),)),

    "metal helmet": 
        Armor(
            name="metal helmet", 
            char="[", 
            color="grey", 
            placement="head", 
            effects=(("dv", 2), ("str", 1),)),

    "leather cap": 
        Armor("leather cap", "[", "grey", "head", (
            ("dv", 1),
        )),

    "cloth hood": 
        Armor("cloth hood", "[", "grey", "head", (
            ("dv", 1),
        )),

    "gold necklace": 
        Armor("gold necklace", "'", "yellow", "neck", (
            ("cha", 2),
        )),

    "holy symbol": 
        Armor("holy_symbol", "'", "white", "neck", (
            ("wis", 2),
        )),

    "whistle": 
        Armor("whistle", "'", "grey", "neck", None),

    "amulet of power": 
        Armor("amulet of power", "'", "red", "neck", (
            ("str", 2),
        )),

    "elven chainmail": 
        Armor("elven chainmail", "[", "blue", "body", (
            ("dv", 4), ("mr", -3),
        )),

    "metal armor": 
        Armor("metal armor", "[", "grey", "body", (
            ("dv", 3), ("mr", -3),
        )),  

    "thick fur coat": 
        Armor("thick fur coat", "[", "grey", "body", (
            ("dv", 2),
        )),

    "light robe": 
        Armor("light robe", "[", "grey", "body", (
            ("dv", 1),
        )),
        
    "heavy cloak":  
        Armor("heavy cloak", "[", "grey", "body", (
            ("dv", 1), ("mr", 2),
        )),

    "leather armor": 
        Armor("leather armor", "[", "grey", "body", (
            ("dv", 1), ("mr", 2),
        )),

    "thick fur bracers": 
        Armor("thick fur bracers", "~", "grey", "body", (
            ("dv", 1),
        )),

    "leather bracers": 
        Armor("leather bracers", "[", "grey", "body", (
            ("dv", 2), ("mr", 1),
        )),

    "cloth gloves": 
        Armor("cloth gloves", "[", "grey", "body", (
            ("mr", 1),
        )),

    "leather gloves": 
        Armor("leather gloves", "[", "grey", "body", (
            ("dv", 1), ("mr", 2),
        )),
    
    # -- WEAPONS -- 
    "long spear": 
        Weapon("long spear", "(", "grey", (
            ("acc", 2), ("dmg", (2, 9)),
        ), hands=2),

    "silver sword": 
        Weapon("silver sword", "(", "grey", (
            ("acc", 2), ("dmg", (3, 7)),
        ), hands=1),

    "battle axe": 
        Weapon("battle axe", "(", "grey", (
            ("acc", -1), ("dmg",  (6, 10)),
        ), hands=2),

    "copper pick": 
        Weapon("copper pick", "(", "grey", (
            ("acc", -2), ("dmg",  (3, 5)),
        ), hands=2),

    "mithril dagger": 
        Weapon("mithril dagger", "(", "grey", (
            ("acc", 1), ("dmg", (2, 4)),
        ), hands=1),

    "broadsword": 
        Weapon("broadsword", "(", "grey", (
            ("acc", 0), ("dmg", (4, 8)),
        ), hands=2),

    "long sword": 
        Weapon("long sword", "(", "grey", (
            ("acc", 1), ("dmg", (5, 7)),
        ), hands=2),

    "medium shield": 
        Weapon("medium shield", "[", "grey", (
            ("dv", 2),
        ), hands=1),

    "small shield": 
        Weapon("small shield", "[", "grey", (
            ("dv", 1),
        ), hands=1),

    "mace": 
        Weapon("mace", "(", "grey", (
            ("acc", -2), ("dmg", (3, 6))
        ), hands=1),

    "warhammer": 
        Weapon("warhammer", "(", "dark green", (
            ("acc", -3), ("dmg", (8, 15)),
        ), hands=2),

    "wooden staff": 
        Weapon("wooden staff", "(", "grey", (
            ("acc", 3), ("dmg", (3, 5)),
        ), hands=2),

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
        Ring("ring of light", '=', "white", (
            ("wis", 1),
        )),

    "ring of chaos": 
        Ring("ring of chaos", "=", "dark red", (
            ("str", 3), ("con", 3), ("dex", 3), 
            ("int", 3), ("wis", 3), ("cha", 3),
        )),

    "ring of ice": 
        Ring("ring of ice", "=", "light blue", (
            ("hp", 10),
        )),

    "ring of fire": 
        Ring("ring of fire", "=", "dark red", (
            ("dmg", 3),
        )),

    "ring of water": 
        Ring("ring of water", "=", "dark blue", (
            ("sp", 10),
        )),

    "ring of lightning": 
        Ring("ring of lightning", "=", "yellow", (
            ("wis", 2),
        )),

    "ring of earth": 
        Ring("ring of earth", "=", "dark green", (
            ("str", 1),
        )),

    "ring of nature": 
        Ring("ring of nature", "=", "green", (
            ("wis", 1),
        )),

    "ring of power": 
        Ring("ring of power", "=", "red", (
            ("str", 2), 
            ("dex", 1),
        )),
    
    # -- PANTS --
    "leather belt": 
        Armor("leather belt", "[", "green", "waist", (
            ("dv", 1),
        )),

    # "rope belt": Armor("rope belt", "[", "green", "waist", 0, 0, 1, 0),
    # "common pants": Armor("common pants", "[", "green", "legs", 0, 0, 0, 0),

    # -- Shoes --
    "leather boots": 
        Shoes(
            name="leather boots", 
            char="[", 
            color="green", 
            effects=(("dv", 1),)),

    # "metal boots": Armor("metal boots", "[", "grey", "feet", 0, 0, 0, 0),
    # "sandals": Armor("sandals", "[", "green", "feet", 0, 0, 0, 0),
    # tome, spellbook, scrolls

    # -- Consumables --
    "small health potion": 
        Potion(
            name="small health potion", 
            char="!", 
            color="light red", 
            effects=(('heal', 5),)),

    "small mana potion": 
        Potion(
            name="small mana potion", 
            char="!", 
            color="light blue", 
            effects=(("gain", 5),)),

    # "medium health potion": Potion("medium health potion", "!", "red", 20),
    # "large health potion": Potion("large health potion", "!", "red", 30),
    # "small shield potion": Potion("small shield potion", "!", "blue", 10),

    "berry": 
        Food(
            name="berry", 
            char="%", 
            color="blue", 
            effects=(("hr", 1),), turns=3),
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
        
def check_item(classifier, item):
    try:
        print(itemlist[classifier][item])
    except KeyError:
        raise KeyError("Classifier or item name is wrong")

if __name__ == "__main__":
    get_all_items()
