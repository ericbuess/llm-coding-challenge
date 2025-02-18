import pygame
from settings import TILE_SIZE
from utils import grid_to_pixel, is_grid_aligned

class BaseEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path=None):
        super().__init__()
        
        # Set up the sprite image
        if image_path:
            try:
                self.image = pygame.image.load(image_path).convert_alpha()
            except pygame.error:
                # Create a default surface if image loading fails
                self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
                self.image.fill((255, 0, 255))  # Magenta for missing textures
        else:
            # Create a default surface if no image path provided
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill((255, 0, 255))
            
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # Movement attributes
        self.direction = pygame.Vector2(0, 0)
        self.speed = 0
        self.grid_pos = (x // TILE_SIZE, y // TILE_SIZE)
    
    def update(self):
        """Base update method to be overridden by child classes."""
        # Update position based on direction and speed
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        
        # Update grid position if aligned
        if is_grid_aligned(self.rect):
            self.grid_pos = (self.rect.x // TILE_SIZE, self.rect.y // TILE_SIZE)
    
    def set_position(self, x, y):
        """Set the entity's position in pixels."""
        self.rect.topleft = (x, y)
        self.grid_pos = (x // TILE_SIZE, y // TILE_SIZE)
    
    def set_grid_position(self, col, row):
        """Set the entity's position using grid coordinates."""
        x, y = grid_to_pixel(col, row)
        self.set_position(x, y)
    
    def can_move(self, direction, wall_group):
        """Check if the entity can move in the given direction."""
        test_rect = self.rect.copy()
        test_rect.x += direction.x * TILE_SIZE
        test_rect.y += direction.y * TILE_SIZE
        
        # Check for collisions with walls
        for wall in wall_group:
            if test_rect.colliderect(wall.rect):
                return False
        return True 