import pygame


pygame.init()
screen = pygame.display.set_mode((500,400))
rec = pygame.Rect(150,100,50,50)
FPS = 100
clock = pygame.time.Clock()

a,b,c,count =0,0,0,0
font20 = pygame.font.Font('fonts/freesans5.ttf', 20)

def textForPause():
    text = font20.render("""Reser - R.      Leave - Q""",True, "black")
    textRect = text.get_rect()
    screen.blit(text, textRect)

# SOUNDS

score = pygame.mixer.Sound("sounds_mem/durachyo.mp3")
count = 0
gameplay = True
running = True
while running:
    if gameplay:
        screen.fill("green")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if count == 10:
            gameplay = False
            count = 0
        else:
            count += 1
    else:
        screen.fill((90,90,90))
        textForPause()
        if count == 3:
            score.play()
        count+=1
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:

                    gameplay = True
                if event.key == pygame.K_q:
                    running = False
            if event.type == pygame.QUIT:
                running = False

    pygame.display.update()
    clock.tick(FPS)