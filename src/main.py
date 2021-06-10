import pygame
import game

if __name__ == "__main__":
    pygame.init()

    resolution = (640, 480)
    display = pygame.display.set_mode(resolution)
    gameInstance = game.Game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        blank = (0, 0, 0)
        display.fill(blank)
        gameInstance.tick()
        pygame.display.flip()
