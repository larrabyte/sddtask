from entity import Entity

import pymunk

import pygame.display
import pygame.event
import pygame.time
import pygame.key
import pygame

UNITS_PER_METRE = 32

class Game:
    display: pygame.Surface
    clock: pygame.time.Clock

    phySpace = pymunk.Space()
    displayScale = 1
    running = True
    entities = []
    bodies = []

    @classmethod
    def add_entity(cls, ent: Entity) -> None:
        """Add an entity to the game's internal tracking system."""
        cls.entities.append(ent)

        if hasattr(ent, "body") and hasattr(ent, "shapes"):
            cls.phySpace.add(ent.body, *ent.shapes)
            cls.bodies.append(ent.body)

    @classmethod
    def tick(cls, deltaTime: float) -> None:
        """Update the game's physics state and ticks all tracked entities."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cls.running = False

        # Tick all tracked entities.
        for entity in cls.entities:
            entity.tick(deltaTime)

        # Update the Pymunk physics space.
        cls.phySpace.step(deltaTime)

    @classmethod
    def render(cls, surface: pygame.Surface) -> None:
        """Draws all entities onto the specified surface."""
        background = (0, 0, 0)
        cls.display.fill(background)

        for entity in cls.entities:
            entity.render(surface)

        pygame.display.flip()

    @classmethod
    def run(cls) -> None:
        """Initialises and starts the game."""
        pygame.init() # Initialise all PyGame subsystems before creating objects.
        resolution, flags = (640, 480), pygame.SCALED | pygame.SHOWN
        cls.display = pygame.display.set_mode(size=resolution, flags=flags)
        cls.clock = pygame.time.Clock()

        # Initialise Pymunk and setup a suitable physics space.
        cls.phySpace.gravity = 0, 9.8

        # Handle event dispatch here.
        while cls.running:
            deltaTime = cls.clock.get_time() / 1000
            cls.tick(deltaTime)
            cls.render(cls.display)
            cls.clock.tick(60)
