import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from collections import namedtuple

class Config:
    def __init__(self, cfg_path):
        with open(cfg_path, 'r') as cfg:
            self.lines = cfg.readlines()
        self.units = []
        self.parse()

    def parse(self):
        unit = namedtuple("Unit", "race unit")
        modifier = ""
        for line in self.lines:
            line = line.strip()
            if line.startswith('#'):
                pass
            elif line.startswith('['):
                modifier = line.replace('[','').replace(']', '').lower()
            else:
                job, number = line.split()
                if modifier == "":
                    raise ValueError("Configuration: file has no race specifier")
                for _ in range(int(number)):
                    self.units.append(unit(modifier, job.lower()))
                
    def build(self):
        '''Builds all units and returns the unit list'''
        # TODO npc builder (character/creature)
        return self.units

    def dump(self):
        if self.units:
            for r, u in self.units:
                print(r, u)
        else:
            raise ValueError("Configuration: class has no units yet")

if __name__ == "__main__":
    path = "./assets/maps/shadowbarrow.cfg"
    cfg = Config(path)
    cfg.dump()
