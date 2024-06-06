from assets import *
import pygame as pg
from EPT import blit_text, Button


class MainMenu:
    def __init__(self) -> None:
        self.target_resolution = 900, 500  # default game resolution
        self.ui_size = 48  # default game ui size
        self.is_active = True

    def run(self, window: pg.Surface) -> str:
        window_width, window_height = window.get_size()

        # buttons
        play_button = Button(
            (
                window_width / 2 - (button_size * menu_scale) / 2,
                window_height / 2 - (button_size * menu_scale) / 2,
            ),
            assets["Play"],
        )
        settings_button = Button(
            (
                0,
                window_height - (button_size * menu_scale),
            ),
            assets["Settings"],
        )
        close_button = Button(
            (
                0, 0
            ),
            assets["Close"]
        )
        showSettings = False


        while self.is_active:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_active = False
                    return "quit"
                if event.type == pg.MOUSEBUTTONUP:
                    if showSettings:
                        if close_button.clicked():
                            showSettings = False
                    else:
                        if play_button.clicked():
                            return "play"
                        if settings_button.clicked():
                            showSettings = True
            window.fill((0, 0, 0))
            if showSettings:
                pass
            else:  
                blit_text(window, "Survival Island",(window_width / 2 - (button_size * menu_scale) / 2,
                window_height / 2 - (button_size * menu_scale)*1.2,), (255, 255, 255))
                play_button.display(window)
                settings_button.display(window)
            pg.display.update()
