from inital import *
from random import randint
import pygame


def start_screen(img='MenuHQ.png'):  # обработка начального окна
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


def generate_level(lvl):  # генерация уровня
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
    return x, y


def draw_text(surf, text, size, x, y, color=pygame.Color('white')):  # отрисовка текста
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def place_tower(x, y):  # создание башен
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


def make_enemy(y, speed, hp):  # создание врага
    x = randint(5, 7)
    fx = 20
    fy = 20 - x - 1
    return Enemy(x, y, fx, fy, hp, speed)


class Tile(pygame.sprite.Sprite):  # инициализация клетки
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player:  # класс игрока
    def __init__(self):
        self.lives = 100

    def draw_lives_bar(self, surf, x, y, pct):  # отрисовка здоровья игрока
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


class Enemy(pygame.sprite.Sprite):  # класс врага
    def __init__(self, pos_x, pos_y, fx, fy, hp, speed, image=creep_image):
        super().__init__(creep_group, all_sprites)
        self.image_boom = load_image("boom.png")
        self.moove = True
        self.hp = hp
        self.speed = speed
        self.fx = fx
        self.fy = fy
        self.image = image
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self):  # обновление расположения врага и проверка на живучесть
        global SCORE
        if print_rect:
            pygame.draw.rect(gamescreen, pygame.Color('Red'), self.rect[:], 2)
        if self.moove:
            x, y = self.rect.x, self.rect.y
            tx, ty = x // sprite_size, y // sprite_size
            if ty != self.fy:
                self.rect.y += int(self.speed / 10 * ratio)
            elif tx != self.fx:
                self.rect.x += int(self.speed / 10 * ratio)
            elif tx == self.fx and ty == self.fy:
                player.lives -= 10
                self.moove = False

        if self.hp <= 0 and self.moove:
            self.moove = False
            self.image = self.image_boom
            SCORE += 25
            death.play()
            tasks.append(['bom', self, 10])

    def check_intersection(self, area):  # проверка на вхождение зоны врага в зону башни
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


class Building(pygame.sprite.Sprite):  # класс башни
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

    def update(self, *args):  # отрисовка башни
        if print_rect:
            pygame.draw.rect(gamescreen, pygame.Color('Cyan'), self.area[:], 2)
        else:
            pass


start_screen()
begin_attack = False
print_rect = False
font_name = pygame.font.match_font('arial')

# звуковая обстановка
boom = pygame.mixer.Sound(resource_path(os.path.join('data', 'boom_sound.wav')))
death = pygame.mixer.Sound(resource_path(os.path.join('data', 'death_sound.wav')))
pygame.mixer.music.load(resource_path(os.path.join('data', 'fon_music.mp3')))
pygame.mixer.music.set_volume(0.1)
tasks = []

# главный цикл прграммы
while pygame.event.wait().type != pygame.QUIT:
    pygame.mixer.music.play(loops=-1)

    all_sprites, tiles_group, creep_group, tower_group = \
        pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()

    is_start = True
    text = False

    # установка таймеров
    pygame.time.set_timer(FIRE, 1000)
    pygame.time.set_timer(start_wait, 5000)
    pygame.time.set_timer(spawn_creep, 1000)

    can_place = []
    level = load_level('level.txt')
    level_x, level_y = generate_level(level)
    size = width, height = level_x * tile_width + tile_width, level_y * tile_height + tile_height
    gamescreen = pygame.display.set_mode(size)

    pygame.init()
    player = Player()
    SCORE = 300
    COST = 100

    while True:
        all_sprites.draw(gamescreen)

        tower_group.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:

                    make_enemy(-1, 20, 10)
                elif event.button == 1:
                    place_tower(*event.pos)

            if event.type == pygame.QUIT:  # Выход из игры
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                if event.key == pygame.K_h:
                    # Отображение областей пересечения объектов
                    print_rect = not print_rect

            if event.type == start_wait and is_start is True:
                is_start = False
                begin_attack = True

            if event.type == spawn_creep and is_start is False:
                x = randint(1, 2)
                if x == 2:
                    make_enemy(0, randint(20, 23), randint(15, 18))

            if event.type == FIRE:  # атака врага башней
                for area in [tower.area[:] for tower in tower_group]:
                    col = [sprite for sprite in creep_group.sprites() if sprite.check_intersection(area)]
                    if col:
                        ncol = randint(0, len(col) - 1)
                        col[ncol].hp -= 6
                        boom.play(loops=1)
                        text_x = col[ncol].rect.x
                        text_y = col[ncol].rect.y
                        tasks.append(['hp', text_x, text_y, 10])

        if begin_attack:
            draw_text(gamescreen, "Attack!!!", 40, 750 * ratio, 200 * ratio, pygame.Color('red'))
        creep_group.update()
        # обработка задач выведения на холст временных изображений
        for n, task in enumerate(tasks):
            if task[0] == 'hp':
                draw_text(gamescreen, '-6', int(10 * (ratio / 0.5)), int(task[1] + 25 * ratio),
                          int(task[2] + 25 * ratio), pygame.Color('red'))
                tasks[n][3] -= 1
                if tasks[n][3] <= 0:
                    del tasks[n]
            elif task[0] == 'bom':
                task[2] -= 1
                if tasks[n][2] <= 0:
                    task[1].kill()

        # отрисовка текста и панели здоровья
        draw_text(gamescreen, str(SCORE), int(18 * (ratio / 0.5)), 200 * ratio, 10 * ratio)
        draw_text(gamescreen, f"Стоимость башни: {str(COST)}", int(15 * (ratio / 0.5)), 800 * ratio, 10 * ratio)
        player.draw_lives_bar(gamescreen, 5, 5, player.lives)

        if player.is_game_over():
            pygame.mixer.music.stop()
            start_screen('gameoverHQ.jpg')
            break
        clock.tick(FPS)
        pygame.display.flip()
