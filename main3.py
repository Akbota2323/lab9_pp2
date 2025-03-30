import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Определение цветов
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Параметры окна
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Paint Application")
screen.fill(white)

# Настройки рисования
clock = pygame.time.Clock()
drawing = False
last_pos = None
tool = "pencil"
radius = 5
current_color = black

# Функция для рисования линии

def draw_line(surface, color, start_pos, end_pos, width):
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start_pos[0] + float(i) / distance * dx)
        y = int(start_pos[1] + float(i) / distance * dy)
        pygame.draw.circle(surface, color, (x, y), width)

# Функция для рисования прямоугольника

def draw_rectangle(surface, color, start_pos, end_pos):
    x = min(start_pos[0], end_pos[0])
    y = min(start_pos[1], end_pos[1])
    width = abs(start_pos[0] - end_pos[0])
    height = abs(start_pos[1] - end_pos[1])
    pygame.draw.rect(surface, color, (x, y, width, height), 2)

# Функция для рисования квадрата

def draw_square(surface, color, start_pos, end_pos):
    x = min(start_pos[0], end_pos[0])
    y = min(start_pos[1], end_pos[1])
    side = min(abs(start_pos[0] - end_pos[0]), abs(start_pos[1] - end_pos[1]))
    pygame.draw.rect(surface, color, (x, y, side, side), 2)

# Функция для рисования прямоугольного треугольника

def draw_right_triangle(surface, color, start_pos, end_pos):
    pygame.draw.polygon(surface, color, [start_pos, (start_pos[0], end_pos[1]), end_pos], 2)

# Функция для рисования равностороннего треугольника

def draw_equilateral_triangle(surface, color, start_pos, end_pos):
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    side = int((dx**2 + dy**2)**0.5)
    pygame.draw.polygon(surface, color, [
        start_pos,
        (start_pos[0] + side, start_pos[1]),
        (start_pos[0] + side // 2, start_pos[1] - int(side * (3**0.5) / 2))
    ], 2)

# Функция для рисования ромба

def draw_rhombus(surface, color, start_pos, end_pos):
    cx = (start_pos[0] + end_pos[0]) // 2
    cy = (start_pos[1] + end_pos[1]) // 2
    dx = abs(end_pos[0] - start_pos[0]) // 2
    dy = abs(end_pos[1] - start_pos[1]) // 2
    pygame.draw.polygon(surface, color, [
        (cx, start_pos[1]),
        (end_pos[0], cy),
        (cx, end_pos[1]),
        (start_pos[0], cy)
    ], 2)

# Функция для рисования круга

def draw_circle(surface, color, start_pos, end_pos):
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    radius = int((dx**2 + dy**2)**0.5)
    pygame.draw.circle(surface, color, start_pos, radius, 2)

# Главный цикл программы
running = True
start_pos = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True
                start_pos = event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
                if tool == "rectangle" and start_pos:
                    draw_rectangle(screen, current_color, start_pos, event.pos)
                elif tool == "square" and start_pos:
                    draw_square(screen, current_color, start_pos, event.pos)
                elif tool == "circle" and start_pos:
                    draw_circle(screen, current_color, start_pos, event.pos)
                elif tool == "right_triangle" and start_pos:
                    draw_right_triangle(screen, current_color, start_pos, event.pos)
                elif tool == "equilateral_triangle" and start_pos:
                    draw_equilateral_triangle(screen, current_color, start_pos, event.pos)
                elif tool == "rhombus" and start_pos:
                    draw_rhombus(screen, current_color, start_pos, event.pos)
                start_pos = None
        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if tool == "pencil":
                    draw_line(screen, current_color, last_pos, event.pos, radius)
                elif tool == "eraser":
                    draw_line(screen, white, last_pos, event.pos, radius)
                last_pos = event.pos
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                tool = "rectangle"
            elif event.key == pygame.K_s:
                tool = "square"
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_i:
                tool = "right_triangle"
            elif event.key == pygame.K_q:
                tool = "equilateral_triangle"
            elif event.key == pygame.K_h:
                tool = "rhombus"
            elif event.key == pygame.K_p:
                tool = "pencil"
            elif event.key == pygame.K_e:
                tool = "eraser"
            elif event.key == pygame.K_1:
                current_color = black
            elif event.key == pygame.K_2:
                current_color = red
            elif event.key == pygame.K_3:
                current_color = green
            elif event.key == pygame.K_4:
                current_color = blue

    pygame.display.update()
    clock.tick(60)
