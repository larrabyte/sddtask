import typing as t

import pygame.mouse
import pygame.key
import pygame

class Keyboard:
    def pressed(self, key: int) -> bool:
        keys = pygame.key.get_pressed()
        return keys[key]

class Mouse:
    def position(self) -> t.Tuple[int, int]:
        return pygame.mouse.get_pos()
