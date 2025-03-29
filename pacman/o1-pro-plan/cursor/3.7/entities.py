"""
Entity classes for Pac-Man game
Includes base Entity class, Pacman, and Ghost classes
"""
import pygame
import random
import math
from constants import *

class Entity:
    """
    Base class for game entities (Pac-Man and Ghosts)
    Handles movement, collision detection, and basic rendering
    """
    
    def __init__(self, x, y, speed):
        """Initialize entity with position and speed"""
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = STOP
        self.next_direction = None
        self.animation_frame = 0
        self.animation_speed = 0.2  # Controls animation speed
        
    def update(self, dt, maze):
        """Update entity position based on direction and handle collisions"""
        # Try to change direction if a new direction is queued
        if self.next_direction:
            # Check if we're at (or close to) a tile center
            tile_center_x = (self.x // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2
            tile_center_y = (self.y // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2
            
            # Check if we're close enough to the tile center to turn
            if (abs(self.x - tile_center_x) < self.speed and 
                abs(self.y - tile_center_y) < self.speed):
                
                # Calculate next tile position based on next_direction
                next_tile_x = (self.x // TILE_SIZE) + self.next_direction[0]
                next_tile_y = (self.y // TILE_SIZE) + self.next_direction[1]
                
                # Check if the next tile in the desired direction is valid
                if not maze.is_wall(next_tile_x, next_tile_y):
                    # Snap to tile center when turning
                    self.x = tile_center_x
                    self.y = tile_center_y
                    self.direction = self.next_direction
                    self.next_direction = None
        
        # Calculate new position based on current direction
        new_x = self.x + self.direction[0] * self.speed
        new_y = self.y + self.direction[1] * self.speed
        
        # Check for wall collision
        next_tile_x = new_x // TILE_SIZE
        next_tile_y = new_y // TILE_SIZE
        
        # If not hitting a wall, update position
        if not maze.is_wall(next_tile_x, next_tile_y):
            self.x = new_x
            self.y = new_y
        else:
            # If we hit a wall, stop in that direction
            if self.direction[0] != 0:  # Moving horizontally
                # Align with tile center horizontally
                self.x = next_tile_x * TILE_SIZE - self.direction[0] * (TILE_SIZE // 2)
            if self.direction[1] != 0:  # Moving vertically
                # Align with tile center vertically
                self.y = next_tile_y * TILE_SIZE - self.direction[1] * (TILE_SIZE // 2)
            
            # Stop movement if we hit a wall
            self.direction = STOP
        
        # Handle wrap-around tunnels
        self.x, self.y = maze.check_wrap_around(self.x, self.y)
        
        # Update animation frame
        if self.direction != STOP:
            self.animation_frame += self.animation_speed
            if self.animation_frame >= 2:  # Assuming 2 frames for animation
                self.animation_frame = 0
    
    def set_direction(self, direction):
        """Queue a direction change for the next tile center"""
        self.next_direction = direction
        
    def get_tile_position(self):
        """Get the current tile position as (tile_x, tile_y)"""
        return self.x // TILE_SIZE, self.y // TILE_SIZE
        
    def get_pixel_position(self):
        """Get the current pixel position as (x, y)"""
        return self.x, self.y
        
    def draw(self, screen):
        """Basic draw method, to be overridden by subclasses"""
        # Base entities are just simple circles
        pygame.draw.circle(
            screen, 
            WHITE, 
            (int(self.x), int(self.y)), 
            TILE_SIZE // 2
        )


class Pacman(Entity):
    """
    Pacman entity controlled by the player
    Handles input, pellet consumption, and specific animation
    """
    
    def __init__(self, x, y):
        """Initialize Pac-Man at the given position"""
        super().__init__(x, y, PACMAN_SPEED)
        self.power_mode = False
        self.power_timer = 0
        self.invincible = False  # Brief invincibility after losing a life
        self.invincible_timer = 0
        self.mouth_open = 0  # For mouth animation (0-1 range)
        self.mouth_direction = 1  # 1: opening, -1: closing
    
    def update(self, dt, maze, score_manager=None):
        """Update Pac-Man position, handle pellet consumption"""
        super().update(dt, maze)
        
        # Update power pellet timer
        if self.power_mode:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.power_mode = False
                if score_manager:
                    score_manager.reset_ghost_multiplier()
        
        # Update invincibility timer
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
        
        # Check for pellet consumption
        if score_manager:
            tile_x, tile_y = self.get_tile_position()
            score = maze.consume_pellet(tile_x, tile_y)
            if score > 0:
                score_manager.add_score(score)
                
                # Check for power pellet
                if score == POWER_PELLET_SCORE:
                    self.activate_power_mode()
                    score_manager.reset_ghost_multiplier()
                    
        # Update mouth animation
        if self.direction != STOP:
            self.mouth_open += 0.1 * self.mouth_direction
            if self.mouth_open >= 1:
                self.mouth_direction = -1
            elif self.mouth_open <= 0:
                self.mouth_direction = 1
    
    def handle_input(self, keys):
        """Handle keyboard input for movement"""
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.set_direction(UP)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.set_direction(DOWN)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.set_direction(LEFT)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.set_direction(RIGHT)
    
    def reset_position(self, x, y):
        """Reset Pac-Man to the start position after dying or starting a new level"""
        self.x = x
        self.y = y
        self.direction = STOP
        self.next_direction = None
        self.invincible = True
        self.invincible_timer = 90  # 1.5 seconds at 60 FPS
    
    def activate_power_mode(self):
        """Activate power pellet mode (ghosts become frightened)"""
        self.power_mode = True
        self.power_timer = FRIGHTENED_TIME
    
    def is_power_active(self):
        """Check if power pellet effect is active"""
        return self.power_mode
    
    def get_power_timer(self):
        """Get the remaining time for power pellet effect"""
        return self.power_timer
    
    def draw(self, screen):
        """Draw Pac-Man with animation based on direction and mouth opening"""
        # Calculate the mouth angle based on direction
        angle = 0
        if self.direction == RIGHT:
            angle = 0
        elif self.direction == UP:
            angle = 90
        elif self.direction == LEFT:
            angle = 180
        elif self.direction == DOWN:
            angle = 270
        
        # Draw a circle with a mouth (using a pie/arc)
        if self.invincible and pygame.time.get_ticks() % 200 < 100:
            # Blink when invincible
            return
        
        pygame.draw.circle(
            screen, 
            YELLOW, 
            (int(self.x), int(self.y)), 
            TILE_SIZE // 2
        )
        
        # Draw mouth as a pie/arc (filled triangle)
        if self.direction != STOP:
            # Define mouth opening angle based on animation
            mouth_angle = 60 * self.mouth_open
            
            # Draw the mouth "cut" from the circle
            pygame.draw.polygon(
                screen,
                BLACK,
                [
                    (int(self.x), int(self.y)),
                    (int(self.x + TILE_SIZE // 2 * math.cos(math.radians(angle - mouth_angle))),
                     int(self.y - TILE_SIZE // 2 * math.sin(math.radians(angle - mouth_angle)))),
                    (int(self.x + TILE_SIZE // 2 * math.cos(math.radians(angle + mouth_angle))),
                     int(self.y - TILE_SIZE // 2 * math.sin(math.radians(angle + mouth_angle))))
                ]
            )


class Ghost(Entity):
    """
    Ghost entity that chases Pac-Man based on different AI behaviors
    Implements scatter, chase, frightened, and eaten states
    """
    
    def __init__(self, x, y, ghost_type):
        """Initialize a ghost with its specific type/color"""
        super().__init__(x, y, GHOST_SPEED)
        self.ghost_type = ghost_type
        
        # Set color based on ghost type
        if ghost_type == BLINKY:
            self.color = RED
        elif ghost_type == PINKY:
            self.color = PINK
        elif ghost_type == INKY:
            self.color = CYAN
        elif ghost_type == CLYDE:
            self.color = ORANGE
        else:
            self.color = WHITE
        
        # Ghost state and timers
        self.state = SCATTER
        self.state_timer = SCATTER_TIME[0]
        self.mode_cycle = 0  # Track which cycle of scatter/chase we're in
        self.frightened_timer = 0
        
        # Define scatter corner (target tile in scatter mode)
        if ghost_type == BLINKY:  # Red - top right
            self.scatter_tile = (GRID_WIDTH - 2, 0)
        elif ghost_type == PINKY:  # Pink - top left
            self.scatter_tile = (1, 0)
        elif ghost_type == INKY:  # Cyan - bottom right
            self.scatter_tile = (GRID_WIDTH - 2, GRID_HEIGHT - 2)
        elif ghost_type == CLYDE:  # Orange - bottom left
            self.scatter_tile = (1, GRID_HEIGHT - 2)
    
    def update(self, dt, maze, pacman):
        """Update ghost position and state"""
        # Update state timers
        if self.state == FRIGHTENED:
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                # Return to previous state (chase or scatter)
                self.state = SCATTER if self.mode_cycle % 2 == 0 else CHASE
        elif self.state in [SCATTER, CHASE]:
            self.state_timer -= 1
            if self.state_timer <= 0:
                # Toggle between scatter and chase
                if self.state == SCATTER:
                    self.state = CHASE
                    self.mode_cycle += 1
                    if self.mode_cycle // 2 < len(CHASE_TIME):
                        self.state_timer = CHASE_TIME[self.mode_cycle // 2]
                    else:
                        # Stay in chase mode indefinitely
                        self.state_timer = -1
                else:  # CHASE -> SCATTER
                    self.state = SCATTER
                    self.mode_cycle += 1
                    if self.mode_cycle // 2 < len(SCATTER_TIME):
                        self.state_timer = SCATTER_TIME[self.mode_cycle // 2]
                    else:
                        # Fallback to chase mode
                        self.state = CHASE
                        self.state_timer = -1
        
        # Adjust speed based on state
        if self.state == FRIGHTENED:
            self.speed = GHOST_FRIGHTENED_SPEED
        elif self.state == EATEN:
            self.speed = GHOST_EATEN_SPEED
        else:
            self.speed = GHOST_SPEED
        
        # Choose direction based on current state and position
        if maze.is_intersection(self.x, self.y) or self.direction == STOP:
            target_tile = self.get_target_tile(pacman)
            self.choose_direction(maze, target_tile)
        
        # Move ghost
        super().update(dt, maze)
        
        # Check if ghost has reached the ghost house when eaten
        if self.state == EATEN:
            # Check if ghost is at its starting position
            ghost_house_center = maze.ghost_spawns[self.ghost_type]
            if (abs(self.x - ghost_house_center[0]) < self.speed and 
                abs(self.y - ghost_house_center[1]) < self.speed):
                # Return to scatter or chase mode
                self.state = SCATTER if self.mode_cycle % 2 == 0 else CHASE
                self.x, self.y = ghost_house_center  # Snap to exact position
    
    def set_frightened(self):
        """Set ghost to frightened state when Pac-Man eats a power pellet"""
        if self.state != EATEN:  # Don't affect ghosts that are already eaten
            self.state = FRIGHTENED
            self.frightened_timer = FRIGHTENED_TIME
            
            # Immediately reverse direction
            if self.direction != STOP:
                self.direction = (-self.direction[0], -self.direction[1])
    
    def is_frightened(self):
        """Check if ghost is in frightened state"""
        return self.state == FRIGHTENED
    
    def set_eaten(self):
        """Set ghost to eaten state when caught by Pac-Man during frightened mode"""
        self.state = EATEN
    
    def is_eaten(self):
        """Check if ghost is in eaten state (returning to ghost house)"""
        return self.state == EATEN
    
    def get_target_tile(self, pacman):
        """
        Determine target tile based on ghost type and current state
        Each ghost has a unique targeting behavior in chase mode
        """
        pacman_tile = pacman.get_tile_position()
        
        # If in scatter mode, target the scatter corner
        if self.state == SCATTER:
            return self.scatter_tile
            
        # If in frightened mode, no specific target (random movement)
        elif self.state == FRIGHTENED:
            return None
            
        # If eaten, target the ghost house
        elif self.state == EATEN:
            return (GRID_WIDTH // 2, GRID_HEIGHT // 2 - 2)
            
        # Chase mode - each ghost has unique targeting behavior
        elif self.state == CHASE:
            if self.ghost_type == BLINKY:  # Red - directly targets Pac-Man
                return pacman_tile
                
            elif self.ghost_type == PINKY:  # Pink - targets 4 tiles ahead of Pac-Man
                # Calculate target 4 tiles ahead of Pac-Man in his direction
                dx, dy = pacman.direction
                target_x = pacman_tile[0] + 4 * dx
                target_y = pacman_tile[1] + 4 * dy
                
                # Special case: in the original game, there's a bug where UP direction
                # also shifts 4 tiles to the left due to an overflow bug
                if pacman.direction == UP:
                    target_x -= 4
                    
                return (target_x, target_y)
                
            elif self.ghost_type == INKY:  # Cyan - uses complex targeting with Blinky
                # Get Blinky's position
                blinky_pos = (0, 0)  # Default if Blinky not found
                
                # Calculate target 2 tiles ahead of Pac-Man
                dx, dy = pacman.direction
                intermediate_x = pacman_tile[0] + 2 * dx
                intermediate_y = pacman_tile[1] + 2 * dy
                
                # Special case: in the original game, there's a bug where UP direction
                # also shifts 2 tiles to the left due to an overflow bug
                if pacman.direction == UP:
                    intermediate_x -= 2
                
                # Calculate vector from Blinky to the intermediate target, then double it
                vector_x = intermediate_x - blinky_pos[0]
                vector_y = intermediate_y - blinky_pos[1]
                
                return (intermediate_x + vector_x, intermediate_y + vector_y)
                
            elif self.ghost_type == CLYDE:  # Orange - targets Pac-Man or scatter mode
                # Calculate distance to Pac-Man
                ghost_tile = self.get_tile_position()
                distance = math.sqrt((ghost_tile[0] - pacman_tile[0])**2 + 
                                     (ghost_tile[1] - pacman_tile[1])**2)
                
                # If distance > 8 tiles, target Pac-Man, otherwise use scatter target
                if distance > 8:
                    return pacman_tile
                else:
                    return self.scatter_tile
        
        # Default to current position if no valid target
        return self.get_tile_position()
    
    def choose_direction(self, maze, target_tile):
        """Choose the best direction toward the target tile"""
        if self.state == FRIGHTENED and target_tile is None:
            # In frightened mode, choose a random valid direction
            valid_dirs = maze.get_valid_directions(self.x, self.y, self.direction)
            if valid_dirs:
                self.direction = random.choice(valid_dirs)
            return
            
        current_tile = self.get_tile_position()
        valid_dirs = maze.get_valid_directions(self.x, self.y, self.direction)
        
        if not valid_dirs:
            # No valid directions, stop movement
            self.direction = STOP
            return
            
        # If ghost is eaten, use the most direct path to ghost house
        if self.state == EATEN:
            # Find direction that minimizes distance to target
            best_dir = valid_dirs[0]
            best_distance = float('inf')
            
            for direction in valid_dirs:
                next_x = current_tile[0] + direction[0]
                next_y = current_tile[1] + direction[1]
                distance = math.sqrt((next_x - target_tile[0])**2 + 
                                    (next_y - target_tile[1])**2)
                
                if distance < best_distance:
                    best_distance = distance
                    best_dir = direction
                    
            self.direction = best_dir
            return
            
        # For normal movement, ghosts have a turn priority
        # They prefer to go up, left, down, right in that order
        # (This is a simplification of the arcade ghost movement)
        
        # If there's a target, find the direction that gets closest to it
        if target_tile:
            # Sort directions by distance to target
            directions_with_dist = []
            
            for direction in valid_dirs:
                next_x = current_tile[0] + direction[0]
                next_y = current_tile[1] + direction[1]
                distance = math.sqrt((next_x - target_tile[0])**2 + 
                                    (next_y - target_tile[1])**2)
                directions_with_dist.append((direction, distance))
                
            # Sort by distance (ascending)
            directions_with_dist.sort(key=lambda x: x[1])
            
            # Choose the direction with minimum distance
            self.direction = directions_with_dist[0][0]
        else:
            # No target, just pick any valid direction
            self.direction = valid_dirs[0]
    
    def draw(self, screen):
        """Draw the ghost with appropriate color based on state"""
        if self.state == FRIGHTENED:
            # Blinking effect when frightened mode is ending
            if self.frightened_timer < 60 and self.frightened_timer % 10 < 5:
                color = FRIGHTENED_END_COLOR
            else:
                color = FRIGHTENED_COLOR
        elif self.state == EATEN:
            # When eaten, only the eyes are visible
            color = BLACK
        else:
            color = self.color
        
        # Draw ghost body
        pygame.draw.circle(
            screen,
            color,
            (int(self.x), int(self.y)),
            TILE_SIZE // 2
        )
        
        # Draw the "skirt" at the bottom of the ghost
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(
                int(self.x) - TILE_SIZE // 2,
                int(self.y),
                TILE_SIZE,
                TILE_SIZE // 2
            )
        )
        
        # Draw eyes (always white, even when frightened)
        eye_size = TILE_SIZE // 6
        eye_offset_x = TILE_SIZE // 5
        
        # Left eye
        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.x) - eye_offset_x, int(self.y) - eye_offset_x),
            eye_size
        )
        
        # Right eye
        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.x) + eye_offset_x, int(self.y) - eye_offset_x),
            eye_size
        )
        
        # Draw pupils (looking in movement direction)
        pupil_size = eye_size // 2
        
        # Default pupil position (looking right)
        pupil_offset_x = eye_size // 2
        pupil_offset_y = 0
        
        # Adjust pupil position based on direction
        if self.direction == LEFT:
            pupil_offset_x = -pupil_offset_x
        elif self.direction == UP:
            pupil_offset_x = 0
            pupil_offset_y = -eye_size // 2
        elif self.direction == DOWN:
            pupil_offset_x = 0
            pupil_offset_y = eye_size // 2
        
        # Draw pupils
        if self.state != FRIGHTENED:
            # Left pupil
            pygame.draw.circle(
                screen,
                BLACK,
                (int(self.x) - eye_offset_x + pupil_offset_x, 
                 int(self.y) - eye_offset_x + pupil_offset_y),
                pupil_size
            )
            
            # Right pupil
            pygame.draw.circle(
                screen,
                BLACK,
                (int(self.x) + eye_offset_x + pupil_offset_x, 
                 int(self.y) - eye_offset_x + pupil_offset_y),
                pupil_size
            )
                
        # In frightened mode, draw a different mouth
        if self.state == FRIGHTENED:
            pygame.draw.line(
                screen,
                WHITE,
                (int(self.x) - TILE_SIZE // 4, int(self.y) + TILE_SIZE // 5),
                (int(self.x) + TILE_SIZE // 4, int(self.y) + TILE_SIZE // 5),
                2
            )
    
    def reset_position(self, x, y):
        """Reset ghost to the given position"""
        self.x = x
        self.y = y
        self.direction = STOP
        self.next_direction = None
        
        # Reset to scatter state
        self.state = SCATTER
        self.state_timer = SCATTER_TIME[0]
        self.mode_cycle = 0
        self.frightened_timer = 0 