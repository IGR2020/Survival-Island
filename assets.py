from EPT import load_assets

assets = {}
assets.update(load_assets("assets\\objects"))
assets.update(load_assets(("assets\\players"), (12, 28)))

landChaos = 0.02
blockSize = 27