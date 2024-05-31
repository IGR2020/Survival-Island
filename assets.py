from EPT import load_assets
import pygame as pg
from pygame import Surface

pg.display.init()
pg.display.set_mode((900, 500))

blockSize = 32
treeSize = 27
player_width = 18
player_height = 42

assets = {}
assets.update(load_assets("assets/objects", None, treeSize/9))
assets.update(load_assets(("assets/players"), (player_width, player_height)))
assets.update(load_assets("assets/tiles", (blockSize, blockSize)))
assets.update(load_assets("assets/items", None, 2))
assets.update(load_assets("assets/players/Robot", (player_width, player_height), getSubDirsAsList=True))
assets.update(load_assets("assets/effects"))

# filter settings
darkness_size = 500
assets["Darkness.png"] = pg.transform.scale(assets["Darkness.png"], (darkness_size, darkness_size))
assets["Filter"] = pg.surface.Surface((900, 500))

landChaos = 0.02
seaChaos = 0.02
grassChaos = 0.08

gameFPS = 60