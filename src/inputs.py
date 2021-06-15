import pygame.mouse
import pygame.key
import pygame

import typing as t

class Keyboard:
    @staticmethod
    def pressed(key: int) -> bool:
        keys = pygame.key.get_pressed()
        return keys[key]

class Mouse:
    @staticmethod
    def position() -> t.Tuple[int, int]:
        return pygame.mouse.get_pos()
