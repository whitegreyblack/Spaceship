# using pil - transforms an image from png to a python string to be used as a map
from PIL import Image

def stringify(string, debug=False):
    with Image.open(string) as img:
        pixels = img.load()
        w, h = img.size
        lines = []
        for j in range(h):
            line = ""
            for i in range(w):
                try:
                    r, g, b, _ = pixels[i,j]
                except:
                    r, g, b = pixels[i, j]
                if (r, g, b)== (0,0,0):
                    line += "#"
                # add some trees
                # buildings
                # some other stuff
                else:
                    print(pixels[i,j])
                    line += "."
            lines.append(line)
        if debug:
            print("\n".join(lines))
        return lines

if __name__ == "__main__":
    stringify("./assets/testmap.png", debug=True)