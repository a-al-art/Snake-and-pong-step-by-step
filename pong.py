import pygame_menu
import pygame
import random

pygame.init()
pygame.font.init()

# цвета
DARK_GREEN = (84, 140, 11)
GREEN = (217, 245, 181)

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

# создание экрана и его названия
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()

fon_img = pygame.image.load('fon.png')


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
            new_game_offer = ARIAl_32.render('нажмите R для запуска игры', True, DARK_GREEN)
            screen.blit(score_on_screen, [WIDTH // 2 - score_on_screen.get_width() // 2, HEIGHT // 3])
            screen.blit(new_game_offer, [WIDTH // 2 - new_game_offer.get_width() // 2,
                                         HEIGHT // 3 + score_on_screen.get_height()])

        clock.tick(FPS)
        pygame.display.flip()


# встроенные темы в модуле menu
main_theme = pygame_menu.themes.THEME_GREEN.copy()
main_theme.set_background_color_opacity(0.7)

# экран с меню
menu = pygame_menu.Menu('Welcome', 400, 300,
                        theme=main_theme)
menu.add.text_input('Имя :', default='Игрок 1')
menu.add.button('Играть', pong)
menu.add.button('Выход', pygame_menu.events.EXIT)

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