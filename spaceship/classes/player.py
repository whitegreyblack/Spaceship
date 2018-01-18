from typing import Tuple
from random import randint

from .color import Color
from .unit import Unit
from .world import World
from .item import Armor, Weapon, Item, items, convert

# Player should inherit from unit just so during main game loop
# the player class can be accessed in the same way as other units
class Equipment:
    '''Tied to body parts'''
    parts=("head", "neck", "body", "arms", "hands", 
           "hand_left", "hand_right", "ring_left", 
           "ring_right", "waist", "legs", "feet")

    def __init__(self, equipment=[]):
        if not equipment:
            for part in self.parts:
                setattr(self, part, None) 

        else:
            for p, part in enumerate(self.parts):
                if not equipment[p]:
                    # No item is set for the current body part
                    setattr(self, part, None) 

                else:
                    # Check to see if the item is defined in the items table already
                    # if defined create the item, else just set the part to the eq
                    try:
                        item = items[equipment[p]]
        
                    except KeyError:
                        item = equipment[p]

                    setattr(self, part, item)
            
                    if hasattr(item, 'equip'):
                        item.equip(self)

        print(list(self.items))

    def by_part(self, index):
        '''Returns the item at the given body part'''
        part = self.parts[index]
        item = getattr(self, part)

        if not item:
            yield part, None

        yield part, item

    @property
    def items(self):
        for part in self.parts:
            yield getattr(self, part)

    def remove(self, part):
        item = getattr(self, part)

        if item:
            if hasattr(item, 'effects'):
                for effect, value in list(item.effects):
                    print(effect, value)
                    print(self, getattr(self, effect))

            # self.inventory_add(item)

        setattr(self, part, None)

    def equip(self, part, item):
        if not getattr(self, part):
            # self.inventory_remove(item)
            setattr(self, part, item)

        else:
            print('Slot is not empty')

