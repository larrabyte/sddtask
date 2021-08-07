import constants
import game

import pygame.math
import pygame

class Bullet:
    def __init__(self, game: "game.Game", position: pygame.math.Vector2, velocity: pygame.math.Vector2) -> None:
        """Initialises an instance of the `Bullet` class."""
        surface = game.resources.get_image("funnybullet")
        self.size = pygame.math.Vector2(12, 12)
        self.sprite = pygame.transform.scale(surface, (int(self.size.x), int(self.size.y)))
        self.game = game

        self.position = position
        self.velocity = velocity

    def tick(self, game: "game.Game", deltaTime: float) -> None:
        """Updates the bullet's internal state."""
        screen = game.display.get_size()
        boundedX = 0 <= self.position.x <= screen[0] + game.viewport.x
        boundedY = 0 <= self.position.y <= screen[1] + game.viewport.y
        bounded = boundedX and boundedY

        if bounded:
            a = pygame.math.Vector2(self.position.x, self.position.y + self.size.y)
            b = pygame.math.Vector2(self.position.x + self.size.x, self.position.y)
            collision = game.currentLevel.collision_check(a, b)

        if not bounded or any(collision):
            game.remove_entity(self)

        self.velocity.y += constants.WORLD_GRAVITY * deltaTime
        self.position += self.velocity * deltaTime

    def render(self, display: pygame.Surface) -> None:
        """Renders the bullet's sprite to the screen."""
        position = pygame.Vector2(self.position.x, self.position.y + self.size.y)
        position = self.game.calculate_offset(position)
        display.blit(self.sprite, position)