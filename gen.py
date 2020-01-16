import random


def genfloor(size, w, n=''):
    map = []
    if (size - 2) ** 2 <= w:
        raise SystemExit('Кол-во блоков превышает кол-во клеток')
    for i in range(size):
        if i == 0 or i == size - 1:
            map.append('#' * size)
        else:
            map.append('#' + '.' * (size - 2) + '#')
    for i in range(w):
        bx, by = random.randint(1, size - 2), random.randint(1, size - 2)
        line = list(map[bx])
        line[by] = '#'
        map[bx] = ''.join(line)
    else:
        bx, by = random.randint(1, size - 2), random.randint(1, size - 2)
        px, py = random.randint(1, size - 2), random.randint(1, size - 2)
        line = list(map[px])
        line[by] = '@'
        map[bx] = ''.join(line)
        line = list(map[px])
        # line[py] = '!'
        map[px] = ''.join(line)
    file = open(f'data/level{n}.txt', 'w', encoding='utf-8')
    print(*map, sep='\n', file=file)
    file.close()


genfloor(20, 0)
