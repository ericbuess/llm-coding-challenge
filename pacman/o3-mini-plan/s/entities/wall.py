from .base import BaseEntity
import pygame
from settings import TILE_SIZE, BLUE

class Wall(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        # Create a blue rectangle for the wall
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(BLUE)
        
        # Add a slight 3D effect with a darker border
        pygame.draw.rect(self.image, (0, 0, 150), (0, 0, TILE_SIZE, TILE_SIZE), 2)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y) 