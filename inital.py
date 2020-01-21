import pygame
import os
import sys
from PIL import Image

move = True
SCORE = 300
COST = 100
FPS = 60
sprite_size = 50
size = WIDTH, HEIGHT = 500, 500
FIRE = 30
is_start = True
start_wait = 31
spawn_creep = 29
ratio = sprite_size / 50
pygame.init()
gamescreen = pygame.display.set_mode(size)
pygame.display.set_caption("WWIII: Castle Defense")
road = False
can_defence = False
play = False
running = True
clock = pygame.time.Clock()



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
tile_images = {'wall': load_image('box.png'), 'empty': load_image('floor.png'), 'road': load_image('road.png'),
               'bplace': load_image('bplace.png')}
building_image = load_image('blace.png')
creep_image = load_image('creep.png')
