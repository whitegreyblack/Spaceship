from bearlibterminal import terminal as term
from collections import namedtuple
from functools import reduce
import textwrap
import random
import math

from ecs.component import (
    Component, Entity, Position, Render, Information, Attribute, Delete, Ai, 
    Damage, Equipment, Inventory, Attribute, Health, Armor
)
from ecs.die import check_sign as check
from ecs.keyboard import Keyboard
from ecs.map import Map, WORLD

# define global game variables
WIDTH, HEIGHT = 0, 0
def init_globals():
    global WIDTH, HEIGHT
    WIDTH = term.state(term.TK_WIDTH)
    HEIGHT = term.state(term.TK_HEIGHT)

# define combat strings
attacked = "[c={}]{}[/c] hits [c={}]{}[/c] for {} damage. ({} -> {})"

# define simple objects
physical_damage = namedtuple("Physical_Damage", "to_hit value")
physical_armor = namedtuple("Physical_Armor", "to_hit value")
magical_damage = namedtuple("Magical_Damage", "to_hit value")
magical_armor = namedtuple("Magical_Armor", "to_hit value")

# define simple functions
double_property_reducer = lambda x, y: (x[0] + y[0], x[1] + y[1])

# -- helper functions -- 
def random_position(floortiles):
    '''Returns a random location using a given set of points reduced by the
    positions already occupied by movable entities on the map
    '''
    tiles = list(floortiles)
    random.shuffle(tiles)
    for p in Position.items:
        if p.moveable:
            tiles.remove(p.at)
    tile = tiles.pop()
    return tile

def letter(index):
    '''Converts an integer value between 0 and 25 to an alphabetical letter'''
    if not 0 <= index <= 25:
        raise ValueError("Cannot make index into letter: Index out of range")
    return chr(ord('a') + index)

def distance(entity, other):
    '''Helper function to calculate distance using euclidean formula'''
    position_e = Position.item(entity)
    position_o = Position.item(other)
    dx = position_o.x - position_e.x
    dy = position_o.y - position_e.y
    return math.sqrt(dx ** 2 + dy ** 2), dx, dy

def towards_target(entity, other):
    '''Helper function to return closest space torwards a targert'''
    d, dx, dy = distance(entity, other)
    return int(round(dx / d)), int(round(dy / d))

# -- Object creation helper functions --
def create_player(entity, floors):
    Position(entity, *random_position(floors))
    Information(entity, name="Hero", race="Human")
    Render(entity, '@')
    Attribute(entity, strength=10)
    Equipment(entity)
    Inventory(entity)
    Damage(entity, to_hit=1, damage="1d4")
    Armor(entity, to_hit=0, armor=2)

def create_enemy(floors):
    entity = Entity()
    Information(entity, race="goblin")
    Render(entity, 'g', "#008800")     
    Damage(entity, to_hit=1, damage="1d6")
    Attribute(entity, strength=6)
    Position(entity, *random_position(floors))
    Ai(entity)

    # entity = Entity()
    # Information(entity, race="rat")
    # Render(entity, 'r', '#664422') 
    # Damage(entity, to_hit=0, damage="1d4")
    # Attribute(entity, strength=3)
    # Position(entity, *random_position(floors))
    # Ai(entity)

def create_weapon(floors):
    e = Entity()
    Render(e, '(', '#00AAAA')
    Information(e, name="sword", race="one-handed weapons")
    Damage(e, to_hit=1, damage="1d6")
    Position(e, *random_position(floors), moveable=False)

    e = Entity()
    Render(e, '(', '#004444')
    Information(e, name="spear", race="two-handed weapons")
    Damage(e, to_hit=2, damage='1d8')
    Damage(e, to_hit=3, damage='2d10')
    Position(e, *random_position(floors), moveable=False)

def create_armor(floors):
    e = Entity()
    Render(e, ']]', '#00FF00')
    Position(e, *random_position(floors), moveable=False)
    Information(e, name="chainmail", race="body armors")
    Armor(e, to_hit=1, armor=2)

    e = Entity()
    Render(e, '[[', '#00AAAA')
    Position(e, *random_position(floors), moveable=False)
    Information(e, name='shield', race="shields")
    Damage(e, to_hit=0, damage='1d6')
    Armor(e, to_hit=2, armor=3)

