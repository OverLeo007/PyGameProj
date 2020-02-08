import pygame
import os
import sys
from PIL import Image

# Основные значения
FPS = 60
sprite_size = 25  # Параметр, регулирующий размер экрана (для получения значения в пикселях умножить на 20)
size = WIDTH, HEIGHT = 500, 500
FIRE = 30
start_wait = 31
spawn_creep = 29
generate_text = 28
ratio = sprite_size / 50
pygame.init()
gamescreen = pygame.display.set_mode(size)
pygame.display.set_caption("WWIII: Castle Defense")
clock = pygame.time.Clock()
move = True


def resource_path(relative):
    # функция позволяющая импортироать файлы при компиляции
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    else:
        return os.path.join(os.path.abspath("."), relative)


def load_level(filename):  # загрузка уровня
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x), list(map(lambda x: x.ljust(max_width, '.'), level_map))))


def resize_image(sizer, exepte=()):  # изменение размера изображения
    width, height = sizer
    os.chdir(os.getcwd() + '\\data')
    for pic in os.listdir(path='.'):
        pic: str
        if not pic.endswith('HQ.png') and pic.endswith('.png') and pic not in exepte:
            img = Image.open(resource_path(pic[:-4] + 'HQ.png'))
            if pic == 'blace.png':
                resized_img = img.resize((width * 2, height * 2), Image.ANTIALIAS)
            else:
                resized_img = img.resize((width, height), Image.ANTIALIAS)
            resized_img.save(pic)
    os.chdir(os.getcwd()[:-5])


def load_image(name, color_key=None):  # загрузка и обработка изображения
    fullname = resource_path(os.path.join('data', name))
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


def terminate():  # выход из программы
    pygame.quit()
    sys.exit()


# загрузка изображений
gameIcon = load_image('creep.png')
pygame.display.set_icon(gameIcon)

tile_width = tile_height = sprite_size
resize_image((tile_width, tile_height))
tile_images = {'wall': load_image('box.png'), 'empty': load_image('floor.png'), 'road': load_image('road.png'),
               'bplace': load_image('bplace.png')}
building_image = load_image('blace.png')
creep_image = load_image('creep.png')
