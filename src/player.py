import datatypes as dt
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
        self.size = pygame.math.Vector2(constants.TILE_SIZE, constants.TILE_SIZE * 2)
        self.sprite = pygame.transform.scale(surface, (int(self.size.x), int(self.size.y)))

        screenX, screenY = game.display.get_size()
        screenX = (screenX / 10.0) - (self.size.x / 2)
        screenY = (screenY / 1.15) - (self.size.y / 2)
        self.position = pygame.math.Vector2(screenX, screenY)
        self.velocity = pygame.math.Vector2(0.0, 0.0)

    def tick(self, game: "game.Game", deltaTime: float) -> None:
        """Updates the player's internal state."""
        if game.keyboard.pressed(pygame.locals.K_a):
            self.velocity.x -= constants.PLAYER_MOVEMENT_SPEED
        if game.keyboard.pressed(pygame.locals.K_d):
            self.velocity.x += constants.PLAYER_MOVEMENT_SPEED

        a = pygame.math.Vector2(self.position.x + game.viewport.x, self.position.y + self.size.y + game.viewport.y)
        b = pygame.math.Vector2(self.position.x + self.size.x + game.viewport.x, self.position.y + game.viewport.y)
        collision = game.currentLevel.collision_check(a, b)

        if collision.top:
            # Top-side collision: snap to the lower bound of the collided tile.
            snapY = int(self.position.y + self.size.y) & ~(constants.TILE_SIZE - 1)
            self.position.y = snapY - self.size.y - 1
            self.velocity.y = 0

        elif collision.bottom:
            if game.keyboard.pressed(pygame.locals.K_SPACE):
                # Player is grounded and key pressed: apply jumping force.
                self.velocity.y = constants.PLAYER_JUMPING_SPEED
            else:
                # Bottom-side collision: snap to the upper bound of the collided tile.
                snapY = int(self.position.y) & ~(constants.TILE_SIZE - 1)
                self.position.y = snapY + constants.TILE_SIZE
                self.velocity.y = 0

        else:
            # No vertical collision: apply gravity as normal.
            self.velocity.y += constants.WORLD_GRAVITY * deltaTime

        # Recompute collisions now that the player's vertical position has been resolved.
        a = pygame.math.Vector2(self.position.x + game.viewport.x, self.position.y + self.size.y + game.viewport.y)
        b = pygame.math.Vector2(self.position.x + self.size.x + game.viewport.x, self.position.y + game.viewport.y)
        collision = game.currentLevel.collision_check(a, b)

        if collision.left:
            # Left-side collision: snap to the right side of the collided tile.
            snapX = int(self.position.x) & ~(constants.TILE_SIZE - 1)
            self.position.x = snapX + self.size.x + 1
            self.velocity.x = 0

        if collision.right:
            # Right-side collision: snap to the left side of the collided tile.
            snapX = int(self.position.x + self.size.x) & ~(constants.TILE_SIZE - 1)
            self.position.x = snapX - self.size.x - 1
            self.velocity.x = 0

        # Update the viewport's position and ensure that the player can't go backwards.
        if self.position.x >= (game.resolution.x / 2):
            game.viewport.x += self.velocity.x * deltaTime
            self.position.x = game.resolution.x / 2

        if self.position.x < 0:
            self.position.x = 0

        # Update the position and scale the velocity to give an impression of friction.
        self.position += self.velocity * deltaTime
        self.velocity.x *= constants.PLAYER_FRICTION_COEFFICIENT

    def render(self, display: pygame.Surface) -> None:
        """Renders the player sprite to the screen."""
        screen = dt.IntVector2.from_tuple(display.get_size())
        position = pygame.Vector2(self.position.x, screen.y - (self.position.y + self.size.y))
        display.blit(self.sprite, position)
