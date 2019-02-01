from bearlibterminal import terminal as term
from spaceship.screen_functions import center
from importlib import import_module as using
import json
import os

"""
{
    class: Manager,
    node: {
        class: OptionGroup,
        options: [
            {
                class: Option,
                name: str
                options: [
                    str, str, str
                ]
            },
            {
                class: Option,
                name: str
                options: [
                    str, str, str
                ]
            }
        },
    }
}
"""
class OptionManager(object):
    def __init__(self, options=None):
        self.options = options if options else list()

    def __repr__(self):
        options = "\n".join(repr(o) for o in self.options)
        return f"{self.__class__.__name__}({options})"

    def add_option(self, option):
        """Order matters"""
        self.options.append(option)

    def display(self):
        """Let the manager handle what gets printed to screen"""
        pass

    @classmethod
    def unserialize(cls, data):
        """Takes in a json object representing manager state"""
        # should this be able to add current object state values in addition to the data?
        options = []
        module = module_info()
        classname = getattr(module, data['class'])
        options.append(classname.unserialize(data['options']))
        return cls(options)

    def serialize(self, data):
        pass
    
"""
[+] OptionGroup1
[-] OptionGroup2
 > option1
 > option2
 > option3
"""
class OptionGroup(object):
    gid = 0
    def __init__(self, name=None, options=None):
        self.gid = OptionGroup.gid
        OptionGroup.gid += 1

        self.name = name if name else f"OptionGroup {self.gid}"
        self.options = options
        self.index = 0
        if self.options:
            self.value = self.options[self.index]
    
    def __repr__(self):
        options = ''
        if self.options:
            options = "\n".join(repr(o) for o in self.options)
        return f"{self.__class__.__name__}({options})"

    @classmethod
    def unserialize(cls, data):
        # module = module_info()
        # classname = getattr(module, data['class'])
        # options = []
        # for option in data['options']:
        #     options.append(classname.unserialize(option['options'])
        return cls()

"""
|------- option               > [value] | [options,...,options]
"""
class Option(object):
    def __init__(self, name, options, default=-1):
        self.name = name
        self.options = options
        self.index = default if default else 0
        if self.options:
            self.value = self.options[self.index]
    
    def select(self):
        self.index = (self.index + 1) % len(self.options)
        self.value = self.options[self.index]

    @classmethod
    def unserialize(self, data):
        return cls(data['name'], data['options'])

"""
|------- option               > [True | False]
"""
class BoolOption(Option):
    def __init__(self, name, default=False):
        self.name = name
        self.value = False

    def select(self):
        self.value = not self.value

    @classmethod
    def unserialize(self, data):
        return cls(data['name'], data['options'], data['default'])


"""                             [option 1]
|------- option               > [option 2]
                                [option 3]
                                [option 4]
"""
class ListOption(Option):
    def select_previous(self):
        self.index = (self.index - 1) % len(self.options)
        self.value = self.options[self.index]

def file_basename(filename=None):
    if not filename:
        filename = __file__
    return os.path.splitext(os.path.basename(filename))[0]

def module_info(filename=None):
    return using(f"{__package__}.{file_basename(filename)}")

class OptionFactory(object):
    @staticmethod
    def unserialize(data):
        """Takes in a json object representing manager state"""
        # takes in 
        objects = []
        module = module_info()
        print(module.__name__)
        classtype = getattr(module, data['class'])
        print(classtype)
        print(data)
        for manager in data:
            objects.append(getattr(module, manager['class']).unserialize(data['options']))
        return objects

if __name__ == "__main__":
    o = {
        'class': 'OptionManager',
        'options': [
        {
            'class': 'OptionGroup',
            'name': 'header 1',
            'options': {}
        }
        # {
        # 'class': 'OptionGroup'
        # }
        ]
    }
    p = {
        'class': 'OptionGroup',
        'name': 'header 1',
        'options': {}
    }
    # can create more than 1 manager
    # options = OptionFactory.unserialize(o)
    # print(options)
    manager = OptionManager.unserialize(p)
    print(manager)