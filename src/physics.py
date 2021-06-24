import pygame.math

class PhysicsBody:
    def __init__(self, mass: float, gravity: bool) -> None:
        self.pos = pygame.math.Vector2(0.0, 0.0)
        self.vel = pygame.math.Vector2(0.0, 0.0)
        self.accel = pygame.math.Vector2(0.0, 0.0)
        self.gravity = gravity
        self.mass = mass

    def intersecting(self, other: "PhysicsBody") -> bool:
        pass
