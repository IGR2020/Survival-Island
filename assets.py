from EPT import load_assets

blockSize = 16
treeSize = 18
player_width = 12
player_height = 28

assets = {}
assets.update(load_assets("assets/objects", None, 2))
assets.update(load_assets(("assets/players"), (player_width, player_height)))
assets.update(load_assets("assets/tiles", (blockSize, blockSize)))
assets.update(load_assets("assets/items", (32, 32)))

landChaos = 0.02
seaChaos = 0.02
grassChaos = 0.08