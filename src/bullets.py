import random
import game
import math

import pygame.transform
import pygame.math
import pygame

class Bullet:
    def __init__(self, game: "game.Game", position: pygame.math.Vector2, velocity: pygame.math.Vector2) -> None:
        """Initialises an instance of the `Bullet` class."""
        surface = game.resources.get_image("bullet")
        self.size = pygame.math.Vector2(16, 16)
        self.sprite = pygame.transform.scale(surface, (int(self.size.x), int(self.size.y)))
        self.game = game

        # Rotate the bullet to face the direction of travel.
        if velocity.x < 0:
            self.sprite = pygame.transform.flip(self.sprite, True, False)

        velocity.x = min(velocity.x, 0.01)
        theta = math.atan(velocity.y / velocity.x) * (180.0 / math.pi)
        self.sprite = pygame.transform.rotozoom(self.sprite, theta, 1.0)

        self.position = position
        self.velocity = velocity

    def tick(self, game: "game.Game", deltaTime: float) -> None:
        """Updates the bullet's internal state."""
        screen = game.display.get_size()
        boundedX = 0 <= self.position.x <= screen[0] + game.viewport.x
        boundedY = 0 <= self.position.y <= screen[1] + game.viewport.y

        if boundedX and boundedY:
            a = pygame.math.Vector2(self.position.x, self.position.y + self.size.y)
            b = pygame.math.Vector2(self.position.x + self.size.x, self.position.y)
            collision = game.currentLevel.collision_check(a, b)

        if not (boundedX and boundedY) or any(x[0] for x in collision):
            game.remove_entity(self)

        playerRef = game.playerEntity
        if playerRef is not None:
            playerHorizontal = playerRef.position.x <= self.position.x <= playerRef.position.x + playerRef.size.x
            playerVertical = playerRef.position.y <= self.position.y <= playerRef.position.y + playerRef.size.y

            if playerHorizontal and playerVertical:
                # We hit the player, deal damage!
                playerRef.healthPoints -= random.randint(7, 15)
                playerRef.hurt.play()
                game.remove_entity(self)

        self.position += self.velocity * deltaTime

    def render(self, display: pygame.Surface) -> None:
        """Renders the bullet's sprite to the screen."""
        position = pygame.Vector2(self.position.x, self.position.y + self.size.y)
        position = self.game.calculate_offset(position)
        display.blit(self.sprite, position)
