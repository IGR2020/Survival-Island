from assets import *
import pygame as pg


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
    def __init__(self, x, y, name, value=None):
        super().__init__(
            x, y, assets[name].get_width(), assets[name].get_height(), name
        )
        if value is None:
            self.value = []
        else:
            self.value = value
