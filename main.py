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

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, pygame.Color('white'))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def place_tower(x, y):
    global COST, SCORE
    for rect in can_place:
        rx1, ry1 = map(lambda x: x * sprite_size, rect)
        rx2, ry2 = rx1 + sprite_size, ry1 + sprite_size

        if rx1 <= x <= rx2 and ry1 <= y <= ry2:
            rx1, ry1 = rx1 // sprite_size, ry1 // sprite_size
            if COST > SCORE:
                return False
            else:
                Tile('empty', rx1, ry1)
                Building(rx1, ry1)
                SCORE -= COST
                COST = int(COST * 1.1)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player:
    def __init__(self):
        self.lives = 100

    def draw_lives_bar(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = int(142 * ratio)
        BAR_HEIGHT = int(20 * ratio)
        fill = (pct / 100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surf, pygame.Color('orange'), fill_rect)
        pygame.draw.rect(surf, pygame.Color('white'), outline_rect, 2)

    def is_game_over(self):
        if self.lives <= 0:
            return True
        return False


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, fx, fy, hp, speed, image=creep_image):
        super().__init__(creep_group, all_sprites)
        self.hp = hp
        self.speed = speed
        self.fx = fx
        self.fy = fy
        self.image = image
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self):
        global SCORE
        if print_rect:
            pygame.draw.rect(gamescreen, (0, 0, 0), self.rect[:], 2)
        x, y = self.rect.x, self.rect.y
        tx, ty = x // sprite_size, y // sprite_size
        if ty != self.fy:
            self.rect.y += int(self.speed / 10)
        elif tx != self.fx:
            self.rect.x += int(self.speed / 10)
        elif tx == self.fx and ty == self.fy:
            player.lives -= 10
            self.kill()

        if self.hp <= 0:
            self.kill()
            SCORE += 25

    def check_intersection(self, area):
        x, y, w, h = self.rect[:]
        x1 = x + w
        y1 = y + h
        xx, yy, ww, hh = area
        xx1 = xx + ww
        yy1 = yy + hh
        s1 = (xx <= x <= xx1) or (xx <= x1 <= xx1)
        s2 = (yy <= y <= yy1) or (yy <= y1 <= yy1)
        s3 = (x <= xx <= x1) or (x <= xx1 <= x1)
        s4 = (y <= yy <= y1) or (y <= yy1 <= y1)
        if ((s1 and s2) or (s3 and s4)) or ((s1 and s4) or (s3 and s2)):
            return True
        else:
            return False


class Building(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image=building_image):
        super().__init__(tower_group, all_sprites)
        self.image = image
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(tile_width * pos_x - sprite_size // 2,
                                               tile_height * pos_y - sprite_size // 2)
        self.area = self.image.get_rect().move(tile_width * pos_x - sprite_size // 2,
                                               tile_height * pos_y - sprite_size // 2)
        self.area.move(-100 * ratio, -100 * ratio)

        self.area.inflate_ip(170 * ratio, 150 * ratio)

    def update(self, *args):
        if print_rect:
            pygame.draw.rect(gamescreen, (0, 0, 0), self.area[:], 2)
        else:
            pass


def make_enemy(y, speed, hp):
    x = randint(5, 7)
    fx = 20
    fy = 20 - x - 1
    return Enemy(x, y, fx, fy, hp, speed)


def start_screen(img='MenuHQ.png'):
    fon = pygame.transform.scale(load_image(img), (WIDTH, HEIGHT))
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


# start_screen()


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
                Tile('bplace', x, y)
                can_place.append((x, y))
                # Building(x, y)

    return x, y


while pygame.event.wait().type != pygame.QUIT:
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    creep_group = pygame.sprite.Group()
    tower_group = pygame.sprite.Group()
    can_place = []
    is_start = True
    pygame.time.set_timer(FIRE, 300)
    pygame.time.set_timer(start_wait, 1000)
    pygame.time.set_timer(spawn_creep, 1000)
    level = load_level('level.txt')
    level_x, level_y = generate_level(level)
    size = width, height = level_x * tile_width + tile_width, level_y * tile_height + tile_height
    pygame.init()
    gamescreen = pygame.display.set_mode(size)
    player = Player()
    print(len(can_place))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    make_enemy(-1, 20, 10)
                elif event.button == 1:
                    place_tower(*event.pos)

            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                if event.key == pygame.K_t:
                    print_rect = not print_rect

            if event.type == FIRE:
                for area in [tower.area[:] for tower in tower_group]:
                    col = [sprite for sprite in creep_group if sprite.check_intersection(area)]
                    if col:
                        col[randint(0, len(col) - 1)].hp -= 2
            if event.type == start_wait and is_start is True:
                is_start = False
                print('Attack!', is_start)
            if event.type == spawn_creep and is_start is False:
                if randint(1, 3) == 3:
                    print('spawned')
                    make_enemy(-1, randint(15, 25), randint(15, 25))


        all_sprites.draw(gamescreen)
        creep_group.update()
        tower_group.update()
        draw_text(gamescreen, str(SCORE), int(18 * (ratio / 0.5)), 200 * ratio, 10 * ratio)
        player.draw_lives_bar(gamescreen, 5, 5, player.lives)
        if player.is_game_over():
            start_screen('gameoverHQ.jpg')
            break
        clock.tick(FPS)
        pygame.display.flip()
