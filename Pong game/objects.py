from loadsValues import *

# Player
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
    # Рендер текста
    winningText = font40.render(f"Player number {winner} won!", False, "white")
    optionText = font40.render("R - RESET       Q - QUIT", True, "white")
    # Его позиционирование
    textRect1 = winningText.get_rect()
    textRect1.center = (WIDTH // 2, 200)
    textRect2 = optionText.get_rect()
    textRect2.center = (WIDTH // 2, 300)
    # Отображение на экране
    screen.blit(winningText, textRect1)
    screen.blit(optionText, textRect2)
    pygame.display.update()
