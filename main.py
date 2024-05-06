import pygame as pg

WIDTH, HEIGHT = 900, 500
window = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
pg.display.set_caption("You Probably Wont Survive")

run = True
clock = pg.time.Clock()
FPS = 60

def display():

    window.fill((200, 120, 90))

    pg.display.update()

while run:

    for event in pg.event.get():

        if event.type == pg.QUIT:
            run = False

    display()

pg.quit()
quit()