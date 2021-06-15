import pygame
import os

images = dict()

def get_image(name: str) -> pygame.Surface:
    """Returns an image from the resource manager."""
    try:
        return images[str]
    except KeyError:
        surface = pygame.image.load(os.path.join("images", name + ".png"))

        images[str] = surface
        return surface
