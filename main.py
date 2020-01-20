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

print_rect = True


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
        if print_rect:
            pygame.draw.rect(gamescreen, (0, 0, 0), self.rect[:], 2)
        x, y = self.rect.x, self.rect.y
        tx, ty = x // sprite_size, y // sprite_size
        if ty != self.fy:
            self.rect.y += int(self.speed / 10)
        elif tx != self.fx:
            self.rect.x += int(self.speed / 10)
        elif tx == self.fx and ty == self.fy:
            self.kill()


class Building(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, fspeed, damage, area, image=building_image):
        super().__init__(tower_group, all_sprites)
        self.image = image
        self.x = pos_x
        self.y = pos_y
        self.fspeed = fspeed
        self.damage = damage
        self.rect = self.image.get_rect().move(tile_width * pos_x - sprite_size // 2,
                                               tile_height * pos_y - sprite_size // 2)
        self.area = self.image.get_rect().move(tile_width * pos_x - sprite_size // 2,
                                               tile_height * pos_y - sprite_size // 2)
        self.area.move(-80, -80)

        self.area.inflate_ip(150, 130)

    def update(self, *args):
        if print_rect:
            pygame.draw.rect(gamescreen, (0, 0, 0), self.area[:], 2)
        else:
            pass

    def check_intersection(self, rect):
        x, y, w, h = self.area[:]
        x1 = x + w
        y1 = y + h
        xx, yy, ww, hh = rect
        xx1 = xx + ww
        yy1 = yy + hh
        rect = xx, yy, xx1, yy1
        selfrect = x, y, x1, y1

        return rect[0] <= selfrect[0] <= rect[3] and rect[1] <= selfrect[1] <= rect[2] or \
               rect[0] <= selfrect[3] <= rect[3] and rect[1] <= selfrect[1] <= rect[2] or \
               rect[0] <= selfrect[0] <= rect[3] and rect[1] <= selfrect[2] <= rect[2] or \
               rect[0] <= selfrect[3] <= rect[3] and rect[1] <= selfrect[2] <= rect[2]


def make_enemy(y, speed, hp):
    x = randint(5, 7)
    fx = 20
    fy = 20 - x - 1
    return Enemy(x, y, fx, fy, hp, speed)


def start_screen():
    fon = pygame.transform.scale(load_image('menuHQ.png'), (WIDTH, HEIGHT))
    gamescreen.blit(fon, (0, 0))
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

    creepsi = make_enemy(-1, randint(10, 25), 10)
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
            if event.key == pygame.K_t:
                print_rect = not print_rect
    for rect in [sprite.rect[:] for sprite in creep_group]:
        col =  [sprite for sprite in tower_group if sprite.check_intersection(rect)]
        if col:
            print(*col, sep='\n')
    tiles_group.draw(gamescreen)
    creep_group.draw(gamescreen)
    tower_group.draw(gamescreen)
    creep_group.update()
    tower_group.update()
    clock.tick(FPS)
    pygame.display.flip()
