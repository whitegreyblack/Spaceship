def center(text, width):
    if isinstance(text, str):
        return width//2-len(text)//2
    if isinstance(text, int):
        return width//2-text//2

def colored(text):
    return "[color=blue]{}[/color]".format(text)

def align(text):
    pass
    
def optionize(text):
    return "[{}] {}".format(text[0], text)

def longest(options):
    return max(map(lambda opt: (len(opt), opt), options))