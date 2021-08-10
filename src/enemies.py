import constants
import bullets
import random
import game

import pygame.transform
import pygame.math
import pygame

class Turret:
    def __init__(self, game: "game.Game", position: pygame.math.Vector2) -> None:
        """Instantiates an instance of the `Turret` class."""
        sprite = game.resources.get_image("turret")
        self.size = pygame.math.Vector2(constants.WORLD_TILE_SIZE, constants.WORLD_TILE_SIZE)
        self.sprite = pygame.transform.scale(sprite, (int(self.size.x), int(self.size.y)))
        self.position = position
        self.game = game

        # Internal turret variables.
        self.shooterTimer = self.reset_timer()

    def reset_timer(self) -> int:
        """Returns a random number for the turret's shooting delay."""
        return random.randint(40, 75)

    def tick(self, game: "game.Game", deltaTime: float) -> None:
        """Updates the turret's internal state."""
        if self.shooterTimer <= 0:
            self.shooterTimer = self.reset_timer()
            position = pygame.math.Vector2(self.position.x, self.position.y)
            velocity = game.playerEntity.position - position
            bullet = bullets.Bullet(game, position, velocity)
            game.add_entity(bullet)
        else:
            self.shooterTimer -= 1

    def render(self, display: pygame.Surface) -> None:
        """Renders this turret to the screen."""
        position = pygame.Vector2(self.position.x, self.position.y + self.size.y)
        position = self.game.calculate_offset(position)
        display.blit(self.sprite, position)
