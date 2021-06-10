import pygame

if __name__ == "__main__":
    pygame.init()

    display = pygame.display.set_mode([640, 480])
    
    isRunning = True
    while isRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False

        display.fill([0, 0, 0])

        pygame.display.flip()
