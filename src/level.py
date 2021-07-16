import typing
import pygame
import json

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
            if layer["name"] == "background":
                self.width = layer["width"]
                self.height = layer["height"]
                data: list[int] = layer["data"]

                for y in range(self.height):
                    self.backgroundLayer.append([])
                    for x in range(self.width):
                        self.backgroundLayer[y].append(int(data[self.width * y + x] - 1))

    def render(self, display: pygame.Surface):
        import game
        from game import Game

        viewportTileOffset = (int(Game.viewport[0] / game.TILE_SIZE), int(Game.viewport[1] / game.TILE_SIZE))

        for y in range(min(Game.viewportSizeTiles[1], self.height - viewportTileOffset[1])): # y: 0 corresponds to the bottom of the level
            for x in range(min(Game.viewportSizeTiles[0], self.height - viewportTileOffset[0])): # Ensure we are within both tilemap and screen bounds
                tileValue = self.backgroundLayer[self.height - y - 1 - viewportTileOffset[1]][x - viewportTileOffset[0]]
                display.blit(self.tilemap, (Game.viewport[0] + x * game.TILE_SIZE, Game.viewportSize[1] - (Game.viewport[1] + y * game.TILE_SIZE)), (tileValue * game.TILE_SIZE, 0, game.TILE_SIZE, game.TILE_SIZE))
