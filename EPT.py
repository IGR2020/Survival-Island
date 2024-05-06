import pygame
from os import listdir
from os.path import join, isfile

pygame.font.init()


def blit_text(win, text, pos, colour=(0, 0, 0), size=30, font="arialblack", blit=True):
    text = str(text)
    font_style = pygame.font.SysFont(font, size)
    text_surface = font_style.render(text, False, colour)
    if blit:
        win.blit(text_surface, pos)
    return text_surface


class Button(pygame.Rect):
    def __init__(self, pos, image, scale=1, *args):
        x, y = pos
        width, height = image.get_width() * scale, image.get_height() * scale
        super().__init__(x, y, width, height)
        self.image = pygame.transform.scale(image, (width, height))
        if len(args) == 1:
            self.info = args[0]
        else:
            self.info = args

    def clicked(self):
        pos = pygame.mouse.get_pos()
        if self.collidepoint(pos):
            return True
        return False

    def display(self, win):
        win.blit(self.image, self)


def load_assets(path, size: int = None):
    sprites = {}
    for file in listdir(path):
        if not isfile(join(path, file)):
            continue
        if size is None:
            sprites[file] = pygame.image.load(join(path, file))
        else:
            sprites[file] = pygame.transform.scale(
                pygame.image.load(join(path, file)), size
            )
    return sprites


def remove_prefix(str: str, prefix: str):
    return str[len(prefix) :] if str.startswith(prefix) else str
