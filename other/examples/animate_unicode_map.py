from bearlibterminal import terminal as term
from maps import dimensions
from maps import evaluate_blocks
from maps import unicode_blocks_thin
from maps import asciify

filename = "./assets/unicodes.png"


if __name__ == "__main__":
    array = asciify(filename, False)
    _, h, w = dimensions(array, True)
    print(w, h)
    blocks = evaluate_blocks(array, w, h)
    term.open()
    term.set(f"window: size={w}x{h}")
    for x in range(w):
        for y in range(h):
            term.put(x, y, blocks[y][x])
    term.refresh()
    term.read()