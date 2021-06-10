import pygame
import entity

class Game:
    def __init__(self) -> None:
        self.entities = [entity.Entity]

    def tick(self) -> None:
        for entity in self.entities:
            entity.Tick()

    def render(self, surface: pygame.Surface) -> None:
        pass

    def add_entity(self, entity: entity.Entity) -> None:
        self.entities.append(entity)
