import pygame
from game import *

if __name__ == "__main__":
    pygame.init()

    display = pygame.display.set_mode([640, 480])
    gameInstance = Game()
    
    isRunning = True
    while isRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False

        display.fill([0, 0, 0])

        gameInstance.Tick()

        pygame.display.flip()
