import pygame
import sys
from pygame.locals import *
import random
import time

# Инициализация pygame
pygame.init()

# Настройки FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Цвета
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Размеры экрана и начальные параметры
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0
COIN_THRESHOLD = 5  # Количество монет для увеличения скорости врагов

# Шрифты и текст
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Загрузка фона
background = pygame.image.load("AnimatedStreet.png")

# Настройка дисплея
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

# Класс монеты
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        original_image = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(original_image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-600, 0))
        self.value = random.randint(1, 3)  # Случайный вес монеты (1-3)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            self.reset_position()

    def reset_position(self):
        self.rect.top = random.randint(-600, 0)
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), self.rect.top)
        self.value = random.randint(1, 3)  # Обновление веса монеты

# Создание объектов
P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Событие увеличения скорости
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Отображение фона и информации о счете
    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    coins_collected = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coins_collected, (SCREEN_WIDTH - 120, 10))

    # Движение и отрисовка объектов
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Проверка столкновения с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Проверка сбора монеты
    if pygame.sprite.spritecollideany(P1, coins):
        for coin in coins:
            if pygame.sprite.collide_rect(P1, coin):
                COINS_COLLECTED += coin.value
                coin.reset_position()

        # Увеличение скорости врага после сбора N монет
        if COINS_COLLECTED >= COIN_THRESHOLD:
            SPEED += 1
            COINS_COLLECTED = 0  # Сброс монет для следующего порога

    pygame.display.update()
    FramePerSec.tick(FPS)
