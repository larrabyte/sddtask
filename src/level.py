import datatypes as dt
import constants
import game

import pygame.math
import pygame.draw
import pygame

class Level:
    def __init__(self, game: "game.Game", name: str) -> None:
        """Creates an instance of a `Level` object."""
        data = game.resources.fetch_level_data(name)
        self.tilemap = game.resources.get_image("tilemap")

        tileResX = int(game.resolution.x / constants.TILE_SIZE)
        tileResY = int(game.resolution.y / constants.TILE_SIZE)
        self.tileResolution = dt.IntVector2(tileResX, tileResY)

        self.width = data["width"]
        self.height = data["height"]
        self.foregroundLayer = None
        self.backgroundLayers = []

        for layer in data["layers"]:
            # OK, so basically: nested list comprehensions are cool. We iterate over the tile
            # array and create a list of lists, where each sub-list contains each row's tile data.
            current = [[layer["data"][self.width * y + x] for x in range(self.width)] for y in range(self.height)]

            if layer["name"] == "foreground":
                if self.foregroundLayer is None:
                    self.foregroundLayer = current
            else:
                self.backgroundLayers.append(current)

    def get_foreground_tile(self, x: float, y: float) -> int:
        """Returns the foreground tile at world coordinates (x, y)."""
        tileX = int(x / constants.TILE_SIZE)
        tileY = int(y / constants.TILE_SIZE)

        # Only access the foreground layer if tileX and tileY are in bounds.
        if 0 <= tileX <= self.width and 0 <= tileY <= self.height:
            return self.foregroundLayer[self.height - tileY - 1][tileX]

        return 0

    def collision_check(self, a: pygame.math.Vector2, b: pygame.math.Vector2) -> dt.CollisionData:
        """Returns whether any physical tiles are adjacent to the given world coordinates."""
        leftTop = self.get_foreground_tile(a.x, b.y + 4)
        leftMiddle = self.get_foreground_tile(a.x, (a.y + b.y) / 2)
        leftBottom = self.get_foreground_tile(a.x, a.y - 4)
        left = leftTop + leftMiddle + leftBottom

        rightTop = self.get_foreground_tile(b.x, b.y + 4)
        rightMiddle = self.get_foreground_tile(b.x, (a.y + b.y) / 2)
        rightBottom = self.get_foreground_tile(b.x, a.y - 4)
        right = rightTop + rightMiddle + rightBottom

        topLeft = self.get_foreground_tile(a.x + 4, a.y)
        topMiddle = self.get_foreground_tile((a.x + b.x) / 2, a.y)
        topRight = self.get_foreground_tile(b.x - 4, a.y)
        top = topLeft + topMiddle + topRight

        bottomLeft = self.get_foreground_tile(a.x + 4, b.y)
        bottomMiddle = self.get_foreground_tile((a.x + b.x) / 2, b.y)
        bottomRight = self.get_foreground_tile(b.x - 4, b.y)
        bottom = bottomLeft + bottomMiddle + bottomRight

        return dt.CollisionData(left > 0, right > 0, top > 0, bottom > 0)

    def render(self, display: pygame.Surface, viewport: dt.IntVector2, resolution: dt.IntVector2) -> None:
        """Renders each layer to the display."""
        # Calculate the viewport offset as a number of tiles (rounded down).
        offsetX = int(viewport.x / constants.TILE_SIZE)
        offsetY = int(viewport.y / constants.TILE_SIZE)
        offset = dt.IntVector2(offsetX, offsetY)

        for layer in self.backgroundLayers:
            # Render each background layer by iterating through the list of background layers.
            self.render_layer(display, viewport, resolution, offset, layer)

        # Render the foreground layer last.
        self.render_layer(display, viewport, resolution, offset, self.foregroundLayer)

    def render_layer(self, display: pygame.Surface, viewport: dt.IntVector2, resolution: dt.IntVector2, offset: dt.IntVector2, layer: list) -> None:
        """Renders a specific layer given a display and viewport information."""
        minimumY = min(self.tileResolution.y, self.height - offset.y)
        mimimumX = min(self.tileResolution.x, self.width - offset.x)

        for y in range(minimumY): # When y = 0, we are at the bottom of the level.
            for x in range(mimimumX): # Ensure we are within both the tilemap and screen bounds.
                if (tile := layer[self.height - y - offset.y - 1][x + offset.x]) > 0:
                    destinationX = (x * constants.TILE_SIZE) - (viewport.x % constants.TILE_SIZE)
                    destinationY = resolution.y - (viewport.y + (y + 1) * constants.TILE_SIZE)

                    destination = pygame.Rect(destinationX, destinationY, constants.TILE_SIZE, constants.TILE_SIZE)
                    area = pygame.Rect((tile - 1) * constants.TILE_SIZE, 0, constants.TILE_SIZE, constants.TILE_SIZE)
                    display.blit(self.tilemap, destination, area)
