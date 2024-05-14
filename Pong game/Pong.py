from objects import *


# Игровая логика
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
                # Движения вверх-вниз при нажатии
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player2YFac = -1
                    if event.key == pygame.K_DOWN:
                        player2YFac = 1
                    if event.key == pygame.K_w:
                        player1YFac = -1
                    if event.key == pygame.K_s:
                        player1YFac = 1
                # Остановка при отжатии
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player2YFac = 0
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        player1YFac = 0

            # Отражение удара (Коллизия)
            for player in listOfPlayers:
                if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
                    ball.hit()
                    hitSound.play() # Звуковое сопровождение при ударе

            # Обновление данных
            player1.update(player1YFac)
            player2.update(player2YFac)
            point = ball.update()

            # Проверка на "забит ли гол"
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
            screen.blit(winImage, (0, 0))
            if losingSoundFlag == True:
                losingSound.play()
                losingSoundFlag = False

            menu(1) if player1Score == 7 else menu(2)

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


# Запуск игры
if __name__ == "__main__":
    main()
    pygame.quit()

