import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
from spaceship.menus.make import test_hero
from spaceship.strings import stats
from spaceship.classes.item import Item, Potion
from spaceship.classes.items import itemlist
from spaceship.classes.player import Player

def test_ring_protection_ring_left():
    hero = test_hero()
    item = itemlist['ring of protection']
    player = Player(*hero.values())
    
    player.item_add(item)

    assert item in list(player.inventory_type('ring_left'))
    assert player.mod_dv == 0

    player.unequip('ring_left')
    player.equip('ring_left', item)

    assert next(player.item_on('ring_left'))[1] == item
    # assert player.mod_hp == item.effect[0][1]
    assert item not in player.inventory

def test_ring_protection_ring_right():
    hero = test_hero()
    item = itemlist['ring of protection']
    player = Player(*hero.values())

    # player.item_add(item)
    # # ring = player.equipment_remove('ring_right')
    # player.unequip('ring_right')
    # # player.equipment.item_by_part('ring_right')
    # player.equip('ring_right', item)
    # # result = item.wear(player, 'ring_right')
    
    # assert player.mod_hp == item.effect[0][1]
    # assert player.ring_right == item
    # assert item not in player.inventory

def test_ring_earth():
    hero = test_hero()
    item = itemlist['ring of protection']
    player = Player(*hero.values())

    # player.inventory_add(item)
    
    # assert player.ring_left is None
    # assert type(player.ring_right) == type(item)
    # assert item in player.inventory
    # assert player.mod_str == 0

    # result = item.wear(player, 'ring_left')

    # assert player.ring_left == item
    # assert item not in player.inventory

    # assert player.mod_str == 1
    # assert player.mod_str + player.str == player.tot_str

def test_ring_power():
    hero = test_hero()
    item = itemlist['ring of protection']
    player = Player(*hero.values())

    # player.inventory_add(item)
    
    # assert player.ring_left is None
    # assert type(player.ring_right) == type(item)
    # assert item in player.inventory
    # assert player.mod_str == 0

    # result = item.wear(player, 'ring_left')

    # assert player.ring_left == item
    # assert item not in player.inventory

    # assert player.mod_str == 1
    # assert player.mod_str + player.str == player.tot_str

    # assert player.mod_dex == 1
    # assert player.mod_dex + player.dex == player.tot_dex

def test_ring_power_two():
    hero = test_hero()
    item = itemlist['ring of protection']
    player = Player(*hero.values())

    # player.unequip('ring_left')
    # assert next(player.item_on('ring_left'))[1] is None
    # assert type(player.ring_right) == type(item)
    # assert item in player.inventory
    # assert player.mod_str == 0
    # assert player.ring_left == item
    # assert item not in player.inventory
    # assert player.mod_str == 1
    # assert player.mod_str + player.str == player.tot_str
    # assert player.mod_dex == 1
    # assert player.mod_dex + player.dex == player.tot_dex

    # item = Ring("ring of power", "=", "green", (("mod_str", 1), ("mod_dex", 1),))
    # assert player.ring_left != item

    # player.inventory_add(item)
    # ring = player.equipment_remove('ring_right')
    # result = item.wear(player, 'ring_right')

    # assert player.mod_str == 2
    # assert player.mod_str + player.str == player.tot_str

    # assert player.mod_dex == 2
    # assert player.mod_dex + player.dex == player.tot_dex

def run_items():
    for _, item in itemlist.items():
        # print(item)
        print(Item(*item))

if __name__ == "__main__":
    run_items()