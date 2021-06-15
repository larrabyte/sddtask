import pygame

class Entity:
    def __init__(self) -> None:
        pass

    def tick(self, deltaTime: float) -> None:
        """Each entity's tick() function is called by the game engine
           every frame to allow the entity to update its internal state."""
        pass

    def render(self, surface: pygame.Surface) -> None:
        """Each entity's render() function is called by the game engine
           whenever its sprite must be drawn to the screen (typically every frame)."""
        pass
