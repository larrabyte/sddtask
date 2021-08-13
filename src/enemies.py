import constants
import bullets
import random
import game

import pygame.transform
import pygame.math
import pygame

class Enemy:
    def __init__(self, game: "game.Game", position: pygame.math.Vector2, type: int) -> None:
        """Instantiates an instance of the `Enemy` class."""
        sprite = game.resources.get_image(f"soldier{type}")
        self.size = pygame.math.Vector2(constants.WORLD_TILE_SIZE, constants.WORLD_TILE_SIZE * 2)
        self.sprite = pygame.transform.scale(sprite, (int(self.size.x), int(self.size.y)))
        self.position = position
        self.game = game

        # Internal turret variables.
        self.shooterTimer = self.reset_timer()

    def reset_timer(self) -> int:
        """Returns a random number for the turret's shooting delay."""
        return random.randint(10, 20) / constants.PROJECTILE_FIRE_RATE

    def tick(self, game: "game.Game", deltaTime: float) -> None:
        """Updates the turret's internal state."""
        if self.shooterTimer <= 0 and game.playerEntity is not None:
            self.shooterTimer = self.reset_timer()

            if game.playerEntity.position.distance_to(self.position) < constants.PLAYER_DETECT_RANGE:
                position = pygame.math.Vector2(self.position.x, self.position.y + self.size.y / 3)
                velocity = (game.playerEntity.position + pygame.Vector2(game.playerEntity.size.x / 2, game.playerEntity.size.y / 2)) - position
                velocity = velocity.normalize() * constants.PROJECTILE_SPEED
                bullet = bullets.Bullet(game, position, velocity)
                game.add_entity(bullet)

        else:
            self.shooterTimer -= 1

    def render(self, display: pygame.Surface) -> None:
        """Renders this turret to the screen."""
        position = pygame.Vector2(self.position.x, self.position.y + self.size.y)
        position = self.game.calculate_offset(position)
        display.blit(self.sprite, position)
