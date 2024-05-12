from EPT import load_assets

assets = {}
assets.update(load_assets("assets\\objects", None, 3))
assets.update(load_assets(("assets\\players"), (12, 28)))
assets.update(load_assets("assets/tiles", (27, 27)))

landChaos = 0.02
blockSize = 27