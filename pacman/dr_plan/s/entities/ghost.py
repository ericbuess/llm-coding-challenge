import pygame
import random
from enum import Enum
from .base import Entity

class GhostMode(Enum):
    CHASE = 1
    SCATTER = 2
    FRIGHTENED = 3
    EATEN = 4

class Ghost(Entity):
    def __init__(self, x: float, y: float, speed: float = 75.0, ghost_type: str = "blinky"):
        super().__init__(x, y, speed)
        self.ghost_type = ghost_type
        self.mode = GhostMode.SCATTER
        self.home_position = (x, y)
        self.scatter_target = self._get_scatter_target()
        self.is_eaten = False
        self.frightened_timer = 0
        self.frightened_duration = 7.0  # seconds
        self.normal_speed = speed
        self.frightened_speed = speed * 0.5

    def _get_scatter_target(self) -> tuple:
        """Return scatter target based on ghost type."""
        # Default scatter targets for each ghost type
        scatter_targets = {
            "blinky": (27, 0),   # Top-right
            "pinky": (0, 0),     # Top-left
            "inky": (27, 30),    # Bottom-right
            "clyde": (0, 30)     # Bottom-left
        }
        return scatter_targets.get(self.ghost_type, (0, 0))

    def get_target_tile(self, pacman, maze) -> tuple:
        """Determine target tile based on current mode and ghost type."""
        if self.mode == GhostMode.FRIGHTENED:
            # Random target when frightened
            return (random.randint(0, maze.width - 1),
                   random.randint(0, maze.height - 1))
        
        if self.mode == GhostMode.SCATTER:
            return self.scatter_target

        if self.mode == GhostMode.EATEN:
            return self.home_position

        # CHASE mode - each ghost has unique targeting
        pacman_pos = pacman.get_grid_position(maze.tile_size)
        pacman_dir = pacman.direction

        if self.ghost_type == "blinky":
            # Blinky directly targets Pac-Man
            return pacman_pos
        
        elif self.ghost_type == "pinky":
            # Pinky targets 4 tiles ahead of Pac-Man
            return (pacman_pos[0] + int(pacman_dir.x * 4),
                   pacman_pos[1] + int(pacman_dir.y * 4))
        
        elif self.ghost_type == "inky":
            # Inky uses both Pac-Man and Blinky's position
            target_x = pacman_pos[0] + int(pacman_dir.x * 2)
            target_y = pacman_pos[1] + int(pacman_dir.y * 2)
            return (target_x, target_y)
        
        elif self.ghost_type == "clyde":
            # Clyde targets Pac-Man directly if far, scatter if close
            dist_to_pacman = ((self.x - pacman.x) ** 2 + 
                            (self.y - pacman.y) ** 2) ** 0.5
            return pacman_pos if dist_to_pacman > 8 * maze.tile_size else self.scatter_target

        return pacman_pos  # Default to targeting Pac-Man directly

    def choose_direction(self, maze, target_tile) -> tuple:
        """Choose next direction based on available paths and target."""
        current_pos = self.get_grid_position(maze.tile_size)
        possible_directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        
        # Remove the opposite of current direction (ghosts can't reverse)
        if self.direction.length() > 0:
            opposite = (-int(self.direction.x), -int(self.direction.y))
            if opposite in possible_directions and self.mode != GhostMode.FRIGHTENED:
                possible_directions.remove(opposite)

        # Filter out directions that lead to walls
        valid_directions = []
        for direction in possible_directions:
            temp_rect = self.rect.copy()
            temp_rect.x += direction[0] * maze.tile_size / 2
            temp_rect.y += direction[1] * maze.tile_size / 2
            if not maze.check_wall_collision(temp_rect):
                valid_directions.append(direction)

        if not valid_directions:
            return (0, 0)

        if self.mode == GhostMode.FRIGHTENED:
            return random.choice(valid_directions)

        # Choose direction that minimizes distance to target
        best_direction = valid_directions[0]
        min_distance = float('inf')
        
        for direction in valid_directions:
            next_pos = (current_pos[0] + direction[0],
                       current_pos[1] + direction[1])
            distance = ((next_pos[0] - target_tile[0]) ** 2 +
                       (next_pos[1] - target_tile[1]) ** 2) ** 0.5
            
            if distance < min_distance:
                min_distance = distance
                best_direction = direction

        return best_direction

    def update(self, dt: float, maze, pacman) -> None:
        """Update ghost state and position."""
        # Update frightened timer
        if self.mode == GhostMode.FRIGHTENED:
            self.frightened_timer -= dt
            if self.frightened_timer <= 0:
                self.set_mode(GhostMode.CHASE)

        # Update speed based on mode
        self.speed = (self.frightened_speed if self.mode == GhostMode.FRIGHTENED 
                     else self.normal_speed)

        # Choose new direction if at center of tile
        if self.is_centered_on_tile(maze.tile_size):
            target = self.get_target_tile(pacman, maze)
            new_direction = self.choose_direction(maze, target)
            self.set_direction(new_direction)

        # Move in current direction
        self.move(dt, maze)
        self.update_animation(dt)

    def set_mode(self, mode: GhostMode) -> None:
        """Change ghost mode and handle related state changes."""
        self.mode = mode
        if mode == GhostMode.FRIGHTENED:
            self.frightened_timer = self.frightened_duration
        elif mode == GhostMode.EATEN:
            self.is_eaten = True

    def reset(self) -> None:
        """Reset ghost to initial state."""
        super().reset()
        self.x, self.y = self.home_position
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.mode = GhostMode.SCATTER
        self.is_eaten = False
        self.frightened_timer = 0
        self.speed = self.normal_speed 