import pygame.image
import pygame

import json
import os

class ResourceManager:
    images = {}
    levels = {}

    @classmethod
    def get_image(cls, name: str) -> pygame.Surface:
        """Returns a surface from the internal store."""
        resource = cls.images.get(name, None)
        if resource is not None:
            return resource

        try: # PyGame on Apple Silicon doesn't support non-BMP images.
            normal = os.path.join("images", f"{name}.png")
            surface = pygame.image.load(normal)
        except pygame.error:
            fallback = os.path.join("images", f"{name}.bmp")
            surface = pygame.image.load(fallback)

        cls.images[name] = surface
        return surface

    # Returns JSON data for a level
    @classmethod
    def get_leveldata(cls, name: str) -> dict:
        file = open(os.path.join("levels", f"{name}.json"))
        return json.load(file)


    from level import Level
    # Returns game Level object
    @classmethod
    def get_level(cls, name: str) -> Level:
        from level import Level
        level = cls.levels.get(name, None)
        if level is not None:
            return level

        level = Level(name)
        cls.levels[name] = level

        return level
