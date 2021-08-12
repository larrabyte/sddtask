import collections
import resources
import constants
import player
import inputs
import level

import pygame.display
import pygame.event
import pygame.mixer
import pygame.time
import pygame.math
import pygame

class Game:
    def __init__(self) -> None:
        """Initialises an instance of the Game."""
        pygame.init()

        # Initialise relevant PyGame subsystems.
        flags = pygame.SHOWN | pygame.HWSURFACE
        self.display = pygame.display.set_mode((0, 0), flags | pygame.FULLSCREEN)
        self.scaledResolution = self.display.get_size()
        self.renderResolution = (int(self.scaledResolution[0] / constants.SCREEN_SCALE), int(self.scaledResolution[1] / constants.SCREEN_SCALE))
        self.renderSurface = pygame.Surface(self.renderResolution)
        self.clock = pygame.time.Clock()

        self.viewportSize = self.renderSurface.get_size()
        self.viewport = pygame.math.Vector2(0.0, 0.0)

        # Internal game subsystems.
        self.keyboard = inputs.Keyboard()
        self.mouse = inputs.Mouse()
        self.resources = resources.Resources()

        # Internal game variables.
        self.healthBar = self.resources.get_image("health")
        self.fuelBar = self.resources.get_image("fuel")
        self.levels = collections.deque()
        self.entities = set()
        self.currentLevel = None
        self.playerEntity = None
        self.gameResult = 0
        self.running = True

    def calculate_offset(self, position: pygame.math.Vector2) -> pygame.math.Vector2:
        """Calculates the offset required for `position` to be rendered."""
        position.x = position.x - self.viewport[0]
        position.y = self.renderResolution[1] - (position.y - self.viewport[1])

        return position

    def add_entity(self, entity: object) -> None:
        """Adds an entity to the internal entity tracking system."""
        if isinstance(entity, player.Player):
            self.playerEntity = entity

        self.entities.add(entity)

    def remove_entity(self, entity: object) -> None:
        """Removes an entity from the internal entity tracking system."""
        self.entities.remove(entity)

    def add_level(self, level: "level.Level") -> None:
        """Adds a level to the game."""
        self.levels.append(level)

    def tick(self, deltaTime: float) -> None:
        """Updates the game's internal state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        for entity in self.entities.copy():
            entity.tick(self, deltaTime)

    def render(self) -> None:
        """Renders all entities and tiles to the screen."""
        self.currentLevel.render(self.renderSurface, self.viewport, self.viewportSize)

        for entity in self.entities:
            entity.render(self.renderSurface)

        if self.playerEntity and self.playerEntity.healthPoints > 0:
            self.renderSurface.blit(pygame.transform.scale(self.healthBar, (int(100 * (self.playerEntity.healthPoints / constants.PLAYER_HEALTH_MAX)), 16)), (1, self.renderResolution[1] - 34))
            self.renderSurface.blit(pygame.transform.scale(self.fuelBar, (int(100 * (self.playerEntity.jetpackFuel / constants.PLAYER_JETPACK_MAX)), 16)),  (1, self.renderResolution[1] - 17))

        pygame.transform.scale(self.renderSurface, self.scaledResolution, self.display)
        pygame.display.flip()

    def run(self) -> None:
        """Starts the game loop. This function does not return."""
        self.currentLevel = self.levels.popleft()
        pygame.mixer.music.load("audio/music.wav")
        pygame.mixer.music.play(-1)

        while self.running:
            self.render()
            deltaTime = self.clock.tick(0) / 1000.0
            self.tick(deltaTime)

        if self.gameResult == -1:
            # -1 means the game is lost (player died).
            blood = (255, 0, 0)
            self.display.fill(blood)
            pygame.display.flip()
            pygame.time.delay(1500)
        elif self.gameResult == 1:
            # 1 means game was won (player reached the flag).
            green = (0, 255, 0)
            self.display.fill(green)
            pygame.display.flip()
            pygame.time.delay(1500)
