import pygame
from .base import BaseEntity
from settings import TILE_SIZE, WHITE

class Pellet(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        # Create a transparent surface
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        
        # Draw a small white dot in the center
        pellet_size = 4
        center_x = TILE_SIZE // 2
        center_y = TILE_SIZE // 2
        pygame.draw.circle(self.image, WHITE, (center_x, center_y), pellet_size)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # Points awarded when collected
        self.points = 10 