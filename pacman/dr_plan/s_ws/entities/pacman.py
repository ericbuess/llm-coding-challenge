import pygame
from pygame.math import Vector2

class PacMan:
    def __init__(self):
        self.position = Vector2(0, 0)  # Will be set by maze
        self.spawn_position = Vector2(0, 0)
        self.direction = Vector2(0, 0)
        self.next_direction = Vector2(0, 0)
        self.speed = 150  # pixels per second
        self.alive = True
        self.current_frame_index = 0
        self.animation_frames = []  # Will be loaded by renderer
        
    def handle_input(self, key):
        """Handle keyboard input for movement"""
        if key == pygame.K_UP:
            self.next_direction = Vector2(0, -1)
        elif key == pygame.K_DOWN:
            self.next_direction = Vector2(0, 1)
        elif key == pygame.K_LEFT:
            self.next_direction = Vector2(-1, 0)
        elif key == pygame.K_RIGHT:
            self.next_direction = Vector2(1, 0)

    def update(self, dt, maze):
        """Update Pac-Man's position and state"""
        if not self.alive:
            return

        # Try to turn if there's a queued direction
        if self.next_direction != Vector2(0, 0):
            # Check if we can move in the next_direction
            next_pos = self.position + self.next_direction * self.speed * dt
            if not maze.is_wall(next_pos.x, next_pos.y):
                self.direction = self.next_direction
                self.next_direction = Vector2(0, 0)

        # Move in current direction
        if self.direction != Vector2(0, 0):
            next_pos = self.position + self.direction * self.speed * dt
            if not maze.is_wall(next_pos.x, next_pos.y):
                self.position = next_pos
                # Handle wrapping around the screen (if maze supports it)
                self.position = maze.wrap_position(self.position)
                
        # Update animation
        self.update_animation(dt)

    def update_animation(self, dt):
        """Update the animation frame"""
        # This will be implemented when we add sprites
        pass

    def die(self):
        """Handle Pac-Man's death"""
        self.alive = False
        # Death animation will be handled by renderer

    def reset(self):
        """Reset Pac-Man to initial state"""
        self.position = Vector2(self.spawn_position)
        self.direction = Vector2(0, 0)
        self.next_direction = Vector2(0, 0)
        self.alive = True
        self.current_frame_index = 0
