"""Pac-Man player class."""
import arcade
from constants import Direction, PLAYER_SPEED, TILE_SIZE

class Pacman(arcade.Sprite):
    def __init__(self, image_path: str = None):
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
            # Create a default yellow circle texture
            texture = arcade.make_soft_square_texture(
                TILE_SIZE, arcade.color.YELLOW, 255, 8
            )
            self.textures = [texture]
            self.texture = self.textures[0]
        
        # Game state
        self.lives = 3
        self.score = 0
        self.is_powered_up = False
        
        # Movement
        self.speed = PLAYER_SPEED
        self.current_direction = Direction.NONE
        self.intended_direction = Direction.NONE
        
        # Animation state (to be implemented)
        self.animation_frame = 0
        self.animation_time = 0

    def update(self, delta_time: float, maze) -> None:
        """Update the Pac-Man sprite position and state."""
        # If aligned on grid and can turn, update current direction
        if self.can_turn(self.intended_direction, maze):
            self.current_direction = self.intended_direction

        # Set the velocity for the physics engine
        self.change_x = self.current_direction[0] * self.speed
        self.change_y = self.current_direction[1] * self.speed

        # Update animation (to be implemented)
        self.update_animation(delta_time)

    def update_animation(self, delta_time: float):
        """Update the animation frame."""
        # To be implemented with sprite animations
        pass

    def set_intended_direction(self, direction: tuple):
        """Set the intended movement direction for Pac-Man."""
        self.intended_direction = direction

    def reset_position(self, x: float, y: float):
        """Reset Pac-Man to starting position."""
        self.center_x = x
        self.center_y = y
        self.current_direction = Direction.NONE
        self.intended_direction = Direction.NONE 