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
        self.body = pymunk.Body(mass=PLAYER_MASS, moment=1.0)
        self.body.position = (1, TILE_SIZE * 10)

        box = pymunk.Poly.create_box(self.body, size=(1.0, 2.0))
        self.shapes = [box]

    def tick(self, deltaTime: float) -> None:
        """Updates the player's internal state."""

        horizontalVelocity = 0
        if Keyboard.pressed(pygame.locals.K_a):
            horizontalVelocity = -PLAYER_MOVEMENT_SPEED
        if Keyboard.pressed(pygame.locals.K_d):
            horizontalVelocity = PLAYER_MOVEMENT_SPEED

        self.body.velocity = pymunk.Vec2d(horizontalVelocity, self.body.velocity.y)

        collison = Game.currentLevel.collisionCheck(
            self.body.position.x, self.body.position.x + TILE_SIZE, self.body.position.y + TILE_SIZE * 2, self.body.position.y)

        if collison[3]: # Bottom
            self.body.apply_impulse_at_local_point((0, -PLAYER_MASS * self.body.velocity.y))
            if Keyboard.pressed(pygame.locals.K_SPACE): # Allow jumping is player is grounded
                self.body.apply_impulse_at_local_point((0, PLAYER_JUMP_FORCE))

        if collison[1]: # Left
            self.body.position = pymunk.Vec2d(int(self.body.position.x + TILE_SIZE - 1) & ~(TILE_SIZE - 1), self.body.position.y) # Move the player to the next tile so it does not collide
        if collison[2]: # Right
            self.body.position = pymunk.Vec2d(int(self.body.position.x - TILE_SIZE) & ~(TILE_SIZE - 1), self.body.position.y) # Move the player to the next tile so it does not collide

        Game.viewport.x = max(0,
            self.body.position.x - Game.viewportSize[0] / 2) # Postion player in centre of screen

    def render(self, surface: pygame.Surface) -> None:
        """Draws the player's sprite to the specified surface."""
        surface.blit(self.sprite,
            (self.body.position.x - Game.viewport[0],
            Game.viewportSize[1] - self.body.position.y - Game.viewport[1] - TILE_SIZE * 2))
