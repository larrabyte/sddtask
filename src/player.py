from resources import ResourceManager
from inputs import Keyboard
from entity import Entity

import pymunk

import pygame.locals
import pygame.math
import pygame

class Player(Entity):
    def __init__(self):
        surface = ResourceManager.get_image("max")
        self.sprite = pygame.transform.scale(surface, (128, 128))

        # Physics shapes go into self.shapes as a list.
        self.body = pymunk.Body(mass=75.0, moment=1.0)
        box = pymunk.Poly.create_box(self.body, size=(1.0, 1.0))
        self.shapes = [box]

    def tick(self, deltaTime: float) -> None:
        """Updates the player's internal state."""
        if Keyboard.pressed(pygame.locals.K_w):
            v = pymunk.Vec2d(0.0, 50.0 * deltaTime)
            self.body.position -= v
        if Keyboard.pressed(pygame.locals.K_s):
            v = pymunk.Vec2d(0.0, 50.0 * deltaTime)
            self.body.position += v
        if Keyboard.pressed(pygame.locals.K_a):
            v = pymunk.Vec2d(50.0 * deltaTime, 0.0)
            self.body.position -= v
        if Keyboard.pressed(pygame.locals.K_d):
            v = pymunk.Vec2d(50.0 * deltaTime, 0.0)
            self.body.position += v

    def render(self, surface: pygame.Surface) -> None:
        """Draws the player's sprite to the specified surface."""
        surface.blit(self.sprite, (self.body.position.x, self.body.position.y))
