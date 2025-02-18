"""
Base class for all game entities.
"""
import pygame
import os
from settings import IMAGE_DIR

class BaseEntity(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image_name: str):
        """Initialize the base entity with position and image."""
        super().__init__()
        
        # Load image
        image_path = os.path.join(IMAGE_DIR, image_name)
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            # Create a default surface if image loading fails
            self.image = pygame.Surface((32, 32))
            self.image.fill((255, 0, 255))  # Magenta for visibility
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # Movement attributes
        self.direction = pygame.Vector2(0, 0)
        self.speed = 0
        
    def move(self, wall_group: pygame.sprite.Group) -> None:
        """Move the entity while checking for wall collisions."""
        # Move in x direction
        self.rect.x += int(self.direction.x * self.speed)
        # Check x collision
        if pygame.sprite.spritecollide(self, wall_group, False):
            if self.direction.x > 0:  # Moving right
                self.rect.right = min(wall.rect.left for wall in wall_group if wall.rect.colliderect(self.rect))
            else:  # Moving left
                self.rect.left = max(wall.rect.right for wall in wall_group if wall.rect.colliderect(self.rect))
        
        # Move in y direction
        self.rect.y += int(self.direction.y * self.speed)
        # Check y collision
        if pygame.sprite.spritecollide(self, wall_group, False):
            if self.direction.y > 0:  # Moving down
                self.rect.bottom = min(wall.rect.top for wall in wall_group if wall.rect.colliderect(self.rect))
            else:  # Moving up
                self.rect.top = max(wall.rect.bottom for wall in wall_group if wall.rect.colliderect(self.rect))
    
    def set_position(self, x: int, y: int) -> None:
        """Set the entity's position."""
        self.rect.topleft = (x, y)
