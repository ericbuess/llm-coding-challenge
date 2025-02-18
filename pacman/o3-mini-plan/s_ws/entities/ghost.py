"""
Ghost enemy class implementation.
"""
import pygame
import random
from entities.base import BaseEntity
from settings import GHOST_SPEED, FRIGHTENED_DURATION
from utils import get_valid_directions

class Ghost(BaseEntity):
    def __init__(self, x: int, y: int, color: str):
        """Initialize ghost with position and color."""
        super().__init__(x, y, f"ghost_{color}.png")
        self.speed = GHOST_SPEED
        self.state = "scatter"  # scatter, chase, frightened, eaten
        self.color = color
        self.home_position = (x, y)
        self.frightened_timer = 0
        self.target = pygame.Vector2(0, 0)
        
        # Load state-specific images
        self.normal_image = self.image
        try:
            self.frightened_image = pygame.image.load("assets/images/ghost_frightened.png").convert_alpha()
            self.eaten_image = pygame.image.load("assets/images/ghost_eaten.png").convert_alpha()
        except pygame.error:
            # Create default images if loading fails
            self.frightened_image = self.normal_image
            self.eaten_image = self.normal_image
    
    def update(self, wall_group: pygame.sprite.Group, pacman_pos: pygame.Vector2) -> None:
        """Update ghost behavior based on current state."""
        # Check if frightened mode should end
        if self.state == "frightened" and pygame.time.get_ticks() > self.frightened_timer:
            self.state = "chase"
            self.image = self.normal_image
        
        # Update target based on state
        if self.state == "chase":
            self.chase(pacman_pos)
        elif self.state == "scatter":
            self.scatter()
        elif self.state == "frightened":
            self.move_randomly(wall_group)
        elif self.state == "eaten":
            self.return_home()
        
        # Move ghost
        self.move(wall_group)
    
    def chase(self, pacman_pos: pygame.Vector2) -> None:
        """Chase mode: move toward Pacman."""
        self.target = pacman_pos
        self.choose_direction()
    
    def scatter(self) -> None:
        """Scatter mode: move toward home corner."""
        self.target = pygame.Vector2(self.get_scatter_target())
        self.choose_direction()
    
    def move_randomly(self, wall_group: pygame.sprite.Group) -> None:
        """Move randomly when frightened."""
        valid_directions = get_valid_directions(self, wall_group)
        if valid_directions and (self.direction == pygame.Vector2(0, 0) or 
                               random.random() < 0.02):  # Small chance to change direction
            self.direction = random.choice(valid_directions)
    
    def return_home(self) -> None:
        """Return to home position when eaten."""
        self.target = pygame.Vector2(self.home_position)
        self.choose_direction()
        
        # Check if reached home
        if (abs(self.rect.x - self.home_position[0]) < self.speed and
            abs(self.rect.y - self.home_position[1]) < self.speed):
            self.rect.topleft = self.home_position
            self.state = "scatter"
            self.image = self.normal_image
    
    def choose_direction(self) -> None:
        """Choose direction that minimizes distance to target."""
        valid_directions = get_valid_directions(self, self.game.wall_group)
        if not valid_directions:
            return
        
        # Find direction that minimizes distance to target
        best_direction = min(
            valid_directions,
            key=lambda d: pygame.Vector2(
                self.rect.x + d.x * TILE_SIZE,
                self.rect.y + d.y * TILE_SIZE
            ).distance_to(self.target)
        )
        self.direction = best_direction
    
    def enter_frightened_mode(self) -> None:
        """Enter frightened mode."""
        if self.state != "eaten":
            self.state = "frightened"
            self.image = self.frightened_image
            self.frightened_timer = pygame.time.get_ticks() + FRIGHTENED_DURATION
    
    def get_eaten(self) -> None:
        """Get eaten by Pacman."""
        self.state = "eaten"
        self.image = self.eaten_image
    
    def get_scatter_target(self) -> tuple[int, int]:
        """Get scatter mode target based on ghost color."""
        # Each ghost has a different corner to retreat to
        corners = {
            "red": (0, 0),  # Top-left
            "pink": (0, 29),  # Bottom-left
            "blue": (27, 0),  # Top-right
            "orange": (27, 29)  # Bottom-right
        }
        return corners.get(self.color, (0, 0))  # Default to top-left if color not found
