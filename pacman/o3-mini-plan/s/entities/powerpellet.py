import pygame
from .base import BaseEntity
from settings import TILE_SIZE, WHITE

class PowerPellet(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        # Create a transparent surface
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        
        # Draw a larger white dot in the center
        pellet_size = 8
        center_x = TILE_SIZE // 2
        center_y = TILE_SIZE // 2
        pygame.draw.circle(self.image, WHITE, (center_x, center_y), pellet_size)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # Points awarded when collected
        self.points = 50
        
        # Animation variables
        self.animation_timer = 0
        self.visible = True
    
    def update(self):
        """Make the power pellet flash."""
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > 200:  # Flash every 200ms
            self.visible = not self.visible
            self.animation_timer = current_time
            
            if self.visible:
                self.image.set_alpha(255)
            else:
                self.image.set_alpha(100) 