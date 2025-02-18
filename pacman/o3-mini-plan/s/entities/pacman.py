import pygame
from .base import BaseEntity
from settings import TILE_SIZE, PACMAN_SPEED, YELLOW
from utils import get_direction_vector, is_grid_aligned

class Pacman(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        # Create base yellow circle for Pacman
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.original_image = self.image.copy()
        pygame.draw.circle(self.image, YELLOW, (TILE_SIZE // 2, TILE_SIZE // 2), TILE_SIZE // 2 - 2)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # Movement attributes
        self.speed = PACMAN_SPEED
        self.direction = pygame.Vector2(0, 0)
        self.next_direction = pygame.Vector2(0, 0)
        self.stored_direction = None
        
        # Animation attributes
        self.angle = 0
        self.mouth_angle = 0
        self.mouth_speed = 5
        self.mouth_opening = True
        
    def update(self):
        """Update Pacman's position and animation."""
        # Handle movement
        self.move()
        
        # Update animation
        self.animate()
        
    def move(self):
        """Handle Pacman's movement and direction changes."""
        # If we're at a grid intersection, try to change direction
        if is_grid_aligned(self.rect) and self.stored_direction is not None:
            # Try to move in the stored direction
            if self.can_move(self.stored_direction, self.groups()[0].game.wall_group):
                self.direction = self.stored_direction
                self.stored_direction = None
            
        # Move in current direction if possible
        if self.can_move(self.direction, self.groups()[0].game.wall_group):
            self.rect.x += self.direction.x * self.speed
            self.rect.y += self.direction.y * self.speed
        
        # Update grid position
        if is_grid_aligned(self.rect):
            self.grid_pos = (self.rect.x // TILE_SIZE, self.rect.y // TILE_SIZE)
            
    def animate(self):
        """Handle Pacman's mouth animation and rotation."""
        # Update mouth animation
        if self.mouth_opening:
            self.mouth_angle += self.mouth_speed
            if self.mouth_angle >= 45:
                self.mouth_opening = False
        else:
            self.mouth_angle -= self.mouth_speed
            if self.mouth_angle <= 0:
                self.mouth_opening = True
                
        # Calculate rotation angle based on direction
        if self.direction.x > 0:
            self.angle = 0
        elif self.direction.x < 0:
            self.angle = 180
        elif self.direction.y > 0:
            self.angle = 90
        elif self.direction.y < 0:
            self.angle = 270
            
        # Create new image for this frame
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        
        # Draw Pacman with current mouth angle
        center = (TILE_SIZE // 2, TILE_SIZE // 2)
        radius = TILE_SIZE // 2 - 2
        
        # Draw the main circle
        pygame.draw.circle(self.image, YELLOW, center, radius)
        
        # Draw the mouth
        if self.direction != pygame.Vector2(0, 0):  # Only show mouth when moving
            # Calculate mouth points
            start_angle = self.angle - self.mouth_angle
            end_angle = self.angle + self.mouth_angle
            
            # Create a polygon for the mouth
            points = [center]
            points.append((
                center[0] + radius * pygame.math.cos(pygame.math.radians(start_angle)),
                center[1] - radius * pygame.math.sin(pygame.math.radians(start_angle))
            ))
            points.append((
                center[0] + radius * pygame.math.cos(pygame.math.radians(end_angle)),
                center[1] - radius * pygame.math.sin(pygame.math.radians(end_angle))
            ))
            
            # Draw the mouth (black triangle)
            pygame.draw.polygon(self.image, (0, 0, 0), points)
    
    def handle_input(self, key):
        """Handle keyboard input for movement."""
        direction = None
        
        if key == pygame.K_UP:
            direction = pygame.Vector2(0, -1)
        elif key == pygame.K_DOWN:
            direction = pygame.Vector2(0, 1)
        elif key == pygame.K_LEFT:
            direction = pygame.Vector2(-1, 0)
        elif key == pygame.K_RIGHT:
            direction = pygame.Vector2(1, 0)
            
        if direction is not None:
            # If we're aligned with the grid, try to change direction immediately
            if is_grid_aligned(self.rect) and self.can_move(direction, self.groups()[0].game.wall_group):
                self.direction = direction
                self.stored_direction = None
            else:
                # Store the direction for the next grid alignment
                self.stored_direction = direction 