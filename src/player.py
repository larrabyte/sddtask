import pygame.locals as local
import pygame
import entity

class Player(entity.Entity):
    def __init__(self):
        self.x = 0
        self.y = 0

    def key_pressed(self, key: int) -> bool:
        """Returns a boolean depending on whether `key` was pressed."""
        keys = pygame.key.get_pressed()
        return keys[key]

    def tick(self):
        if self.key_pressed(local.K_w):
            self.y += 1
        elif self.key_pressed(local.K_s):
            self.y -= 1
        elif self.key_pressed(local.K_d):
            self.x += 1
        elif self.key_pressed(local.K_a):
            self.x -= 1
