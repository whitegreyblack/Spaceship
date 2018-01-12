import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
from spaceship.menus.make import test_hero
from spaceship.strings import stats
from spaceship.classes.item import Ring, Potion
from spaceship.classes.player import Player

def test_ring_protection_ring_left():
    hero = test_hero()
    item = Ring("ring of protection", "=", "grey", ("tot_hp", 10))
    player = Player(*hero.values())
    
    player.inventory_add(item)

    assert item in player.inventory

    result = item.wear(player, 'eq_ring_left')
    
    assert player.eq_ring_left == item
    assert player.cur_hp + item.effect[1] == player.tot_hp
    assert item not in player.inventory

def test_ring_protection_ring_right():
    hero = test_hero()
    item = Ring("ring of protection", "=", "grey", ("tot_hp", 10))
    player = Player(*hero.values())

    player.inventory_add(item)
    ring = player.equipment_remove('eq_ring_right')
    result = item.wear(player, 'eq_ring_right')
    
    assert player.cur_hp + item.effect[1] == player.tot_hp
    assert player.eq_ring_right == item
    assert item not in player.inventory

def test_ring_earth_ring_left():
    hero = test_hero()
    item = Ring("ring of earth", "=", "green", ("mod_str", 1))
    player = Player(*hero.values())

    player.inventory_add(item)
    
    assert player.eq_ring_left == None
    assert type(player.eq_ring_right) == type(item)
    assert item in player.inventory
    assert player.mod_str == 0

    result = item.wear(player, 'eq_ring_left')

    assert player.eq_ring_left == item
    assert item not in player.inventory

    assert player.mod_str == 1
    assert player.mod_str + player.str == player.tot_str + 1

    player.calculate_total_str()
    assert player.mod_str + player.str == player.tot_str

if __name__ == "__main__":
    print(*test_hero())
    print(test_hero())
    print(RingProtection())