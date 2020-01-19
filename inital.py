import pygame
import os
import sys
from PIL import Image

move = True
FPS = 60
sprite_size = 35
size = WIDTH, HEIGHT = 500, 500
pygame.init()
screen = pygame.display.set_mode(size)
road = False
can_defence = False
play = False
running = True
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
creep_group = pygame.sprite.Group()


def resize_image(sizer, exepte=()):
    width, height = sizer
    os.chdir(os.getcwd() + '\\data')
    for pic in os.listdir(path='.'):
        pic: str
        if not pic.endswith('HQ.png') and pic.endswith('.png') and pic not in exepte:
            img = Image.open(pic[:-4] + 'HQ.png')
            if pic == 'blace.png':
                resized_img = img.resize((width * 2, height * 2), Image.ANTIALIAS)
            else:
                resized_img = img.resize((width, height), Image.ANTIALIAS)
            resized_img.save(pic)
    os.chdir(os.getcwd()[:-5])


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


tile_width = tile_height = sprite_size
resize_image((tile_width, tile_height))
tile_images = {'wall': load_image('box.png'), 'empty': load_image('floor.png'), 'road': load_image('road.png')}
building_image = load_image('blace.png')
creep_image = load_image('creep.png')
