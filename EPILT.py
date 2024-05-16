# Esential Pillow Tools

import PIL
from PIL import Image
from os import listdir
from os.path import isfile, join

def fill(image: Image, color: tuple[int, int, int, int]):
    image.convert("RGBA")
    data = image.load()
    width, height = image.size
    for x in range(width):
        for y in range(height):
            data[x, y] = color
    return image

def fill_color(image: Image, color: tuple[int, int, int, int], replacment_color: tuple[int, int, int, int]):
    image = image.convert("RGBA")
    data = image.load()
    width, height = image.size
    for x in range(width):
        for y in range(height):
            if data[x, y] == color:
                data[x, y] = replacment_color
    return image

def load_dir(dir):
    """Returns a list of list with fist element of every list being Image.open() and the second being the path."""
    images = []
    for file in listdir(dir):
        images.append([Image.open(join(dir, file)), join(dir, file)])
    return images

fill_color(Image.open("assets/objects/Tree1.png"), (255, 255, 255, 255), (0, 0, 0, 0)).save("assets/objects/Tree1.png")