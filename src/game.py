import entity
import pygame

class Game():
    def __init__(self) -> None:
        self.entities = [entity.Entity];

    def Tick(self) -> None:
        for entity in self.entities:
            entity.Tick()

    def Render(self, surface : pygame.Surface) -> None:
        pass

    def AddEntity(self, entity : entity.Entity) -> None:
        self.entities.append(entity)
