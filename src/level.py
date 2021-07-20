import typing
import pygame
import json

from game import TILE_SIZE

class Level:
    backgroundLayer = [[]]
    foregroundLayer = [[]]
    width = 0
    height = 0

    tilemap: pygame.Surface

    def __init__(self, name: str):
        from resources import ResourceManager
        data = ResourceManager.get_leveldata(name)
        self.tilemap = ResourceManager.get_image("tilemap")

        layers = data["layers"]
        for layer in layers:
            currentLayer = None
            if layer["name"] == "background":
                currentLayer = self.backgroundLayer
            elif layer["name"] == "foreground":
                currentLayer = self.foregroundLayer

            self.width = layer["width"]
            self.height = layer["height"]
            data: list[int] = layer["data"]

            for y in range(self.height):
                currentLayer.append([])
                for x in range(self.width):
                    currentLayer[y].append(int(data[self.width * y + x]))

    """Get foregroudn tile at position x and y (in world units)"""
    def getTileAt(self, x: int, y: int) -> int:
        tileX = int(x / TILE_SIZE)
        tileY = int(y / TILE_SIZE)
        
        if tileX >= self.width or tileY >= self.height or tileX < 0 or tileY < 0:
            return 0

        return self.foregroundLayer[self.height - tileY - 1][tileX]

    """
    Box collision check. (in world units).
    It is assumed that the size of the box does not exceed 1x2 tiles

    Returns boolean of collision
    """
    def collisionCheck(self, x1: int, x2: int, y1: int, y2: int) -> typing.Tuple[bool, bool, bool, bool]:
        left: int = self.getTileAt(x1, y1) + self.getTileAt(x1, y2) + self.getTileAt(x1, (y1 + y2) / 2)
        right: int = self.getTileAt(x2, y1) + self.getTileAt(x2, y2) + self.getTileAt(x2, (y1 + y2) / 2)
        top: int = self.getTileAt(x1, y1) + self.getTileAt(x2, y1)
        bottom: int = self.getTileAt(x1, y2) + self.getTileAt(x2, y2)

        print(f"l {left} r {right} t {top} b {bottom}")

        return [left > 0, right > 0, top > 0, bottom > 0]

    def render(self, display: pygame.Surface):
        from game import Game

        # Viewport offset as a number of tiles,
        # Convert to int to round down
        viewportTileOffset = (int(Game.viewport[0] / TILE_SIZE), int(Game.viewport[1] / TILE_SIZE))

        self.renderLayer(display, viewportTileOffset, self.backgroundLayer)
        self.renderLayer(display, viewportTileOffset, self.foregroundLayer)

    def renderLayer(self, display: pygame.Surface, viewportTileOffset, layer):
        from game import Game

        for y in range(min(Game.viewportSizeTiles[1], self.height - viewportTileOffset[1])): # y: 0 corresponds to the bottom of the level
            for x in range(min(Game.viewportSizeTiles[0], self.width - viewportTileOffset[0])): # Ensure we are within both tilemap and screen bounds
                tileValue = layer[self.height - y - 1 - viewportTileOffset[1]][x + viewportTileOffset[0]]

                if tileValue > 0:
                    display.blit(self.tilemap, (-(Game.viewport[0] % TILE_SIZE) + x * TILE_SIZE, Game.viewportSize[1] - (Game.viewport[1] + (y + 1) * TILE_SIZE)), ((tileValue - 1) * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE))
