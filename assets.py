from EPT import load_assets
import pygame as pg
from pygame import Surface
import json

pg.display.init()
pg.display.set_mode((900, 500))

blockSize = 32
treeSize = 27
player_width = 18
player_height = 42
item_size = 32
item_asset_size = 16

assets = {}
assets.update(load_assets("assets/objects", None, treeSize/9))
assets.update(load_assets(("assets/players"), (player_width, player_height)))
assets.update(load_assets("assets/tiles", (blockSize, blockSize)))
assets.update(load_assets("assets/items", None, 2))
assets.update(load_assets("assets/players/Robot", (player_width, player_height), getSubDirsAsList=True))
assets.update(load_assets("assets/effects"))
assets.update(load_assets("assets/icons"))
with open("object data/items/weapons.json") as file:
    data = json.load(file)
    file.close()
weapon_names = data.keys()
del data
for weapon_name in weapon_names:
    surface = Surface((assets[weapon_name].get_width()*2, assets[weapon_name].get_height()*2), pg.SRCALPHA, 32)
    surface.blit(assets[weapon_name], (assets[weapon_name].get_width()-1, 0))
    assets[f"{weapon_name} Centre"] = surface


# filter settings
darkness_size = 500
assets["Darkness"] = pg.transform.scale(assets["Darkness"], (darkness_size, darkness_size))
assets["Filter"] = pg.surface.Surface((900, 500))

landChaos = 0.02
seaChaos = 0.02
grassChaos = 0.08

spawnerSpeedRange = [i*0.1 for i in range(15, 120)]

gameFPS = 60

healthBarWidth = 100
healthBarHeight = 25

hitCooldown = 0.3

slotSize = 48
playerHotbarSlots = list(range(10))