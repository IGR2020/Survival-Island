import pygame as pg
from player import Player, agrivate_inventory
from land import get_world_from_directory
from assets import *
from time import time
from objects import Sword
from math import ceil, floor
from EPT import blit_text, Button
from pygame.image import load
from effects import draw_darkness_filter_at_player
from ui import render_health
import tkinter

MONITER_WIDTH, MONITER_HEIGHT = tkinter.Tk().winfo_screenwidth(), tkinter.Tk().winfo_screenheight()

WIDTH, HEIGHT = 900, 500
window = pg.display.set_mode((WIDTH, HEIGHT), flags=pg.RESIZABLE)
pg.display.set_caption("Survival Island")
pg.display.set_icon(load("assets/icons/Icon.png"))

run = True
clock = pg.time.Clock()
FPS = 60

# Android Support
button_size = 48
up_button = Button((button_size, HEIGHT - button_size*3), assets["Up Button"])
down_button = Button((button_size, HEIGHT - button_size), assets["Down Button"])
left_button = Button((0, HEIGHT - button_size*2), assets["Left Button"])
right_button = Button((button_size*2, HEIGHT - button_size*2), assets["Right Button"])
attack_button = Button((WIDTH - button_size*2, HEIGHT - button_size*2), assets["Attack Button"])
maximise_button = Button((WIDTH-button_size, 0), assets["Maximise"])
f3_button = Button((WIDTH-button_size*2, 0), assets["F3"])

portal_travel_cooldown = 0.5
portal_time = time()
x_offset, y_offset = 0, 0

base_damage = 1
player = Player(100, 100, "Player1")
player.inventory[0].item = Sword(name="Magma Sword")
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
            for x in range(
                max(floor((x_offset) / blockSize), 0),
                min(ceil((WIDTH + x_offset) / blockSize), len(land) - 1),
            )
            for y in range(
                max(floor((y_offset) / blockSize), 0),
                min(ceil((HEIGHT + y_offset) / blockSize), len(land[0]) - 1),
            )
        ]
    except IndexError:
        pass


showDebug = False
showDarkness = False
mouse_down = False

tool_rect = None


def display():
    global tool_rect, x_offset, y_offset, gameFPS

    window.fill((29, 117, 139))

    mapBlocks(x_offset, y_offset)

    for structure in structures:
        structure.display(window, x_offset, y_offset)

    for monster in monsters:
        monster.display(window, x_offset, y_offset)

    if player.inventory[player.selected_slot].item is not None:
        if player.inventory[player.selected_slot].item.type == "Tool":
            tool_rect = player.inventory[player.selected_slot].item.display_as_object(
                window, x_offset, y_offset, player
            )
        else:
            None
    else:
        None

    player.display(window, x_offset, y_offset)

    if showDarkness:
        draw_darkness_filter_at_player(window, player, x_offset, y_offset)

    for i, slot in enumerate(player.inventory):
        if i == player.selected_slot: slot.display(window, True)
        else: slot.display(window, False)
    render_health(window, player.health, player.maxHealth, (0, 0))

    up_button.display(window)
    down_button.display(window)
    left_button.display(window)
    right_button.display(window)
    attack_button.display(window)
    maximise_button.display(window)
    f3_button.display(window)

    if showDebug:
        averageFPS = round(clock.get_fps())
        blit_text(window, averageFPS, (0, healthBarHeight+10))

    pg.display.update()

while run:

    delta_time = clock.tick(gameFPS) / 16

    for event in pg.event.get():

        if event.type == pg.QUIT:
            run = False
            

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_down = True

            mouse_pos = pg.mouse.get_pos()

            for i, slot in enumerate(player.inventory):
                if slot.collidepoint(mouse_pos):
                    player.selected_slot = i
                    break

            if f3_button.clicked():
                showDebug = not showDebug

            # Resize Support
            if maximise_button.clicked():
                pg.display.set_mode((MONITER_WIDTH, MONITER_HEIGHT), pg.RESIZABLE)
                WIDTH, HEIGHT = MONITER_WIDTH, MONITER_HEIGHT
                assets["Filter"] = pg.surface.Surface((WIDTH, HEIGHT))
                
                for i, x in enumerate(range(round((WIDTH*0.22)/slotSize), round((WIDTH-WIDTH*0.22)/slotSize))):

                    if i == len(player.inventory):
                        break

                    player.inventory[i].topleft = x * slotSize, HEIGHT - slotSize

                up_button = Button((button_size, HEIGHT - button_size*3), assets["Up Button"])
                down_button = Button((button_size, HEIGHT - button_size), assets["Down Button"])
                left_button = Button((0, HEIGHT - button_size*2), assets["Left Button"])
                right_button = Button((button_size*2, HEIGHT - button_size*2), assets["Right Button"])
                attack_button = Button((WIDTH - button_size*2, HEIGHT - button_size*2), assets["Attack Button"])
                maximise_button = Button((WIDTH-button_size, 0), assets["Maximise"])


        if event.type == pg.MOUSEBUTTONUP:
            mouse_down = False

    if mouse_down:
        offset_mouse_x, offset_mouse_y = pg.mouse.get_pos()
        offset_mouse_x += x_offset
        offset_mouse_y += y_offset
        for structure in structures:
            if structure.collidepoint((offset_mouse_x, offset_mouse_y)):
                gain = structure.destroy()
                if gain is not None:
                    player.inventory = agrivate_inventory(player.inventory, gain)
                    structures.remove(structure)
                break
        else:
            if attack_button.clicked() and tool_rect is not None:
                if player.inventory[player.selected_slot].item is not None:
                    if player.inventory[player.selected_slot].item.type == "Tool":
                        player.inventory[player.selected_slot].item.attack = True
                for monster in monsters:
                    if monster.colliderect(tool_rect):
                        if monster.hit(base_damage + player.inventory[0].item.damage):
                            agrivate_inventory(player.inventory, monster.value)
                            monsters.remove(monster)
                        break
    else:
        if player.inventory[player.selected_slot].item is not None:
            if player.inventory[player.selected_slot].item.type == "Tool":
                player.inventory[player.selected_slot].item.attack = False
        

    if mouse_down:
        if left_button.clicked():
            player.moveLeft()
            player.isMovingH = True
        if right_button.clicked():
            player.moveRight()
            player.isMovingH = True
        if up_button.clicked():
            player.moveUp()
            player.isMovingV = True
        if down_button.clicked():
            player.moveDown()
            player.isMovingV = True
            

    player.script(land, delta_time)
    x_offset, y_offset = player.x - WIDTH / 2, player.y - HEIGHT / 2

    for structure in structures:
        if (
            player.colliderect(structure)
            and time() - portal_time > portal_travel_cooldown
            and structure.name == "Gateway"
        ):
            save_current_world()
            current_land = structure.land_link
            land, structures, spawn, spawners, monsters = load_current_world()
            for structure in structures:
                if structure.name == "Gateway":
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
        if player.colliderect(monster):
            player.hit(monster.damage)

    display()

pg.quit()
quit()
