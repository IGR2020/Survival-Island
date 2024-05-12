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
        

