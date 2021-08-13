import resources
import constants
import player
import inputs

import pygame.transform
import pygame.display
import pygame.locals
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
        self.paused = self.resources.get_image("paused")

        self.font = self.resources.get_font("vcr_osd_mono")
        self.entities = set()
        self.currentLevel = None
        self.playerEntity = None
        self.gameResult = 0
        self.running = True
        self.score = 0
        self.finishTime = 0

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

    def game_pause_loop(self):
        """Game pause loop."""
        paused = True

        self.display.blit(pygame.transform.scale(self.paused, self.scaledResolution), (0, 0))
        pygame.display.flip()

        while paused and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.locals.K_ESCAPE:
                        # Unpause on Escape.
                        paused = False
                    elif event.key == pygame.locals.K_r:
                        # Restart on R.
                        self.running = False
                        self.gameResult = 2
                    elif event.key == pygame.locals.K_q:
                        # Quit on Q.
                        self.running = False

    def tick(self, deltaTime: float) -> None:
        """Updates the game's internal state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.locals.K_ESCAPE:
                    # Interrupt game loop to pause.
                    self.game_pause_loop()
                    self.clock.tick(0)
                    return

        for entity in self.entities.copy():
            entity.tick(self, deltaTime)

        # Used to add a time bonus to score
        self.finishTime += deltaTime

    def render(self) -> None:
        """Renders all entities and tiles to the screen."""
        self.currentLevel.render(self.renderSurface, self.viewport, self.viewportSize)

        for entity in self.entities:
            entity.render(self.renderSurface)

        if self.playerEntity is not None and self.playerEntity.healthPoints > 0:
            self.renderSurface.blit(pygame.transform.scale(self.healthBar, (int(150 * (self.playerEntity.healthPoints / constants.PLAYER_HEALTH_MAX)), 16)), (1, self.renderResolution[1] - 34))
            self.renderSurface.blit(pygame.transform.scale(self.fuelBar, (int(150 * (self.playerEntity.jetpackFuel / constants.PLAYER_JETPACK_MAX)), 16)),  (1, self.renderResolution[1] - 17))
            self.renderSurface.blit(self.font.render(f"Score: {int(self.score)}", False, (0, 0, 0)), (10, 10))

        pygame.transform.scale(self.renderSurface, self.scaledResolution, self.display)
        pygame.display.flip()

    def postgame(self) -> bool:
        """Post game loop."""
        while True: # Now we listen for keystrokes.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.locals.K_r:
                        return True
                    elif event.key == pygame.locals.K_ESCAPE:
                        return False

    def run(self) -> bool:
        """Starts the game loop."""
        pygame.mixer.music.load("audio/music.wav")
        pygame.mixer.music.play(-1)

        while self.running:
            self.render()
            deltaTime = self.clock.tick(0) / 1000.0
            self.tick(deltaTime)

        # A return value of false indicates that the game was quit.
        # A return value of true indicates that the game should be restarted.

        if self.gameResult == -1:
            # -1 means the game is lost (player died).
            gameOver = self.resources.get_image("gameover")
            self.display.blit(pygame.transform.scale(gameOver, self.scaledResolution), (0, 0))

            white = (255, 255, 255)
            text = self.font.render(f"Final Score: {int(self.score)}", False, white)
            textPosition = (self.scaledResolution[0] / 2.275, self.scaledResolution[1] / 1.75)
            self.display.blit(text, textPosition)

            pygame.mixer.music.stop()
            pygame.display.flip()
            return self.postgame()
        elif self.gameResult == 1:
            # 1 means game was won (player reached the flag).
            gameOver = self.resources.get_image("gamewon")
            self.display.blit(pygame.transform.scale(gameOver, self.scaledResolution), (0, 0))

            white = (255, 255, 255)
            scoreString = f"Score: {int(self.score)}    "
            if self.finishTime < 5 * 60: # 5 Minutes
                scoreString += f"Time Bonus: {int(5 * 60 - self.finishTime)}    "
                self.score += 5 * 60 - self.finishTime

            scoreString += f"Final Score: {int(self.score)}"

            text = self.font.render(scoreString, False, white)
            textPosition = (self.scaledResolution[0] / 2 - self.font.size(scoreString)[0] / 2, self.scaledResolution[1] / 2.675)
            self.display.blit(text, textPosition)

            pygame.display.flip()
            return self.postgame()
        elif self.gameResult == 2: # Restart in pause menu
            return True
