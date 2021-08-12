import constants
from enemies import Enemy
from bullets import Bullet
import game

import pygame.transform
import pygame.locals
import pygame.math
import pygame.draw
import pygame

class Player:
    def __init__(self, game: "game.Game") -> None:
        """Initialises an instance of the `Player` class."""
        self.size = pygame.math.Vector2(constants.WORLD_TILE_SIZE, constants.WORLD_TILE_SIZE * 2)
        self.sprite = game.resources.get_image("max")
        self.game = game

        self.position = pygame.math.Vector2(64, 512)
        self.velocity = pygame.math.Vector2(0.0, 0.0)
        self.direction = 0 # Left or right? 1 - left, 0 - right

        # Player game attributes.
        self.jetpackFuel = constants.PLAYER_JETPACK_MAX
        self.healthPoints = 100
        self.grounded = False
        self.gunCooldown = 0

    def vibe_check(self, game: "game.Game") -> None:
        """Performs vibe checks to ensure the player is still alive."""
        if self.healthPoints <= 0:
            game.remove_entity(self)
            game.playerEntity = None

        if self.position.y + self.size.y < 0: # The player has fallen off the world.
            game.remove_entity(self)
            game.playerEntity = None

    def update_movement(self, game: "game.Game", deltaTime: float) -> None:
        """Updates player movement based on `deltaTime`."""

        # 1x normally, 2x when shift held down
        self.isRunning = game.keyboard.pressed(pygame.locals.K_LSHIFT)
        runSpeed = constants.PLAYER_MOVEMENT_SPEED * (self.isRunning + 1)

        a = pygame.math.Vector2(self.position.x, self.position.y + self.size.y)
        b = pygame.math.Vector2(self.position.x + self.size.x, self.position.y)
        collision = game.currentLevel.collision_check(a, b)

        self.grounded = False

        if collision[2]:
            # Top-side collision: snap to the lower bound of the collided tile.
            snapY = int(self.position.y + self.size.y) & ~(constants.WORLD_TILE_SIZE - 1)
            self.position.y = snapY - self.size.y - 1
            self.velocity.y = 0
        elif collision[3]:
            self.grounded = True

            if game.keyboard.pressed(pygame.locals.K_SPACE):
                # Player is grounded and key pressed: apply jumping force.
                self.velocity.y = constants.PLAYER_JUMPING_SPEED
            else:
                # Bottom-side collision: snap to the upper bound of the collided tile.
                snapY = int(self.position.y) & ~(constants.WORLD_TILE_SIZE - 1)
                self.position.y = snapY + constants.WORLD_TILE_SIZE - 0.1
                self.velocity.y = 0
        else:
            # No vertical collision: apply gravity as normal.
            self.velocity.y += constants.WORLD_GRAVITY * deltaTime

        if game.keyboard.pressed(pygame.locals.K_SPACE) and self.jetpackFuel > 0:
            # If the player is holding space and jetpack fuel is available, update as needed.
            self.velocity.y += constants.PLAYER_JETPACK_SPEED * deltaTime
            self.jetpackFuel -= 30 * deltaTime
        elif self.grounded and self.jetpackFuel < constants.PLAYER_JETPACK_MAX:
            # If space isn't being held and jetpack fuel isn't maxed out, add.
            self.jetpackFuel += 15 * deltaTime

        if game.keyboard.pressed(pygame.locals.K_a):
            self.velocity.x -= runSpeed
            self.direction = 1
        if game.keyboard.pressed(pygame.locals.K_d):
            self.velocity.x += runSpeed
            self.direction = 0

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

        # Update the player and game state accordingly.
        self.position += self.velocity * deltaTime
        self.velocity.x *= constants.PLAYER_FRICTION_COEFFICIENT

    def check_enemy_collision(self, game: "game.Game", deltaTime: float) -> None:
        rect = pygame.Rect(self.position, self.size)
        for entity in game.entities:
            if isinstance(entity, Enemy):
                # Make sure player is above the enemy
                enemyCollision = pygame.Rect(entity.position + pygame.Vector2(0, entity.size.y - 16), (entity.size.x, 16))
                if self.position.y > entity.position.y + entity.size.y - 20 and rect.colliderect(enemyCollision): # Check for collision with enemy's head.
                    game.remove_entity(entity)
                    self.velocity.y = constants.PLAYER_JUMPING_SPEED # Player bounces off entity
                    self.position.y += constants.PLAYER_JUMPING_SPEED * deltaTime
                    return

    def tick(self, game: "game.Game", deltaTime: float) -> None:
        """Updates the player's internal state."""
        self.update_movement(game, deltaTime)
        self.check_enemy_collision(game, deltaTime)
        self.vibe_check(game)

    def render(self, display: pygame.Surface) -> None:
        """Renders the player sprite to the screen."""

        # Move the viewport when the player hits the first or last third of the screen
        if self.position.x - self.game.viewport[0] <= self.game.renderResolution[0] / 2.5:
            self.game.viewport.x = max(0, self.position.x - self.game.viewportSize[0] / 2.5)
        elif self.position.x - self.game.viewport[0] >= self.game.renderResolution[0] - self.game.renderResolution[0] / 2.5:
            self.game.viewport.x = max(0, self.position.x - (self.game.renderResolution[0] - self.game.renderResolution[0] / 2.5))

        self.game.viewport.y = max(0, self.position.y - self.game.viewportSize[1] / 2)

        playerPosition = pygame.Vector2(self.position.x, self.position.y + self.size.y)
        playerPosition = self.game.calculate_offset(playerPosition)

        timeSinceStart = pygame.time.get_ticks() # Time since pygame init called in ms
        spriteSourcePos = pygame.Vector2(0, 0);
        if self.grounded: # Walking animation
            if abs(self.velocity.x) >= constants.PLAYER_MOVEMENT_SPEED: # Check if player is moving
                if self.isRunning: # Faster animations when running
                    spriteSourcePos.x = int(((timeSinceStart % 500) / 125)) * constants.WORLD_TILE_SIZE
                else:
                    spriteSourcePos.x = int(((timeSinceStart % 1000) / 250)) * constants.WORLD_TILE_SIZE

        spriteSourcePos.y = self.size.y * self.direction

        display.blit(self.sprite, playerPosition, pygame.Rect(spriteSourcePos, self.size))

        jetpackScale = self.jetpackFuel / constants.PLAYER_JETPACK_MAX
        jetpackOffset = self.size.y * jetpackScale
        jetpackPosition = pygame.Vector2(self.position.x + self.size.x + 1, self.position.y + jetpackOffset)
        jetpackPosition = self.game.calculate_offset(jetpackPosition)
        jetpackRect = pygame.Rect(jetpackPosition.x, jetpackPosition.y, 3, jetpackOffset)
        pygame.draw.rect(display, (255, 0, 0), jetpackRect)
