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
import startboard
import pygame
road = False
can_defence = False
fps = 10
size = 1000, 1000
screen = pygame.display.set_mode(size)
play = False
running = True
clock = pygame.time.Clock()

class Enemy:
    def __init__(self, hp, speed):
        pass


class Building:
    def __init__(self, fspeed, damage):
        pass


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, surf):

        for i in range(self.height):
            for j in range(self.width):

                rect = (self.left + j * self.cell_size, self.top + i * self.cell_size,
                        self.cell_size, self.cell_size)

                if self.board[i][j] == 0:
                    pygame.draw.rect(surf, (255, 255, 255), rect, 1)
                elif self.board[i][j] == 1:
                    pygame.draw.rect(surf, (189, 183, 107), rect)
                else:
                    pygame.draw.rect(surf, (0, 0, 205), rect)

    def get_cell(self, mouse_pos):
        xm, ym = mouse_pos
        for nl, line in enumerate(self.board):
            for nc, cell in enumerate(line):
                xc, yc = self.left + nl * self.cell_size, self.top + nc * self.cell_size
                if xc <= xm <= xc + self.cell_size and yc <= ym <= yc + self.cell_size:
                    return xc // self.cell_size, yc // self.cell_size

    def on_click(self, cell_coords):

        try:
            x, y = cell_coords
            if self.board[y][x] == 2:
                # pass
                self.board[y][x] = 0
            else:
                self.board[y][x] = 2
        except TypeError:
            pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


board = Board(40, 40)

board.set_view(0, 0, 25)
board.board = startboard.boardd
while running:
    screen.fill((0, 0, 0))
    board.render(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if event.button == 1:
            board.get_click(event.pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                board.board = [[0] * board.width for _ in range(board.height)]

    # screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()
print(board.board, sep='\n')