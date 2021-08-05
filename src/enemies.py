import pygame
import random
from entity import Entity
from player import Player
player = Player()

class Enemy(Entity):
    def __init__(self):
        super(Enemy, self). __init__()
        self.surf = pygame.surface((30, 10))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(
            center = (
                random.randint(150, 200),
                random.randint(0,150)
            )
        )
        self.speed = random.randint(7,15)

def update(self):
    self.rect.move_ip(-self.speed,0)

if pygame.sprite.spritecollideany(Player, Enemy):
    Player.kill()
    running = False

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

for entity in all_sprites:
    pygame.surface.blit(entity.surf, entity.rect)
