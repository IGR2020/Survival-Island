import pygame as pg
from player import Player, agrivate_inventory
from land import get_land_from_image

WIDTH, HEIGHT = 900, 500
window = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
pg.display.set_caption("You Probably Wont Survive")

run = True
clock = pg.time.Clock()
FPS = 60

x_offset, y_offset = 0, 0

player = Player(100, 100, "Player1.png")
current_land = 0
land, player.topleft, structures = get_land_from_image("assets/land presets/Island1.png", True)

def display():

    window.fill((29, 117, 139))

    for block in land:
        block.display(window, x_offset, y_offset)

    for structure in structures:
        structure.display(window, x_offset, y_offset)

    player.display(window, x_offset, y_offset)

    for item in player.inventory:
        y = 0
        item.display(window, (0, y))
        y += 20

    pg.display.update()

while run:

    clock.tick()

    for event in pg.event.get():

        if event.type == pg.QUIT:
            run = False

        if event.type == pg.MOUSEBUTTONDOWN:
            offset_mouse_x, offset_mouse_y = pg.mouse.get_pos()
            offset_mouse_x += x_offset
            offset_mouse_y += y_offset
            for structure in structures:
                if structure.collidepoint((offset_mouse_x, offset_mouse_y)):
                    gain = structure.destroy()
                    if gain is not None:
                        player.inventory = agrivate_inventory(player.inventory, [gain])
                        structures.remove(structure)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_F3:
                print(round(clock.get_fps()))
                print([i.name for i in player.inventory])
                print([i.count for i in player.inventory])

    keys = pg.key.get_pressed()

    if keys[pg.K_a]:
        player.moveLeft()
        player.isMovingH = True
    if keys[pg.K_d]:
        player.moveRight()
        player.isMovingH = True
    if keys[pg.K_w]:
        player.moveUp()
        player.isMovingV = True
    if keys[pg.K_s]:
        player.moveDown()
        player.isMovingV = True

    player.script(land)

    x_offset, y_offset = player.x-WIDTH/2, player.y-HEIGHT/2

    display()

pg.quit()
quit()