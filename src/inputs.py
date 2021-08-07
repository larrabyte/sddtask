import typing as t

import pygame.mouse
import pygame.key
import pygame

class Keyboard:
    def pressed(self, key: int) -> bool:
        """Returns whether `key` was pressed."""
        keys = pygame.key.get_pressed()
        return keys[key]

class Mouse:
    def position(self) -> t.Tuple[int, int]:
        """Returns the screen coordinates of the mouse."""
        return pygame.mouse.get_pos()

    def pressed(self, key: int) -> bool:
        """Returns whether `key` was pressed."""
        buttons = pygame.mouse.get_pressed(5)
        return buttons[key - 1]
