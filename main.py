"""
Враги хп урон скорость (сильнее с каждой волной + босс в конце (сила зависит от цвета)) враг машинка разных цветов
Защита скорострельность урон выстрел - спавн частиц
Поле (40 на 40 клеток 15 на 15 пикс, 5 толщина дороги, 1 враг, 3х3 сооружения) клетка
Экраны:
Меню Лого Старт
Игра Хп Золото Волна Пауза меню защиты (выбор защиты, апгрейд?) Старт Волны(5 шт) + босс
Победа Молодец Новая игра
Смэрть Не молодец Новая игра
"""

from inital import *
from random import randint


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(creep_group, all_sprites)
        self.image = image
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Enemy(Player):

    def __init__(self, pos_x, pos_y, fx, fy, hp, speed, image=creep_image):
        self.hp = hp
        self.speed = speed
        self.fx = fx
        self.fy = fy
        super().__init__(pos_x, pos_y, image)

    def update(self):
        x, y = self.rect.x, self.rect.y
        tx, ty = x // sprite_size, y // sprite_size
        if ty != self.fy:
            self.rect.y += int(1 * (self.speed / 10))
        elif tx != self.fx:
            self.rect.x += int(1 * (self.speed / 10))
        elif tx == self.fx and ty == self.fy:
            self.kill()


class Building(Player):
    def __init__(self, pos_x, pos_y, fspeed, damage, area, image=building_image):
        super().__init__(pos_x, pos_y, image)
        self.fspeed = fspeed
        self.damage = damage
        self.area = area  # rect
        self.rect = self.image.get_rect().move(tile_width * pos_x - sprite_size // 2,
                                               tile_height * pos_y - sprite_size // 2)


def make_enemy(y, speed, hp):
    x = randint(5, 7)
    fx = 20
    fy = 20 - x - 1
    return Enemy(x, y, fx, fy, hp, speed)


def start_screen():
    fon = pygame.transform.scale(load_image('menuHQ.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for eventt in pygame.event.get():
            if eventt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif eventt.type == pygame.KEYDOWN or eventt.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


start_screen()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x), list(map(lambda x: x.ljust(max_width, '.'), level_map))))


def generate_level(lvl):
    enemy, x, y, p_pos = None, None, None, None
    for y in range(len(lvl)):
        for x in range(len(lvl[y])):
            if lvl[y][x] == '.':
                Tile('empty', x, y)
            elif lvl[y][x] == '#':
                Tile('wall', x, y)
            elif lvl[y][x] == '@':
                Tile('road', x, y)
            elif lvl[y][x] == ':':
                Tile('road', x, y)
            elif lvl[y][x] == '%':
                Tile('empty', x, y)
                Building(x, y, 10, 20, (10, 10, 10, 10))

    creepsi = [make_enemy(-1 * i, randint(10, 25), 10) for i in range(1, 10)]
    # enemy = Enemy(6, -1, 20, 13, 10, 30)
    return creepsi, x, y


level = load_level('level.txt')
creeps, level_x, level_y = generate_level(level)
size = width, height = level_x * tile_width + tile_width, level_y * tile_height + tile_height
pygame.init()
gamescreen = pygame.display.set_mode(size)

while True:

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            make_enemy(-1, randint(10, 30), 10)

        if event.type == pygame.QUIT:
            terminate()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                terminate()

    creep_group.update()
    # print(enemy.rect)
    # print(enemy.rect.x // sprite_size, enemy.rect.y // sprite_size)

    tiles_group.draw(gamescreen)
    creep_group.draw(gamescreen)
    clock.tick(FPS)
    pygame.display.flip()
