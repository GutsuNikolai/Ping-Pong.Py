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
class Striker():
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height

        self.speed = speed
        self.color = color

        self.playerRect = pygame.Rect(posx, posy, width, height)
        self.player = pygame.draw.rect(screen, self.color, self.playerRect)

    # Отображение ракетки на экране
    def display(self):
        self.player = pygame.draw.rect(screen, self.color, self.playerRect)

    # Оновление состояния ракетки
    def update(self, yFac):
        self.posy = self.posy + self.speed * yFac

        # Контроль выхода за экран
        if self.posy <= 0:
            self.posy = 0
        elif self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT - self.height

        self.playerRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    # Рендер текста и создание прямоугольника для текста
    def displayScore(self, text, score, x, y, color):
        text = font20.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)  # Позиционирование

        screen.blit(text, textRect)

    def getRect(self):
        return self.playerRect

# Ball
class Ball():
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac = 1
        self.yFac = -1
        self.ball = pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)
        self.firstTime = 1

    # Отображение
    def display(self, ):
        self.ball = pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)

    def update(self):
        self.posy += self.speed * self.yFac
        self.posx += self.speed * self.xFac

        # Имитация физики при столкновении с объектами
        if self.posy <= 0 or self.posy >= HEIGHT:
            self.yFac *= -1

        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posx >= WIDTH and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    def reset(self, speed):
        self.speed = speed
        self.posx = WIDTH // 2
        self.posy = HEIGHT // 2
        self.xFac *= -1
        self.firstTime = 1

    # Отражение по оси х
    def hit(self):
        self.xFac *= -1

    def getRect(self):
        return self.ball

# Текста для меню
def menu(winner):
    winningText = font40.render(f"Player number {winner} won!", False, "white")
    optionText = font40.render("R - RESET       Q - QUIT", True, "white")
    textRect1 = winningText.get_rect()
    textRect1.center = (WIDTH // 2, 200)
    textRect2 = optionText.get_rect()
    textRect2.center = (WIDTH // 2, 300)

    screen.blit(winningText, textRect1)
    screen.blit(optionText, textRect2)
    pygame.display.update()

def main():
    # Объявление объектов
    player1 = Striker(20, HEIGHT // 2 - 50, 10, 100, 10, "green")
    player2 = Striker(WIDTH - 10, HEIGHT // 2 - 50, 10, 100, 10, "green")
    ball = Ball(WIDTH // 2, HEIGHT // 2, 7, 7, "white")
    speed = ball.speed
    listOfPlayers = [player1, player2]

    # Начальные параметры игроков
    player1Score, player2Score = 0, 0
    player1YFac, player2YFac = 0, 0

    pause = False
    running = True
    losingSoundFlag = True

    while running:
        score = False
        screen.fill("black")

        if player1Score == 7 or player2Score == 7:
            pause = True

        if pause == False:
            losingSoundFlag = True
            # Проверка закрытия и движения ракетки
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player2YFac = -1
                    if event.key == pygame.K_DOWN:
                        player2YFac = 1
                    if event.key == pygame.K_w:
                        player1YFac = -1
                    if event.key == pygame.K_s:
                        player1YFac = 1
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player2YFac = 0
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        player1YFac = 0

            # Отражение удара (Коллизия)
            for player in listOfPlayers:
                if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
                    ball.hit()
                    hitSound.play()

            # Обновление данных
            player1.update(player1YFac)
            player2.update(player2YFac)
            point = ball.update()

            # Проверка на результат столкновения
            if point == -1:  # 1-й игрок
                player1Score += 1

            elif point == 1:  # 2-й игрок
                player2Score += 1

            # Если кто-то забил обновляем позицию мяча
            if point:
                ball.reset(speed)
                score = True
                scoreSound.play()

            # Отображение объектов на экране
            player1.display()
            player2.display()
            ball.display()

            # Отображение счета
            player1.displayScore("Player1: ", player1Score, 100, 20, "white")
            player2.displayScore("Player2: ", player2Score, WIDTH - 100, 20, "white")


        else:
            screen.fill("gray")
            screen.blit(winImage, (0, 0))
            if losingSoundFlag == True:
                losingSound.play()
                losingSoundFlag = False
            if player1Score == 7:
                menu(1)
            else:
                menu(2)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        player1Score, player2Score = 0, 0
                        pause = False
                    if event.key == pygame.K_q:
                        running = False
                if event.type == pygame.QUIT:
                    running = False

        clock.tick(FPS)
        pygame.display.update()
        ball.speed += 0.01
        if score:
            pygame.time.delay(1000)

if __name__ == "__main__":
    main()
    pygame.quit()