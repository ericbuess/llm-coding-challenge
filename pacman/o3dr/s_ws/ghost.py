"""Ghost class implementation with AI behavior."""
import arcade
import random
from typing import Tuple, List
from constants import (
    Direction, DIRECTION_VECTORS, GHOST_SPEED,
    GhostState, GHOST_FRIGHTENED_SPEED, TILE_SIZE
)
from utils.asset_manager import asset_manager

class Ghost(arcade.Sprite):
    def __init__(self, ghost_type: str):
        """Initialize a ghost with a specific type (e.g., 'blinky', 'pinky', etc.)."""
        super().__init__(scale=1.0)
        self.ghost_type = ghost_type
        
        # Load textures for different states
        self.normal_texture = asset_manager.get_texture(f"{ghost_type}.png")
        self.frightened_texture = asset_manager.get_texture("ghost_frightened.png")
        self.eaten_texture = asset_manager.get_texture("ghost_eaten.png")
        
        # Set initial texture
        self.texture = self.normal_texture
        
        # Movement and state
        self.speed = GHOST_SPEED
        self.state = GhostState.SCATTER
        self.current_direction = Direction.NONE
        self.home_corner = self._get_home_corner()
        
        # Starting position (will be set by game view)
        self.start_x = 0
        self.start_y = 0
        
    def _get_home_corner(self) -> Tuple[int, int]:
        """Get the home corner for this ghost type in scatter mode."""
        if self.ghost_type == "blinky":
            return (27, 31)  # Top-right
        elif self.ghost_type == "pinky":
            return (2, 31)   # Top-left
        elif self.ghost_type == "inky":
            return (27, 0)   # Bottom-right
        else:  # clyde
            return (2, 0)    # Bottom-left
    
    def get_valid_directions(self, walls_layer) -> List[Direction]:
        """Get list of valid directions from current position."""
        valid = []
        for direction in Direction:
            if direction == Direction.NONE:
                continue
                
            dx, dy = DIRECTION_VECTORS[direction]
            next_x = self.center_x + dx * TILE_SIZE
            next_y = self.center_y + dy * TILE_SIZE
            
            # Create temporary sprite to check collision
            temp_sprite = arcade.Sprite(
                center_x=next_x,
                center_y=next_y,
                width=self.width,
                height=self.height
            )
            
            if not arcade.check_for_collision_with_list(temp_sprite, walls_layer):
                valid.append(direction)
                
        return valid
    
    def choose_direction(self, walls_layer, pacman) -> Direction:
        """Choose a new direction based on current state and valid moves."""
        valid_directions = self.get_valid_directions(walls_layer)
        
        # Remove the opposite of current direction (no 180° turns)
        if self.current_direction != Direction.NONE:
            opposite = {
                Direction.UP: Direction.DOWN,
                Direction.DOWN: Direction.UP,
                Direction.LEFT: Direction.RIGHT,
                Direction.RIGHT: Direction.LEFT
            }
            if opposite[self.current_direction] in valid_directions:
                valid_directions.remove(opposite[self.current_direction])
        
        if not valid_directions:
            return Direction.NONE
            
        if self.state == GhostState.FRIGHTENED:
            # Choose random direction when frightened
            return random.choice(valid_directions)
        elif self.state == GhostState.EATEN:
            # Head back to ghost house
            return self._choose_direction_to_target(
                valid_directions,
                (self.start_x, self.start_y)
            )
        elif self.state == GhostState.SCATTER:
            # Head to home corner
            return self._choose_direction_to_target(
                valid_directions,
                self.home_corner
            )
        else:  # CHASE mode
            # Implement specific ghost behavior
            target = self._get_chase_target(pacman)
            return self._choose_direction_to_target(valid_directions, target)
    
    def _choose_direction_to_target(
        self,
        valid_directions: List[Direction],
        target: Tuple[float, float]
    ) -> Direction:
        """Choose the direction that gets closest to the target."""
        best_direction = valid_directions[0]
        best_distance = float('inf')
        
        for direction in valid_directions:
            dx, dy = DIRECTION_VECTORS[direction]
            next_x = self.center_x + dx * TILE_SIZE
            next_y = self.center_y + dy * TILE_SIZE
            
            # Calculate Manhattan distance to target
            distance = abs(next_x - target[0]) + abs(next_y - target[1])
            
            if distance < best_distance:
                best_distance = distance
                best_direction = direction
                
        return best_direction
    
    def _get_chase_target(self, pacman) -> Tuple[float, float]:
        """Get chase target based on ghost type."""
        if self.ghost_type == "blinky":
            # Directly target Pac-Man
            return (pacman.center_x, pacman.center_y)
        elif self.ghost_type == "pinky":
            # Target 4 tiles ahead of Pac-Man
            dx, dy = DIRECTION_VECTORS[pacman.current_direction]
            return (
                pacman.center_x + dx * TILE_SIZE * 4,
                pacman.center_y + dy * TILE_SIZE * 4
            )
        elif self.ghost_type == "inky":
            # Complex targeting based on Blinky's position
            # For now, just target 2 tiles ahead
            dx, dy = DIRECTION_VECTORS[pacman.current_direction]
            return (
                pacman.center_x + dx * TILE_SIZE * 2,
                pacman.center_y + dy * TILE_SIZE * 2
            )
        else:  # clyde
            # If far from Pac-Man, chase directly
            # If close, go to home corner
            distance = abs(self.center_x - pacman.center_x) + \
                      abs(self.center_y - pacman.center_y)
            if distance > TILE_SIZE * 8:
                return (pacman.center_x, pacman.center_y)
            else:
                return self.home_corner
    
    def update(self, delta_time: float, walls_layer, pacman):
        """Update ghost position and state."""
        # Update speed based on state
        if self.state == GhostState.FRIGHTENED:
            self.speed = GHOST_FRIGHTENED_SPEED
        else:
            self.speed = GHOST_SPEED
        
        # Update texture based on state
        if self.state == GhostState.FRIGHTENED:
            self.texture = self.frightened_texture
        elif self.state == GhostState.EATEN:
            self.texture = self.eaten_texture
        else:
            self.texture = self.normal_texture
        
        # Check if we need to choose a new direction
        if self.center_x % TILE_SIZE < 2 and self.center_y % TILE_SIZE < 2:
            self.current_direction = self.choose_direction(walls_layer, pacman)
        
        # Move in current direction
        if self.current_direction != Direction.NONE:
            dx, dy = DIRECTION_VECTORS[self.current_direction]
            self.center_x += dx * self.speed * delta_time
            self.center_y += dy * self.speed * delta_time
    
    def set_state(self, new_state: GhostState):
        """Set the ghost's state."""
        self.state = new_state
    
    def reset_position(self):
        """Reset ghost to starting position."""
        self.center_x = self.start_x
        self.center_y = self.start_y
        self.current_direction = Direction.NONE
        self.state = GhostState.SCATTER
