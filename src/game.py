from constants import *
from entity import Entity
from resources import ResourceManager

import typing as t
import pymunk

import pygame.display
import pygame.event
import pygame.time
import pygame.key
import pygame

class Game:
    display: pygame.Surface
    clock: pygame.time.Clock

    phySpace = pymunk.Space()
    displayScale = 1
    running = True
    entities = []
    bodies = []

    viewport = pygame.Vector2(0, 0)
    viewportSize: t.Tuple[int, int]
    viewportSizeTiles: t.Tuple[int, int] # Viewport size in tiles

    from level import Level
    currentLevel: Level = ResourceManager.get_level("level1")

    @classmethod
    def add_entity(cls, ent: Entity) -> None:
        """Add an entity to the game's internal tracking system."""
        cls.entities.append(ent)

        if hasattr(ent, "body") and hasattr(ent, "shapes"):
            cls.phySpace.add(ent.body, *ent.shapes)
            cls.bodies.append(ent.body)

    @classmethod
    def tick(cls, deltaTime: float) -> None:
        # Update the Pymunk physics space.
        cls.phySpace.step(deltaTime)

        """Update the game's physics state and ticks all tracked entities."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cls.running = False

        # Tick all tracked entities.
        for entity in cls.entities:
            entity.tick(deltaTime)

    @classmethod
    def render(cls, surface: pygame.Surface) -> None:
        """Draws all entities onto the specified surface."""
        cls.currentLevel.render(surface)

        for entity in cls.entities:
            entity.render(surface)

        pygame.display.flip()

    @classmethod
    def run(cls) -> None:
        """Initialises and starts the game."""
        pygame.init() # Initialise all PyGame subsystems before creating objects.
        cls.viewportSize = (1024, 768)
        cls.viewportSizeTiles = (int((cls.viewportSize[0] + TILE_SIZE - 1) / TILE_SIZE), int((cls.viewportSize[1] / TILE_SIZE + TILE_SIZE - 1))) # Ensure that we round up

        flags = pygame.SCALED | pygame.SHOWN
        cls.display = pygame.display.set_mode(size=cls.viewportSize, flags=flags)
        cls.clock = pygame.time.Clock()

        # Initialise Pymunk and setup a suitable physics space.
        cls.phySpace.gravity = 0, -9.8 * UNITS_PER_METRE

        for i, row in enumerate(cls.currentLevel.foregroundLayer):
            for j, tile in enumerate(row):
                if tile > 0:
                    x, y = j * TILE_SIZE, (cls.currentLevel.height - i - 1) * TILE_SIZE
                    phyBody = pymunk.Body(mass=1.0, moment=1.0, body_type=pymunk.Body.STATIC)
                    phyBody.position = (x, y)
                    phyShape = pymunk.Poly.create_box(phyBody, size=(TILE_SIZE, TILE_SIZE))
                    Game.phySpace.add(phyBody, phyShape)

        # Handle event dispatch here.
        while cls.running:
            deltaTime = cls.clock.get_time() / 1000
            cls.tick(deltaTime)
            cls.render(cls.display)
            cls.clock.tick(60)
import pygame
import random
from entity import Entity
