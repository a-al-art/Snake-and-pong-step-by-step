import sys
import random
import pygame
import pygame_menu

from config import ICON, FILE_BACK

pygame.init()
pygame.font.init()

# snake constance

# цветa
RED = (255, 0, 0)
BLACK = (0, 0, 0)
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
print(size)

# создаем окно с размером size
screen = pygame.display.set_mode(size)

# даём название окну
NAME = 'Snake game'
pygame.display.set_caption(NAME)

# делаем другую иконку окна
img = pygame.image.load(ICON)
pygame.display.set_icon(img)
timer = pygame.time.Clock()
# шрифт
comicsansms = pygame.font.SysFont('comicsansms', 32)

# фон для меню
fon_img = pygame.image.load(FILE_BACK)

# pong constance
# цвета
DARK_GREEN = (84, 140, 11)
# GREEN = (217, 245, 181)

# задаем раземры экрана
WIDTH = 460
HEIGHT = 530

FPS = 30
# шрифты
ARIAl = pygame.font.match_font('arial')
ARIAl_42 = pygame.font.Font(ARIAl, 42)
ARIAl_32 = pygame.font.Font(ARIAl, 32)

# название окна
TITLE = 'Single ping pong'

# парамерты платформы
PLAT_WIDTH = 150
PLAT_HEIGHT = 15
PLAT_SPEED = 15

# параметры шаркика
CIR_RADIUS = 15
CIR_SPEED = 10


# класс для змейки
class Snake:
    # с координатами поля
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # проверка внутри ли поля находится змейка
    def correct_coords(self):
        return 0 <= self.x < LEN_SQ and 0 <= self.y < LEN_SQ

    # магический метод для сравнения на равенство
    def __eq__(self, other):
        return isinstance(other, Snake) and self.x == other.x and self.y == other.y


# функция для рисования квадратиков (как для поля, так и для змейки)
def add_new_block(color, row, col):
    pygame.draw.rect(screen, color, [LEN_SQ + col * LEN_SQ + INDENT * (col + 1),
                                     TITLE_INDENT + LEN_SQ + row * LEN_SQ + INDENT * (row + 1),
                                     LEN_SQ, LEN_SQ])


def apple_square():
    # функция для получения рандомной клетки для яблочка
    def new_blocks():
        x = random.randint(0, NUM_SQ - 1)
        y = random.randint(0, NUM_SQ - 1)
        new_block = Snake(x, y)
        while new_block in snake_pos:
            new_block.x = random.randint(0, NUM_SQ - 1)
            new_block.y = random.randint(0, NUM_SQ - 1)
        return new_block

    # положение змейки
    snake_pos = [Snake(9, 8), Snake(9, 9), Snake(9, 10)]

    # положение яблочка
    apple = new_blocks()

    # смещения
    d_row = 0
    d_col = 1
    del_row = 0
    del_col = 1

    # очки
    score = 0

    # скорость змейки
    speed = 1

    # игровой цикл while
    while True:
        for eve in pygame.event.get():

            # обработка выхода
            if eve.type == pygame.QUIT:
                print('выход')
                pygame.quit()
                sys.exit()

            elif eve.type == pygame.KEYDOWN:
                # обработка нажатий клавиш-стрелок
                if eve.key == pygame.K_UP and d_col != 0:
                    del_row = -1
                    del_col = 0
                elif eve.key == pygame.K_DOWN and d_col != 0:
                    del_row = 1
                    del_col = 0
                elif eve.key == pygame.K_LEFT and d_row != 0:
                    del_row = 0
                    del_col = -1
                elif eve.key == pygame.K_RIGHT and d_row != 0:
                    del_row = 0
                    del_col = 1

                # выход на ESCAPE
                elif eve.key == pygame.K_ESCAPE:
                    print('выход escape')
                    pygame.quit()
                    sys.exit()

        screen.fill(MAIN_COLOR)

        # шапочка
        pygame.draw.rect(screen, TITLE_COL, [0, 0, size[0], TITLE_INDENT])

        # отображение текста со скоростью и резутьтатом на шапочке
        text_score = comicsansms.render(f'Счёт: {score}', True, BLACK)
        text_speed = comicsansms.render(f'Скорость: {speed}', True, BLACK)
        screen.blit(text_score, (LEN_SQ, LEN_SQ))
        screen.blit(text_speed, (LEN_SQ + 250, LEN_SQ))

        # рисуем игровое поле
        for row in range(NUM_SQ):
            for col in range(NUM_SQ):
                # проверка на четность => цвет квадратика
                if (col + row) % 2 == 0:
                    color = GREEN
                else:
                    color = WHITE

                add_new_block(color, row, col)

        # движение змейки и ее отрисовка
        # тк голова - последний эдемент списка
        head = snake_pos[-1]
        if not head.correct_coords():
            print('змейка врезалась в стенку')
            break
            # pygame.quit()
            # sys.exit()
        # отрисовка яблочка
        add_new_block(RED, apple.x, apple.y)
        for block in snake_pos:
            add_new_block(SNAKE_COLOR, block.x, block.y)

        pygame.display.flip()

        # встреча головы змейки и яблока:
        if apple == head:
            score += 1
            speed = score // 4 + 1
            snake_pos.append(apple)
            apple = new_blocks()

        # для поедания змейки самой себя
        d_row = del_row
        d_col = del_col

        new_head = Snake(head.x + d_row, head.y + d_col)

        if new_head in snake_pos:
            print('змейка врезалась в себя')
            break
            # pygame.quit()
            # sys.exit()
        snake_pos.append(new_head)
        snake_pos.pop(0)

        timer.tick(4 + speed)


