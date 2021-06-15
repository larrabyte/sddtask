import pygame
import entity
import player

class Game:
    def __init__(self) -> None:
        self.entities = {
            "player": player.Player()
        }

    def tick(self) -> None:
        for entity in self.entities.values():
            entity.tick()

    def render(self, surface: pygame.Surface) -> None:
        pass

    def add_entity(self, entity: entity.Entity) -> None:
        self.entities.append(entity)
