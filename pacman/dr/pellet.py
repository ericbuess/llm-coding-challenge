import pygame
from settings import WHITE

# Pellet class for the small dots that increase score.
class Pellet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 4), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (2, 2), 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.points = 10

# PowerPellet class (larger dot) that makes ghosts vulnerable.
class PowerPellet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (4, 4), 4)
        self.rect = self.image.get_rect(center=(x, y))
        self.points = 50
