import pygame
import random
from entities.entity import Entity
import config
from utils.path_finding import get_best_direction

class Ghost(Entity):
    def __init__(self, x, y, maze, name, scatter_target):
        super().__init__(x, y, maze)
        self.name = name
        self.speed = 1.75
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.mode = "scatter"  # scatter, chase, frightened
        self.scatter_target = scatter_target
        self.home_position = (x, y)
        self.target_tile = (0, 0)
        self.animation_timer = 0
        self.animation_frame = 0
        self.frightened_timer = 0
        self.is_eaten = False
        self.in_house = True
        
        # For initial implementation, just use a colored rectangle
        self.color = config.RED  # Default color, should be overridden in subclasses
        
    def update(self, dt):
        # Update animation
        self.animation_timer += dt
        if self.animation_timer >= 0.2:
            self.animation_timer = 0
            self.animation_frame = 1 - self.animation_frame  # Toggle between 0 and 1
        
        # Update frightened timer if applicable
        if self.mode == "frightened" and not self.is_eaten:
            self.frightened_timer -= dt
            if self.frightened_timer <= 0:
                self.mode = "chase"  # Revert to chase mode
        
        # If ghost is eaten, just move eyes back to ghost house
        if self.is_eaten:
            self.return_to_house(dt)
            return
        
        # At each tile center, decide next direction
        grid_x, grid_y = self.get_grid_position()
        center_x = grid_x * self.maze.tile_size + self.maze.tile_size / 2
        center_y = grid_y * self.maze.tile_size + self.maze.tile_size / 2
        
        # If at a tile center (or close enough), choose next direction
        if abs(self.x - center_x) < 1 and abs(self.y - center_y) < 1:
            self.x = center_x
            self.y = center_y
            
            # In frightened mode, choose random direction
            if self.mode == "frightened" and not self.is_eaten:
                self.choose_random_direction()
            else:
                # In scatter or chase mode, use path finding
                self.choose_next_direction()
        
        # Move in current direction
        dx, dy = self.direction
        if self.can_move(dx * self.speed, dy * self.speed):
            self.x += dx * self.speed
            self.y += dy * self.speed
            
            # Handle tunnel wrap-around
            self.handle_tunnel_wrap()
    
    def set_mode(self, mode, duration=None):
        """Set ghost mode to 'scatter', 'chase', or 'frightened'"""
        self.mode = mode
        if mode == "frightened":
            self.frightened_timer = duration if duration else 7.0
            # Reverse direction when entering frightened mode
            self.reverse_direction()
        elif mode != self.mode:
            # Reverse direction when changing between scatter and chase
            self.reverse_direction()
    
    def reverse_direction(self):
        """Reverse the current direction"""
        dx, dy = self.direction
        self.direction = (-dx, -dy)
    
    def choose_next_direction(self):
        """Choose next direction based on shortest path to target"""
        x, y = self.get_grid_position()
        
        # Determine target based on mode
        if self.mode == "scatter":
            target = self.scatter_target
        else:  # chase mode or eaten
            target = self.get_chase_target()
        
        # Use path finding to determine best direction
        self.direction = get_best_direction(
            self.maze, 
            (x, y), 
            target, 
            self.direction
        )
    
    def choose_random_direction(self):
        """Choose a random direction (for frightened mode)"""
        x, y = self.get_grid_position()
        possible_dirs = []
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:  # Up, Right, Down, Left
            if self.can_move(dx, dy) and (dx, dy) != (-self.direction[0], -self.direction[1]):
                possible_dirs.append((dx, dy))
        
        if possible_dirs:
            self.direction = random.choice(possible_dirs)
    
    def get_chase_target(self):
        """Override in subclasses to implement specific ghost behavior"""
        return (0, 0)
    
    def handle_tunnel_wrap(self):
        """Handle tunnel wrap-around"""
        if self.x < 0:
            self.x = self.maze.width * self.maze.tile_size
        elif self.x >= self.maze.width * self.maze.tile_size:
            self.x = 0
    
    def eaten(self):
        """Set ghost to eaten state (eyes only)"""
        self.is_eaten = True
    
    def return_to_house(self, dt):
        """Return to ghost house after being eaten"""
        # Simplified version: just respawn at home position after a delay
        self.animation_timer += dt
        if self.animation_timer >= 3.0:  # 3-second delay
            self.animation_timer = 0
            self.is_eaten = False
            self.x = self.home_position[0]
            self.y = self.home_position[1]
            self.direction = (0, 0)
    
    def render(self, screen, offset_x=0, offset_y=0):
        rect_x = int(self.x + offset_x)
        rect_y = int(self.y + offset_y)
        
        if self.is_eaten:
            # Draw eyes only
            pygame.draw.circle(screen, config.WHITE, 
                              (rect_x + self.maze.tile_size // 3, rect_y + self.maze.tile_size // 3), 2)
            pygame.draw.circle(screen, config.WHITE, 
                              (rect_x + 2 * self.maze.tile_size // 3, rect_y + self.maze.tile_size // 3), 2)
        else:
            # Choose color based on mode
            if self.mode == "frightened":
                if self.frightened_timer <= 2.0 and int(self.frightened_timer * 5) % 2 == 0:
                    # Flashing white/blue when almost done
                    color = config.WHITE
                else:
                    color = (0, 0, 150)  # Blue
            else:
                color = self.color
            
            # Draw ghost body (simple rectangle for now)
            pygame.draw.rect(screen, color, 
                           (rect_x, rect_y, self.maze.tile_size, self.maze.tile_size))
            
            # Draw eyes
            pygame.draw.circle(screen, config.WHITE, 
                              (rect_x + self.maze.tile_size // 3, rect_y + self.maze.tile_size // 3), 2)
            pygame.draw.circle(screen, config.WHITE, 
                              (rect_x + 2 * self.maze.tile_size // 3, rect_y + self.maze.tile_size // 3), 2)