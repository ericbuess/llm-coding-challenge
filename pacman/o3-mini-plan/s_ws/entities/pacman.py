"""
Pacman player class implementation.
"""
import pygame
from entities.base import BaseEntity
from settings import PACMAN_SPEED
from utils import can_move_in_direction

class Pacman(BaseEntity):
    def __init__(self, x: int, y: int):
        """Initialize Pacman."""
        super().__init__(x, y, "pacman.png")
        self.speed = PACMAN_SPEED
        self.next_direction = pygame.Vector2(0, 0)
        self.angle = 0  # For rotation
        self.animation_frame = 0
        self.animation_speed = 0.2
        
    def update(self, wall_group: pygame.sprite.Group) -> None:
        """Update Pacman's position and animation."""
        # Try to change direction if requested
        if self.next_direction != pygame.Vector2(0, 0):
            if can_move_in_direction(self, self.next_direction, wall_group):
                self.direction = self.next_direction
                self.next_direction = pygame.Vector2(0, 0)
        
        # Move
        self.move(wall_group)
        
        # Update animation
        self.animate()
        
        # Update rotation based on direction
        self.update_rotation()
    
    def handle_input(self, key: int) -> None:
        """Handle keyboard input for movement."""
        if key == pygame.K_UP:
            self.next_direction = pygame.Vector2(0, -1)
        elif key == pygame.K_DOWN:
            self.next_direction = pygame.Vector2(0, 1)
        elif key == pygame.K_LEFT:
            self.next_direction = pygame.Vector2(-1, 0)
        elif key == pygame.K_RIGHT:
            self.next_direction = pygame.Vector2(1, 0)
    
    def animate(self) -> None:
        """Animate Pacman's mouth."""
        # This would be replaced with actual animation frames
        self.animation_frame = (self.animation_frame + self.animation_speed) % 4
    
    def update_rotation(self) -> None:
        """Update Pacman's rotation based on direction."""
        if self.direction.x > 0:
            self.angle = 0
        elif self.direction.x < 0:
            self.angle = 180
        elif self.direction.y > 0:
            self.angle = 90
        elif self.direction.y < 0:
            self.angle = 270
        
        # Rotate the image
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def reset_position(self, x: int, y: int) -> None:
        """Reset Pacman's position and direction."""
        self.set_position(x, y)
        self.direction = pygame.Vector2(0, 0)
        self.next_direction = pygame.Vector2(0, 0)
