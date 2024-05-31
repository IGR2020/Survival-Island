import pygame as pg
from assets import assets, blockSize
from objects import Item


class Player(pg.Rect):

    def __init__(self, x, y, name) -> None:
        self.name = name
        self.x_vel = 0
        self.y_vel = 0
        self.speed = 0.5
        self.maxSpeed = 5
        self.isMovingH = False
        self.isMovingV = False
        self.inventory = []
        self.health = 50
        return super().__init__(
            x, y, assets[self.name].get_width(), assets[self.name].get_height()
        )

    def display(self, window: pg.Surface, x_offset=0, y_offset=0):
        window.blit(assets[self.name], (self.x - x_offset, self.y - y_offset))

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
    for i2, item2 in enumerate(inv2):
        for i1, item1 in enumerate(inv1):
            if item1.name == item2.name:
                inv1[i1].count += item2.count
                break
        else:
            inv1.append(item2)

    return inv1
