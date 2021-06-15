import pygame.locals
import pygame

import resources
import entity
import inputs

class Player(entity.Entity):
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.speed = 50.0

        surface = resources.Manager.get_image("max")
        self.sprite = pygame.transform.scale(surface, (128, 128))

    def tick(self, deltaTime: float) -> None:
        """Updates the player's internal state."""
        if inputs.Keyboard.pressed(pygame.locals.K_w):
            self.y -= self.speed * deltaTime
        if inputs.Keyboard.pressed(pygame.locals.K_s):
            self.y += self.speed * deltaTime
        if inputs.Keyboard.pressed(pygame.locals.K_a):
            self.x -= self.speed * deltaTime
        if inputs.Keyboard.pressed(pygame.locals.K_d):
            self.x += self.speed * deltaTime

    def render(self, surface: pygame.Surface) -> None:
        """Draws the player's sprite to the specified surface."""
        surface.blit(self.sprite, (self.x, self.y))
