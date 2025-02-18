import pygame
from pygame.math import Vector2
import random

class Ghost:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.position = Vector2(0, 0)  # Will be set by maze
        self.direction = Vector2(0, 0)
        self.speed = 130  # Slightly slower than Pac-Man
        self.mode = "SCATTER"  # SCATTER, CHASE, FRIGHTENED
        self.home_position = Vector2(0, 0)
        self.scatter_target = Vector2(0, 0)  # Will be set based on ghost type
        self.is_eaten = False
        self.frightened_timer = 0
        self.animation_frames = {}  # Will be loaded by renderer
        
    def update(self, dt, pacman, maze):
        """Update ghost position and state"""
        # Update frightened timer
        if self.mode == "FRIGHTENED" and self.frightened_timer > 0:
            self.frightened_timer -= dt
            if self.frightened_timer <= 0:
                self.mode = "CHASE"

        # If eaten, return to home
        if self.is_eaten:
            target = self.home_position
            if (self.position - self.home_position).length() < 2:
                self.respawn()
        else:
            target = self.get_target_tile(pacman)

        # Choose next direction at intersections
        if self.at_intersection(maze):
            self.choose_direction(target, maze)

        # Move in current direction
        next_pos = self.position + self.direction * self.speed * dt
        if not maze.is_wall(next_pos.x, next_pos.y):
            self.position = next_pos
            # Handle wrapping around the screen
            self.position = maze.wrap_position(self.position)

    def get_target_tile(self, pacman):
        """Get target tile based on ghost personality and mode"""
        if self.mode == "FRIGHTENED":
            # Random target when frightened
            return Vector2(
                random.randint(0, maze.width - 1),
                random.randint(0, maze.height - 1)
            )
        elif self.mode == "SCATTER":
            return self.scatter_target
        
        # CHASE mode - each ghost has unique targeting
        if self.name == "Blinky":  # Red ghost
            return Vector2(pacman.position)
        elif self.name == "Pinky":  # Pink ghost
            # Target 4 tiles ahead of Pac-Man
            return pacman.position + pacman.direction * 4
        elif self.name == "Inky":   # Cyan ghost
            # Complex targeting using Blinky's position (simplified for now)
            return Vector2(pacman.position)
        else:  # Clyde (Orange ghost)
            # If far from Pac-Man, chase; if close, scatter
            dist = (self.position - pacman.position).length()
            return pacman.position if dist > 8 else self.scatter_target

    def choose_direction(self, target, maze):
        """Choose next direction at intersection"""
        possible_directions = [
            Vector2(0, -1),  # Up
            Vector2(0, 1),   # Down
            Vector2(-1, 0),  # Left
            Vector2(1, 0)    # Right
        ]
        
        # Remove current opposite direction (ghosts can't reverse)
        if self.direction != Vector2(0, 0):
            opposite = -self.direction
            if opposite in possible_directions:
                possible_directions.remove(opposite)

        # Remove directions that lead to walls
        valid_directions = [
            d for d in possible_directions
            if not maze.is_wall(self.position.x + d.x, self.position.y + d.y)
        ]

        if not valid_directions:
            return  # No valid moves, stay in place

        if self.mode == "FRIGHTENED":
            # Random movement when frightened
            self.direction = random.choice(valid_directions)
        else:
            # Choose direction that gets closest to target
            self.direction = min(
                valid_directions,
                key=lambda d: (self.position + d - target).length_squared()
            )

    def at_intersection(self, maze):
        """Check if ghost is at a maze intersection"""
        # Check if we're at a tile center (within small epsilon)
        pos = Vector2(round(self.position.x), round(self.position.y))
        if (pos - self.position).length_squared() > 0.1:
            return False

        # Count valid directions
        valid_directions = 0
        for d in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            if not maze.is_wall(pos.x + d[0], pos.y + d[1]):
                valid_directions += 1

        # It's an intersection if there are more than 2 valid directions
        return valid_directions > 2

    def set_mode(self, mode):
        """Change ghost mode (CHASE, SCATTER, FRIGHTENED)"""
        if mode == "FRIGHTENED":
            self.mode = mode
            self.frightened_timer = 7.0  # 7 seconds of frightened mode
            self.speed = 75  # Slower when frightened
            # Reverse direction immediately when frightened
            self.direction = -self.direction
        else:
            self.mode = mode
            self.speed = 130  # Normal speed

    def respawn(self):
        """Reset ghost after being eaten"""
        self.is_eaten = False
        self.mode = "SCATTER"
        self.speed = 130
        self.position = Vector2(self.home_position)

    def reset(self):
        """Reset ghost to initial state"""
        self.position = Vector2(self.home_position)
        self.direction = Vector2(0, 0)
        self.mode = "SCATTER"
        self.is_eaten = False
        self.frightened_timer = 0
        self.speed = 130
