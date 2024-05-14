import pygame
import os
import random

pygame.init()
# Цвета в RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# FPS
FPS = 80
clock = pygame.time.Clock()

# Screen
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping-pong")

# Шрифт для текста
font20 = pygame.font.Font('fonts/freesans5.ttf', 20)
font40 = pygame.font.Font('fonts/freesans5.ttf', 49)

# Изображение победы
images_list = os.listdir("images")
winImagePrev = pygame.image.load(f"images/{images_list[random.randint(0, len(images_list) - 1)]}")
winImage = pygame.transform.scale(winImagePrev, (WIDTH, HEIGHT))
winImage.set_alpha(170)

# Звуки
hitSound = pygame.mixer.Sound("sounds/shot2.mp3")
scoreSound = pygame.mixer.Sound("sounds/score.mp3")
losingSound = pygame.mixer.Sound("sounds/applause.mp3")
