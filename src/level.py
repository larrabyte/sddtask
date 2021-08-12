import typing as t
import constants
import enemies
import game

import pygame.math
import pygame.draw
import pygame

class Level:
    def __init__(self, game: "game.Game", name: str) -> None:
        """Creates an instance of a `Level` object."""
        data = game.resources.fetch_level_data(name)
        self.tilemap = game.resources.get_image("tilemap")
        self.tilemapTilesPerRow = self.tilemap.get_width() / constants.WORLD_TILE_SIZE

        tileResX = int(game.viewportSize[0] + constants.WORLD_TILE_SIZE * 2 - 1) >> constants.WORLD_TILE_SHIFT
        tileResY = int(game.viewportSize[1] + constants.WORLD_TILE_SIZE * 2 - 1) >> constants.WORLD_TILE_SHIFT
        self.viewportSizeTiles = (tileResX, tileResY)

        self.width = data["width"]
        self.height = data["height"]
        self.foregroundLayer = None
        self.layers = []

        for layer in data["layers"]:
            # OK, so basically: nested list comprehensions are cool. We iterate over the tile
            # array and create a list of lists, where each sub-list contains each row's tile data.
            current = [[layer["data"][self.width * y + x] for x in range(self.width)] for y in range(self.height)]

            if layer["name"] == "foreground":
                if self.foregroundLayer is None:
                    self.foregroundLayer = current

            if layer["name"] == "enemies":
                # If this layer contains enemy spawn points, add them as entities.
                for y in range(self.height):
                    for x in range(self.width):
                        if (identifier := current[y][x] - 256) > 0 and identifier <= 3:
                            # Enemy tiles start at 257.
                            tileY = self.height - y - 1
                            position = pygame.math.Vector2(x * constants.WORLD_TILE_SIZE, tileY * constants.WORLD_TILE_SIZE)
                            enemy = enemies.Enemy(game, position, identifier)
                            game.add_entity(enemy)

            else:
                self.layers.append(current)

    def get_foreground_tile(self, x: float, y: float) -> int:
        """Returns the foreground tile at world coordinates (x, y)."""
        tileX = int(x / constants.WORLD_TILE_SIZE)
        tileY = int(y / constants.WORLD_TILE_SIZE)

        # Only access the foreground layer if tileX and tileY are in bounds.
        if 0 <= tileX <= self.width and 0 <= tileY <= self.height:
            return self.foregroundLayer[self.height - tileY - 1][tileX]

        return 0

    def collision_check(self, a: pygame.math.Vector2, b: pygame.math.Vector2) -> t.Tuple[t.Tuple[bool, int]]:
        """Returns the value of any adjacent physical tiles that are adjacent to the physical world coodinates."""
        leftTop = self.get_foreground_tile(a.x, b.y + 4)
        leftMiddle = self.get_foreground_tile(a.x, (a.y + b.y) / 2)
        leftBottom = self.get_foreground_tile(a.x, a.y - 4)
        left = (leftTop + leftMiddle + leftBottom > 0, leftMiddle)

        rightTop = self.get_foreground_tile(b.x, b.y + 4)
        rightMiddle = self.get_foreground_tile(b.x, (a.y + b.y) / 2)
        rightBottom = self.get_foreground_tile(b.x, a.y - 4)
        right = (rightTop + rightMiddle + rightBottom > 0, rightMiddle)

        topLeft = self.get_foreground_tile(a.x + 4, a.y)
        topMiddle = self.get_foreground_tile((a.x + b.x) / 2, a.y)
        topRight = self.get_foreground_tile(b.x - 4, a.y)
        top = (topLeft + topMiddle + topRight > 0, topMiddle)

        bottomLeft = self.get_foreground_tile(a.x + 4, b.y)
        bottomMiddle = self.get_foreground_tile((a.x + b.x) / 2, b.y)
        bottomRight = self.get_foreground_tile(b.x - 4, b.y)
        bottom = (bottomLeft + bottomMiddle + bottomRight > 0, bottomMiddle)

        return (left, right, top, bottom)

    def render(self, display: pygame.Surface, viewport: pygame.math.Vector2, resolution: t.Tuple[int, int]) -> None:
        """Renders each layer to the display."""
        # Calculate the viewport offset as a number of tiles (rounded down).
        offsetX = int(viewport.x) >> (constants.WORLD_TILE_SHIFT)
        offsetY = int(viewport.y) >> (constants.WORLD_TILE_SHIFT)

        for layer in self.layers:
            # Render each layer by iterating through the list of layers.
            self.render_layer(display, viewport, resolution, (offsetX, offsetY), layer)

    def render_layer(self, display: pygame.Surface, viewport: pygame.math.Vector2, resolution: t.Tuple[int, int], offset: t.Tuple[int, int], layer: list) -> None:
        """Renders a specific layer given a display and viewport information."""
        viewportUnalignedX = (viewport[0] % constants.WORLD_TILE_SIZE)
        viewportUnalignedY = (viewport[1] % constants.WORLD_TILE_SIZE)

        # When y = 0, we are at the bottom of the level.
        for y in range(min(self.viewportSizeTiles[1], self.height - offset[1])):
            for x in range(min(self.viewportSizeTiles[0], self.width - offset[0])):
                yRenderOffset = resolution[1] - ((y + 1) * constants.WORLD_TILE_SIZE - viewportUnalignedY)

                if (tile := layer[self.height - y - offset[1] - 1][x + offset[0]]) > 0:
                    destination = (x * constants.WORLD_TILE_SIZE - viewportUnalignedX, yRenderOffset)
                    area = (((tile - 1) % self.tilemapTilesPerRow) * constants.WORLD_TILE_SIZE, int((tile - 1) / self.tilemapTilesPerRow) * constants.WORLD_TILE_SIZE, constants.WORLD_TILE_SIZE, constants.WORLD_TILE_SIZE)
                    display.blit(self.tilemap, destination, area)
