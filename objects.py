from assets import *
import pygame as pg
from time import time
from EPT import blit_text
from math import degrees, atan2
import json


class Item:
    def __init__(self, name, count, item_type="Item"):
        self.name = name
        self.count = count
        self.image_width = assets[self.name].get_width()
        self.type = item_type

    def display(self, window, pos):
        x, y = pos
        window.blit(assets[self.name], (x, y))
        blit_text(window, self.name, (x + self.image_width + 5, y), size=15)
        blit_text(window, self.count, pos, size=15)


class Object(pg.Rect):
    def __init__(self, x, y, width, height, name):
        super().__init__(x, y, width, height)
        self.name = name

    def display(self, window, x_offset, y_offset):
        window.blit(assets[self.name], (self.x - x_offset, self.y - y_offset))

    def script(self, *args): ...


class Block(Object):
    def __init__(self, x, y, size, name):
        super().__init__(x, y, size, size, name)


class Structure(Object):
    def __init__(self, x, y, name, value=None, health=3):
        super().__init__(
            x, y, assets[name].get_width(), assets[name].get_height(), name
        )
        if value is None:
            self.value = []
        else:
            self.value = value
        self.time = time()
        self.isBreaking = False
        self.health = health
        self.original_pos = self.topleft

    def destroy(
        self,
    ):  # reduces the health of the structure and destroys it if health = 0 and return its value if its health is 0
        if self.isBreaking:
            return None
        self.isBreaking = True
        self.time = time()
        self.health -= 1
        if self.health < 1:
            return self.value
        return None

    def animateBreakng(self):
        if time() - self.time < 0.06:
            self.x -= 1
        elif time() - self.time < 0.12:
            self.x += 2
        elif time() - self.time < 0.18:
            self.x -= 1
        else:
            self.isBreaking = False
            self.topleft = self.original_pos

    def display(self, window, x_offset, y_offset):
        if self.isBreaking:
            self.animateBreakng()
        super().display(window, x_offset, y_offset)


class Gateway(Structure):
    def __init__(self, x, y, name, value=None, health=3, land_link=None):
        super().__init__(x, y, name, value, health)
        self.land_link = land_link


class Spawner(Block):
    def __init__(self, x, y, size, name, spawn_speed, monster, monster_name):
        super().__init__(x, y, size, name)
        self.spawnSpeed = spawn_speed
        self.monster = monster
        self.monster_name = monster_name
        self.cooldown = time()

    def script(self, *args):
        if time() - self.cooldown > self.spawnSpeed:
            self.cooldown = time()
            return self.monster(
                self.x, self.y, player_width, player_height, self.monster_name
            )


