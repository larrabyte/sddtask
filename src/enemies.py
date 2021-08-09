import constants
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

    def tick(self, game: "game.Game", deltaTime: float) -> None:
        """Updates the turret's internal state."""
        pass

    def render(self, display: pygame.Surface) -> None:
        """Renders this turret to the screen."""
        position = pygame.Vector2(self.position.x, self.position.y + self.size.y)
        position = self.game.calculate_offset(position)
        display.blit(self.sprite, position)
