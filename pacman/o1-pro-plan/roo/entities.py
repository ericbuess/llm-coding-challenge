"""
Entities module for the Pac-Man game
Defines the Entity base class, Pacman, and Ghost classes
"""

import pygame
import math
import random
from constants import *

class Entity:
    """Base class for all moving entities in the game"""
    
    def __init__(self, x, y, color):
        # Position in pixel coordinates
        self.x = x * TILE_SIZE + TILE_SIZE // 2
        self.y = y * TILE_SIZE + TILE_SIZE // 2
        self.color = color
        
        # Movement properties
        self.direction = STOP
        self.next_direction = STOP
        self.speed = 0
        
        # Animation properties
        self.animation_frame = 0
        self.animation_timer = 0
    
    def update(self, dt, maze):
        """Update the entity's position and handle wall collisions"""
        # Calculate the tile coordinates for the entity
        current_tile_x, current_tile_y = self.get_tile_pos()
        
        # Calculate the pixel center of the current tile
        tile_center_x = current_tile_x * TILE_SIZE + TILE_SIZE // 2
        tile_center_y = current_tile_y * TILE_SIZE + TILE_SIZE // 2
        
        # Check if we're at a tile center (or very close to it)
        at_tile_center = (abs(self.x - tile_center_x) < self.speed and
                          abs(self.y - tile_center_y) < self.speed)
        
        # If at a tile center, try to change direction if needed
        if at_tile_center:
            self.x = tile_center_x
            self.y = tile_center_y
            
            # Try to turn in the next direction if it's different and valid
            if self.next_direction != self.direction and self.next_direction != STOP:
                next_x = current_tile_x + self.next_direction[0]
                next_y = current_tile_y + self.next_direction[1]
                
                if maze.can_move_to(next_x, next_y):
                    self.direction = self.next_direction
                    
        # Always try to keep moving in the current direction
        if self.direction != STOP:
            # Calculate new position
            new_x = self.x + self.direction[0] * self.speed
            new_y = self.y + self.direction[1] * self.speed
            
            # Calculate the new tile coordinates
            new_tile_x = int(new_x // TILE_SIZE)
            new_tile_y = int(new_y // TILE_SIZE)
            
            # Handle wrap-around for tunnels
            if new_tile_x < 0:
                new_x = GRID_WIDTH * TILE_SIZE - 1
            elif new_tile_x >= GRID_WIDTH:
                new_x = 0
            
            # Get updated tile positions after possible wrap-around
            new_tile_x = int(new_x // TILE_SIZE)
            new_tile_y = int(new_y // TILE_SIZE)
            
            # Check if the new position is valid (not a wall)
            if maze.can_move_to(new_tile_x, new_tile_y):
                self.x = new_x
                self.y = new_y
            else:
                # If we can't move in the current direction, try to align with the center of the current tile
                if self.direction[0] != 0:  # Moving horizontally
                    self.y = tile_center_y
                else:  # Moving vertically
                    self.x = tile_center_x
                
                # Only stop if we've already aligned with the center
                if (abs(self.x - tile_center_x) < self.speed and
                    abs(self.y - tile_center_y) < self.speed):
                    self.direction = STOP
    
    def get_tile_pos(self):
        """Convert pixel coordinates to tile coordinates"""
        return (int(self.x // TILE_SIZE), int(self.y // TILE_SIZE))
    
    def reset_position(self, x, y):
        """Reset the entity to a specific tile position"""
        self.x = x * TILE_SIZE + TILE_SIZE // 2
        self.y = y * TILE_SIZE + TILE_SIZE // 2
        self.direction = STOP
        self.next_direction = STOP
    
    def draw(self, screen):
        """Default drawing method for entities - can be overridden by subclasses"""
        # Draw a simple circle at the entity's position
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), TILE_SIZE // 2)


class Pacman(Entity):
    """Player-controlled Pac-Man entity"""
    
    def __init__(self, x, y):
        super().__init__(x, y, YELLOW)
        self.speed = PACMAN_SPEED
        self.lives = LIVES
        self.power_mode = False
        self.power_timer = 0
        self.mouth_angle = 0
        self.mouth_open = True
        self.animation_speed = 0.15
    
    def handle_input(self, keys):
        """Handle player input to set the next direction"""
        # Store previous direction to ensure it doesn't get reset
        prev_direction = self.next_direction
        
        # Check each key individually to prevent the "elif" from blocking certain key combinations
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.next_direction = UP
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.next_direction = DOWN
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.next_direction = LEFT
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.next_direction = RIGHT
            
        # If no key is pressed, maintain previous direction
        if not (keys[pygame.K_UP] or keys[pygame.K_w] or
                keys[pygame.K_DOWN] or keys[pygame.K_s] or
                keys[pygame.K_LEFT] or keys[pygame.K_a] or
                keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.next_direction = prev_direction
    
    def update(self, dt, maze):
        """Update Pac-Man's position and check for pellet collisions"""
        super().update(dt, maze)
        
        # Update power mode timer
        if self.power_mode:
            self.power_timer -= dt
            if self.power_timer <= 0:
                self.power_mode = False
        
        # Update animation
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.mouth_open = not self.mouth_open
    
    def check_pellet_collision(self, maze, score_manager):
        """Check if Pac-Man is eating a pellet and update score"""
        tile_x, tile_y = self.get_tile_pos()
        score = maze.eat_pellet(tile_x, tile_y)
        
        if score > 0:
            score_manager.add_score(score)
            
            # If a power pellet was eaten, activate power mode
            if score == POWER_PELLET_SCORE:
                self.activate_power_mode()
            
            return True
        return False
    
    def activate_power_mode(self):
        """Activate power mode after eating a power pellet"""
        self.power_mode = True
        self.power_timer = FRIGHTENED_TIME / 1000  # Convert to seconds
    
    def lose_life(self):
        """Lose a life and reset position"""
        self.lives -= 1
        return self.lives >= 0
    
    def draw(self, screen):
        """Draw Pac-Man with mouth animation"""
        # Calculate rotation angle based on direction
        rotation = 0
        if self.direction == UP:
            rotation = 90
        elif self.direction == DOWN:
            rotation = 270
        elif self.direction == LEFT:
            rotation = 180
        
        # Draw Pac-Man as a circle with a mouth
        if self.mouth_open:
            # Draw pac-man with open mouth
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), TILE_SIZE // 2)
            
            # Draw the mouth as a triangle
            mouth_x = self.x + math.cos(math.radians(rotation)) * TILE_SIZE // 2
            mouth_y = self.y - math.sin(math.radians(rotation)) * TILE_SIZE // 2
            
            # Define the triangle points
            points = [
                (self.x, self.y),
                (self.x + math.cos(math.radians(rotation - 45)) * TILE_SIZE // 2,
                 self.y - math.sin(math.radians(rotation - 45)) * TILE_SIZE // 2),
                (self.x + math.cos(math.radians(rotation + 45)) * TILE_SIZE // 2,
                 self.y - math.sin(math.radians(rotation + 45)) * TILE_SIZE // 2)
            ]
            
            # Draw the triangle in black to create the mouth effect
            pygame.draw.polygon(screen, BLACK, points)
        else:
            # Draw full circle when mouth is closed
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), TILE_SIZE // 2)


class Ghost(Entity):
    """Enemy ghost entity with AI behavior"""
    
    # Ghost states
    SCATTER = 0
    CHASE = 1
    FRIGHTENED = 2
    EATEN = 3
    
    def __init__(self, x, y, ghost_type):
        # Set color based on ghost type
        color = RED  # Default (Blinky)
        if ghost_type == 'PINKY':
            color = PINK
        elif ghost_type == 'INKY':
            color = CYAN
        elif ghost_type == 'CLYDE':
            color = ORANGE
        
        super().__init__(x, y, color)
        
        self.ghost_type = ghost_type
        self.speed = GHOST_NORMAL_SPEED
        self.state = Ghost.SCATTER
        self.previous_state = Ghost.SCATTER
        self.state_timer = 0
        self.frightened_timer = 0
        self.scatter_index = 0
        
        # Set scatter target based on ghost type
        if ghost_type == 'BLINKY':
            self.scatter_target = (GRID_WIDTH - 3, 0)
        elif ghost_type == 'PINKY':
            self.scatter_target = (2, 0)
        elif ghost_type == 'INKY':
            self.scatter_target = (GRID_WIDTH - 1, GRID_HEIGHT - 1)
        elif ghost_type == 'CLYDE':
            self.scatter_target = (0, GRID_HEIGHT - 1)
    
    def update(self, dt, maze, pacman, blinky_position=None):
        """Update ghost position and state"""
        # Update timers based on state
        if self.state == Ghost.SCATTER or self.state == Ghost.CHASE:
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.switch_between_scatter_chase()
        
        elif self.state == Ghost.FRIGHTENED:
            self.frightened_timer -= dt
            if self.frightened_timer <= 0:
                self.state = self.previous_state
                self.speed = GHOST_NORMAL_SPEED
        
        # Get target tile based on current state
        target_tile = self.get_target_tile(pacman, blinky_position)
        
        # At tile centers, choose the best direction towards the target
        current_tile_x, current_tile_y = self.get_tile_pos()
        tile_center_x = current_tile_x * TILE_SIZE + TILE_SIZE // 2
        tile_center_y = current_tile_y * TILE_SIZE + TILE_SIZE // 2
        
        # If at a tile center (or very close), determine the next direction
        if (abs(self.x - tile_center_x) < self.speed and
            abs(self.y - tile_center_y) < self.speed):
            self.x = tile_center_x
            self.y = tile_center_y
            
            # Choose next direction
            self.choose_next_direction(maze, target_tile)
        
        # Move ghost according to current direction
        if self.direction != STOP:
            # Calculate new position
            new_x = self.x + self.direction[0] * self.speed
            new_y = self.y + self.direction[1] * self.speed
            
            # Handle wrap-around for tunnels
            if new_x < 0:
                new_x = GRID_WIDTH * TILE_SIZE - 1
            elif new_x >= GRID_WIDTH * TILE_SIZE:
                new_x = 0
                
            # Calculate the new tile coordinates
            new_tile_x = int(new_x // TILE_SIZE)
            new_tile_y = int(new_y // TILE_SIZE)
            
            # Check if the new position is valid (not a wall)
            if self.state == Ghost.EATEN or maze.can_move_to(new_tile_x, new_tile_y):
                self.x = new_x
                self.y = new_y
            else:
                # If we can't move in the current direction, realign to the tile center
                if self.direction[0] != 0:  # Moving horizontally
                    self.y = tile_center_y
                else:  # Moving vertically
                    self.x = tile_center_x
    
    def choose_next_direction(self, maze, target_tile):
        """Choose the best direction to move towards the target tile"""
        current_tile_x, current_tile_y = self.get_tile_pos()
        
        # Available directions (excluding the opposite of the current direction)
        available_directions = []
        opposite_direction = (-self.direction[0], -self.direction[1])
        
        # Check each possible direction
        for direction in [UP, DOWN, LEFT, RIGHT]:
            # Skip the opposite direction (no reversing allowed except in certain cases)
            if direction == opposite_direction and self.state != Ghost.FRIGHTENED and self.state != Ghost.EATEN:
                continue
            
            # Check if the next tile in this direction is valid
            next_x = current_tile_x + direction[0]
            next_y = current_tile_y + direction[1]
            
            if maze.can_move_to(next_x, next_y):
                available_directions.append(direction)
        
        # If no valid directions, allow reversing as a last resort
        if not available_directions and self.direction != STOP:
            next_x = current_tile_x + opposite_direction[0]
            next_y = current_tile_y + opposite_direction[1]
            
            if maze.can_move_to(next_x, next_y):
                self.direction = opposite_direction
                self.next_direction = opposite_direction
                return
        
        # Choose a direction based on the current state
        if self.state == Ghost.FRIGHTENED and available_directions:
            # In frightened mode, choose a random direction
            self.direction = random.choice(available_directions)
            self.next_direction = self.direction
        
        elif self.state == Ghost.EATEN and available_directions:
            # When eaten, take the shortest path back to the ghost house
            best_direction = None
            min_distance = float('inf')
            
            for direction in available_directions:
                next_x = current_tile_x + direction[0]
                next_y = current_tile_y + direction[1]
                
                # Calculate Manhattan distance to the ghost house
                distance = abs(next_x - 14) + abs(next_y - 14)  # Ghost house center
                
                if distance < min_distance:
                    min_distance = distance
                    best_direction = direction
            
            self.direction = best_direction
            self.next_direction = best_direction
        
        elif available_directions:
            # In scatter or chase mode, choose the direction that gets closest to the target
            best_direction = None
            min_distance = float('inf')
            
            for direction in available_directions:
                next_x = current_tile_x + direction[0]
                next_y = current_tile_y + direction[1]
                
                # Calculate Manhattan distance to target
                distance = abs(next_x - target_tile[0]) + abs(next_y - target_tile[1])
                
                if distance < min_distance:
                    min_distance = distance
                    best_direction = direction
            
            self.direction = best_direction
            self.next_direction = best_direction
    
    def get_target_tile(self, pacman, blinky_position):
        """Get the target tile based on the ghost's state and type"""
        pacman_tile_x, pacman_tile_y = pacman.get_tile_pos()
        
        # If frightened, there's no specific target (random movement)
        if self.state == Ghost.FRIGHTENED:
            return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        
        # If eaten, target the ghost house
        elif self.state == Ghost.EATEN:
            return (14, 14)  # Ghost house center
        
        # If in scatter mode, target the ghost's corner
        elif self.state == Ghost.SCATTER:
            return self.scatter_target
        
        # If in chase mode, target based on ghost personality
        elif self.state == Ghost.CHASE:
            # Blinky targets Pac-Man directly
            if self.ghost_type == 'BLINKY':
                return (pacman_tile_x, pacman_tile_y)
            
            # Pinky targets 4 tiles ahead of Pac-Man
            elif self.ghost_type == 'PINKY':
                # Calculate target 4 tiles ahead of Pac-Man
                target_x = pacman_tile_x + 4 * pacman.direction[0]
                target_y = pacman_tile_y + 4 * pacman.direction[1]
                
                # Handle the "Pinky corner" bug from the original game
                if pacman.direction == UP:
                    target_x -= 4  # 4 tiles to the left when Pac-Man is moving up
                
                return (target_x, target_y)
            
            # Inky uses both Pac-Man and Blinky's positions
            elif self.ghost_type == 'INKY':
                if blinky_position:
                    blinky_tile_x, blinky_tile_y = blinky_position
                    
                    # Calculate a point 2 tiles ahead of Pac-Man
                    pivot_x = pacman_tile_x + 2 * pacman.direction[0]
                    pivot_y = pacman_tile_y + 2 * pacman.direction[1]
                    
                    # Same bug as Pinky
                    if pacman.direction == UP:
                        pivot_x -= 2
                    
                    # Calculate the vector from Blinky to this point and double it
                    vector_x = pivot_x - blinky_tile_x
                    vector_y = pivot_y - blinky_tile_y
                    
                    target_x = pivot_x + vector_x
                    target_y = pivot_y + vector_y
                    
                    return (target_x, target_y)
                else:
                    # Fallback if Blinky's position is not available
                    return (pacman_tile_x, pacman_tile_y)
            
            # Clyde targets Pac-Man when far, scatters when close
            elif self.ghost_type == 'CLYDE':
                # Calculate Manhattan distance to Pac-Man
                distance = abs(self.get_tile_pos()[0] - pacman_tile_x) + abs(self.get_tile_pos()[1] - pacman_tile_y)
                
                # If further than 8 tiles, target Pac-Man; otherwise, go to scatter corner
                if distance > 8:
                    return (pacman_tile_x, pacman_tile_y)
                else:
                    return self.scatter_target
        
        # Default to the ghost's scatter target
        return self.scatter_target
    
    def switch_between_scatter_chase(self):
        """Switch between scatter and chase modes"""
        if self.state == Ghost.SCATTER:
            self.state = Ghost.CHASE
            self.state_timer = CHASE_TIMES[min(self.scatter_index, len(CHASE_TIMES) - 1)] / 1000
            
            if self.state_timer < 0:  # -1 means indefinite chase
                self.state_timer = float('inf')
        else:  # CHASE mode
            self.state = Ghost.SCATTER
            self.scatter_index += 1
            
            if self.scatter_index < len(SCATTER_TIMES):
                self.state_timer = SCATTER_TIMES[self.scatter_index] / 1000
            else:
                # If we've gone through all scatter phases, stay in chase mode
                self.state = Ghost.CHASE
                self.state_timer = float('inf')
    
    def set_frightened(self):
        """Set the ghost to frightened mode"""
        if self.state != Ghost.EATEN:  # Don't affect ghosts that are already eaten
            self.previous_state = self.state
            self.state = Ghost.FRIGHTENED
            self.frightened_timer = FRIGHTENED_TIME / 1000  # Convert to seconds
            self.speed = GHOST_FRIGHTENED_SPEED
            
            # Reverse direction immediately when frightened
            self.direction = (-self.direction[0], -self.direction[1])
            self.next_direction = self.direction
    
    def set_eaten(self):
        """Set the ghost to eaten mode"""
        self.state = Ghost.EATEN
        self.speed = GHOST_EATEN_SPEED
    
    def reset_state(self):
        """Reset the ghost's state to scatter"""
        self.state = Ghost.SCATTER
        self.previous_state = Ghost.SCATTER
        self.state_timer = SCATTER_TIMES[0] / 1000
        self.frightened_timer = 0
        self.scatter_index = 0
        self.speed = GHOST_NORMAL_SPEED
    
    def draw(self, screen):
        """Draw the ghost with its current state appearance"""
        # Determine the color based on ghost state
        color = self.color
        
        if self.state == Ghost.FRIGHTENED:
            # Blinking effect near the end of frightened mode
            if self.frightened_timer < 2.0 and int(self.frightened_timer * 10) % 2 == 0:
                color = WHITE
            else:
                color = FRIGHTENED_COLOR
        
        elif self.state == Ghost.EATEN:
            # Only draw eyes when eaten
            self.draw_ghost_eyes(screen)
            return
        
        # Draw the ghost body
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), TILE_SIZE // 2)
        
        # Draw a rectangle for the bottom half to create the ghost shape
        pygame.draw.rect(screen, color, 
                        (int(self.x) - TILE_SIZE // 2, 
                         int(self.y), 
                         TILE_SIZE, 
                         TILE_SIZE // 2))
        
        # Draw the eyes
        self.draw_ghost_eyes(screen)
    
    def draw_ghost_eyes(self, screen):
        """Draw the ghost's eyes based on its direction"""
        # Base eye positions
        eye_distance = TILE_SIZE // 4
        left_eye_pos = (int(self.x - eye_distance), int(self.y - TILE_SIZE // 6))
        right_eye_pos = (int(self.x + eye_distance), int(self.y - TILE_SIZE // 6))
        
        # Adjust pupil positions based on direction
        pupil_offset_x = 0
        pupil_offset_y = 0
        
        if self.direction == LEFT:
            pupil_offset_x = -1
        elif self.direction == RIGHT:
            pupil_offset_x = 1
        elif self.direction == UP:
            pupil_offset_y = -1
        elif self.direction == DOWN:
            pupil_offset_y = 1
        
        # White part of eyes
        pygame.draw.circle(screen, WHITE, left_eye_pos, TILE_SIZE // 6)
        pygame.draw.circle(screen, WHITE, right_eye_pos, TILE_SIZE // 6)
        
        # Pupils (black part)
        pygame.draw.circle(screen, BLACK, 
                          (left_eye_pos[0] + pupil_offset_x * 2, 
                           left_eye_pos[1] + pupil_offset_y * 2), 
                          TILE_SIZE // 10)
        pygame.draw.circle(screen, BLACK, 
                          (right_eye_pos[0] + pupil_offset_x * 2, 
                           right_eye_pos[1] + pupil_offset_y * 2), 
                          TILE_SIZE // 10)