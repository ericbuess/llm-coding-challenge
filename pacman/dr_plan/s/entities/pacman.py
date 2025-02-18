import pygame
from .base import Entity

class PacMan(Entity):
    def __init__(self, x: float, y: float, speed: float = 100.0):
        super().__init__(x, y, speed)
        self.lives = 3
        self.spawn_position = (x, y)
        self.alive = True
        self.score = 0
        # Direction mappings for input handling
        self.direction_map = {
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0)
        }

    def handle_input(self, key: int) -> None:
        """Handle keyboard input for movement."""
        if key in self.direction_map:
            self.set_next_direction(self.direction_map[key])

    def update(self, dt: float, maze) -> None:
        """Update Pac-Man's position and state."""
        if not self.alive:
            return

        # Try to turn if we have a queued direction
        if self.next_direction.length() > 0 and self.is_centered_on_tile(maze.tile_size):
            # Check if we can move in the next direction
            temp_rect = self.rect.copy()
            temp_rect.x += self.next_direction.x * maze.tile_size / 2
            temp_rect.y += self.next_direction.y * maze.tile_size / 2
            
            if not maze.check_wall_collision(temp_rect):
                self.direction = self.next_direction
                self.next_direction = pygame.math.Vector2(0, 0)

        # Move in current direction
        self.move(dt, maze)
        self.update_animation(dt)

    def die(self) -> None:
        """Handle Pac-Man's death."""
        self.alive = False
        self.lives -= 1

    def reset(self) -> None:
        """Reset Pac-Man to starting position."""
        self.x, self.y = self.spawn_position
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.direction = pygame.math.Vector2(0, 0)
        self.next_direction = pygame.math.Vector2(0, 0)
        self.alive = True

    def eat_pellet(self, points: int) -> None:
        """Handle pellet consumption."""
        self.score += points 