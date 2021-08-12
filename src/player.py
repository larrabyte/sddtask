import constants
import enemies
import game

import pygame.transform
import pygame.locals
import pygame.mixer
import pygame.math
import pygame.draw
import pygame

class Player:
    def __init__(self, game: "game.Game") -> None:
        """Initialises an instance of the `Player` class."""
        self.size = pygame.math.Vector2(constants.WORLD_TILE_SIZE, constants.WORLD_TILE_SIZE * 2)
        self.sprite = game.resources.get_image("max")
        self.hurt = pygame.mixer.Sound("audio/hurt.wav")
        self.game = game

        self.position = pygame.math.Vector2(64, 512)
        self.velocity = pygame.math.Vector2(0.0, 0.0)

        # Player game attributes.
        self.jetpackFuel = constants.PLAYER_JETPACK_MAX
        self.healthPoints = constants.PLAYER_HEALTH_MAX
        self.grounded = False
        self.gunCooldown = 0

    def vibe_check(self, game: "game.Game") -> None:
        """Performs vibe checks to ensure the player is still alive."""
        if self.healthPoints <= 0 or self.position.y + self.size.y < -512:
            # The player is either dead or under the world.
            game.remove_entity(self)
            game.playerEntity = None
            game.gameResult = -1
            game.running = False

    def update_movement(self, game: "game.Game", deltaTime: float) -> None:
        """Updates player movement based on `deltaTime`."""
        self.isRunning = game.keyboard.pressed(pygame.locals.K_LSHIFT)
        runSpeed = constants.PLAYER_MOVEMENT_SPEED * (self.isRunning + 1)

        a = pygame.math.Vector2(self.position.x, self.position.y + self.size.y)
        b = pygame.math.Vector2(self.position.x + self.size.x, self.position.y)
        collision = game.currentLevel.collision_check(a, b)
        self.grounded = collision[3][0]

        if collision[2][0]:
            # Top-side collision: snap to the lower bound of the collided tile.
            snapY = int(self.position.y + self.size.y) & ~(constants.WORLD_TILE_SIZE - 1)
            self.position.y = snapY - self.size.y - 1
            self.velocity.y = 0
        elif collision[3][0]:
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
            self.jetpackFuel -= 50 * deltaTime
        elif self.grounded and self.jetpackFuel < constants.PLAYER_JETPACK_MAX:
            # If space isn't being held and jetpack fuel isn't maxed out, add.
            self.jetpackFuel += 30 * deltaTime

        if game.keyboard.pressed(pygame.locals.K_a):
            self.velocity.x -= runSpeed
        if game.keyboard.pressed(pygame.locals.K_d):
            self.velocity.x += runSpeed

        # Recompute collisions now that the player's vertical position has been resolved.
        a = pygame.math.Vector2(self.position.x, self.position.y + self.size.y)
        b = pygame.math.Vector2(self.position.x + self.size.x, self.position.y)
        collision = game.currentLevel.collision_check(a, b)

        if collision[0][0]:
            # Left-side collision: snap to the right side of the collided tile.
            snapX = int(self.position.x) & ~(constants.WORLD_TILE_SIZE - 1)
            self.position.x = snapX + self.size.x + 1
            self.velocity.x = 0

        if collision[1][0]:
            # Right-side collision: snap to the left side of the collided tile.
            snapX = int(self.position.x + self.size.x) & ~(constants.WORLD_TILE_SIZE - 1)
            self.position.x = snapX - self.size.x - 1
            self.velocity.x = 0

        if any(256 in x[1] for x in collision):
            # The player has hit the flag: win screen!
            game.remove_entity(self)
            game.playerEntity = None
            game.gameResult = 1
            game.running = False
            return

        if self.position.x < 0:
            self.position.x = 0
        if self.position.y > game.currentLevel.height * constants.WORLD_TILE_SIZE:
            self.position.y = game.currentLevel.height * constants.WORLD_TILE_SIZE

        # Update the player and game state accordingly.
        self.position += self.velocity * deltaTime
        self.velocity.x *= constants.PLAYER_FRICTION_COEFFICIENT

    def check_enemy_collision(self, game: "game.Game", deltaTime: float) -> None:
        """Check for enemy collisions using the player's position."""
        rect = pygame.Rect(self.position, self.size)

        for entity in game.entities:
            if isinstance(entity, enemies.Enemy):
                # Make sure player is above the enemy.
                enemyCollision = pygame.Rect(entity.position + pygame.Vector2(0, entity.size.y - 16), (entity.size.x, 16))

                # Check for collision with enemy's head.
                if self.position.y > entity.position.y + entity.size.y - 20 and rect.colliderect(enemyCollision):
                    self.velocity.y = constants.PLAYER_JUMPING_SPEED
                    game.remove_entity(entity)
                    break

    def tick(self, game: "game.Game", deltaTime: float) -> None:
        """Updates the player's internal state."""
        self.update_movement(game, deltaTime)
        self.check_enemy_collision(game, deltaTime)
        self.vibe_check(game)

    def render(self, display: pygame.Surface) -> None:
        """Renders the player sprite to the screen."""
        # Move the viewport when the player hits the first or last third of the screen.
        if self.position.x - self.game.viewport[0] <= self.game.renderResolution[0] / 2.5:
            self.game.viewport.x = max(0, self.position.x - self.game.viewportSize[0] / 2.5)
        elif self.position.x - self.game.viewport[0] >= self.game.renderResolution[0] - self.game.renderResolution[0] / 2.5:
            self.game.viewport.x = max(0, self.position.x - (self.game.renderResolution[0] - self.game.renderResolution[0] / 2.5))

        self.game.viewport.y = max(0, self.position.y - self.game.viewportSize[1] / 2)
        playerPosition = pygame.Vector2(self.position.x, self.position.y + self.size.y)
        playerPosition = self.game.calculate_offset(playerPosition)

        # Time since pygame init called in milliseconds.
        timeSinceStart = pygame.time.get_ticks()
        spriteSourcePos = pygame.Vector2(0, 0)

        if self.grounded: # Controls the walking animation.
            if abs(self.velocity.x) >= constants.PLAYER_MOVEMENT_SPEED:
                if self.isRunning: # Faster animations when running.
                    spriteSourcePos.x = int(((timeSinceStart % 500) / 125)) * constants.WORLD_TILE_SIZE
                else:
                    spriteSourcePos.x = int(((timeSinceStart % 1000) / 250)) * constants.WORLD_TILE_SIZE

        direction = 0 if self.velocity.x > 0 else 1
        spriteSourcePos.y = self.size.y * direction
        display.blit(self.sprite, playerPosition, pygame.Rect(spriteSourcePos, self.size))
