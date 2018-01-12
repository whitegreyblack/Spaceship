import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
from spaceship.menus.make import test_hero
from spaceship.strings import stats
from spaceship.classes.item import Ring, Potion
from spaceship.classes.player import Player

def test_ring_protection_ring_left():
    hero = test_hero()
    item = Ring("ring of protection", "=", "grey", (("mod_hp", 10),))
    player = Player(*hero.values())
    
    player.inventory_add(item)

    assert item in player.inventory
    assert player.mod_hp == 0

    result = item.wear(player, 'eq_ring_left')
    
    assert player.eq_ring_left == item
    assert player.mod_hp == item.effect[0][1]
    assert item not in player.inventory

def test_ring_protection_ring_right():
    hero = test_hero()
    item = Ring("ring of protection", "=", "grey", (("mod_hp", 10),))
    player = Player(*hero.values())

    player.inventory_add(item)
    ring = player.equipment_remove('eq_ring_right')
    result = item.wear(player, 'eq_ring_right')
    
    assert player.mod_hp == item.effect[0][1]
    assert player.eq_ring_right == item
    assert item not in player.inventory

def test_ring_earth():
    hero = test_hero()
    item = Ring("ring of earth", "=", "green", (("mod_str", 1),))
    player = Player(*hero.values())

    player.inventory_add(item)
    
    assert player.eq_ring_left is None
    assert type(player.eq_ring_right) == type(item)
    assert item in player.inventory
    assert player.mod_str == 0

    result = item.wear(player, 'eq_ring_left')

    assert player.eq_ring_left == item
    assert item not in player.inventory

    assert player.mod_str == 1
    assert player.mod_str + player.str == player.tot_str

def test_ring_power():
    hero = test_hero()
    item = Ring("ring of power", "=", "green", (("mod_str", 1), ("mod_dex", 1),))
    player = Player(*hero.values())

    player.inventory_add(item)
    
    assert player.eq_ring_left is None
    assert type(player.eq_ring_right) == type(item)
    assert item in player.inventory
    assert player.mod_str == 0

    result = item.wear(player, 'eq_ring_left')

    assert player.eq_ring_left == item
    assert item not in player.inventory

    assert player.mod_str == 1
    assert player.mod_str + player.str == player.tot_str

    assert player.mod_dex == 1
    assert player.mod_dex + player.dex == player.tot_dex

def test_ring_power_two():
    hero = test_hero()
    item = Ring("ring of power", "=", "green", (("mod_str", 1), ("mod_dex", 1),))
    player = Player(*hero.values())

    player.inventory_add(item)
    
    assert player.eq_ring_left is None
    assert type(player.eq_ring_right) == type(item)
    assert item in player.inventory
    assert player.mod_str == 0

    result = item.wear(player, 'eq_ring_left')

    assert player.eq_ring_left == item
    assert item not in player.inventory

    assert player.mod_str == 1
    assert player.mod_str + player.str == player.tot_str

    assert player.mod_dex == 1
    assert player.mod_dex + player.dex == player.tot_dex

    item = Ring("ring of power", "=", "green", (("mod_str", 1), ("mod_dex", 1),))
    assert player.eq_ring_left != item

    player.inventory_add(item)
    ring = player.equipment_remove('eq_ring_right')
    result = item.wear(player, 'eq_ring_right')

    assert player.mod_str == 2
    assert player.mod_str + player.str == player.tot_str

    assert player.mod_dex == 2
    assert player.mod_dex + player.dex == player.tot_dex

if __name__ == "__main__":
    print(*test_hero())
    print(test_hero())
    print(RingProtection())