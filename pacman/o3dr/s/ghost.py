"""Ghost enemy class with AI behavior."""
import arcade
import random
from constants import Direction, GhostState, GHOST_SPEED, GHOST_FRIGHTENED_SPEED, TILE_SIZE

class Ghost(arcade.Sprite):
    def __init__(self, image_path: str = None, ghost_type: str = "blinky"):
        if image_path:
            super().__init__(
                filename=image_path,
                scale=1.0,
                hit_box_algorithm="Simple"
            )
        else:
            super().__init__(
                scale=1.0,
                hit_box_algorithm="Simple"
            )
            # Create a default colored square texture based on ghost type
            color = self._get_ghost_color(ghost_type)
            texture = arcade.make_soft_square_texture(
                TILE_SIZE, color, 255, 8
            )
            self.textures = [texture]
            self.texture = self.textures[0]
        
        self.ghost_type = ghost_type
        self.state = GhostState.SCATTER
        self.speed = GHOST_SPEED
        self.home_corner = self._get_home_corner()
        self.current_direction = Direction.NONE
        self.spawn_point = (0, 0)  # Will be set by game view
        
    def _get_ghost_color(self, ghost_type: str) -> tuple:
        """Get the color for this ghost type."""
        colors = {
            "blinky": arcade.color.RED,
            "pinky": arcade.color.PINK,
            "inky": arcade.color.CYAN,
            "clyde": arcade.color.ORANGE
        }
        return colors.get(ghost_type, arcade.color.RED)

    def _get_home_corner(self) -> tuple:
        """Get the home corner for this ghost type."""
        # These would be adjusted based on actual maze dimensions
        corners = {
            "blinky": (700, 500),  # Top-right
            "pinky": (100, 500),   # Top-left
            "inky": (700, 100),    # Bottom-right
            "clyde": (100, 100)    # Bottom-left
        }
        return corners.get(self.ghost_type, (700, 500))

    def update(self, delta_time: float, walls: arcade.SpriteList, pacman: arcade.Sprite):
        """Update ghost position and state."""
        # Update speed based on state
        self.speed = GHOST_FRIGHTENED_SPEED if self.state == GhostState.FRIGHTENED else GHOST_SPEED
        
        # Check if we're at a grid intersection
        if self._is_at_intersection():
            self._choose_direction(walls, pacman)
        
        # Move in current direction
        self.center_x += self.current_direction[0] * self.speed * delta_time
        self.center_y += self.current_direction[1] * self.speed * delta_time
        
        # If we hit a wall, choose a new direction
        if arcade.check_for_collision_with_list(self, walls):
            self.center_x -= self.current_direction[0] * self.speed * delta_time
            self.center_y -= self.current_direction[1] * self.speed * delta_time
            self._choose_direction(walls, pacman)

    def _is_at_intersection(self) -> bool:
        """Check if ghost is at a grid intersection."""
        return (self.center_x % TILE_SIZE < 2 and 
                self.center_y % TILE_SIZE < 2)

    def _choose_direction(self, walls: arcade.SpriteList, pacman: arcade.Sprite):
        """Choose a new direction based on current state and surroundings."""
        possible_directions = self._get_valid_directions(walls)
        
        if not possible_directions:
            return
        
        if self.state == GhostState.FRIGHTENED:
            # Choose random direction when frightened
            self.current_direction = random.choice(possible_directions)
        else:
            target = self._get_target_position(pacman)
            # Choose direction that gets us closest to target
            best_direction = min(
                possible_directions,
                key=lambda d: self._distance_to_target(
                    (self.center_x + d[0] * TILE_SIZE,
                     self.center_y + d[1] * TILE_SIZE),
                    target
                )
            )
            self.current_direction = best_direction

    def _get_valid_directions(self, walls: arcade.SpriteList) -> list:
        """Get list of valid directions from current position."""
        valid = []
        for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            # Don't allow reversing
            if (direction[0] == -self.current_direction[0] and 
                direction[1] == -self.current_direction[1]):
                continue
                
            # Check if direction is valid
            self.center_x += direction[0] * TILE_SIZE
            self.center_y += direction[1] * TILE_SIZE
            
            if not arcade.check_for_collision_with_list(self, walls):
                valid.append(direction)
                
            self.center_x -= direction[0] * TILE_SIZE
            self.center_y -= direction[1] * TILE_SIZE
            
        return valid

    def _get_target_position(self, pacman: arcade.Sprite) -> tuple:
        """Get target position based on ghost type and state."""
        if self.state == GhostState.SCATTER:
            return self.home_corner
            
        # Basic chase behavior - can be expanded for different ghost personalities
        if self.ghost_type == "blinky":
            return pacman.position
        elif self.ghost_type == "pinky":
            # Target 4 tiles ahead of Pacman
            return (pacman.center_x + pacman.current_direction[0] * 4 * TILE_SIZE,
                   pacman.center_y + pacman.current_direction[1] * 4 * TILE_SIZE)
        else:
            return pacman.position  # Default behavior

    def _distance_to_target(self, pos: tuple, target: tuple) -> float:
        """Calculate Manhattan distance to target."""
        return (abs(pos[0] - target[0]) + 
                abs(pos[1] - target[1]))

    def enter_frightened_mode(self):
        """Enter frightened state."""
        if self.state != GhostState.FRIGHTENED:
            self.state = GhostState.FRIGHTENED
            # Reverse direction
            self.current_direction = (
                -self.current_direction[0],
                -self.current_direction[1]
            )

    def exit_frightened_mode(self):
        """Exit frightened state."""
        self.state = GhostState.CHASE

    def reset_position(self):
        """Reset ghost to spawn point."""
        self.center_x, self.center_y = self.spawn_point
        self.current_direction = Direction.NONE
        self.state = GhostState.SCATTER 