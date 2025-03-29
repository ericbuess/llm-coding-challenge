import pygame
from entities.entity import Entity
import config

class Pacman(Entity):
    def __init__(self, x, y, maze):
        super().__init__(x, y, maze)
        self.speed = 2.0
        self.lives = 3
        self.score = 0
        self.direction = (0, 0)  # Initial direction
        self.next_direction = (0, 0)  # Buffered input
        self.animation_speed = 0.15
        self.animation_timer = 0
        self.mouth_open = 0  # 0 to 3, for animation frames
        self.is_dead = False
        self.death_animation_frame = 0
        
        # For initial implementation, we'll render Pac-Man as a simple yellow circle
        # Later we can implement proper sprite loading
        self.color = config.YELLOW
        self.radius = maze.tile_size // 2 - 2
    
    def update(self, dt):
        if self.is_dead:
            self.update_death_animation(dt)
            return
        
        # Try to change direction if there's buffered input
        if self.next_direction != (0, 0):
            if self.can_move(self.next_direction[0], self.next_direction[1]):
                self.direction = self.next_direction
                self.next_direction = (0, 0)
        
        # Update position if can move in current direction
        dx, dy = self.direction
        if self.can_move(dx * self.speed, dy * self.speed):
            self.x += dx * self.speed
            self.y += dy * self.speed
            
            # Handle wrap-around tunnels
            self.handle_tunnel_wrap()
        
        # Update animation
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.mouth_open = (self.mouth_open + 1) % 4
        
        # Check for pellet collisions
        self.check_pellet_collisions()
    
    def set_next_direction(self, direction):
        """Buffer the next direction change"""
        self.next_direction = direction
    
    def handle_tunnel_wrap(self):
        """Handle wrap-around when Pac-Man goes through a tunnel"""
        if self.x < 0:
            self.x = self.maze.width * self.maze.tile_size
        elif self.x >= self.maze.width * self.maze.tile_size:
            self.x = 0
    
    def check_pellet_collisions(self):
        """Check for and handle collisions with pellets"""
        grid_x, grid_y = self.get_grid_position()
        tile = self.maze.get_tile(grid_x, grid_y)
        
        if tile == 2:  # Regular pellet
            self.maze.layout[grid_y][grid_x] = 0  # Remove pellet
            self.score += 10
            self.maze.pellets_remaining -= 1
            # Play eating sound (would be handled by game object)
        elif tile == 3:  # Power pellet
            self.maze.layout[grid_y][grid_x] = 0  # Remove power pellet
            self.score += 50
            self.maze.pellets_remaining -= 1
            # Trigger ghost frightened mode (would be handled by game object)
            # Play power pellet sound (would be handled by game object)
    
    def die(self):
        """Start Pac-Man's death animation"""
        self.is_dead = True
        self.death_animation_frame = 0
        self.direction = (0, 0)
        # Play death sound (would be handled by game object)
    
    def update_death_animation(self, dt):
        """Update Pac-Man's death animation"""
        self.animation_timer += dt
        if self.animation_timer >= 0.1:  # Slower animation for death
            self.animation_timer = 0
            self.death_animation_frame += 1
            if self.death_animation_frame >= 11:  # Simplified death animation with 11 frames
                # Animation complete
                self.death_animation_frame = 0
                self.lives -= 1
                self.is_dead = False
                # Reset position
                self.x = 14 * self.maze.tile_size
                self.y = 23 * self.maze.tile_size
                # Signal game to reset ghost positions (would be handled by game object)
    
    def render(self, screen, offset_x=0, offset_y=0):
        center_x = int(self.x + self.maze.tile_size // 2 + offset_x)
        center_y = int(self.y + self.maze.tile_size // 2 + offset_y)
        
        if self.is_dead:
            # Simple death animation - shrinking circle
            death_progress = self.death_animation_frame / 10
            radius = int(self.radius * (1 - death_progress))
            pygame.draw.circle(screen, self.color, (center_x, center_y), radius)
        else:
            # Draw Pac-Man as a circle with a "mouth"
            pygame.draw.circle(screen, self.color, (center_x, center_y), self.radius)
            
            # Draw mouth based on direction and animation frame
            # For simplicity, just change the angle of the pie slice based on direction
            start_angle = 0
            if self.direction == (1, 0):  # Right
                start_angle = 0
            elif self.direction == (0, 1):  # Down
                start_angle = 90
            elif self.direction == (-1, 0):  # Left
                start_angle = 180
            elif self.direction == (0, -1):  # Up
                start_angle = 270
            
            # Mouth opening angle depends on animation frame
            mouth_angle = 45 - (self.mouth_open * 15)
            
            # Draw mouth as a pie slice with same color as background
            if self.direction != (0, 0):  # Only draw mouth if Pac-Man is moving
                pygame.draw.polygon(screen, config.BLACK, [
                    (center_x, center_y),
                    (center_x + int(self.radius * pygame.math.Vector2(1, 0).rotate(start_angle - mouth_angle).x),
                     center_y + int(self.radius * pygame.math.Vector2(1, 0).rotate(start_angle - mouth_angle).y)),
                    (center_x + int(self.radius * pygame.math.Vector2(1, 0).rotate(start_angle + mouth_angle).x),
                     center_y + int(self.radius * pygame.math.Vector2(1, 0).rotate(start_angle + mouth_angle).y))
                ])