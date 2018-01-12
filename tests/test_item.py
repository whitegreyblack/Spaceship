import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
from spaceship.menus.make import test_hero
from spaceship.strings import stats
from spaceship.classes.item import Ring, RingProtection
from spaceship.classes.player import Player

def test_ring_protection():
    hero = test_hero()

    player = Player(*hero.values())
    
    item = RingProtection()
    player.inventory_add(item)

    assert item in player.inventory

    result = item.wear(player, 'eq_ring_left')
    
    assert player.cur_health + item.effect[1] == player.max_health
    assert player.eq_ring_left == item
    assert item not in player.inventory
    
if __name__ == "__main__":
    print(*test_hero())
    print(test_hero())
    print(RingProtection())