class Inventory(list):
    '''Regular list'''
    def __init__(self, items):
        super().__init__()
        self.extend([convert(item) for item in items])

    def by_part(self, part):
        for item in self:
            if hasattr(item, 'placement') and part in item.placement:
                yield item

    @property
    def item(self, item):
        try:
            index = self.index(item)

        except ValueError:
            raise ValueError('No item in inventory with that value')

        else:
            return self.pop(index)

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
        self.calculate_initial_stats()
            
        self.__equipment = Equipment(character.equipment)
        self.__inventory = Inventory(character.inventory)

        self.calculate_final_stats()
        self.calculate_attack_variables()

        self.profile_save_path()
        
    def setup(self, home: str) -> None:
        self.home, self.hpointer = home, World.capitals(home)
        self.wx, self.wy = self.hpointer
        self.wz = 0

    def __str__(self):
        return self.name

    @property
    def equipment(self):
        for part in self.__equipment.items:
            yield part, getattr(self, part)

    @property
    def inventory(self):
        for item in self.__inventory:
            yield item

    def profile_save_path(self):
        name = self.name.replace(' ', '_')
        desc = name + " " + self.job
        self.desc = name + "(" + str(abs(hash(desc))) + ")"

    def profile(self):
        return (profile[0].format(
            *self.stats_attributes(),
            name=self.name,
            sex=self.gender,
            race=self.race,
            job=self.job), 
            profile[1].format(
                dmg="(" + str(self.damage_lower) + ", " + str(self.damage_higher) + ")",
                acc=self.damage_accuracy))

    def status(self):
        return (self.name, self.gender, self.race, self.job, self.level,
            "{}/{}".format(self.exp, self.advexp),
            "{}/{}".format(self.cur_hp, self.tot_hp),
            "{}/{}".format(self.cur_mp, self.tot_mp),
            self.tot_str, self.tot_con, self.tot_dex, 
            self.tot_int, self.tot_wis, self.tot_cha,
            self.gold)

    def stats_unpack(self):
        self.str, self.con, self.dex, self.int, self.wis, self.cha = \
                                    tuple(s + g + r + c for s, g, r, c in zip(
                                                            self.base_stats,
                                                            self.gender_bonus,
                                                            self.race_bonus,
                                                            self.job_bonus))

    def stats_modifiers(self):
        self.mod_str = 0
        self.mod_con = 0
        self.mod_dex = 0
        self.mod_int = 0
        self.mod_wis = 0
        self.mod_cha = 0
        self.mod_hp = 0
        self.mod_mp = 0
        self.mod_sp = 0

    def calculate_initial_stats(self) -> None:
        self.stats_unpack()
        self.stats_modifiers()

    def calculate_final_stats(self) -> None:
        self.calculate_total_str()
        self.calculate_total_con()
        self.calculate_total_dex()
        self.calculate_total_int()
        self.calculate_total_wis()
        self.calculate_total_cha()

        self.calculate_health()
        self.calculate_mana()
        self.calculate_speed()

    def calculate_health(self):
        self.base_hp = self.tot_str + self.tot_con * 2
        self.cur_hp = self.tot_hp = self.base_hp + self.mod_hp

    def calculate_mana(self):
        self.cur_mp = self.tot_mp = self.tot_int * self.tot_wis * 2

    def calculate_speed(self):
        self.sp = self.tot_dex // 2

    def calculate_total_str(self):
        self.tot_str = self.str + self.mod_str

    def calculate_total_con(self):
        self.tot_con = self.con + self.mod_con

    def calculate_total_dex(self):
        self.tot_dex = self.dex + self.mod_dex

    def calculate_total_int(self):
        self.tot_int = self.int + self.mod_int

    def calculate_total_wis(self):
        self.tot_wis = self.wis + self.mod_wis

    def calculate_total_cha(self):
        self.tot_cha = self.cha + self.mod_cha

    def stats_attributes(self):
        return self.str, self.con, self.dex, self.int, self.wis, self.cha

    def calculate_attack_variables(self):
        # two items
        self.damage_accuracy = 0
        self.damage_lower = 0
        self.damage_higher = 0

        print(self.damage_accuracy, self.damage_lower, self.damage_higher)
        for dmgattr in 'accuracy damage_lower damage_higher':
            if hasattr(self.__equipment.hand_left, dmgattr):
                value = getattr(self.__equipment.hand_left, dmgattr)
                setattr(self, dmgattr, value)   

        if not self.damage_accuracy:
            self.damage_accuracy = 1
        if not self.damage_lower:
            self.damage_lower = 1
        if not self.damage_higher:
            self.damage_higher = 2

        print(self.damage_accuracy, self.damage_lower, self.damage_higher)

    def calculate_attack_chance(self) -> int:
        '''Returns 0 for miss, 1 for regular hit, 2 for critical'''
        for var in ('damage_accuracy', 'damage_lower', 'damage_higher'):
            if not hasattr(self, var):
                raise AttributeError("Attack Variables not set")

        chance = randint(0, 20) + self.damage_accuracy

        if chance <= 1:
            return 0

        elif chance >= 20:
            return 2

        else:
            return 1

    def calculate_attack_damage(self) -> int:
        return randint(self.damage_lower, self.damage_higher) # + max(self.str, self.dex)

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
        return self.wz
        
    def move_height(self, move: int) -> None:
        def check_height(move: int) -> int:
            return max(self.wz + move, -1)
        self.wz = check_height(move)
    
    def ascend(self) -> None:
        self.wz = max(self.wz + 1, -1)
    
    def descend(self) -> None:
        self.wz = max(self.wz - 1, -1)

    @property
    def location(self) -> Tuple[int, int]:
        '''returns global position on the world map'''
        return self.wx, self.wy

    @location.setter
    def location(self, location: Tuple[int, int]) -> None:
        '''sets global position given a tuple(x,y)'''
        self.wx, self.wy = location    

    def travel(self, dx: int, dy: int) -> None:
        self.location = (self.wx + dx, self.wy + dy)

    def save_location(self) -> None:
        self.last_location = self.location
        # print('saved {}'.format(self.last_location))
    
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

    def dump(self) -> str:
        '''Prints out player information to terminal'''

        dump_template="""
            [Character Sheet -- Spaceship]
            ======== Player Stats ========
            Name     : {}
            Sex      : {}
            Race     : {}
            Class    : {}

            Level    : {}
            Exp      : {}
            ========   Equipment  ========
            He       :
            Neck     :
            Torso    : Peasant garb
            Ring(L)  :
            Hand(L)  : Sword
            Ring(R)  :
            Hand(R)  :
            Waist    : Thin rope
            Legs     : Common pants
            Feet     : Sandals
            ======== Player Items ========
            ========  Alignments  ========
            ========  Relations   ========
            """[1:]

        return dump_template.format(
            self.name,
            self.gender,
            self.race,
            self.job,
            self.level,
            self.exp)
'''
class Character(Object):
    def __init__(self, n, x, y, i, c='white', r='human', m=10, s=10, b=6, l=5):
        super().__init__(n, x, y, i, c, r)
        self.m=m
        self.s=s
        self.l=l
        self.inventory = Inventory(b)
        self.backpack = Backpack()
'''
if __name__ == "__main__":
    pass