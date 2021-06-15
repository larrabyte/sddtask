import pygame.locals as local
import pygame

import entity
import resources

class Player(entity.Entity):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 50

        self.sprite = pygame.transform.scale(resources.get_image("max"), [128, 128])

    def key_pressed(self, key: int) -> bool:
        """Returns a boolean depending on whether `key` was pressed."""
        keys = pygame.key.get_pressed()
        return keys[key]

    def tick(self, elaspedTime: float):
        if self.key_pressed(local.K_w):
            self.y -= self.speed * elaspedTime
        if self.key_pressed(local.K_s):
            self.y += self.speed * elaspedTime
        if self.key_pressed(local.K_a):
            self.x -= self.speed * elaspedTime
        if self.key_pressed(local.K_d):
            self.x += self.speed * elaspedTime

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.sprite, (self.x, self.y))