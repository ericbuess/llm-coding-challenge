import pygame
import random
from .base import BaseEntity
from settings import TILE_SIZE, GHOST_SPEED, RED, BLUE, PINK, ORANGE
from utils import is_grid_aligned, get_direction_vector

class Ghost(BaseEntity):
    def __init__(self, x, y, color='red'):
        super().__init__(x, y)
        
        # Set ghost color and create the base image
        self.color = color
        self.base_color = self._get_color_from_name(color)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self._draw_ghost(self.base_color)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # Movement attributes
        self.speed = GHOST_SPEED
        self.direction = pygame.Vector2(0, 0)
        self.home_position = (x, y)
        
        # State management
        self.state = 'scatter'  # possible states: scatter, chase, frightened, eaten
        self.state_timer = 0
        self.animation_timer = 0
        self.flash_timer = 0
        self.is_frightened_flashing = False
        
    def update(self):
        """Update ghost position and state."""
        current_time = pygame.time.get_ticks()
        
        # Update state timers and transitions
        self._update_state(current_time)
        
        # Move based on current state
        if is_grid_aligned(self.rect):
            self._choose_direction()
            
        # Move in current direction
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        
        # Update grid position
        if is_grid_aligned(self.rect):
            self.grid_pos = (self.rect.x // TILE_SIZE, self.rect.y // TILE_SIZE)
            
        # Update appearance based on state
        self._update_appearance(current_time)
        
    def _update_state(self, current_time):
        """Update ghost state and handle transitions."""
        if self.state == 'frightened' and current_time > self.state_timer:
            self.state = 'chase'
            self._draw_ghost(self.base_color)
        elif self.state == 'eaten' and self.rect.collidepoint(self.home_position):
            self.state = 'scatter'
            self._draw_ghost(self.base_color)
            
    def _choose_direction(self):
        """Choose next direction based on current state and position."""
        possible_directions = self._get_possible_directions()
        
        if not possible_directions:
            return
            
        if self.state == 'frightened':
            # Choose random direction when frightened
            self.direction = random.choice(possible_directions)
        elif self.state == 'eaten':
            # Head back to home position
            self.direction = self._get_direction_to_target(self.home_position, possible_directions)
        else:
            # Get target based on state (chase or scatter)
            target = self._get_target_position()
            self.direction = self._get_direction_to_target(target, possible_directions)
            
    def _get_possible_directions(self):
        """Get list of possible directions excluding walls and opposite direction."""
        directions = [
            pygame.Vector2(0, -1),  # up
            pygame.Vector2(0, 1),   # down
            pygame.Vector2(-1, 0),  # left
            pygame.Vector2(1, 0)    # right
        ]
        
        # Remove opposite direction unless eaten
        if self.state != 'eaten' and self.direction != pygame.Vector2(0, 0):
            opposite = -self.direction
            if opposite in directions:
                directions.remove(opposite)
                
        # Remove directions that would hit walls
        return [d for d in directions if self.can_move(d, self.groups()[0].game.wall_group)]
        
    def _get_target_position(self):
        """Get target position based on current state."""
        if self.state == 'scatter':
            # Return to corner based on ghost color
            corners = {
                'red': (0, 0),
                'pink': (0, len(self.groups()[0].game.level.layout[0])),
                'blue': (len(self.groups()[0].game.level.layout), 0),
                'orange': (len(self.groups()[0].game.level.layout),
                          len(self.groups()[0].game.level.layout[0]))
            }
            return corners.get(self.color, (0, 0))
        else:  # chase
            # Target Pacman (simple chase behavior)
            pacman = self.groups()[0].game.pacman
            if pacman:
                return pacman.rect.topleft
            return (0, 0)
            
    def _get_direction_to_target(self, target, possible_directions):
        """Choose direction that gets closest to target."""
        best_direction = possible_directions[0]
        min_distance = float('inf')
        
        for direction in possible_directions:
            # Calculate position after moving in this direction
            new_pos = (
                self.rect.x + direction.x * TILE_SIZE,
                self.rect.y + direction.y * TILE_SIZE
            )
            
            # Calculate distance to target
            distance = ((new_pos[0] - target[0]) ** 2 + 
                       (new_pos[1] - target[1]) ** 2) ** 0.5
                       
            if distance < min_distance:
                min_distance = distance
                best_direction = direction
                
        return best_direction
        
    def _draw_ghost(self, color):
        """Draw the ghost sprite with given color."""
        self.image.fill((0, 0, 0, 0))  # Clear with transparency
        
        # Draw body
        body_rect = pygame.Rect(0, TILE_SIZE//4, TILE_SIZE, TILE_SIZE*3//4)
        pygame.draw.ellipse(self.image, color, body_rect)
        
        # Draw head (semi-circle)
        head_rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE//2)
        pygame.draw.ellipse(self.image, color, head_rect)
        
        # Draw eyes
        eye_color = (255, 255, 255)
        pupil_color = (0, 0, 255)
        
        # Left eye
        pygame.draw.circle(self.image, eye_color, (TILE_SIZE//3, TILE_SIZE//3), 4)
        pygame.draw.circle(self.image, pupil_color, (TILE_SIZE//3, TILE_SIZE//3), 2)
        
        # Right eye
        pygame.draw.circle(self.image, eye_color, (2*TILE_SIZE//3, TILE_SIZE//3), 4)
        pygame.draw.circle(self.image, pupil_color, (2*TILE_SIZE//3, TILE_SIZE//3), 2)
        
    def _update_appearance(self, current_time):
        """Update ghost appearance based on state."""
        if self.state == 'frightened':
            if current_time - self.state_timer > 6000:  # Start flashing after 6 seconds
                if current_time - self.flash_timer > 200:  # Flash every 200ms
                    self.is_frightened_flashing = not self.is_frightened_flashing
                    self.flash_timer = current_time
                    if self.is_frightened_flashing:
                        self._draw_ghost((255, 255, 255))  # White
                    else:
                        self._draw_ghost((0, 0, 255))  # Blue
            else:
                self._draw_ghost((0, 0, 255))  # Blue
        elif self.state == 'eaten':
            self._draw_ghost((0, 0, 0, 0))  # Transparent
            # Draw eyes only
            pygame.draw.circle(self.image, (255, 255, 255), (TILE_SIZE//3, TILE_SIZE//3), 4)
            pygame.draw.circle(self.image, (0, 0, 255), (TILE_SIZE//3, TILE_SIZE//3), 2)
            pygame.draw.circle(self.image, (255, 255, 255), (2*TILE_SIZE//3, TILE_SIZE//3), 4)
            pygame.draw.circle(self.image, (0, 0, 255), (2*TILE_SIZE//3, TILE_SIZE//3), 2)
            
    def enter_frightened_mode(self):
        """Enter frightened state."""
        if self.state != 'eaten':
            self.state = 'frightened'
            self.state_timer = pygame.time.get_ticks() + 8000  # 8 seconds of frightened mode
            self.direction = -self.direction  # Reverse direction
            self._draw_ghost((0, 0, 255))  # Blue
            
    def _get_color_from_name(self, color_name):
        """Convert color name to RGB tuple."""
        colors = {
            'red': RED,
            'pink': PINK,
            'blue': BLUE,
            'orange': ORANGE
        }
        return colors.get(color_name, RED) 