# создали змейку
import pygame

# цветa
MAIN_COLOR = (185, 247, 104)
WHITE = (255, 255, 255)
GREEN = (217, 245, 181)
SNAKE_COLOR = (84, 140, 11)
TITLE_COL = (227, 240, 211)
# отступы
INDENT = 1
TITLE_INDENT = 70
# размер одного маленького квадратика
LEN_SQ = 20
NUM_SQ = 20
# расчитываем размер экрана
size = [LEN_SQ * NUM_SQ + 2 * LEN_SQ + INDENT * NUM_SQ,
        LEN_SQ * NUM_SQ + 2 * LEN_SQ + INDENT * NUM_SQ + TITLE_INDENT]

# создаем окно с размером size
screen = pygame.display.set_mode(size)
# даём название окну
pygame.display.set_caption('Snake game')


# функция для рисования квадратиков (как для поля, так и для змейки)
def add_new_block(color, row, col):
    pygame.draw.rect(screen, color, [LEN_SQ + col * LEN_SQ + INDENT * (col + 1),
                                     TITLE_INDENT + LEN_SQ + row * LEN_SQ + INDENT * (row + 1),
                                     LEN_SQ, LEN_SQ])


class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y


snake_pos = [Snake(9, 9)]

# игровой цикл while
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('выход')
            pygame.quit()

    screen.fill(MAIN_COLOR)
    pygame.draw.rect(screen, TITLE_COL, [0, 0, size[0], TITLE_INDENT])

    # рисуем игровое поле
    for row in range(NUM_SQ):
        for col in range(NUM_SQ):
            # проверка на четность => цвет квадратика
            if (col + row) % 2 == 0:
                color = GREEN
            else:
                color = WHITE

            add_new_block(color, row, col)

    for block in snake_pos:
        add_new_block(SNAKE_COLOR, block.x, block.y)
    pygame.display.flip()