import collections
import resources
import constants
import inputs
import level

import pygame.display
import pygame.event
import pygame.time
import pygame.math
import pygame

class Game:
    def __init__(self) -> None:
        """Initialises an instance of the Game."""
        pygame.init()

        # Initialise relevant PyGame subsystems.
        resolution = (1366, 768)
        flags = pygame.SCALED | pygame.SHOWN | pygame.HWSURFACE | pygame.DOUBLEBUF
        self.display = pygame.display.set_mode(resolution, flags, vsync=1)
        self.clock = pygame.time.Clock()

        self.viewportSize = self.display.get_size()
        self.viewport = pygame.math.Vector2(0.0, 0.0)

        # Internal game subsystems.
        self.keyboard = inputs.Keyboard()
        self.mouse = inputs.Mouse()
        self.resources = resources.Resources()

        # Internal game variables.
        self.levels = collections.deque()
        self.currentLevel = None
        self.running = True
        self.entities = []

    def add_entity(self, entity: object) -> None:
        """Adds an entity to the internal entity tracking system."""
        self.entities.append(entity)

    def add_level(self, level: "level.Level") -> None:
        """Adds a level to the game."""
        self.levels.append(level)

    def tick(self, deltaTime: float) -> None:
        """Updates the game's internal state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        for entity in self.entities:
            entity.tick(self, deltaTime)

    def render(self) -> None:
        """Renders all entities and tiles to the screen."""
        self.display.fill(constants.BACKGROUND_COLOUR)
        self.currentLevel.render(self.display, self.viewport, self.viewportSize)

        for entity in self.entities:
            entity.render(self.display)

        pygame.display.flip()

    def run(self) -> None:
        """Starts the game loop. This function does not return."""
        self.currentLevel = self.levels.popleft()

        while self.running:
            self.render()
            deltaTime = self.clock.tick(0) / 1000.0
            self.tick(deltaTime)
