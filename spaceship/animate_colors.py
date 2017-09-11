from bearlibterminal import terminal as term
from maps import blender
if __name__ == "__main__":
    term.open()
    term.set(f"window: size=80x25")
    color1 = "#000000"
    color2 = "#ffffff"
    color3 = blender(color1, color2)
    print(color3)
    for x in range(0,25):
        for y in range(25):
            term.puts(x, y, f"[color={color1}]a[/color]")
    for x in range(25, 55):
        for y in range(25):
            term.puts(x, y, f"[color={color3}]c[/color]")
    for x in range(55, 80):
        for y in range(25):
            term.puts(x, y, f"[color={color2}]b[/color]")
    term.refresh()
    term.read()
