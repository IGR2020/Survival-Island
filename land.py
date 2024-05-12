from assets import *
import perlin_noise
from objects import Block, Structure, Item
from PIL import Image
from random import randint, choice

def generate_island(size: tuple[int, int]) -> list:
    noise = perlin_noise.PerlinNoise()
    width, height = size
    land = []
    for x in range(width):
        for y in range(height):
            if abs(noise((x*landChaos, y*landChaos))) > 0.1:
                land.append(Block(x*blockSize, y*blockSize, blockSize, "Sand.png"))
            else:
                land.append(Block(x*blockSize, y*blockSize, blockSize, "Water.png"))
    return land

def get_land_from_image(image_path, water_land_check=True) -> tuple[list, tuple, list]:
    """Scans a image and creates a land aproximate and also returns a spawn point if lime green is present.\n
    Sand recomended R.G.B is 239r, 228g, 176b.\n
    Water recomended R.G.B is 0r, 162g, 232b.\n
    Spawn point recomended R.G.B is 181r, 230g, 29b"""
    land = []
    structures = []
    spawn_point = (0, 0)
    image = Image.open(image_path)
    image = image.convert("RGBA")
    width, height = image.size
    data = image.load()
    sea_noise = perlin_noise.PerlinNoise()
    for x in range(width):
        for y in range(height):
            if data[x, y] == (239, 228, 176, 255):
               if randint(0, 1) == 0: land.append(Block(x*blockSize, y*blockSize, blockSize, "Sand.png"))
               else: land.append(Block(x*blockSize, y*blockSize, blockSize, "Flat Sand.png"))
               if randint(0, 40) == 0: structures.append(Structure(x*blockSize, y*blockSize, choice(("Palm Tree1.png", "Palm Tree2.png", "Palm Tree3.png")), Item("Wood", randint(1, 6))))
            elif data[x, y] == (181, 230, 29, 255):
                land.append(Block(x*blockSize, y*blockSize, blockSize, "Spawn Point.png"))
                spawn_point = (x*blockSize, y*blockSize)
            else:
                if not water_land_check:
                    land.append(get_water_type_by_noise(x, y, sea_noise))
                    continue
                found = False
                for reg_x in range(x-1, x+2):
                    for reg_y in range(y-1, y+2):
                        try:
                            if data[reg_x, reg_y] == (239, 228, 176, 255):
                                land.append(Block(x*blockSize, y*blockSize, blockSize, "Calm Water.png"))
                                found = True
                                break
                        except IndexError:
                            land.append(get_water_type_by_noise(x, y, sea_noise))
                            found = True
                            break
                    if found:
                        break
                if found:
                    continue
                land.append(get_water_type_by_noise(x, y, sea_noise))

    return land, spawn_point, structures

def get_water_type_by_noise(x, y, sea_noise):
    if abs(sea_noise((x*landChaos, y*landChaos))) > 0.2:
        return (Block(x*blockSize, y*blockSize, blockSize, "Calm Deep Water.png"))
    elif abs(sea_noise((x*landChaos, y*landChaos))) > 0.1:
        return (Block(x*blockSize, y*blockSize, blockSize, "Calm Moderate Water.png"))
    else:
        return (Block(x*blockSize, y*blockSize, blockSize, "Calm Water.png"))