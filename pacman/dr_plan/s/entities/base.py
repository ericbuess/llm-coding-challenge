import pygame
from typing import Tuple, Optional

class Entity:
    def __init__(self, x: float, y: float, speed: float, size: int = 20):
        self.x = float(x)
        self.y = float(y)
        self.speed = speed
        self.size = size
        self.direction = pygame.math.Vector2(0, 0)
        self.next_direction = pygame.math.Vector2(0, 0)
        self.rect = pygame.Rect(x, y, size, size)
        self.sprite = None
        self.animation_frames = []
        self.current_frame_index = 0
        self.animation_speed = 0.2
        self.animation_timer = 0

    def move(self, dt: float, maze) -> None:
        """Move the entity based on its current direction and speed."""
        # Calculate new position
        new_x = self.x + self.direction.x * self.speed * dt
        new_y = self.y + self.direction.y * self.speed * dt

        # Check if new position is valid (not in a wall)
        temp_rect = self.rect.copy()
        temp_rect.x = new_x
        temp_rect.y = new_y

        if not maze.check_wall_collision(temp_rect):
            self.x = new_x
            self.y = new_y
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)

    def set_direction(self, direction: Tuple[int, int]) -> None:
        """Set the entity's movement direction."""
        self.direction = pygame.math.Vector2(direction)

    def set_next_direction(self, direction: Tuple[int, int]) -> None:
        """Set the next intended direction (for Pac-Man turns)."""
        self.next_direction = pygame.math.Vector2(direction)

    def update_animation(self, dt: float) -> None:
        """Update the entity's animation frame."""
        if not self.animation_frames:
            return

        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame_index = (self.current_frame_index + 1) % len(self.animation_frames)
            self.sprite = self.animation_frames[self.current_frame_index]

    def get_grid_position(self, tile_size: int) -> Tuple[int, int]:
        """Get the entity's position in grid coordinates."""
        return (int(self.x / tile_size), int(self.y / tile_size))

    def is_centered_on_tile(self, tile_size: int) -> bool:
        """Check if the entity is centered on a tile (for turning)."""
        return (self.x % tile_size < self.speed and 
                self.y % tile_size < self.speed) 