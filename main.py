import pygame as pg
from player import Player, agrivate_inventory
from land import get_world_from_directory
from assets import *
from time import time

WIDTH, HEIGHT = 900, 500
window = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
pg.display.set_caption("You Probably Won't Survive")

run = True
clock = pg.time.Clock()
FPS = 60

portal_travel_cooldown = 0.5
portal_time = time()

x_offset, y_offset = 0, 0

player = Player(100, 100, "Player1.png")
current_land = 0

word = get_world_from_directory("assets/land presets", True, True)

def load_current_word():
    land = word[current_land]["land"]
    structures = word[current_land]["structures"]
    spawn = word[current_land]["spawn"]
    gateway_point = word[current_land]["gateway point"]
    gateway_link = word[current_land]["gateway link"]
    return land, structures, spawn, gateway_point, gateway_link

land, structures, spawn, gateway_point, gateway_link = load_current_word()
player.topleft = spawn

def display():

    window.fill((29, 117, 139))
    for x in range(round((WIDTH+x_offset)//blockSize)+1):
        for y in range(round((HEIGHT+y_offset)//blockSize)+1):
            try:
                land[x][y].display(window, x_offset, y_offset)
            except IndexError:
                pass

    for structure in structures:
        structure.display(window, x_offset, y_offset)

    player.display(window, x_offset, y_offset)

    for item in player.inventory:
        y = 0
        item.display(window, (0, y))
        y += 20

    pg.display.update()

while run:

    delta_time = clock.tick() / 16

    for event in pg.event.get():

        if event.type == pg.QUIT:
            run = False

        if event.type == pg.VIDEORESIZE:
            WIDTH, HEIGHT = event.dict["size"]

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

    player.script(land, delta_time)

    if player.collidepoint(gateway_point) and time() - portal_time > portal_travel_cooldown:
        current_land = gateway_link
        land, structures, spawn, gateway_point, gateway_link = load_current_word()
        player.topleft = gateway_point
        portal_time = time()

    x_offset, y_offset = player.x-WIDTH/2, player.y-HEIGHT/2

    display()

pg.quit()
quit()