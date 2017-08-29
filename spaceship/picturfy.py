# using pil -transformas an image from string to png -- used to transform string map to image back to string for usage
from PIL import Image, ImageDraw
from stringify import stringify
from maps import MAPS
characters = {
    "#": (0,0,0),
    "+": (185, 122, 87),
    "~": (112, 146, 190),
    ".": (255, 255, 255),
}

def picturfy(string, asciify=False, debug=False):
    '''Takes in a string map and two positional parameters to determine
    output. If asciify is specified then returns color codes reflective
    of their ascii character code else returns color based on regular
    character code. Debug is specified for testing and output viewing'''

    filename = "picturfy-img.png"
    mapping = string.split('\n')
    h, w = len(mapping), len(mapping[0])
    img_to_save = Image.new('RGB', (w, h))
    drawer = ImageDraw.Draw(img_to_save)

    for j in range(h):
        string_list = list(mapping[j])
        for i in range(len(string_list)):
            drawer.rectangle((i, j, i+1, j+1), characters[string_list[i]])

    img_to_save.save(filename)
    return filename

if __name__ == "__main__":
    stringify(picturfy(MAPS.TOWN), debug=True)
