from resources import ResourceManager
from inputs import Keyboard
from entity import Entity

import pygame.locals
import pygame

class Player(Entity):
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.speed = 50.0

        surface = ResourceManager.get_image("max")
        self.sprite = pygame.transform.scale(surface, (128, 128))

    def tick(self, deltaTime: float) -> None:
        """Updates the player's internal state."""
        if Keyboard.pressed(pygame.locals.K_w):
            self.y -= self.speed * deltaTime
        if Keyboard.pressed(pygame.locals.K_s):
            self.y += self.speed * deltaTime
        if Keyboard.pressed(pygame.locals.K_a):
            self.x -= self.speed * deltaTime
        if Keyboard.pressed(pygame.locals.K_d):
            self.x += self.speed * deltaTime

    def render(self, surface: pygame.Surface) -> None:
        """Draws the player's sprite to the specified surface."""
        surface.blit(self.sprite, (self.x, self.y))
