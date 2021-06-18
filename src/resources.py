import pygame.image
import pygame

import os

class ResourceManager:
    images = {}

    @classmethod
    def get_image(cls, name: str) -> object:
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
