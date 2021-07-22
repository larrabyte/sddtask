from constants import *
from entity import Entity
from game import Game
from inputs import Keyboard
from resources import ResourceManager

import pymunk

import pygame.locals
import pygame.math
import pygame


class Player(Entity):
    def __init__(self):
        surface = ResourceManager.get_image("max")
        self.sprite = pygame.transform.scale(surface, (TILE_SIZE, TILE_SIZE * 2))

        # Physics shapes go into self.shapes as a list.
        self.body = pymunk.Body(mass=PLAYER_MASS, moment=1.0, body_type=pymunk.Body.DYNAMIC)
        self.body.position = (TILE_SIZE, TILE_SIZE * 10)

        box = pymunk.Poly.create_box_bb(self.body, pymunk.BB(0, 0, TILE_SIZE, TILE_SIZE * 2))
        self.shapes = [box]

    def tick(self, deltaTime: float) -> None:
        """Updates the player's internal state."""
        horizontalVelocity = 0

        if Keyboard.pressed(pygame.locals.K_a):
            horizontalVelocity = -PLAYER_MOVEMENT_SPEED
        if Keyboard.pressed(pygame.locals.K_d):
            horizontalVelocity = PLAYER_MOVEMENT_SPEED

        self.body.velocity = pymunk.Vec2d(horizontalVelocity, self.body.velocity.y)
        self.body.angle = 0
        self.body.space.reindex_shapes_for_body(self.body)

        # Ensure that the player remains in the centre of the screen while scrolling.
        Game.viewport.x = max(0, self.body.position.x - Game.viewportSize[0] / 2)

    def render(self, surface: pygame.Surface) -> None:
        """Draws the player's sprite to the specified surface."""
        surface.blit(self.sprite,
            (self.body.position.x - Game.viewport[0],
            Game.viewportSize[1] - self.body.position.y - Game.viewport[1] - TILE_SIZE * 2))