def base_damage(entity, damage_type):
    '''Gets damage ranges dependent on damage type'''
    all_damages = Damage.item(entity)
    # we still don't know if physical damage exists -- have to filter, reduce
    if all_damages:
        damages = [d.damage.ranges 
                   for d in all_damages if d.damage_type == damage_type]
        if damages:
            return reduce(double_property_reducer, damages)
    return 0, 0

def equipment_damage(entity, damage_type):
    '''Returns equipment damage values dependent on damage type'''
    equipment = Equipment.item(entity)
    if equipment:
        damages = [base_damage(equipped_item, damage_type) 
                   for _, equipped_item in equipment.parts]
        if damages:
            return reduce(double_property_reducer, damages)
    return 0, 0

def total_damage(entity, damage_type):
    '''Returns both base and equipment damage values of specific type'''
    damages = [base_damage(entity, damage_type), 
               equipment_damage(entity, damage_type)]
    return reduce(double_property_reducer, damages)

def base_armor(entity):
    '''Gets armor values dependent on armor type'''
    armors = Armor.item(entity)
    # map and reduce all armor into armor type that we want
    if armors:
        return reduce(double_property_reducer, [a.info for a in armors])
    return 0, 0

def equipment_armor(entity):
    '''Returns armor to_hit and armor value from equipped items'''
    equipment = Equipment.item(entity)
    if equipment:
        # get all instances of armor for every equipped item
        armor = []
        for _, equipped_item in equipment.parts:
            armor.append(base_armor(equipped_item))

        # make sure list is not empty before reducing
        if armor:
            return reduce(double_property_reducer, armor)
    return 0, 0

def total_armor(entity):
    '''Returns total to hit and armor values from base and equipment armor'''
    return reduce(double_property_reducer, 
                  [base_armor(entity), equipment_armor(entity)])

def title_bar(x, y, bars, string, color="#444444"):
    '''Creates a x-axis bar with string at the specified coordinates'''
    index = bars // 2 - len(string) // 2
    term.bkcolor(color)
    term.puts(x, y, ' ' * bars)
    term.bkcolor("#000000")
    term.puts(x + index, y, string)

def action_bar(x, y, bars, strings, color="#444444"):
    '''Max actions should be 8? Could do two lines if need be'''
    length = 0

    # determine string offset depending on number of strings
    if strings:
        length = (bars - 2) // len(strings)

    # background 
    term.bkcolor(color)
    term.puts(x, y, ' ' * bars)
    term.bkcolor("#000000")

    # print each action
    for i, string in enumerate(strings):
        offset = len(string) // 2
        term.puts(x + length * i + offset, y, string)

def plot_bar(x, y, color1, color2, string, bars):
    '''Creates a x-axis bar graph used to show percentages'''
    index = len(string[:bars])
    term.bkcolor(color1)
    term.puts(x, y, string[:bars])
    term.bkcolor(color2)
    term.puts(x + index, y, string[bars:])
    term.bkcolor("#000000")

def draw_entity(position, entity):
    '''Draws entity using its render component if it exists'''
    # get the entity draw properties
    render = Render.item(entity)
    if render:
        revert = False
        background, string = render.string
        
        # change background if it is not black
        if background != "#000000":
            term.bkcolor(background)
            revert = True

        term.puts(*position, string)

        # change background back to black if it was changed
        if revert:
            term.bkcolor('#000000')

def draw_main_menu():
    '''Simple main menu that will be improved later'''
    term.clear()
    term.puts(0, 0, "Play Game")
    term.puts(0, 1, "Exit")
    term.refresh()

    # make sure the key read in is recognized by our keyboard
    key = term.read()
    while key not in Keyboard.MAIN_MENU.keys():
        key = term.read()

    return Keyboard.MAIN_MENU[key]

def draw_create_menu():
    gender_index = 0
    genders = ['Male', 'Female']
    race_index = 0
    races = ['Dwarf', 'Human', 'Elf']
    term.clear()
    title_bar(x=0, y=0, bars=WIDTH, string='Creation Menu')
    term.refresh()
    key = term.read()
    g = Game(world=WORLD)
    g.run()

