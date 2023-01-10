# создали поле
import pygame

# цветa
MAIN_COLOR = (185, 247, 104)
WHITE = (255, 255, 255)
GREEN = (217, 245, 181)
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
# игровой цикл while
while True:
    for eve in pygame.event.get():
        if eve.type == pygame.QUIT:
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
            pygame.draw.rect(screen, color, (LEN_SQ + col * LEN_SQ + INDENT * (col + 1),
                                             TITLE_INDENT + LEN_SQ + row * LEN_SQ + INDENT * (row + 1),
                                             LEN_SQ, LEN_SQ))

    pygame.display.flip()