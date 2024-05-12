import pygame as pg
from player import Player
from land import get_land_from_image

WIDTH, HEIGHT = 900, 500
window = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
pg.display.set_caption("You Probably Wont Survive")

run = True
clock = pg.time.Clock()
FPS = 60

x_offset, y_offset = 0, 0

player = Player(100, 100, 10, 10, "Player1.png")
land, player.topleft = get_land_from_image("assets/land presets/Island1.png", True)

def display():

    window.fill((200, 120, 90))

    for block in land:
        block.display(window, x_offset, y_offset)

    player.display(window, x_offset, y_offset)

    pg.display.update()

while run:

    clock.tick(FPS)

    for event in pg.event.get():

        if event.type == pg.QUIT:
            run = False

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

    player.script()

    x_offset, y_offset = player.x-WIDTH/2, player.y-HEIGHT/2

    display()

pg.quit()
quit()