def system_status(entity):
    '''Draws player information to screen'''

    attribute = Attribute.item(entity)
    information = Information.item(entity)
    s, a, i, mods, attrs = attribute.status

    # attribute bonuses
    strmod, strscore = mods['strength'], attrs['strength']
    agimod, agiscore = mods['agility'], attrs['agility']
    intmod, intscore = mods['intelligence'], attrs['intelligence']
    
    # health stat variables
    hc, hm = attribute.health.status
    health_bars = int((max(0, hc) / hm) * 15)
    health_string = f"HP: {hc:2}/{hm:2}"
    health_string = health_string + ' ' * (15 - len(health_string))

    # mana stat variables
    mc, mm = attribute.mana()
    mana_bars = int((max(0, mc) / mm) * 15) if mm != 0 else 0
    mana_string = f"MP: {mc:2}/{mm:2}"
    mana_string = mana_string + ' ' * (15 - len(mana_string))

    # armor values := BASE_ARMOR + EQ_ARMOR
    armor = physical_armor(*total_armor(entity))
    armor_to_hit = check(armor.to_hit, save_zero=True)
    armor_value = check(armor.value, save_zero=True)

    # variables used in spacing and formatting
    spacer = '-' * 16
    index = 0

    # done with variables -- lets clear the player status screen
    term.clear_area(64, 0, 16, 7)

    # name of player character
    term.puts(65, index, f"{information.title}")
    
    # health and mana bars -- visual ui
    plot_bar(65, index + 1, "#880000", "#440000", health_string, health_bars)
    plot_bar(65, index + 2, "#000088", "#000044", mana_string, mana_bars)
    term.bkcolor("#000000")

    # character attributes: DMG | STR | AGI | INT
    term.puts(65, index + 4, f"AMR: [[{armor_to_hit}, {armor_value}]]")
    term.puts(65, index + 5, f"STR: {s}{check(strmod)}({strscore})")
    term.puts(65, index + 6, f"AGI: {a}{check(agimod)}({agiscore})")
    term.puts(65, index + 7, f"INT: {i}{check(intmod)}({intscore})")
    
    # border between hero status and other unit statuses
    term.puts(64, 8, spacer)

def system_enemy_status(world, entity):
    '''Draws enemy information to screen if they are viewable by player'''
    index = 9
    lighted = world.lighted
    entities_in_range = {
        p.entity for p in Position.items
                 if Ai.item(p.entity) and p.at in lighted
    }

    # clear enemy status area
    term.clear_area(64, 8, 16, 16)

    # we print entities by distance from player entity
    for e in sorted(entities_in_range, key=lambda e: distance(entity, e))[:5]:
        information = Information.item(e)
        attribute = Attribute.item(e)
        render = Render.item(e)
        
        # make sure these objects exist for each entity
        if not bool(information and attribute and render):
            continue

        # health variables
        hc, hm = attribute.health.status
        health_bars = int((hc / hm) * 15)
        health_string = f"HP: {hc:2}/{hm:2}"
        health_string = health_string + ' ' * (15 - len(health_string))
        string = f"[c={render.foreground}]{information.title}[/c]"

        # output name and health
        term.puts(65, index, string)
        plot_bar(65, index+1, "#880000", "#440000", health_string, health_bars)
        index += 2

def system_draw(recalc, world):
    '''Draws the world to screen if recalc is true'''

    if recalc:
        # map offset depending on where map will be drawn
        width_offset = 0
        height_offset = 1

        # clear entire screen -- make sure this is the first draw system
        term.clear_area(0, 0, WIDTH, HEIGHT)
        title_bar(x=0, y=0, bars=64, string="Tiphmore")

        # renders the map according to priority - movable entities to the front
        positions = dict()
        for position in Position.items:
            if position.at in positions:
                if Position.item(positions[position.at]).moveable:
                    continue
            positions[position.at] = position.entity

        # go through map array and color if location is lighted/seen
        for j, row in enumerate(world.world):
            for i, cell in enumerate(row):
                lighted = world.lit(i, j)
                color = "#222222"
                
                if lighted == 2:
                    # we found an entity -- draw it to screen instead of a tile
                    if (i, j) in positions.keys():
                        draw_entity((i + width_offset, j + height_offset), 
                                    positions[(i, j)])
                        continue
                    color = "#999999"

                # if there are no entities then draw the tile properties
                if lighted:
                    term.puts(i + width_offset, 
                              j + height_offset, 
                              f"[c={color}]{cell}[/c]")

def system_draw_all(recalc, world, entity, refresh=True):
    term.clear()

    system_draw(recalc, world)
    system_status(entity)
    system_enemy_status(world, entity)

    if refresh:
        term.refresh()

def system_alive(entity):
    '''Checks if entity is alive by running entity id against Delete items'''
    return entity not in Delete

def system_remove():
    '''Deletes self and components of the Delete entity'''
    # return [e for e in entities if not has(e, Delete)]
    remove = [d.entity for d in Delete.items]
    for entity in remove:
        for subclass in Component.__subclasses__():
            if entity in subclass:
                subclass.remove(entity)
        Entity.instances.remove(entity)
        print(f"Removing {entity}")

