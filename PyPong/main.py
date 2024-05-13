import pygame

pygame.init()


# Цвета в RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Screen
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping-pong")

# FPS
FPS = 60
clock = pygame.time.Clock()

# Шрифт для текста
font20 = pygame.font.Font('fonts/freesans5.ttf', 20)
#Текста для меню
def menu(winner):
    winningText = font20.render(f"Player number {winner} won!",  False, BLACK)
    optionText = font20.render("Press R/Q- to reset or  quite the game:")
    textRect =



# Player
class Striker():
    def __init__(self, posx, posy, width, height, speed, color ):
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
    def update(self, yFac ):
        self.posy = self.posy + self.speed*yFac

        # Контроль выхода за экран
        if self.posy <=0:
            self.posy = 0
        elif self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT - self.height
        
        self.playerRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    # Рендер текста и создание прямоугольника для текста
    def displayScore(self, text, score, x, y, color):
        text = font20.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x,y)#Позиционирование

        screen.blit(text,textRect)

    def getRect(self):
        return self.playerRect

# Мяч
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
    def display(self,):
        self.ball = pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)

    def update(self):


        self.posy += self.speed*self.yFac
        self.posx += self.speed*self.xFac

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

    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT // 2
        self.xFac *= -1
        self.firstTime = 1

    # Отражение по оси х
    def hit(self):
        self.xFac *= -1

    def getRect(self):
        return self.ball



def main():

    # Объявление объектов
    player1 = Striker(20,0,10,100,10,"green")
    player2 = Striker(WIDTH - 10,0,10,100,10,"green")
    ball = Ball(WIDTH//2, HEIGHT//2,7,15,"white")

    listOfPlayers = [player1,player2]

    # Начальные параметры игроков
    player1Score, player2Score = 0, 0
    player1YFac, player2YFac = HEIGHT//2 - 50, HEIGHT//2 - 50

    pause = False
    running = True
    while running:
        screen.fill("black")
        if player1Score == 3:
            pause = True

        if player2Score == 3:
            pause = True

        if pause == False:

            #Проверка событий
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

            # Обновление данных
            player1.update(player1YFac)
            player2.update(player2YFac)
            point = ball.update()

            # Проверка на результат столкновения
            if point == -1:  # 1-й игрок
                player1Score += 1
            elif point == 1: # 2-й игрок
                player2Score += 1

            # Если кто-то забил обновляем позицию мяча
            if point:
                ball.reset()

            # Отображение объектов  на экране
            player1.display()
            player2.display()
            ball.display()

            # Отображение счета
            player1.displayScore("Player1: ", player1Score, 100, 20, "white")
            player2.displayScore("Player2: ", player2Score, WIDTH - 100, 20, "white")

            #Ну и конечно отображение игры и обновление кадров
            pygame.display.update()
            clock.tick(FPS)
        else:
            screen.fill("gray")
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        player1Score, player2Score = 0,0
                        pause = False
                    if event.key == pygame.K_q:
                        running = False
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()


if __name__ == "__main__":
    main()
    pygame.quit()
