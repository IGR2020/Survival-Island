import pygame as pg
from assets import *
from time import time
from ui import find_slot

class Slot(pg.Rect):
    def __init__(self, x, y, width, height, item=None):
        super().__init__(x, y, width, height)
        self.item = item

    def display(self, window, is_selected_slot):
        if is_selected_slot: window.blit(assets["Selected Slot"], self)
        else: window.blit(assets["Slot"], self)
        if self.item is not None:
            self.item.display(window, (self.x + 8, self.y + 8))


class Player(pg.Rect):

    def __init__(self, x, y, name) -> None:

        self.name = name
        
        # movement
        self.x_vel = 0
        self.y_vel = 0
        self.speed = 0.5
        self.maxSpeed = 5
        self.isMovingH = False
        self.isMovingV = False
        
        self.inventory = []
        for x in range(200//slotSize, 700//slotSize):
            self.inventory.append(Slot(x * slotSize, 500 - slotSize, slotSize, slotSize))
        self.held = None
        self.selected_slot = 0
        
        # health
        self.health = 50
        self.maxHealth = 50
        self.is_hit = False
        self.timeSinceLastHit = time()
        
        return super().__init__(
            x, y, assets[self.name].get_width(), assets[self.name].get_height()
        )

    def display(self, window: pg.Surface, x_offset=0, y_offset=0):
        window.blit(assets[self.name], (self.x - x_offset, self.y - y_offset))

    def hit(self, damage):
        if time() - self.timeSinceLastHit < hitCooldown:
            return
        self.health -= damage
        self.timeSinceLastHit = time()
        self.is_hit = True

    def moveLeft(self):
        self.x_vel -= self.speed
        self.x_vel = max(self.x_vel, -self.maxSpeed)

    def moveRight(self):
        self.x_vel += self.speed
        self.x_vel = min(self.x_vel, self.maxSpeed)

    def moveDown(self):
        self.y_vel += self.speed
        self.y_vel = min(self.y_vel, self.maxSpeed)

    def moveUp(self):
        self.y_vel -= self.speed
        self.y_vel = max(self.y_vel, -self.maxSpeed)

    def stopMovingH(self):
        self.x_vel = 0

    def stopMovingV(self):
        self.y_vel = 0

    def script(self, land, dt):
        if self.hit and time() - self.timeSinceLastHit > hitCooldown:
            self.is_hit = False

        self.y += self.y_vel * dt
        by, bx = self.y // blockSize, self.centerx // blockSize
        if land[bx][by].name in (
            "Calm Water",
            "Calm Moderate Water",
            "Calm Deep Water",
            "Water",
        ) and self.colliderect(land[bx][by]):
            self.top = land[bx][by].bottom
        by, bx = self.bottom // blockSize, self.centerx // blockSize
        if land[bx][by].name in (
            "Calm Water",
            "Calm Moderate Water",
            "Calm Deep Water",
            "Water",
        ) and self.colliderect(land[bx][by]):
            self.bottom = land[bx][by].top
        self.x += self.x_vel * dt
        by, bx = self.centery // blockSize, self.x // blockSize
        if land[bx][by].name in (
            "Calm Water",
            "Calm Moderate Water",
            "Calm Deep Water",
            "Water",
        ) and self.colliderect(land[bx][by]):
            self.left = land[bx][by].right
        by, bx = self.centery // blockSize, self.right // blockSize
        if land[bx][by].name in (
            "Calm Water",
            "Calm Moderate Water",
            "Calm Deep Water",
            "Water",
        ) and self.colliderect(land[bx][by]):
            self.right = land[bx][by].left

        if not self.isMovingH:
            self.stopMovingH()
        else:
            self.isMovingH = False
        if not self.isMovingV:
            self.stopMovingV()
        else:
            self.isMovingV = False


def agrivate_inventory(inv1, inv2):
    """Inventory 1 should be player style inventory"""
    for item in inv2:
        slotFound = find_slot(item, inv1)
        if slotFound is None:
            continue
        if inv1[slotFound].item is None:
            inv1[slotFound].item = item
            continue
        inv1[slotFound].item.count += item.count
    return inv1
    