def system_update():
    '''Updates variables in health and mana for all entities with an 
    attribute component by iterating and updating inner components.
    '''
    for a in Attribute.items:
        a.health.cur_hp = min(a.health.cur_hp + a.health.regen, 
                              a.health.max_hp)
        a.mana.cur_mp = min(a.mana.cur_mp + a.mana.regen, 
                            a.mana.max_mp)

# def cache(lines):
    #     lines = lines
    #     index = 0
    #     messagelog = []    
    #     def funcwrap(logger):
    #         def wrapper(messages):
    #             nonlocal index, messagelog, lines
    #             current = len(messagelog)
    #             for m in messages:
    #                 for twm in textwrap.wrap(m, term.state(term.TK_WIDTH)):
    #                     messagelog.append(twm)
    #             if len(messagelog) <= lines:
    #                 logger(messagelog)
    #             else:
    #                 logger(messagelog[index:index + lines])
    #             index += len(messagelog) - current
    #         return wrapper
    #     return funcwrap

# @cache(5)
    # def system_logger(messages):
    #     term.clear_area(0, 
    #         term.state(term.TK_HEIGHT) - 5, 
    #         term.state(term.TK_WIDTH), 
    #         5)
    #     for i in range(len(messages)):
    #         try:
    #             # print(messages)
    #             term.puts(0, 
    #                 term.state(term.TK_HEIGHT) - len(messages) + i, 
    #                 messages[i])
    #         except:
    #             break

def get_input():
    '''Returns a validated 3 tuple action determined by key pressed'''
    a, (x, y) = None, (0, 0)

    # do while loop in a pythonic way?
    key = term.read()
    shifted = term.state(term.TK_SHIFT)

    # simplify booleans
    not_exit = key != Keyboard.ESCAPE
    not_arrows = key not in Keyboard.ARROWS.keys()
    not_keypad = key not in Keyboard.KEYPAD.keys()
    not_keyboard = (key, shifted) not in Keyboard.KEYBOARD.keys()

    # loop until valid key is entered
    while not_exit and not_arrows and not_keypad and not_keyboard:
        key = term.read()
        shifted = term.state(term.TK_SHIFT)
        
        not_exit = key != Keyboard.ESCAPE
        not_arrows = key not in Keyboard.ARROWS.keys()
        not_keypad = key not in Keyboard.KEYPAD.keys()
        not_keyboard = (key, shifted) not in Keyboard.KEYBOARD.keys()

    # finally get the right key value after parsing invalid keys
    if key == Keyboard.ESCAPE:
        x, y, = None, None
    elif key in Keyboard.ARROWS.keys():
        x, y = Keyboard.ARROWS[key]
    elif key in Keyboard.KEYPAD.keys():
        x, y = Keyboard.KEYPAD[key]
    elif (key, shifted) in Keyboard.KEYBOARD.keys():
        a = Keyboard.KEYBOARD[(key, shifted)]
    return a, x, y

def take_turn(entity):
    '''Processes ai and player actions into a 4 tuple variable'''

    # default action/position return value
    a, (x, y) = None, (0, 0)

    if entity in Ai:
        other = None

        # checks if ai entity is within view distance of player?chase:random
        for e in Entity.instances:
            if entity != e and e not in Ai and e in Position:
                if Position.item(e).moveable and distance(entity, e)[0] < 7:
                    other = e
                    break

        # the return value for ai's will always be a directional x, y value
        # Don't care about monsters outside radius -- they do whatever            
        if not other:
            x, y = random.randint(-1, 1), random.randint(-1, 1)
        else:
            x, y = towards_target(entity, e)
    else:
        # a :- action variable if action is chosen
        a, x, y = get_input()

        # on escape inputs -- early exit
        if (x, y) == (None, None):
            return None, x, y, False

    return a, x, y, True