class Monster(pg.Rect):
    def __init__(self, x, y, width, height, name, health=4, speed=0.25):
        super().__init__(x, y, width, height)
        self.name = name
        self.x_vel = 0
        self.y_vel = 0
        self.speed = speed
        self.maxSpeed = 2.5
        self.isHit = False
        self.timeSinceLastHit = time()
        self.health = health
        self.delay = 0.3 # time to show blood overlay
        self.animation_count = 0
        self.animate_speed = 3

    def script(self, info_dict, *args):
        player_x, player_y = info_dict["player pos"]
        dt = info_dict["delta time"]
        land = info_dict["land"]
        window_width, window_height = info_dict["window size"]
        if abs(player_x - self.x) > window_width*1.4 and abs(player_y - self.y) > window_height*1.4 and not self.isHit:
            return
        if abs(player_x - self.x) < 48 and abs(player_y - self.y) < 48 and not self.isHit:
            self.x_vel, self.y_vel = 0, 0
        if player_x > self.x:
            self.x_vel += self.speed
        if player_y > self.y:
            self.y_vel += self.speed
        if player_x < self.x:
            self.x_vel -= self.speed
        if player_y < self.y:
            self.y_vel -= self.speed
        if not self.isHit:
            self.x_vel = max(self.x_vel, -self.maxSpeed)
            self.x_vel = min(self.x_vel, self.maxSpeed)
            self.y_vel = min(self.y_vel, self.maxSpeed)
            self.y_vel = max(self.y_vel, -self.maxSpeed)
        else:
            self.x_vel = max(self.x_vel, -self.maxSpeed * 5)
            self.x_vel = min(self.x_vel, self.maxSpeed * 5)
            self.y_vel = min(self.y_vel, self.maxSpeed * 5)
            self.y_vel = max(self.y_vel, -self.maxSpeed * 5)
        self.y += self.y_vel * dt
        by, bx = self.y // blockSize, self.centerx // blockSize
        if land[bx][by].name in (
            "Calm Water.png",
            "Calm Moderate Water.png",
            "Calm Deep Water.png",
            "Water.png",
        ) and self.colliderect(land[bx][by]):
            self.top = land[bx][by].bottom
        by, bx = self.bottom // blockSize, self.centerx // blockSize
        if land[bx][by].name in (
            "Calm Water.png",
            "Calm Moderate Water.png",
            "Calm Deep Water.png",
            "Water.png",
        ) and self.colliderect(land[bx][by]):
            self.bottom = land[bx][by].top
        self.x += self.x_vel * dt
        by, bx = self.centery // blockSize, self.x // blockSize
        if land[bx][by].name in (
            "Calm Water.png",
            "Calm Moderate Water.png",
            "Calm Deep Water.png",
            "Water.png",
        ) and self.colliderect(land[bx][by]):
            self.left = land[bx][by].right
        by, bx = self.centery // blockSize, self.right // blockSize
        if land[bx][by].name in (
            "Calm Water.png",
            "Calm Moderate Water.png",
            "Calm Deep Water.png",
            "Water.png",
        ) and self.colliderect(land[bx][by]):
            self.right = land[bx][by].left

    def display(self, window, x_offset, y_offset):
        window.blit(assets[self.name], (self.x - x_offset, self.y - y_offset))
        if self.isHit:
            window.blit(assets["Blood Overlay.png"], (self.x - x_offset, self.y - y_offset))
        if time() - self.timeSinceLastHit > self.delay:
            self.isHit = False

    def hit(self, damage) -> bool:
        self.health -= damage
        self.isHit = True
        self.x_vel = -self.x_vel * 20
        self.y_vel = -self.y_vel * 20
        self.timeSinceLastHit = time()
        if self.health < 1:
            return True
        return False
    
class Sword(Item):

    def  __init__(self, name="Black Sword.png", count=1, item_type="Tool", damage=1):
        self.correction_angle = 45
        self.damage = damage
        super().__init__(name, count, item_type)

    def display(self, window, pos):
        super().display(window, pos)

    def display_as_object(self, window, x_offset, y_offset, player):

        offset_mouse_x, offset_mouse_y = pg.mouse.get_pos()
        offset_mouse_x += x_offset
        offset_mouse_y += y_offset
        dx, dy = offset_mouse_x - player.centerx, offset_mouse_y - player.centery
        angle = degrees(atan2(-dy, dx)) - self.correction_angle

        rotated_image = pg.transform.rotate(assets[self.name], angle)
        rotated_image_rect = rotated_image.get_rect(center=player.center)

        window.blit(rotated_image, (rotated_image_rect.x - x_offset, rotated_image_rect.y - y_offset))
        return rotated_image_rect
    
class Robot(Monster):
    def __init__(self, x, y, width, height, name=None):
        super().__init__(x, y, width, height, name, None, None)
        self.state = None
        with open("object data/enemy.json") as file:
            data = json.load(file)["Robot"]
            self.maxSpeed = data["Max Speed"]
            self.speed = data["Speed"]
            self.animate_speed = data["Animate Speed"]
            self.health = data["Health"]
            file.close()

    def display(self, window, x_offset, y_offset):
        if self.x_vel > 0:
            self.state = "Right"
        if self.x_vel < 0:
            self.state = "Left"
        else:
            self.state = "Idle"
        self.animation_count += 1
        window.blit(assets[self.state][(self.animation_count // self.animate_speed) % len(assets[self.state])], (self.x - x_offset, self.y - y_offset))
        if self.isHit:
            window.blit(assets["Blood Overlay.png"], (self.x - x_offset, self.y - y_offset))
        if time() - self.timeSinceLastHit > self.delay:
            self.isHit = False