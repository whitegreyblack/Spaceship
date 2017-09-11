from bearlibterminal import terminal as term
from maps import blender
import sys
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(sys.argv)
        exit('ERROR :- incorrect num of args')
        
    term.open()
    term.set(f"window: size=80x25")
    colors = blender(sys.argv[1], sys.argv[2], 80)
    print(colors)
    step = 80 // len(colors)
    for i in range(len(colors)):
        for y in range(25):
            for x in range(step):
                term.puts(step*i+x, y, f"[color={colors[i]}]#[/color]")
    term.refresh()
    term.read()
