from resources import ResourceManager
from physics import PhysicsBody
from inputs import Keyboard
from entity import Entity

import pygame.locals
import pygame.math
import pygame

class Player(Entity):
    def __init__(self):
        surface = ResourceManager.get_image("max")
        self.sprite = pygame.transform.scale(surface, (128, 128))
        self.body = PhysicsBody(1.0, True)

    def tick(self, deltaTime: float) -> None:
        """Updates the player's internal state."""
        if Keyboard.pressed(pygame.locals.K_w):
            self.body.pos.y -= 50.0 * deltaTime
        if Keyboard.pressed(pygame.locals.K_s):
            self.body.pos.y += 50.0 * deltaTime
        if Keyboard.pressed(pygame.locals.K_a):
            self.body.pos.x -= 50.0 * deltaTime
        if Keyboard.pressed(pygame.locals.K_d):
            self.body.pos.x += 50.0 * deltaTime

    def render(self, surface: pygame.Surface) -> None:
        """Draws the player's sprite to the specified surface."""
        surface.blit(self.sprite, (self.body.pos.x, self.body.pos.y))
