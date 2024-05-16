from assets import *
import perlin_noise
from objects import Block, Structure, Item, Gateway
from PIL import Image
from random import randint, choice
from os import listdir
from os.path import join

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

def get_land_from_image(image_path, water_land_check=True, create_gateway = False, gateway_link=None) -> tuple[list, tuple, list]:
    """Scans a image and creates a land aproximate and also returns a spawn point if lime green is present.\n
    Sand recomended R.G.B is 239r, 228g, 176b.\n
    Water recomended R.G.B is 0r, 162g, 232b.\n
    Spawn point recomended R.G.B is 181r, 230g, 29b.\n
    Grass recomended R.G.B is 34r, 177g, 76b.\n
    Gateway recomended R.G.B is 163r, 73g, 164b."""
    land = []
    structures = []
    spawn_point = (0, 0)
    gateway_point = (0, 0)
    image = Image.open(image_path)
    image = image.convert("RGBA")
    width, height = image.size
    data = image.load()
    sea_noise = perlin_noise.PerlinNoise()
    grass_noise = perlin_noise.PerlinNoise()
    for x in range(width):
        land.append([])
        for y in range(height):
            if data[x, y] == (239, 228, 176, 255):
                if randint(0, 1) == 0: land[-1].append(Block(x*blockSize, y*blockSize, blockSize, "Sand.png"))
                else: land[-1].append(Block(x*blockSize, y*blockSize, blockSize, "Flat Sand.png"))
                if randint(0, 40) == 0: structures.append(Structure(x*blockSize - treeSize/3, y*blockSize - treeSize/3, choice(("Palm Tree1.png", "Palm Tree2.png", "Palm Tree3.png")), Item("Wood.png", randint(1, 6))))
            elif data[x, y] == (34, 177, 76, 255):
                land[-1].append(get_grass_type_by_noise(x, y, grass_noise))
                structure_added = get_grass_tree_by_noise(x, y, grass_noise)
                if structure_added is not None:
                    structures.append(structure_added)
            elif data[x, y] == (163, 73, 164, 255):
                gateway_point = (x*blockSize - treeSize/3, y*blockSize - treeSize/3)
                land[-1].append(Block(x*blockSize, y*blockSize, blockSize, "Gateway Point.png"))
                structures.append(Gateway(x*blockSize - treeSize/3, y*blockSize - treeSize/3, "Gateway.png", health=64, land_link=gateway_link))
            elif data[x, y] == (181, 230, 29, 255):
                land[-1].append(Block(x*blockSize, y*blockSize, blockSize, "Spawn Point.png"))
                spawn_point = (x*blockSize, y*blockSize)
            else:
                if not water_land_check:
                    land[-1].append(get_water_type_by_noise(x, y, sea_noise))
                    continue
                found = False
                for reg_x in range(x-1, x+2):
                    for reg_y in range(y-1, y+2):
                        try:
                            if data[reg_x, reg_y] == (239, 228, 176, 255):
                                land[-1].append(Block(x*blockSize, y*blockSize, blockSize, "Calm Water.png"))
                                found = True
                                break
                        except IndexError:
                            if (y == height-1 or x == width-1) and randint(0, 4) == 0:
                                land[-1].append(Block(x*blockSize, y*blockSize, blockSize, "Calm Deep Water.png"))
                                found = True
                                break
                            land[-1].append(get_water_type_by_noise(x, y, sea_noise))
                            found = True
                            break
                    if found:
                        break
                if found:
                    continue
                if (y == 0 or x == 0) and randint(0, 4) == 0:
                    land[-1].append(Block(x*blockSize, y*blockSize, blockSize, "Calm Deep Water.png"))
                    continue
                land[-1].append(get_water_type_by_noise(x, y, sea_noise))
    return land, spawn_point, structures, gateway_point

def get_water_type_by_noise(x, y, sea_noise):
    if abs(sea_noise((x*seaChaos, y*seaChaos))) > 0.2:
        return (Block(x*blockSize, y*blockSize, blockSize, "Calm Deep Water.png"))
    elif abs(sea_noise((x*seaChaos, y*seaChaos))) > 0.1:
        return (Block(x*blockSize, y*blockSize, blockSize, "Calm Moderate Water.png"))
    else:
        return (Block(x*blockSize, y*blockSize, blockSize, "Calm Water.png"))
    

def get_grass_type_by_noise(x, y, grass_noise):
    if abs(grass_noise((x*grassChaos, y*grassChaos))) > 0.4:
        return (Block(x*blockSize, y*blockSize, blockSize, "Flat Grass.png"))
    elif abs(grass_noise((x*grassChaos, y*grassChaos))) > 0.3:
        return (Block(x*blockSize, y*blockSize, blockSize, "Grass.png"))
    elif abs(grass_noise((x*grassChaos, y*grassChaos))) > 0.2:
        return (Block(x*blockSize, y*blockSize, blockSize, "Short Grass.png"))
    elif abs(grass_noise((x*grassChaos, y*grassChaos))) > 0.1:
        return (Block(x*blockSize, y*blockSize, blockSize, "Lawn Grass.png"))
    else:
        return (Block(x*blockSize, y*blockSize, blockSize, "Flat Lawn Grass.png"))
    
def get_grass_tree_by_noise(x, y, grass_noise):
    if abs(grass_noise((x*grassChaos, y*grassChaos))) > 0.4:
        if randint(0, 2) == 0: return (Structure(x*blockSize - treeSize/3, y*blockSize - treeSize/4, "Tree1.png", Item("Wood.png", randint(2, 9))))
    elif abs(grass_noise((x*grassChaos, y*grassChaos))) > 0.3:
        if randint(0, 7) == 0: return Structure(x*blockSize - treeSize/3, y*blockSize - treeSize/4, "Tree1.png", Item("Wood.png", randint(2, 9)))
    elif abs(grass_noise((x*grassChaos, y*grassChaos))) > 0.2:
        if randint(0, 10) == 0: return Structure(x*blockSize - treeSize/3, y*blockSize - treeSize/4, "Tree1.png", Item("Wood.png", randint(2, 9)))
    elif abs(grass_noise((x*grassChaos, y*grassChaos))) > 0.1:
        if randint(0, 15) == 0: return Structure(x*blockSize - treeSize/3, y*blockSize - treeSize/4, "Tree1.png", Item("Wood.png", randint(2, 9)))
    else:
        if randint(0, 21) == 0: return Structure(x*blockSize - treeSize/3, y*blockSize - treeSize/4, "Tree1.png", Item("Wood.png", randint(2, 9)))


def get_world_from_directory(dir_path, water_land_check=True, create_land_links=False):
    world = []
    paths = listdir(dir_path)
    for i, path in enumerate(paths):
        land, spawn, stuctures, gateway_point = get_land_from_image(join(dir_path, path), water_land_check, create_land_links, i-1)
        world.append({"land": land, "spawn": spawn, "structures": stuctures, "gateway point": gateway_point, "gateway link": i-1})
    return world