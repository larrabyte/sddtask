import constants
import game

import pygame.transform
import pygame.locals
import pygame.math
import pygame

class Player:
    def __init__(self, game: "game.Game") -> None:
        """Initialises an instance of the `Player` class."""
        surface = game.resources.get_image("max")
        self.pixels = pygame.math.Vector2(constants.TILE_SIZE * 2, constants.TILE_SIZE * 4)
        self.sprite = pygame.transform.scale(surface, (int(self.pixels.x), int(self.pixels.y)))

        spawnXCoordinate, spawnYCoordinate = game.display.get_size()
        spawnXCoordinate = (spawnXCoordinate / 10.0) - (self.pixels.x / 2)
        spawnYCoordinate = (spawnYCoordinate / 1.15) - (self.pixels.y / 2)
        self.position = pygame.math.Vector2(spawnXCoordinate, spawnYCoordinate)
        self.velocity = pygame.math.Vector2()

    def tick(self, game: "game.Game", deltaTime: float) -> None:
        """Updates the player's internal state."""
        groundCheckX = self.position.x + (self.pixels.x / 2)
        groundCheckY = self.position.y + self.pixels.y
        groundTile = game.currentLevel.get_tile("foreground", groundCheckX, groundCheckY)
        grounded = groundTile > 0

        rightCheckX = self.position.x + self.pixels.x
        rightCheckY = self.position.y + (self.pixels.y / 2)
        rightTile = game.currentLevel.get_tile("foreground", rightCheckX, rightCheckY)
        righted = rightTile > 0

        leftCheckX = self.position.x
        leftCheckY = self.position.y + (self.pixels.y / 2)
        leftTile = game.currentLevel.get_tile("foreground", leftCheckX, leftCheckY)
        lefted = leftTile > 0

        topCheckX = self.position.x + (self.pixels.x / 2)
        topCheckY = self.position.y
        topTile = game.currentLevel.get_tile("foreground", topCheckX, topCheckY)
        topped = topTile > 0

        # Handle any player input after collision checks have been computed.
        if game.keyboard.pressed(pygame.locals.K_a):
            self.velocity.x -= constants.PLAYER_MOVEMENT_SPEED * deltaTime
        if game.keyboard.pressed(pygame.locals.K_d):
            self.velocity.x += constants.PLAYER_MOVEMENT_SPEED * deltaTime
        if game.keyboard.pressed(pygame.locals.K_SPACE) and grounded:
            self.velocity.y = -(constants.PLAYER_JUMPING_SPEED * deltaTime)
            grounded = False

        # Handle any new collisions if needed.
        if lefted:
            tileX, tileY = game.currentLevel.get_tile_position("foreground", leftCheckX, leftCheckY)
            snapX, snapY = game.currentLevel.get_screen_position("foreground", tileX, tileY)
            self.position.x = snapX + self.pixels.x + 1
            self.velocity.x = 0
        if righted:
            tileX, tileY = game.currentLevel.get_tile_position("foreground", rightCheckX, rightCheckY)
            snapX, snapY = game.currentLevel.get_screen_position("foreground", tileX, tileY)
            self.position.x = snapX - self.pixels.x - 1
            self.velocity.x = 0

        if topped:
            tileX, tileY = game.currentLevel.get_tile_position("foreground", topCheckX, topCheckY)
            snapX, snapY = game.currentLevel.get_screen_position("foreground", tileX, tileY)
            self.position.y = snapY + constants.TILE_SIZE
            self.velocity.y = 0
        elif grounded:
            tileX, tileY = game.currentLevel.get_tile_position("foreground", groundCheckX, groundCheckY)
            snapX, snapY = game.currentLevel.get_screen_position("foreground", tileX, tileY)
            self.position.y = snapY - self.pixels.y
            self.velocity.y = 0

            # Squishing code (very funny, squishes player to 0 however).
            # squishFactor = 1 / abs(1 + (snapY - self.pixels.y) / 10000)
            # self.pixels = pygame.math.Vector2(self.pixels.x, self.pixels.y * squishFactor)
            # self.sprite = pygame.transform.scale(self.sprite, (int(self.pixels.x), int(self.pixels.y)))
        else:
            self.velocity.y += constants.WORLD_GRAVITY * deltaTime

        # Update the position and scale the velocity to give an impression of friction.
        self.position += self.velocity
        self.velocity.x *= 0.8

    def render(self, display: pygame.Surface) -> None:
        """Renders the player sprite to the screen."""
        display.blit(self.sprite, self.position)
