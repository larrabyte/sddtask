from physics import PhysicsBody
from entity import Entity

import typing as t
import pygame.display
import pygame.event
import pygame.time
import pygame.key
import pygame

UNITS_PER_METRE = 32

class Game:
    display: pygame.Surface
    clock: pygame.time.Clock

    bodies: t.List[PhysicsBody] = []
    entities: t.List[Entity] = []
    running = True

    displayScale = 1

    @classmethod
    def add_entity(cls, ent: Entity) -> None:
        """Add an entity to the game's internal tracking system."""
        cls.entities.append(ent)

        if hasattr(ent, "body"):
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

        # Perform physics calculations.
        for body in cls.bodies:
            if body.gravity:
                body.accel.y = -9.8

            body.vel += body.accel * deltaTime
            
            body.pos.y += -(body.vel.y * deltaTime) * UNITS_PER_METRE
            body.pos.x += (body.vel.x * deltaTime) * UNITS_PER_METRE

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

        # Handle event dispatch here.
        while cls.running:
            deltaTime = cls.clock.get_time() / 1000
            cls.tick(deltaTime)
            cls.render(cls.display)
            cls.clock.tick(60)
import pygame
import random
from entity import Entity
