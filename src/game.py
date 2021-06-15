import pygame.display
import pygame.event
import pygame.time
import pygame.key
import pygame

import entity

class Game:
    def __init__(self) -> None:
        # Not defined during initialisation.
        self.display: pygame.Surface
        self.clock: pygame.time.Clock

        self.entities = []
        self.running = True

    def add_entity(self, ent: entity.Entity) -> None:
        """Add an entity to the game's internal tracking system."""
        self.entities.append(ent)

    def tick(self, deltaTime: float) -> None:
        """Update the game's internal state and ticks all tracked entities."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # Tick all tracked entities.
        for entity in self.entities:
            entity.tick(deltaTime)

    def render(self, surface: pygame.Surface) -> None:
        """Draws all entities onto the specified surface."""
        background = (0, 0, 0)
        self.display.fill(background)

        for entity in self.entities:
            entity.render(surface)

        pygame.display.flip()

    def run(self) -> None:
        """Initialises and starts the game."""
        pygame.init() # Initialise all PyGame subsystems before creating objects.
        resolution, flags = (640, 480), pygame.SCALED | pygame.SHOWN
        self.display = pygame.display.set_mode(size=resolution, flags=flags)
        self.clock = pygame.time.Clock()

        # Handle event dispatch here.
        while self.running:
            deltaTime = self.clock.get_time() / 1000
            self.tick(deltaTime)
            self.render(self.display)
            self.clock.tick(60)
