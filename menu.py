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
        back_button = Button((0, 0), assets["Back"])
        text_box_resolution = Button((100, 150), assets["Text Box Inactive"], 1, "900 500")
        plus_button = Button((text_box_resolution.right - button_size/2, button_size*menu_scale+300), assets["Plus"])
        minus_button = Button((plus_button.right + 150, plus_button.y), assets["Minus"])
        is_typing_resolution = False
        showSettings = False

        while self.is_active:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_active = False
                    return "quit"
                if event.type == pg.KEYDOWN:
                    if is_typing_resolution:
                        if event.key == pg.K_BACKSPACE:
                            text_box_resolution.info = text_box_resolution.info[:-1]
                        else:
                            text_box_resolution.info += event.unicode
                if event.type == pg.MOUSEBUTTONUP:
                    if showSettings:
                        if back_button.clicked():
                            showSettings = False
                        if plus_button.clicked():
                            self.ui_size += 2
                        if minus_button.clicked():
                            self.ui_size -= 2
                        if text_box_resolution.clicked():
                            is_typing_resolution = True
                            text_box_resolution.image = assets["Text Box Active"]
                        else:
                            is_typing_resolution = False
                            text_box_resolution.image = assets["Text Box Inactive"]
                    else:
                        text_box_resolution.image = assets["Text Box Inactive"]
                        is_typing_resolution = False
                        if play_button.clicked():
                            resolution = text_box_resolution.info.split()
                            try:
                                r_width = int(resolution[0]) 
                                r_height = int(resolution[1])
                                self.target_resolution = r_width, r_height
                            except Exception as e:
                                print(e)
                                print("Cannot convert new resolution to int, using default resolution (900x500)")
                            return "play"
                        if settings_button.clicked():
                            showSettings = True
            window.fill((0, 0, 0))
            if showSettings:
                back_button.display(window)
                blit_text(
                    window,
                    "Target Resolution",
                    (100, 100),
                    colour=(200, 200, 255),
                    size=35,
                )
                blit_text(window, "G.U.I scale", (text_box_resolution.right, 300), (190, 190, 255), 50)
                text_box_resolution.display(window)
                blit_text(window, text_box_resolution.info, (text_box_resolution.x + text_box_resolution.width/25, text_box_resolution.y + text_box_resolution.height/25))
                plus_button.display(window)
                blit_text(window, self.ui_size, (plus_button.right + 50, plus_button.y), colour=(180, 180, 255), size=50)
                minus_button.display(window)
            else:
                blit_text(
                    window,
                    "Survival Island",
                    (
                        window_width / 2,
                        window_height / 2 - (button_size * menu_scale) * 2,
                    ),
                    (255, 255, 255),
                    50,
                    center=True,
                )
                play_button.display(window)
                settings_button.display(window)
            pg.display.update()
