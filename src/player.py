import constants
import game

import pygame.transform
import pygame.locals
import pygame.math
import pygame

class Player:
    def __init__(self, game: "game.Game") -> None:
        """Initialises an instance of the `Player` class."""
        self.size = pygame.math.Vector2(constants.TILE_SIZE, constants.TILE_SIZE * 2)
        self.sprite = game.resources.get_image("max")

        spawnXCoordinate, spawnYCoordinate = game.display.get_size()
        spawnXCoordinate = (spawnXCoordinate / 10.0) - (self.size.x / 2)
        spawnYCoordinate = (spawnYCoordinate / 1.15) - (self.size.y / 2)
        self.position = pygame.math.Vector2(spawnXCoordinate, spawnYCoordinate)
        self.velocity = pygame.math.Vector2()

    def tick(self, game: "game.Game", deltaTime: float) -> None:
        collision = game.currentLevel.collision_check(self.position.x, self.position.x + constants.TILE_SIZE, self.position.y + constants.TILE_SIZE * 2, self.position.y)

        # Handle any player input after collision checks have been computed.
        if game.keyboard.pressed(pygame.locals.K_a):
            self.velocity.x -= constants.PLAYER_MOVEMENT_SPEED
        if game.keyboard.pressed(pygame.locals.K_d):
            self.velocity.x += constants.PLAYER_MOVEMENT_SPEED

        if collision[2]: # Top
            snapY = int(self.position.y + self.size.y) & ~(constants.TILE_SIZE - 1)
            self.position.y = snapY - self.size.y - 1
            self.velocity.y = 0
        elif collision[3]: # Bottom
            snapY = int(self.position.y) & ~(constants.TILE_SIZE - 1)
            self.position.y = snapY + constants.TILE_SIZE
            self.velocity.y = 0
        else: # Otherwise add gravity
            self.velocity.y += constants.WORLD_GRAVITY * deltaTime

        if game.keyboard.pressed(pygame.locals.K_SPACE) and collision[3]:
            self.velocity.y = (constants.PLAYER_JUMPING_SPEED)

        # Recheck collision now that the player has been pushed out of the floor/ceiling
        collision = game.currentLevel.collision_check(self.position.x, self.position.x + constants.TILE_SIZE, self.position.y + constants.TILE_SIZE * 2, self.position.y)

        # Handle any new collisions if needed.
        if collision[0]: # Left
            # Get the world position of the tile by rounding to TILE_SIZE
            snapX = int(self.position.x) & ~(constants.TILE_SIZE - 1)
            self.position.x = snapX + self.size.x
            self.velocity.x = 0
        if collision[1]: # Right
            # Get the world position of the tile by rounding to TILE_SIZE
            snapX = int(self.position.x + self.size.x) & ~(constants.TILE_SIZE - 1)
            self.position.x = snapX - self.size.x - 1
            self.velocity.x = 0

        # Update the position and scale the velocity to give an impression of friction.
        self.position += self.velocity * deltaTime
        self.velocity.x *= 0.8

    def render(self, display: pygame.Surface) -> None:
        """Renders the player sprite to the screen."""
        display.blit(self.sprite, pygame.Vector2(self.position.x, display.get_size()[1] - (self.position.y + self.size.y)))
