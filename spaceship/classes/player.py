from typing import Tuple
from random import randint
from .object import Point
from .color import Color
from .unit import Unit
from .world import World
from .item import Ring, Weapon
from .item import totattr, modattr, sort, curattr
from .items import itemlist, convert
from .equipment import Equipment, parts
from .inventory import Inventory
from spaceship.strings import dump_template

attrs=('str con dex wis int cha hp sp mp acc att_lo att_hi')

class Stats:
    def __init__(self, bstats, jbonus, rbonus, gbonus):
        self.bstats = bstats
        self.gbonus = gbonus
        self.rbonus = rbonus
        self.jbonus = jbonus
        self.initialize_stats()
    
    def initialize_base(self):
        self.str, self.con, self.dex, self.int, self.wis, self.cha = \
                            tuple(s + g + r + c for s, g, r, c in zip(
                                                    self.base_stats,
                                                    self.gender_bonus,
                                                    self.race_bonus,
                                                    self.job_bonus))

# Player should inherit from unit just so during main game loop
# the player class can be accessed in the same way as other units
class Player(Unit):
    def __init__(self, character, name):
        '''Unpacks the character tuple and calculates stats

        Initial position for world and locations are set here
        as well as the bonuses from race, gender and class
        '''
        super().__init__(0, 0, race=character.race)
        self.exp = 0
        self.level = 1
        self.sight_world = round(self.sight_norm / 1.5)
        self.job = character.job
        self.gold = character.gold
        self.gender = character.gender
        self.skills = character.skills
        self.advexp = self.level * 150

        self.equip_weapon_double = False

        self.base_stats = character.stats
        self.job_bonus = character.jbonus
        self.race_bonus = character.rbonus
        self.gender_bonus = character.gbonus
        self.name = name[0].upper() + name[1:]

        # functions after unpacking
        self.setup(character.home)
        self.initialize_base_stats()
        
        self.equipment = character.equipment
        self.inventory = Inventory(character.inventory)

        self.calculate_final_stats()
        self.profile_save_path()
        
    def setup(self, home: str) -> None:
        self.home, self.hpointer = home, World.capitals(home)
        self.world = Point(*self.hpointer)
        self.__height = 0

    def __str__(self):
        return self.name

    def profile_save_path(self):
        name = self.name.replace(' ', '_')
        desc = name + " " + self.job
        hash_desc = str(abs(hash(desc)))
        self.desc = name + "(" + hash_desc + ")"

    def profile(self):
        return (profile[0].format(
            *self.stats_attributes(),
            name=self.name,
            sex=self.gender,
            race=self.race,
            job=self.job), 
            profile[1].format(
                dmg="(" + str(self.dmg_lo) + ", " + str(self.dmg_hi) + ")",
                acc=self.acc))

    def status(self):
        '''
        Returns the string formatted status drawn onto the game screen
        each loop
        '''
        def overloaded(attr):
            '''
            Returns a color value given the total attr value vs current value
            '''
            if getattr(self, totattr(attr)) > getattr(self, attr):
                return "green"
            elif getattr(self, totattr(attr)) < getattr(self, attr):
                return "red"
            return "white"

        return (self.name, self.gender[0], self.race[0], self.job[0], self.level,
            "{}/{}".format(self.exp, self.advexp),
            "{}/{}".format(self.cur_hp, self.tot_hp),
            "{}/{}".format(self.cur_mp, self.tot_mp),
            "{}-{}".format(self.tot_dmg_lo, self.tot_dmg_hi),
            "{}/{}".format(self.tot_dv, self.tot_mr),
            overloaded("str"), self.tot_str,
            overloaded("con"), self.tot_con, 
            overloaded("dex"), self.tot_dex, 
            overloaded("int"), self.tot_int, 
            overloaded("wis"), self.tot_wis, 
            overloaded("cha"), self.tot_cha,
            self.gold)

    @property
    def equipment(self):
        for part, item in self.__equipment.items:
            yield part, item

    @equipment.setter
    def equipment(self, equipment):
        self.__equipment = Equipment(parts, equipment)
        for attr, value in list(self.__equipment.stats()):
            self.stat_update(attr, value)
            self.stat_update_final(attr)

    def equip(self, part, item):
        self.__inventory.remove(item)
        if self.__equipment.equip(part, item):
            for attr, value in list(self.__equipment.stats_by_part(part)):
                self.stat_update(attr, value)
                self.stat_update_final(attr)

    def unequip(self, part):
        for attr, value in list(self.__equipment.stats_by_part(part)):
            self.stat_update(attr, -value)
            self.stat_update_final(attr)

        item =  next(self.__equipment.unequip(part))
        self.__inventory.add(item)

    def item_on(self, index):
        yield next(self.__equipment.item_by_part(index))

    def holding_two_handed_weapon(self):
        return self.__equipment.weapon_slots == 2

    @property
    def inventory(self):
        for group, items in self.__inventory.items:
            yield group, items

    @inventory.setter
    def inventory(self, inventory):
        self.__inventory = inventory

    def inventory_type(self, part):
        for item in self.__inventory.by_type(part):
            yield item

    def inventory_prop(self, prop):
        for item in self.__inventory.by_prop(prop):
            yield item

    def item_add(self, item):
        return self.__inventory.add(item)

    def item_remove(self, item):
        self.__inventory.remove(item)

    def item_use(self, item):
        if hasattr(item, 'use'):
            self.item_remove(item)
            print('used item', {})  
            return True
        return True

    def item_eat(self, item):
        if hasattr(item, 'eat'):
            self.item_remove(item)
            return True
        return False
    
    def initialize_base_stats(self) -> None:
        '''Sets the stats used in determining final statuses'''
        for stat in ('str con dex int wis cha hp mp sp dv mr'.split()):
            setattr(self, stat, 0)
            setattr(self, modattr(stat), 0)
            setattr(self, totattr(stat), 0)

        self.str, self.con, self.dex, self.int, self.wis, self.cha = \
                                    tuple(s + g + r + c for s, g, r, c in zip(
                                                            self.base_stats,
                                                            self.gender_bonus,
                                                            self.race_bonus,
                                                            self.job_bonus))
    
        for stat in 'acc dmg_lo dmg_hi'.split():
            for stat in (stat, modattr(stat), totattr(stat)):
                setattr(self, stat, 0)

        self.acc, self.dmg_lo, self.dmg_hi = 0, 1, 2

    def stats_attributes(self):
        return self.str, self.con, self.dex, self.int, self.wis, self.cha

    def stat_update(self, stat, value):
        current = getattr(self, modattr(stat))
        setattr(self, modattr(stat), current + value)

    def stat_update_final(self, stat):
        base = getattr(self, stat)
        mods = getattr(self, modattr(stat))
        setattr(self, totattr(stat), base + mods)

        if stat in ('hp mp'.split()):
            setattr(self, curattr(stat), base + mods)

    def calculate_final_stats(self) -> None:
        for stat in ('str con dex int wis cha'.split()):
            self.stat_update_final(stat)

        self.calculate_health()
        self.calculate_mana()
        self.calculate_speed()
        self.calculate_attack()

    def calculate_health(self):
        self.hp = self.str + self.con * 2
        self.cur_hp = self.tot_hp = self.hp + self.mod_hp

    def calculate_mana(self):
        self.cur_mp = self.tot_mp = self.tot_int + self.tot_wis * 2

    def calculate_speed(self):
        self.sp = self.tot_dex // 2
        
    def calculate_attack(self):
        '''Damage: (Physical | Magical | Pure)'''
        for stat in ('acc dmg_lo dmg_hi'.split()):
            self.stat_update_final(stat)

    def calculate_accuracy(self) -> int:
        '''Returns 0 for miss, 1 for regular hit, 2 for critical'''
        for var in ('acc dmg_lo dmg_hi'):
            if not hasattr(self, var):
                raise AttributeError("Attack Variables not set")

        chance = randint(0, 20) + self.acc

        if chance <= 1:
            return 0

        elif chance >= 20:
            return 2

        else:
            return 1

    def calculate_attack_damage(self) -> int:
        return randint(self.tot_dmg_lo, self.tot_dmg_hi) # + max(self.str, self.dex)

    def gain_exp(self, exp: int) -> None:
        self.exp += exp

    def check_exp(self) -> bool:
        if self.exp >= self.advexp:
            self.level += 1
            self.exp = 0
            self.advexp = self.level * 150
            return True

        return False

    @property
    def height(self) -> int:
        return self.__height
        
    def move_height(self, move: int) -> None:
        def check_height(move: int) -> int:
            return max(self.__height + move, -1)
        self.__height = check_height(move)
    
    def ascend(self) -> None:
        self.__height = max(self.__height - 1, 0)
    
    def descend(self) -> None:
        self.__height = max(self.__height + 1, 0)

    @property
    def location(self) -> Tuple[int, int]:
        '''returns global position on the world map'''
        return self.world.position

    @location.setter
    def location(self, location: Tuple[int, int]) -> None:
        '''sets global position given a tuple(x,y)'''
        self.world = location    

    def travel(self, dx: int, dy: int) -> None:
        self.location = self.world + (dx, dy)

    def save_location(self) -> None:
        self.last_location = self.location
    
    def get_position_on_enter(self) -> Tuple[float, float]:
        def direction(x: float, y: float) -> Tuple[float, float]:
            '''Normalizes the position of the coordinates from 0 to 1'''
            return (x + 1) / 2, (y + 1) / 2

        if not hasattr(self, "last_location"):
            raise AttributeError("No last location variable")

        try:
            return direction(
                self.last_location[0] - self.wx, 
                self.last_location[1] - self.wy)
        
        except KeyError:
            raise KeyError("Error in -directions-")

    def save_position_local(self) -> None:
        self.last_position_local = self.x, self.y

def dump(hero):
    print(dump_template.format(
        hero.name,
        hero.gender,
        hero.race,
        hero.job,
        hero.level,
        hero.exp))

if __name__ == "__main__":
    pass