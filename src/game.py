import pygame
import entity
import player

class Game:
    def __init__(self) -> None:
        self.entities = {
            "player": player.Player()
        }

    def tick(self, deltaTime: float) -> None:
        """Update each entity's internal state."""
        for entity in self.entities.values():
            entity.tick(deltaTime)

    def render(self, surface: pygame.Surface) -> None:
        """Draws all entities onto the specified surface."""
        for entity in self.entities.values():
            entity.render(surface)

    def add_entity(self, entity: entity.Entity) -> None:
        """Adds an entity to the game's internal tracking system."""
        self.entities.append(entity)
