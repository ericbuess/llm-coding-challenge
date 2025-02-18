"""Player (Pac-Man) class implementation."""
import arcade
from constants import (
    Direction, DIRECTION_VECTORS, PLAYER_SPEED,
    INITIAL_LIVES, TILE_SIZE
)
from utils.asset_manager import asset_manager

class PacMan(arcade.Sprite):
    def __init__(self):
        super().__init__(
            scale=1.0
        )
        # Load textures for different directions and animation frames
        self.textures = {
            Direction.RIGHT: [
                asset_manager.get_texture("pacman_right_1.png"),
                asset_manager.get_texture("pacman_right_2.png")
            ],
            Direction.LEFT: [
                asset_manager.get_texture("pacman_left_1.png"),
                asset_manager.get_texture("pacman_left_2.png")
            ],
            Direction.UP: [
                asset_manager.get_texture("pacman_up_1.png"),
                asset_manager.get_texture("pacman_up_2.png")
            ],
            Direction.DOWN: [
                asset_manager.get_texture("pacman_down_1.png"),
                asset_manager.get_texture("pacman_down_2.png")
            ]
        }
        
        # Set initial texture
        self.texture = self.textures[Direction.RIGHT][0]
        
        # Game state
        self.lives = INITIAL_LIVES
        self.score = 0
        self.current_direction = Direction.NONE
        self.intended_direction = Direction.NONE
        self.speed = PLAYER_SPEED
        
        # Animation state
        self.animation_frame = 0
        self.animation_time = 0
        self.ANIMATION_SPEED = 0.1  # seconds per frame
        
    def update_animation(self, delta_time: float):
        """Update the animation frame."""
        if self.current_direction == Direction.NONE:
            return
            
        self.animation_time += delta_time
        if self.animation_time >= self.ANIMATION_SPEED:
            self.animation_time = 0
            self.animation_frame = (self.animation_frame + 1) % 2
            self.texture = self.textures[self.current_direction][self.animation_frame]
    
    def is_grid_aligned(self) -> bool:
        """Check if Pac-Man is aligned with the tile grid."""
        return (
            self.center_x % TILE_SIZE < 2 and
            self.center_y % TILE_SIZE < 2
        )
    
    def can_move(self, direction: Direction, walls_layer) -> bool:
        """Check if Pac-Man can move in the given direction."""
        if direction == Direction.NONE:
            return False
            
        # Get the direction vector
        dx, dy = DIRECTION_VECTORS[direction]
        
        # Calculate the position after moving one tile
        next_x = self.center_x + dx * TILE_SIZE
        next_y = self.center_y + dy * TILE_SIZE
        
        # Create a temporary sprite to check collision
        temp_sprite = arcade.Sprite(
            center_x=next_x,
            center_y=next_y,
            width=self.width,
            height=self.height
        )
        
        # Check for collision with walls
        wall_hit = arcade.check_for_collision_with_list(temp_sprite, walls_layer)
        return not bool(wall_hit)
    
    def update(self, delta_time: float, walls_layer):
        """Update Pac-Man's position and state."""
        # Update animation
        self.update_animation(delta_time)
        
        # Check if we can change direction
        if self.is_grid_aligned() and self.intended_direction != Direction.NONE:
            if self.can_move(self.intended_direction, walls_layer):
                self.current_direction = self.intended_direction
                self.intended_direction = Direction.NONE
        
        # Move in current direction
        if self.current_direction != Direction.NONE:
            dx, dy = DIRECTION_VECTORS[self.current_direction]
            new_x = self.center_x + dx * self.speed * delta_time
            new_y = self.center_y + dy * self.speed * delta_time
            
            # Create a temporary sprite to check collision
            temp_sprite = arcade.Sprite(
                center_x=new_x,
                center_y=new_y,
                width=self.width,
                height=self.height
            )
            
            # Only update position if we won't hit a wall
            if not arcade.check_for_collision_with_list(temp_sprite, walls_layer):
                self.center_x = new_x
                self.center_y = new_y
    
    def set_intended_direction(self, direction: Direction):
        """Set the intended direction for Pac-Man to move."""
        self.intended_direction = direction
    
    def reset_position(self, x: float, y: float):
        """Reset Pac-Man to starting position."""
        super().__init__(
            scale=1.0,
            center_x=x,
            center_y=y
        )
        self.current_direction = Direction.NONE
        self.intended_direction = Direction.NONE
