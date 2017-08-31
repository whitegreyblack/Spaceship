from PIL import Image, ImageDraw


# Key-value pairs are mapped from characters to color tuples
picturfy_chars = {
    "#": (0,0,0),
    ",": (34, 177, 76),
    "+": (185, 122, 87),
    "~": (112, 146, 190),
    ".": (127, 127, 127),
    ".": (255, 255, 255),

}

# Key-Value pairs are tuples to tuple pertaining to color and character mapping
stringify_chars = { 
    (0, 0, 0): ("#", "89"),
    (34, 177, 76): (",", "71"),
    (185, 122, 87): ("+", "90"),
    (127, 127, 127): (".", "72"),
    (112, 146, 190): ("~", "91"),
    (255, 255, 255): (".", "92"),
}

def picturfy(string, filename="picturfy-img.png", asciify=False, debug=False):
    '''Takes in a string map and two positional parameters to determine
    output. If asciify is specified then returns color codes reflective
    of their ascii character code else returns color based on regular
    character code. Debug is specified for testing and output viewing'''

    mapping = string.split('\n')
    h, w = len(mapping), len(mapping[0])
    img_to_save = Image.new('RGB', (w, h))
    drawer = ImageDraw.Draw(img_to_save)

    for j in range(h):
        string_list = list(mapping[j])
        for i in range(len(string_list)):
            drawer.rectangle((i, j, i+1, j+1), picturfy_chars[string_list[i]])

    img_to_save.save("assets/"+filename)
    return filename


def stringify(string, asciify=False, debug=False):
    '''Takes in a file location string and two positional parameters
    to determine output. If asciify is specified then returns ascii
    character codes for use in map construction else outputs regular
    character text. Debug is specified for testing and output viewing'''

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
            line += stringify_chars[(r, g, b)][int(asciify)]
        lines.append(line)

    if debug:
        print("\n".join(lines))
        print(colors)

    return "\n".join(lines)