import pygame as pg
from assets import assets

class Player(pg.Rect):

   def __init__(self, x, y, width, height, name) -> None:
        self.name = name
        return super().__init__(x, y, width, height)
   
   def display(self, window: pg.Surface, x_offset=0, y_offset=0):
        window.blit(assets[self.name], (self.x - x_offset, self.y - y_offset))
   