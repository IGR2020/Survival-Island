from assets import *
import pygame as pg
from time import time
from EPT import blit_text

class Item:
    def __init__(self, name, count):
        self.name = name
        self.count = count
        self.image_width = assets[self.name].get_width()

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

    def destroy(self): # reduces the health of the structure and destroys it if health = 0 and return its value if its health is 0
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

