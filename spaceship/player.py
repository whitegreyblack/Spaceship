import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
# from spaceship.objects import Object, Character

def builder() -> object:
    pass

def build_player() -> object:
    """
    background=(name, race, subr, clas)
    _name, _race, _subr, _clas = get_background()
    stats = get_stats(_name, _race, _subr, _clas)/get_stats(background)
    stats = (hp, mp, sp, str, con, dex, wis, int, cha)
    character = new Character(background , stats)
    return character()
    """
    pass

def build_monster() -> object:
    pass

def build_npc() -> object:
    pass

def build_monsters() -> list:
    return

