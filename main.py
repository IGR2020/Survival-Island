import pygame as pg
from player import Player, agrivate_inventory
from land import get_world_from_directory
from assets import *
from time import time
from objects import Sword
from math import ceil
from EPT import blit_text, convert_to_thread
from pygame.image import load
from effects import draw_darkness_filter_at_player

WIDTH, HEIGHT = 900, 500
window = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
pg.display.set_caption("Survival Island")
pg.display.set_icon(load("assets/Icon.png"))

run = True
clock = pg.time.Clock()
FPS = 60

portal_travel_cooldown = 0.5
portal_time = time()
x_offset, y_offset = 0, 0

base_damage = 1
player = Player(100, 100, "Player1.png")
player.inventory.append(Sword(name="Long Sword.png"))
current_land = 0

correction_angle = 45

word = get_world_from_directory("assets/land presets", True, True)


def load_current_world():
    land = word[current_land]["land"]
    structures = word[current_land]["structures"]
    spawn = word[current_land]["spawn"]
    spawners = word[current_land]["spawners"]
    monsters = word[current_land]["monsters"]
    return land, structures, spawn, spawners, monsters


def save_current_world():
    word[current_land]["land"] = land
    word[current_land]["structures"] = structures
    word[current_land]["spawn"] = spawn
    word[current_land]["spawners"] = spawners
    word[current_land]["monsters"] = monsters


land, structures, spawn, spawners, monsters = load_current_world()
player.topleft = spawn


def mapBlocks(x_offset, y_offset):
    try:
        [
            land[x][y].display(window, x_offset, y_offset)
            for x in range(min(ceil((WIDTH + x_offset) / blockSize), len(land)-1))
            for y in range(min(ceil((HEIGHT + y_offset) / blockSize), len(land[0])-1))
        ]
    except IndexError:
        pass


showDebug = False
tool_rect = player.inventory[0].display_as_object(window, x_offset, y_offset, player)


def display(internal_clock):
    global tool_rect

    x_offset, y_offset = player.x - WIDTH / 2, player.y - HEIGHT / 2

    window.fill((29, 117, 139))

    mapBlocks(x_offset, y_offset)
    
    for structure in structures:
        structure.display(window, x_offset, y_offset)

    for monster in monsters:
        monster.display(window, x_offset, y_offset)

    tool_rect = player.inventory[0].display_as_object(window, x_offset, y_offset, player)

    player.display(window, x_offset, y_offset)

    draw_darkness_filter_at_player(window, player, x_offset, y_offset)

    y = 0
    for item in player.inventory:
        item.display(window, (0, y))
        y += 32

    if showDebug:
        blit_text(window, round(clock.get_fps()), (0, 0), colour=(255, 255, 255))
        blit_text(window, round(internal_clock.get_fps()), (0, 50), colour=(255, 255, 255))

    pg.display.update()


display_thread = convert_to_thread(display, 60, True)
display_thread.start()


while run:

    delta_time = clock.tick(60) / 16

    for event in pg.event.get():

        if event.type == pg.QUIT:
            run = False

        if event.type == pg.VIDEORESIZE:
            WIDTH, HEIGHT = event.dict["size"]
            assets["Filter"] = pg.surface.Surface((WIDTH, HEIGHT))

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
                    break
            else:
                for monster in monsters:
                    if monster.colliderect(tool_rect):
                        if monster.hit(base_damage + player.inventory[0].damage):
                            monsters.remove(monster)
                        break

        if event.type == pg.KEYDOWN: 
            if event.key == pg.K_F3:
                showDebug = not showDebug

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

    for structure in structures:
        if (
            player.colliderect(structure)
            and time() - portal_time > portal_travel_cooldown
            and structure.name == "Gateway.png"
        ):
            save_current_world()
            current_land = structure.land_link
            land, structures, spawn, spawners, monsters = load_current_world()
            for structure in structures:
                if structure.name == "Gateway.png":
                    player.topleft = structure.topleft
            portal_time = time()
            break

    for spawner_coords in spawners:
        x, y = spawner_coords
        monster = land[x][y].script()
        if monster is not None:
            monsters.append(monster)

    for monster in monsters:
        monster.script(
            {
                "player pos": player.topleft,
                "land": land,
                "delta time": delta_time,
                "window size": (WIDTH, HEIGHT),
            }
        )

pg.quit()
quit()
