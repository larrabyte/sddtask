import collections
import constants
import resources
import inputs
import level

import pygame.display
import pygame.event
import pygame.time
import pygame

instance = None

class Game:
    viewport = (0, 0)

    def __init__(self) -> None:
        global instance

        """Initialises an instance of the Game."""
        pygame.init()

        assert(instance == None)
        instance = self

        # Initialise relevant PyGame subsystems.
        resolution = (1366, 768)
        flags = pygame.SCALED | pygame.SHOWN
        self.display = pygame.display.set_mode(resolution, flags)
        self.clock = pygame.time.Clock()

        # Internal game subsystems.
        self.keyboard = inputs.Keyboard()
        self.mouse = inputs.Mouse()
        self.resources = resources.Resources()

        # Internal game variables.
        self.levels = collections.deque()
        self.currentLevel = None
        self.running = True
        self.entities = []

        self.viewportSize = self.display.get_size()

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
        background = constants.BACKGROUND_COLOUR
        self.display.fill(background)
        self.currentLevel.render(self.display)

        for entity in self.entities:
            entity.render(self.display)

        pygame.display.flip()

    def run(self) -> None:
        """Starts the game loop. This function does not return."""
        self.currentLevel = self.levels.popleft()

        while self.running:
            deltaTime = self.clock.get_time() / 1000
            self.render()
            self.tick(deltaTime)
            self.clock.tick(60)