def combat(entity, other):
    '''Processes components used in determining combat logic'''

    # get combatant info variables
    iatt = Information.item(entity)
    idef = Information.item(other)
    loggable = bool(iatt and idef)

    ratt = Render.item(entity)
    rdef = Render.item(entity)

    damage = physical_damage(*total_damage(entity, 0))
    magic = magical_damage(*total_damage(entity, 1))
    armor = physical_armor(*total_armor(other))
    health = Attribute.item(other).health

    # finally process the damage output from attacker and apply to defender
    if armor.to_hit < random.randint(1, 20) + damage.to_hit:
        damage_dealt = damage.value - armor.value
        health.cur_hp -= damage_dealt
        term.puts(0, HEIGHT - 1,
                  attacked.format(ratt.foreground, 
                                  iatt.title,
                                  rdef.foreground, 
                                  idef.title,
                                  damage_dealt, 
                                  health.cur_hp + damage_dealt,
                                  health.cur_hp))
        term.refresh()

    if not health.alive:
        Delete(other)

    # term.refresh()
    # term.read()

def item_description(entity):
    '''Returns info about an entity of type item'''

    # make sure entity has at least one of the two components
    damages = Damage.item(entity)
    armors = Armor.item(entity)

    # description changes if entity has variable components 
    if bool(damages and armors):
        damage = f"{''.join(f'{d}' for d in damages)}"
        armor = f"{''.join(f'{a}' for a in armors)}"
        description = f"{armor}{damage}"
    elif damages:
        description = f"{''.join(f'{d}' for d in damages)}"
    else:
        description = f"{''.join(f'{a}' for a in armors)}"        

    return Information.item(entity), description

