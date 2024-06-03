from assets import *
import pygame as pg


# finds available or matching slots for an item
def find_slot(item, inventory):
    for i, button in enumerate(inventory):
        if button.item is None:
            return i
        elif button.item == item:
            return i
    return None


def manage_inventory(inventory, held): # call when mouse down
    x, y = pg.mouse.get_pos()
    for slot in inventory: 
        if slot.collidepoint((x, y)):
            if held.item == slot.item:
                slot.item.count += held.item.count
                held = None
            else:
                held.item, slot.item = slot.item, held.item

def render_health(window, health: int, maxHealth: int, pos: tuple[int, int]):
    x, y = pos

    outline_rect = pg.Rect(
        x,
        y,
        healthBarWidth + healthBarHeight / 2.5,
        healthBarHeight + healthBarHeight / 2.5,
    )

    health_rect = pg.Rect(
        x + healthBarHeight / 5,
        y + healthBarHeight / 5,
        healthBarWidth * health / maxHealth,
        healthBarHeight,
    )

    pg.draw.rect(window, (0, 0, 0), outline_rect)
    pg.draw.rect(window, (200, 50, 5), health_rect)