# создание экрана и его названия
# screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()


# fon_img = pygame.image.load('fon.png')


def pong():
    # было ли перове столкновение
    c_pos = False
    c_x = 0
    c_y = CIR_SPEED

    # для операций с прямоугольными областями
    plat_rect = pygame.rect.Rect(WIDTH // 2 - PLAT_WIDTH // 2,
                                 HEIGHT - PLAT_HEIGHT * 2,
                                 PLAT_WIDTH,
                                 PLAT_HEIGHT)

    cir_rect = pygame.rect.Rect(WIDTH // 2 - CIR_RADIUS,
                                HEIGHT // 2 - CIR_RADIUS,
                                CIR_RADIUS * 2,
                                CIR_RADIUS * 2)

    # очки
    score = 0

    # игровой цикл
    finish = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            # выход на ESCAPE
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    continue

                # перезапуск игры
                elif event.key == pygame.K_r:
                    finish = False

                    # возвращение на начальные позиции
                    plat_rect.centerx = WIDTH // 2
                    plat_rect.bottom = HEIGHT - PLAT_HEIGHT

                    cir_rect.center = [WIDTH // 2, HEIGHT // 2]
                    c_x = 0
                    c_y = CIR_SPEED
                    c_pos = False

                    score = 0

        screen.fill(GREEN)

        if not finish:
            # получаем список нажатых клавишей
            keys = pygame.key.get_pressed()

            # проверка клавиш клавиатуры
            if keys[pygame.K_a]:
                plat_rect.x -= PLAT_SPEED
            elif keys[pygame.K_d]:
                plat_rect.x += PLAT_SPEED

            # если столкнулись платфонма и шарик
            if plat_rect.colliderect(cir_rect):
                if not c_pos:
                    if random.randint(0, 1) == 0:
                        c_x = CIR_SPEED
                    else:
                        c_x = -CIR_SPEED
                    c_pos = True

                c_y = -CIR_SPEED
                score += 1

            # рисуем платформу
            pygame.draw.rect(screen, DARK_GREEN, plat_rect)

        # скорости в зависимости от отражения
        cir_rect.x += c_x
        cir_rect.y += c_y

        # отражение шарика от полей и придание скорости
        if cir_rect.bottom >= HEIGHT:
            finish = True
            c_y = -CIR_SPEED

        elif cir_rect.top <= 0:
            c_y = CIR_SPEED

        elif cir_rect.left <= 0:
            c_x = CIR_SPEED

        elif cir_rect.right >= WIDTH:
            c_x = -CIR_SPEED

        # рисуем шарик
        pygame.draw.circle(screen, DARK_GREEN, cir_rect.center, CIR_RADIUS)

        # печатаем текст на экране
        score_on_screen = ARIAl_42.render(str(score), True, DARK_GREEN)
        if not finish:
            screen.blit(score_on_screen, [WIDTH // 2 - score_on_screen.get_width() // 2, 15])
        else:
            new_game_offer = ARIAl_32.render('Нажмите R для запуска игры', True, DARK_GREEN)
            esc_offer = ARIAl_32.render('Esc для выхода в главное меню', True, DARK_GREEN)
            screen.blit(score_on_screen, [WIDTH // 2 - score_on_screen.get_width() // 2, HEIGHT // 3])
            screen.blit(new_game_offer, [WIDTH // 2 - new_game_offer.get_width() // 2,
                                         HEIGHT // 3 + score_on_screen.get_height()])
            screen.blit(esc_offer, [WIDTH // 2 - new_game_offer.get_width() // 2 - 10,
                                    HEIGHT // 3 + score_on_screen.get_height() + 30])

        clock.tick(FPS)
        pygame.display.flip()


# встроенные темы в модуле menu
main_theme = pygame_menu.themes.THEME_GREEN.copy()
main_theme.set_background_color_opacity(0.7)

# экран с меню
menu = pygame_menu.Menu('Welcome', 400, 300,
                        theme=main_theme)
menu.add.text_input('Имя: ', default='Игрок 1')
menu.add.button('Играть в змейку', apple_square)
menu.add.button('Играть в пинг понг', pong)
menu.add.button('Выход', pygame_menu.events.EXIT)

# цикл для меню

while True:

    screen.blit(fon_img, (0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()
