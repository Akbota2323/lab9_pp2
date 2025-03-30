import pygame
import time
import random

# Инициализация pygame
pygame.init()

# Цвета
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
background_color = (204, 51, 255)

# Размеры дисплея
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("SNAKE")

# Настройки игры
clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

# Шрифты
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Функция для отображения счёта

def Your_score(score):
    value = score_font.render("Your score: " + str(score), True, black)
    dis.blit(value, [0, 0])

# Функция для отрисовки змеи

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

# Функция для отображения сообщений

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

# Основной цикл

def gameLoop():
    game_over = False
    game_close = False

    # Начальная позиция
    x1 = dis_width / 2
    y1 = dis_height / 2

    # Изменения координат
    x1_change = 0
    y1_change = 0

    # Список для сегментов змеи и её длина
    snake_List = []
    Length_of_snake = 1

    # Генерация первой еды и её таймера
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    food_timer = time.time()  # Время создания еды
    food_weight = random.randint(1, 3)  # Вес еды

    while not game_over:

        while game_close == True:
            dis.fill(background_color)
            message("You've lost! Press Q to exit or C to replay the game.", white)
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Проверка выхода за границы экрана
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(background_color)

        # Проверка времени жизни еды
        if time.time() - food_timer > 5:  # Еда исчезает через 5 секунд
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            food_timer = time.time()  # Сброс таймера
            food_weight = random.randint(1, 3)  # Новый вес еды

        # Отрисовка еды
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

        # Обновление позиции змеи
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Проверка столкновения головы змеи с её телом
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)

        pygame.display.update()

        # Проверка на съедение еды
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            food_timer = time.time()  # Сброс таймера еды
            food_weight = random.randint(1, 3)  # Новый вес еды
            Length_of_snake += food_weight  # Увеличение длины змеи в зависимости от веса еды

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Запуск игры
gameLoop()

