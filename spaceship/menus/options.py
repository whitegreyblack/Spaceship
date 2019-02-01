from bearlibterminal import terminal as term
from spaceship.screen_functions import center
from importlib import import_module as using
import json
import os


class OptionManager(object):
    def __init__(self, options=None):
        self.options = options if options else list()

    def __repr__(self):
        options = ", ".join(repr(o) for o in self.options)
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
        module = module_info()
        options = []
        for group in data.get('options', []):
            classname = getattr(module, group['class'])
            options.append(classname.unserialize(group))
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
    def __init__(self, groupname, options=None):
        self.options = options
        self.groupname = groupname
        self.index = 0
        if self.options:
            self.value = self.options[self.index]
    
    def __repr__(self):
        options = ''
        if self.options:
            options = "\n".join(repr(o) for o in self.options)
        return f"{self.__class__.__name__}[{self.groupname}]({options})"

    @classmethod
    def unserialize(cls, data):
        module = module_info()
        options = []
        for option in data.get('options', []):
            classname = getattr(module, option['class'])
            options.append(classname.unserialize(option))
        return cls(data['name'], options)

"""
|------- option               > [value] | [options,...,options]
"""
class Option(object):
    def __init__(self, name, options, default=None):
        self.name = name
        self.options = options
        self.index = default if default else 0
    
    @property
    def value(self):
        return self.options[self.index]

    def select(self):
        self.index = (self.index + 1) % len(self.options)

    @classmethod
    def unserialize(self, data):
        return cls(data['name'], data['options'])

"""
|------- option               > [True | False]
"""
class BoolOption(Option):
    def __init__(self, name, default=False):
        super().__init__(name, ['True', 'False'], 1)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"

    def select(self):
        self.value = not self.value

    @classmethod
    def unserialize(cls, data):
        name = data['name']
        default = data.get('default', False)
        return cls(name, default)


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
        module = module_info()
        objects = []
        classname = getattr(module, data['class'])
        for options in data.get('options', []):
            subclass = getattr(module, options['class'])
            objects.append(subclass.unserialize(options))
        return classname(objects)

if __name__ == "__main__":
    o = {
        'class': 'OptionManager',
        'options': [
            {
                'class': 'OptionGroup',
                'name': 'yes no questions',
                'options': [{
                    'class': 'BoolOption',
                    'name': 'typeable?'
                }]
            },
            {
                'class': 'OptionGroup',
                'name': 'subgroup 2'
            }]
    }
    # can create more than 1 manager
    options = OptionFactory.unserialize(o)
    print(options)
    manager = OptionManager.unserialize(o)
    print(manager)