def draw_inventory(inventory):
    '''Displays items in inventory'''
    term.clear()
    title_bar(x=0, y=0, bars=WIDTH, string="Inventory")

    # displays a different screen if the inventory is empty/nonexistant
    if not inventory or len(inventory.bag) == 0:
        string = "No items in inventory"
        term.puts(WIDTH // 2 - (len(string) // 2), HEIGHT // 2, string)
        action_bar(0, HEIGHT - 1, WIDTH, [])
    else:
        # display variables
        category = 0
        x_offset = 2
        y_offset = 1
        item_index = 0
        item_offset = 2
        
        action_bar(0, HEIGHT - 1, WIDTH, ["[[u]] use",
                                          "[[e]] equip",
                                          "[[d]] detail",
                                          "[[D]] drink",])

        # splits items into item categories
        item_categories = dict()
        for item in inventory.bag:
            info = Information.item(item)
            if info.race in item_categories.keys():
                item_categories[info.race].append(item)
            else:
                item_categories[info.race] = [item]

        # puts items onto screen seperated by categories
        for key, items in sorted(item_categories.items(), key=lambda x: x[0]):
            # only shows categories if there exists an item(s) in the list
            if items:
                y_position = category + item_index + y_offset
                term.puts(x_offset, y_position, key)
                
                # print each item within the category
                for index, item in enumerate(items):
                    info, description = item_description(item)
                    char = letter(item_index)

                    item_index += 1
                    term.puts(x_offset + item_offset, 
                              category + item_index + y_offset, 
                              f"{char}. {info.name:15} {description}")
                category += 1

    term.refresh()

def draw_equipment(equipment):
    '''Displays items in equipment'''
    term.clear()
    title_bar(x=0, y=0, bars=WIDTH, string="Equipment")

    # if equipment exists then show first screen with equipment parts
    if equipment:
        for i, (part, item) in enumerate(equipment.parts):
            name, description = "-", ""
            if item:
                info, description = item_description(item)
                name = info.name
            eqp_str = f"{letter(i)}. {part.title():15}: {name} {description}"
            term.puts(1, i + 2, eqp_str)
    else:
        # secondary screen to show no equipment for entity
        term.puts(WIDTH // 2, HEIGHT // 2, "No equipment")
    term.refresh()

def inventory_pick(entity):
    '''Places item at location of entity into entity inventory if it exists'''
    pickup = False
    # this gets all entities with position components
    items = [
        p.entity for p in Position.items 
                 if not p.moveable and p.at == Position.item(entity).at
    ]
    
    # just print single items for now
    if len(items) == 1:
        item = items.pop()
        Position.remove(item)
        Inventory.item(entity).put_in(item)
        print(f"You put the {Information.item(item).name} in your bag.")
        pickup = True

    # no items on entity position
    if not pickup:
        print("No item where you stand")

def inventory_drop(entity):
    '''Places item from entity invnetory into entity location if it exists'''
    inventory = Inventory.item(entity)
    draw_inventory(inventory)
    key = term.read()
    item = None
    if term.TK_A <= key < term.TK_A + len(inventory.bag):
        item = inventory.bag.pop(key - term.TK_A)
        Position(item, *Position.item(entity).at, moveable=False)
        print(f"You drop the {Information.item(item).name}")

def inventory_show(entity):
    '''Displays inventory and waits for user input to determine next command'''
    inventory = Inventory.item(entity)
    draw_inventory(inventory)
    term.read()

def equipment_show(entity):
    '''Displays equipment and waits for user input to determine next command'''
    equipment = Equipment.item(entity)
    draw_equipment(equipment)
    key = term.read()
    if term.TK_A <= key < term.TK_A + len(equipment.parts):
        part, _ = equipment.parts[key - term.TK_A]
        inventory = Inventory.item(entity)
        if inventory:
            draw_inventory(inventory)
            items = len(inventory.bag)
            key = term.read()
            if items and term.TK_A <= key < term.TK_A + items:
                item = inventory.bag.pop(key - term.TK_A)
                setattr(equipment, part, item)

def system_action(world):
    '''Iterates through each entity of the entity list that can take action'''
    recompute = False
    proceed = True
    for entity in Entity.instances:

        # boolean to control to next entity
        next_entity = False

        # if entity doesnt exist on map or is to be delete -- pass
        if entity not in Position or entity in Delete:
            continue

        # if entity has a position and can move
        position = Position.item(entity)
        if position.moveable:

            # loop until next_entity is false -- only happens on a move command
            while not next_entity:
                # let entity take a move or action turn
                a, x, y, proceed = take_turn(entity)

                # exit early during take_turn function and propagate exit value
                if not proceed:
                    break

                # action variable is set -- determine correct action
                # only specific to certain actions that modify view screen
                if a:
                    if a == "pickup": 
                        inventory_pick(entity)
                    elif a == "inventory":
                        recompute = True
                        inventory_show(entity)
                        system_draw_all(recompute, world, entity)
                    elif a == "equipment":
                        recompute = True
                        equipment_show(entity)
                        system_draw_all(recompute, world, entity)
                    elif a == "drop":
                        inventory_drop(entity)
                    continue

                # x, y is set -- calculate new position to move to
                recompute = True
                next_entity = True
                dx, dy = position.x + x, position.y + y

                # determine if new position is occupied
                if (dx, dy) in world.floors:
                    positions = {
                        position.at: position.entity 
                            for position in Position.items
                            if entity != position.entity
                            and position.moveable
                            and position.entity not in Delete
                    }

                    # free space -- entity can move there
                    if (dx, dy) not in positions.keys():
                        position.x += x
                        position.y += y

                    # entity exists on that position -- fight it
                    else:
                        combat(entity, other=positions[(dx, dy)])

            # check again for proceed outside of the while loop
            if not proceed:
                break

    return proceed, recompute, []

class Game:
    '''Holds the variables used in processing the game
    Player := Entity()
    Dungeon := Map()
    '''

    def __init__(self, world: str):
        '''Initializes all game objects used to run the game'''

        # world variables
        self.dungeon = Map(world)
        self.player = Entity()
        
        # entities -- game objects
        self.eindex = 0     
        create_player(entity=self.player, floors=self.dungeon.floors)
        
        # for i in range(random.randint(5, 7)):
        create_enemy(floors=self.dungeon.floors)
        create_weapon(floors=self.dungeon.floors)
        create_armor(floors=self.dungeon.floors)

    def run(self):
        '''Main driver loop to play game'''

        # loop variables
        proceed = True
        fov_recalc = True
        messages = []

        # run main loop until exit status is recieved
        while proceed:
            self.dungeon.do_fov(*Position.item(self.player).at, 15)
            system_draw_all(fov_recalc, self.dungeon, self.player)

            # read write -- if user presses exit here then quit next loop?
            proceed, fov_recalc, messages = system_action(world=self.dungeon)

            # check if player is still alive 
            if not system_alive(entity=self.player):
                system_draw_all(fov_recalc, self.dungeon, self.player)
                break

            system_remove()
            system_update()

        print('Exit Game' if not proceed else 'You died')
        term.refresh()
        term.read()

if __name__ == "__main__":
    # print(tilemap(world))
    # print(random_position(floortiles))
    # print([c.__name__.lower() for c in Component.__subclasses__()])
    # for i in range(5):
    #     create_player()
    # for i in range(3):
    #     print(random_position())
    term.open()
    init_globals()
    if draw_main_menu() == "pressed play":
        # draw_create_menu()
        g = Game(world=WORLD)
        g.run()
    # term.close()
    # print(COMPONENTS)
    # print(Entity.compdict)
    # import os
    # import psutil
    # process = psutil.Process(os.getpid())
    # print(process.memory_info().rss)