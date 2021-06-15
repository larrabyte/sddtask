import pygame.locals as local
import pygame

import entity
import resources

class Player(entity.Entity):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 50

        surface = resources.get_image("max")
        self.sprite = pygame.transform.scale(surface, (128, 128))

    def key_pressed(self, key: int) -> bool:
        """Returns a boolean depending on whether `key` was pressed."""
        keys = pygame.key.get_pressed()
        return keys[key]

    def tick(self, deltaTime: float) -> None:
        """Updates the player's internal state."""
        if self.key_pressed(local.K_w):
            self.y -= self.speed * deltaTime
        if self.key_pressed(local.K_s):
            self.y += self.speed * deltaTime
        if self.key_pressed(local.K_a):
            self.x -= self.speed * deltaTime
        if self.key_pressed(local.K_d):
            self.x += self.speed * deltaTime

    def render(self, surface: pygame.Surface) -> None:
        """Draws the player's sprite to the specified surface."""
        surface.blit(self.sprite, (self.x, self.y))
