import pygame as pg
from assets import assets
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
        return super().__init__(x, y, assets[self.name].get_width(), assets[self.name].get_height())
   
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
        for collum in land:
            for block in collum:
                if block.name in ("Calm Water.png", "Calm Moderate Water.png", "Calm Deep Water.png", "Water.png") and self.colliderect(block):
                    if self.y_vel < 0:
                        self.top = block.bottom
                    else:
                        self.bottom = block.top
        self.x += self.x_vel * dt
        for collum in land:
            for block in collum:
                if block.name in ("Calm Water.png", "Calm Moderate Water.png", "Calm Deep Water.png", "Water.png") and self.colliderect(block):
                    if self.x_vel < 0:
                        self.left = block.right
                    else:
                        self.right = block.left
        if not self.isMovingH:
            self.stopMovingH()
        else:
            self.isMovingH = False
        if not self.isMovingV:
            self.stopMovingV()
        else:
            self.isMovingV = False
          

def agrivate_inventory(inv1, inv2):
    aggrivated_inv = []
    if len(inv1) == 0:
        aggrivated_inv = inv2
    for item1 in inv1:
        for item2 in inv2:
            if item1.name == item2.name:
                aggrivated_inv.append(Item(item1.name, item1.count + item2.count))
                break
    return aggrivated_inv