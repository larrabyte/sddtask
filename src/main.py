import pygame
import pygame.time
import game
import resources

if __name__ == "__main__":
    pygame.init()

    resolution = (640, 480)
    backgroundColour = (0, 0, 0)

    display = pygame.display.set_mode(resolution)
    gameInstance = game.Game()

    lastTime = pygame.time.get_ticks()
    running = True
    while running:
        newTime = pygame.time.get_ticks()
        elaspedTime: float = (newTime - lastTime) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        display.fill(backgroundColour)

        gameInstance.tick(elaspedTime)
        gameInstance.render(display)

        pygame.display.flip()

        lastTime = newTime
