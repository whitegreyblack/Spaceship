from imports import *

# Module Types:
""" ----------------------------
    Room Attributes:
        Livable:
            Breathable
            Sleepable
            Eatable
            Workable
        Workable:
            ...
        Sustainable
    Object Attributes
        Washable
        Wearable
        Tearable
        Sittable
        Standable
        Breakable
        Splittable
        Ridable
        Flamable
        Freezable
        Lightable
        Activateable
        Hittable
        Replaceable
#   ----------------------------
    Health:
        Kitchen
        Dining
        GreenHouse
        Medical Bay
    Science:
        Archives
        Labs
        Workstation
    Engineering:
        Engine Room
            Reactors
            Cores
            Turbines
            Engines
        Gas/Liquid Generators
            Combustor
            Cycler
        Raw Material Storage
            Storeroom
            Pantry?
    Security:
        Armory
            Wearables
            Armor
            Weapons
        Hangar
            Ridable
            Vehicles
    Living:
        Officer Offices
            Livable
        Crew Quarters
        Showers
    Situational:
        Science:
            Replication Lab
        Security:
            Robotics Lab
            Prison
            On/Offboard Vehicles
        Storage:
            Cargo Hold
        Engineering:
            Advanced Workstations
            Reactor Core
-------------------------------"""
class Module:
    def __init__(self, name="Module"):
        self.name == name
