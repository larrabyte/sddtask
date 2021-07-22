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
    wasJumping = False

    def __init__(self):
        surface = ResourceManager.get_image("max")
        self.sprite = pygame.transform.scale(surface, (TILE_SIZE, TILE_SIZE * 2))

        # Physics shapes go into self.shapes as a list.
        self.body = pymunk.Body(mass=PLAYER_MASS, moment=1.0, body_type=pymunk.Body.DYNAMIC)
        self.body.position = (TILE_SIZE, TILE_SIZE * 10)

        box = pymunk.Poly.create_box_bb(self.body, pymunk.BB(0, 0, TILE_SIZE, TILE_SIZE * 2))
        box.friction = 0.9;
        box.elasticity = 0
        
        self.shapes = [box]

    def tick(self, deltaTime: float) -> None:
        """Updates the player's internal state."""
        horizontalVelocity = 0

        if Keyboard.pressed(pygame.locals.K_a):
            self.body.apply_force_at_local_point([-PLAYER_MOVEMENT_FORCE, 0])
        if Keyboard.pressed(pygame.locals.K_d):
            self.body.apply_force_at_local_point([PLAYER_MOVEMENT_FORCE, 0])

        if Keyboard.pressed(pygame.locals.K_SPACE):
            if not self.wasJumping and\
                Game.currentLevel.collisionCheck(self.body.position.x, self.body.position.x + TILE_SIZE, self.body.position.y + TILE_SIZE * 2, self.body.position.y)[3]:
                self.body.apply_impulse_at_local_point([0, PLAYER_JUMP_FORCE])
            wasJumping = True
        else:
            wasJumping = False

        self.body.angle = 0
        self.body.space.reindex_shapes_for_body(self.body)

        # Ensure that the player remains in the centre of the screen while scrolling.
        Game.viewport.x = max(0, self.body.position.x - Game.viewportSize[0] / 2)

    def render(self, surface: pygame.Surface) -> None:
        """Draws the player's sprite to the specified surface."""
        surface.blit(self.sprite,
            (self.body.position.x - Game.viewport[0],
            Game.viewportSize[1] - self.body.position.y - Game.viewport[1] - TILE_SIZE * 2))
