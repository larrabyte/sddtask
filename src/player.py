import constants
import bullets
import game

import pygame.transform
import pygame.locals
import pygame.math
import pygame.draw
import pygame

class Player:
    def __init__(self, game: "game.Game") -> None:
        """Initialises an instance of the `Player` class."""
        surface = game.resources.get_image("max")
        self.size = pygame.math.Vector2(constants.WORLD_TILE_SIZE, constants.WORLD_TILE_SIZE * 2)
        self.sprite = pygame.transform.scale(surface, (int(self.size.x), int(self.size.y)))
        self.game = game

        screenX, screenY = game.display.get_size()
        screenX = (screenX / 10.0) - (self.size.x / 2)
        screenY = (screenY / 1.15) - (self.size.y / 2)
        self.position = pygame.math.Vector2(screenX, screenY)
        self.velocity = pygame.math.Vector2(0.0, 0.0)

        # Player game attributes.
        self.jetpackFuel = constants.PLAYER_JETPACK_MAX
        self.gunCooldown = 0

    def update_movement(self, game: "game.Game", deltaTime: float) -> None:
        """Updates player movement based on `deltaTime`."""
        if game.keyboard.pressed(pygame.locals.K_a):
            self.velocity.x -= constants.PLAYER_MOVEMENT_SPEED
        if game.keyboard.pressed(pygame.locals.K_d):
            self.velocity.x += constants.PLAYER_MOVEMENT_SPEED

        a = pygame.math.Vector2(self.position.x, self.position.y + self.size.y)
        b = pygame.math.Vector2(self.position.x + self.size.x, self.position.y)
        collision = game.currentLevel.collision_check(a, b)

        if collision[2]:
            # Top-side collision: snap to the lower bound of the collided tile.
            snapY = int(self.position.y + self.size.y) & ~(constants.WORLD_TILE_SIZE - 1)
            self.position.y = snapY - self.size.y - 1
            self.velocity.y = 0
        elif collision[3]:
            if game.keyboard.pressed(pygame.locals.K_SPACE):
                # Player is grounded and key pressed: apply jumping force.
                self.velocity.y = constants.PLAYER_JUMPING_SPEED
            else:
                # Bottom-side collision: snap to the upper bound of the collided tile.
                snapY = int(self.position.y) & ~(constants.WORLD_TILE_SIZE - 1)
                self.position.y = snapY + constants.WORLD_TILE_SIZE
                self.velocity.y = 0
        else:
            # No vertical collision: apply gravity as normal.
            self.velocity.y += constants.WORLD_GRAVITY * deltaTime

        # Recompute collisions now that the player's vertical position has been resolved.
        a = pygame.math.Vector2(self.position.x, self.position.y + self.size.y)
        b = pygame.math.Vector2(self.position.x + self.size.x, self.position.y)
        collision = game.currentLevel.collision_check(a, b)

        if collision[0]:
            # Left-side collision: snap to the right side of the collided tile.
            snapX = int(self.position.x) & ~(constants.WORLD_TILE_SIZE - 1)
            self.position.x = snapX + self.size.x + 1
            self.velocity.x = 0

        if collision[1]:
            # Right-side collision: snap to the left side of the collided tile.
            snapX = int(self.position.x + self.size.x) & ~(constants.WORLD_TILE_SIZE - 1)
            self.position.x = snapX - self.size.x - 1
            self.velocity.x = 0

        if self.position.x < 0:
            # Ensure the player can't go off screen to the left.
            self.position.x = 0

        if game.keyboard.pressed(pygame.locals.K_SPACE) and self.jetpackFuel > 0:
            # If the player is holding space and jetpack fuel is available, update as needed.
            self.velocity.y += constants.PLAYER_JUMPING_SPEED * deltaTime
            self.jetpackFuel -= 1
        elif not game.keyboard.pressed(pygame.locals.K_SPACE) and self.jetpackFuel < constants.PLAYER_JETPACK_MAX:
            # If space isn't being held and jetpack fuel isn't maxed out, add.
            self.jetpackFuel += 1

        # Update the player and game state accordingly.
        game.viewport.x = max(0, self.position.x - game.viewportSize[0] / 2)
        self.position += self.velocity * deltaTime
        self.velocity.x *= constants.PLAYER_FRICTION_COEFFICIENT

    def update_gun_state(self, game: "game.Game") -> None:
        """Update the internal state of the player's gun."""
        if self.gunCooldown > 0:
            self.gunCooldown -= 1

        if game.mouse.pressed(1) and self.gunCooldown <= 0:
            spawn = pygame.math.Vector2(self.position.x + self.size.x + 1, self.position.y + (self.size.y / 2))
            velocity = pygame.math.Vector2(self.velocity.x + 1250, 0)
            bullet = bullets.Bullet(game, spawn, velocity)
            game.add_entity(bullet)
            self.gunCooldown = 20

    def tick(self, game: "game.Game", deltaTime: float) -> None:
        """Updates the player's internal state."""
        self.update_movement(game, deltaTime)
        self.update_gun_state(game)


    def render(self, display: pygame.Surface) -> None:
        """Renders the player sprite to the screen."""
        playerPosition = pygame.Vector2(self.position.x, self.position.y + self.size.y)
        playerPosition = self.game.calculate_offset(playerPosition)
        display.blit(self.sprite, playerPosition)

        jetpackScale = self.jetpackFuel / constants.PLAYER_JETPACK_MAX
        jetpackOffset = self.size.y * jetpackScale
        jetpackPosition = pygame.Vector2(self.position.x + self.size.x + 1, self.position.y + jetpackOffset)
        jetpackPosition = self.game.calculate_offset(jetpackPosition)
        jetpackRect = pygame.Rect(jetpackPosition.x, jetpackPosition.y, 3, jetpackOffset)
        pygame.draw.rect(display, (255, 0, 0), jetpackRect)
