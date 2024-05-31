from assets import *
import pygame as pg

def draw_darkness_filter_at_player(window, player, x_offset, y_offset) -> None:
    assets["Filter"].fill(pg.color.Color("White"))
    assets["Filter"].blit(assets["Darkness"], (player.x - x_offset - darkness_size/2, player.y - y_offset - darkness_size/2))
    window.blit(assets["Filter"], (0, 0), special_flags=pg.BLEND_RGBA_SUB)