
import sys, pygame, pygame.mixer
from pygame.constants import MOUSEBUTTONDOWN
from pygame.locals import *
pygame.init()

clock = pygame.time.Clock()

bullets = []

size = width, height = 800, 600

screen = pygame.display.set_mode(size)




bullets = pygame.image.load('bullet.png')
def combat():

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT():
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
            
                bullets.append([event.pos[0] -32, 500])

        clock.tick(60)

        mx, my = pygame.mouse.get_pos()

        for b in range(len(bullets)):
            bullets[b][0] -=10

        for bullet in bullets[:]:
            if bullet[0] < 0:
                bullets.remove(bullet)
            
        
        

        for bullet in bullets:
            screen.blit(bullet, pygame.Rect(bullet[0], bullet[1], 0, 0))
            screen.blit(player,(mx-32,500))
            pygame.display.flip()
