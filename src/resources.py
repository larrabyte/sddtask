import json
import os

import pygame.image
import pygame.font
import pygame

class Resources:
    def __init__(self) -> None:
        """Initialises an instance of the Resource Manager."""
        self.data = {}
        self.fonts = {}

    def fetch_level_data(self, name: str) -> dict:
        """Returns the JSON data for a level, specified by `name` (read from disk)."""
        filepath = os.path.join("levels", f"{name}.json")

        with open(filepath, "r") as file:
            return json.load(file)

    def get_image(self, name: str) -> pygame.Surface:
        """Returns a surface, identified by `name`. Caches if required."""
        if (resource := self.data.get(name, None)) is not None:
            return resource

        try: # PyGame on Apple Silicon doesn't support non-BMP images.
            normal = os.path.join("images", f"{name}.png")
            surface = pygame.image.load(normal).convert_alpha()
        except pygame.error:
            fallback = os.path.join("images", f"{name}.bmp")
            surface = pygame.image.load(fallback).convert_alpha()

        self.data[name] = surface
        return surface

    def get_font(self, name: str) -> pygame.font.Font:
        """Returns a font, identified by `name`. Caches if required."""
        if (resource := self.fonts.get(name, None)) is not None:
            return resource

        path = os.path.join("fonts", f"{name}.ttf")
        font = pygame.font.Font(path, 24)

        self.fonts[name] = font
        return font
