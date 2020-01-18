'''
Враги хп урон скорость (сильнее с каждой волной + босс в конце (сила зависит от цвета)) враг машинка разных цветов
Защита скорострельность урон выстрел - спавн частиц
Поле (40 на 40 клеток 15 на 15 пикс, 5 толщина дороги, 1 враг, 3х3 сооружения) клетка
Экраны:
Меню Лого Старт
Игра Хп Золото Волна Пауза меню защиты (выбор защиты, апгрейд?) Старт Волны(5 шт) + босс
Победа Молодец Новая игра
Смэрть Не молодец Новая игра
'''

from inital import *


def start_screen():
    intro_text = ["Марио для бедных", "",
                  "Починил стены",
                  "теперь они твердые"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
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


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(player_group, all_sprites)
        self.image = image
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Enemy(Player):

    def __init__(self, pos_x, pos_y, hp, speed, image=creep_image):
        self.hp = hp
        self.speed = speed
        super().__init__(pos_x, pos_y, image)


class Building(Player):
    def __init__(self, pos_x, pos_y, fspeed, damage, area, image=tile_images['ptower']):
        super().__init__(pos_x, pos_y, image)
        self.fspeed = fspeed
        self.damage = damage
        self.area = area  # rect



def generate_level(level):
    new_player, x, y, p_pos = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('road', x, y)
                p_pos = x, y
                enemy = Enemy(x, y, 10, 20)
            elif level[y][x] == ':':
                Tile('road', x, y)
            elif level[y][x] == '%':
                Tile('empty', x, y)
                Building(x, y, 10, 20, (10, 10, 10, 10))
                # tower = Player(x, y, 'ptower')
    return enemy, x, y, p_pos


level = load_level('level.txt')
player, level_x, level_y, player_pos = generate_level(level)
size = width, height = level_x * tile_width + tile_width, level_y * tile_height + tile_height
pygame.init()
gamescreen = pygame.display.set_mode(size)
px, py = player_pos
while True:
    # camera.update(player)
    # for sprite in all_sprites:
    #     camera.apply(sprite)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                py -= 1
                player.rect.y -= player.rect.h
            elif event.key == pygame.K_DOWN:
                py += 1
                player.rect.y += player.rect.h
            elif event.key == pygame.K_RIGHT:
                px += 1
                player.rect.x += player.rect.w
            elif event.key == pygame.K_LEFT:
                px -= 1
                player.rect.x -= player.rect.w
    tiles_group.draw(gamescreen)
    player_group.draw(gamescreen)
    pygame.display.flip()
