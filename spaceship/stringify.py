# using pil - transforms an image from png to a python string to be used
# as a map
from PIL import Image

characters = {
    (0, 0, 0): ("#", "89"),
    (185, 122, 87): ("+", "90"),
    (112, 146, 190): ("~", "91"),
    (255, 255, 255): (".", "92"),
}


def stringify(string, asciify=False, debug=False):
    lines = []
    colors = set()
    with Image.open(string) as img:
        pixels = img.load()
        w, h = img.size
    for j in range(h):
        line = ""
        for i in range(w):
            # sometimes alpha channel is included so test for all values first
            try:
                r, g, b, _ = pixels[i, j]
            except BaseException:
                r, g, b = pixels[i, j]
            if (r, g, b) not in colors:
                colors.add((r, g, b))
            line += characters[(r, g, b)][int(asciify)]
        lines.append(line)
    if debug:
        print("\n".join(lines))
        print(colors)
        print(characters)
    return "\n".join(lines)


if __name__ == "__main__":
    stringify("./assets/testmap.png", debug=True)
