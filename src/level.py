import typing as t
from constants import *
import game

import pygame.math
import pygame.draw
import pygame

class Level:
    def __init__(self, name: str) -> None:
        """Creates an instance of a `Level` object."""
        data = game.instance.resources.fetch_level_data(name)
        self.tilemap = game.instance.resources.get_image("tilemap")

        self.viewportSizeTiles = (int(game.instance.viewportSize[0] / TILE_SIZE), int(game.instance.viewportSize[1] / TILE_SIZE))
        
        self.backgroundLayers = [] # Background layers are purely cosmetic
        self.foregroundLayer = None # The foreground layer is used for collisions and is rendered in front

        self.width = data["width"]
        self.height = data["height"]

        """
            Returns the offset required to align the bottom-left of the tilemap and display.
            Basically, both the tilemap and display start from the top left at (0, 0).
            However the tilemap extends well past the display vertically, so we have
            to compensate by adding a vertical offset to the tilemap. This offset is calculated
            such that the bottom of the tilemape ends up corresponding to the bottom of the display.
        """
        self.screenOffset = (self.height * TILE_SIZE) - game.instance.display.get_size()[1]
        
        layers = data["layers"]
        for layer in layers:
            currentLayer = [[]]

            data: list[int] = layer["data"]

            for y in range(self.height):
                currentLayer.append([])
                for x in range(self.width):
                    currentLayer[y].append(int(data[self.width * y + x]))
            
            if layer["name"] == "foreground":
                self.foregroundLayer = currentLayer
            else:
                self.backgroundLayers.append(currentLayer)

    def get_world_position(self, layer: str, x: int, y: int) -> t.Tuple[float, float]:
        """Converts tile coordinates into world coordinates (top-left of a tile)."""
        return (x * TILE_SIZE, y * TILE_SIZE)

    def get_foreground_tile(self, x: float, y: float) -> int:
        """Returns the tile at world coordinates (x, y) for a specified layer."""
        tileX = int(x / TILE_SIZE)
        tileY = int(y / TILE_SIZE)
        
        if tileX >= self.width or tileY >= self.height or tileX < 0 or tileY < 0:
            return 0

        return self.foregroundLayer[self.height - tileY - 1][tileX]

    def collision_check(self, x1: int, x2: int, y1: int, y2: int) -> t.Tuple[bool, bool, bool, bool]:
        left: int = self.get_foreground_tile(x1, (y1 + y2) / 2) + self.get_foreground_tile(x1, y1 - 4) + self.get_foreground_tile(x1, y2 + 4)
        right: int = self.get_foreground_tile(x2, (y1 + y2) / 2) + self.get_foreground_tile(x2, y1 - 4) + self.get_foreground_tile(x2, y2 + 4)
        top: int = self.get_foreground_tile((x1 + x2) / 2, y1)
        bottom: int = self.get_foreground_tile((x1 + x2) / 2, y2)

        return [left > 0, right > 0, top > 0, bottom > 0]

    def render(self, display: pygame.Surface):
        # Viewport offset as a number of tiles,
        # Convert to int to round down
        viewportTileOffset = (int(game.instance.viewport[0] / TILE_SIZE), int(game.instance.viewport[1] / TILE_SIZE))

        for layer in self.backgroundLayers:
            self.render_layer(display, game.instance.viewport, game.instance.viewportSize, viewportTileOffset, layer)

        self.render_layer(display, (0, 0), game.instance.viewportSize, viewportTileOffset, self.foregroundLayer)

    def render_layer(self, display: pygame.Surface, viewport, viewportSize, viewportTileOffset, layer):
        for y in range(min(self.viewportSizeTiles[1], self.height - viewportTileOffset[1])): # y: 0 corresponds to the bottom of the level
            for x in range(min(self.viewportSizeTiles[0], self.width - viewportTileOffset[0])): # Ensure we are within both tilemap and screen bounds
                tileValue = layer[self.height - y - 1 - viewportTileOffset[1]][x + viewportTileOffset[0]]

                if tileValue > 0:
                    display.blit(self.tilemap, (-(viewport[0] % TILE_SIZE) + x * TILE_SIZE, viewportSize[1] - (viewport[1] + (y + 1) * TILE_SIZE)), ((tileValue - 1) * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE))
