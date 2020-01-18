import pygame
import os
import sys

FPS = 50
size = WIDTH, HEIGHT = 400, 300
pygame.init()
screen = pygame.display.set_mode(size)
road = False
can_defence = False
play = False
running = True
piczie = 50
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


tile_images = {'wall': load_image('box.png'), 'empty': load_image('floor.png'), 'road': load_image('road.png'),
               'ptower': load_image('blace.png')}
creep_image = pygame.transform.flip(load_image('creep.png'), True, False)

tile_width = tile_height = 50
