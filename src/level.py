import typing as t
import constants
import game

import pygame.math
import pygame.draw
import pygame

class Level:
    def __init__(self, game: "game.Game", name: str) -> None:
        """Creates an instance of a `Level` object."""
        data = game.resources.fetch_level_data(name)

        # Convert screen resolution into tile resolution.
        x, y = game.display.get_size()
        x = int((x + constants.TILE_SIZE - 1) / constants.TILE_SIZE)
        y = int((y + constants.TILE_SIZE - 1) / constants.TILE_SIZE)

        self.resolution = pygame.math.Vector2(x, y)
        self.tilemap = game.resources.get_image("tilemap")
        self.tileSize = data["height"]
        self.display = game.display
        self.layers = {}

        for layer in data["layers"]:
            key = layer["name"]
            value = Layer(layer)
            self.layers[key] = value

    def get_screen_position(self, layer: str, x: int, y: int) -> t.Tuple[float, float]:
        """Converts tile coordinates into screen coordinates (top-left of a tile)."""
        layerObject = self.layers[layer]
        return layerObject.get_screen_position(self.display, x, y)

    def get_tile_position(self, layer: str, x: float, y: float) -> t.Tuple[int, int]:
        """Converts screen coordinates into the nearest corresponding tile."""
        layerObject = self.layers[layer]
        return layerObject.get_tile_position(self.display, x, y)

    def get_tile(self, layer: str, x: float, y: float) -> t.Tuple[int, int, int]:
        """Returns the tile at screen coordinates (x, y) for a specified layer."""
        layerObject = self.layers[layer]
        return layerObject.get_tile(self.display, x, y)

    def render(self, display: pygame.Surface) -> None:
        """Renders all tiles to the screen."""
        for layer in self.layers.values():
            layer.render(self.tilemap, display)

class Layer:
    def __init__(self, data: dict) -> None:
        """Creates an instance of a `Layer` object."""
        self.width = data["width"]
        self.height = data["height"]
        self.tiles = data["data"]
        self.type = data["type"]
        self.visible = data["visible"]
        self.x = data["x"]
        self.y = data["y"]

    def calculate_offset(self, y: int) -> int:
        """Returns the offset required to align the bottom-left of the tilemap and display."""
        # Basically, both the tilemap and display start from the top left at (0, 0).
        # However the tilemap extends well past the display vertically, so we have
        # to compensate by adding a vertical offset to the tilemap. This offset is calculated
        # such that the bottom of the tilemape ends up corresponding to the bottom of the display.
        return (self.height * constants.TILE_SIZE) - y

    def get_screen_position(self, display: pygame.Surface, x: int, y: int) -> t.Tuple[float, float]:
        """Converts tile coordinates into screen coordinates (top-left of a tile)."""
        displayX, displayY = display.get_size()
        verticalOffset = self.calculate_offset(displayY)

        screenX = float(x * constants.TILE_SIZE)
        screenY = float((y * constants.TILE_SIZE) - verticalOffset)
        return (screenX, screenY)

    def get_tile_position(self, display: pygame.Surface, x: float, y: float) -> t.Tuple[int, int]:
        """Converts screen coordinates into the nearest corresponding tile."""
        displayX, displayY = display.get_size()
        verticalOffset = self.calculate_offset(displayY)

        tileX = int(x / constants.TILE_SIZE)
        tileY = int((y + verticalOffset) / constants.TILE_SIZE)
        return (tileX, tileY)

    def get_tile(self, display: pygame.Surface, x: float, y: float) -> int:
        """Returns the tile at screen coordinates (x, y) on this layer."""
        tileX, tileY = self.get_tile_position(display, x, y)
        index = self.width * tileY + tileX

        if index < len(self.tiles):
            return self.tiles[self.width * tileY + tileX]

        return 0

    def render(self, tilemap: pygame.Surface, display: pygame.Surface) -> None:
        """Renders this layer's tiles to the screen."""
        displayX, displayY = display.get_size()
        verticalOffset = self.calculate_offset(displayY)
        tileX, tileY = (0, -verticalOffset)

        for tile in self.tiles:
            # Only render the tile if it is physically present and is within the bounds of the display.
            if tile > 0 and tileX < displayX and tileY < displayY:
                source = pygame.Rect((tile - 1) * constants.TILE_SIZE, 0, constants.TILE_SIZE, constants.TILE_SIZE)
                destination = pygame.Rect(tileX, tileY, constants.TILE_SIZE, constants.TILE_SIZE)
                display.blit(tilemap, destination, source)

            # Advance the tile coordinates each time we iterate.
            if (tileX := tileX + constants.TILE_SIZE) > ((self.width - 1) * constants.TILE_SIZE):
                tileY += constants.TILE_SIZE
                tileX = 0
