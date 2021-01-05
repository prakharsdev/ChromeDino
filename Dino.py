import pygame
from pygame.locals import *

#modules initialized
x = pygame.init()

#screen height and width
screen = pygame.display.set_mode((950, 573))
#screen title
pygame.display.set_caption("Chrome Dino")
message = pygame.font.Font('freesansbold.ttf', 30)

white = (255,255,255)
orange = (255, 100, 100)

#images
cactus = pygame.image.load("cactusSmallMany0000.png")
cactus = pygame.transform.scale(cactus, (200, 110))
cactus1 = pygame.image.load("cactusBig0000.png")
cactus1 = pygame.transform.scale(cactus1, (100, 120))
cactus2 = pygame.image.load("cactusSmall0000.png")
cactus2 = pygame.transform.scale(cactus2, (100, 120))
dino = pygame.image.load("dinorun0000.png")
dino1 = pygame.image.load("dinorun0001.png")


walk = [dino,dino, dino1, dino1, dino,dino]
background = pygame.image.load("background.png")


def gameloop():

    #images
    cactus = pygame.image.load("cactusSmallMany0000.png")
    cactus = pygame.transform.scale(cactus, (200, 110))
    cactus1 = pygame.image.load("cactusBig0000.png")
    cactus1 = pygame.transform.scale(cactus1, (100, 120))
    cactus2 = pygame.image.load("cactusSmall0000.png")
    cactus2 = pygame.transform.scale(cactus2, (100, 120))
    dino = pygame.image.load("dinorun0000.png")
    dino1 = pygame.image.load("dinorun0001.png")


    walk = [dino,dino, dino1, dino1, dino,dino]
    background = pygame.image.load("background.png")




    backx = 0
    backy = 0
    drawx = 310
    drawy = 440
    cactusx = 100
    cactusy = 430
    backvelocity = 0
    walkpoint = 0
    gravity = 10
    game = False
    jump = False
    gameover = False
    jump = False
    score = 0

   


    while True:
 
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    if drawy == 440:
                        jump = True
                        #Change the speed then alter the value of below backvelocity
                        backvelocity = 4
                        game = True
                if event.key == K_SPACE:
                        gameloop()
        if backx == -600:
            backx = 0
        if cactusx < -1600:
            cactusx = 550
        if 441 > drawy > 50:
            if jump == True:
                drawy -= 10
        else:
            jump = False
        print(drawy)
        if drawy < 440:
            if jump == False:
                drawy +=gravity
        #collision
        if cactusx < drawx + 100 < cactusx +200 and cactusy < drawy + 100 < cactusy + 100 :
            backvelocity = 0
            walkpoint = 0
            game = False
            gameover = True

        if cactusx +800 < drawx + 100 < cactusx +1000 and cactusy < drawy + 100 < cactusy + 100 :
            backvelocity = 0
            walkpoint = 0
            game = False
            gameover = True

        if cactusx + 1600< drawx + 100 < cactusx +1800 and cactusy < drawy + 100 < cactusy + 100 :
            backvelocity = 0
            walkpoint = 0
            game = False
            gameover = True


                 
        if game == True:
            score += 1
        screen.fill(white)
        text = message.render("Score: "+ str(score), True, orange)
        text1 = message.render("GAME OVER", True, (255,255,0))
        backx -= backvelocity
        cactusx -= backvelocity
        
        screen.blit(background, [backx,backy])
        screen.blit(background, [backx + 780,backy])
        screen.blit(text, [700, 100])
        if gameover == True:
            screen.blit(text1, [400, 190])
        screen.blit(walk[walkpoint], [drawx, drawy])
        
        if game == True:

            walkpoint +=1
            if walkpoint > 5:
                walkpoint = 0
        screen.blit(cactus, [cactusx,cactusy])
        screen.blit(cactus1, [cactusx + 800,cactusy - 8])
        screen.blit(cactus2, [cactusx + 1600,cactusy - 10])
        pygame.display.update()

gameloop()