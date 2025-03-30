import pygame
import random
import math
from constants import *

# Initialize global game entities list for ghost AI reference
GAME_ENTITIES = []

class Entity:
    def __init__(self, x, y, speed):
        self.x = x * TILE_SIZE + TILE_SIZE // 2  # Center position in pixels
        self.y = y * TILE_SIZE + TILE_SIZE // 2
        self.speed = speed
        self.direction = STOP
        self.intended_direction = STOP
        self.radius = TILE_SIZE // 2 - 2  # Slightly smaller than tile for collision
    
    def update(self, dt, maze):
        # Get current tile position
        tile_x, tile_y = self.get_tile_pos()
        
        # Check if we can change direction to the intended direction
        if self.intended_direction != self.direction and self.intended_direction != STOP:
            # Check if we're at a tile center or close enough to turn
            pixel_x = tile_x * TILE_SIZE + TILE_SIZE // 2
            pixel_y = tile_y * TILE_SIZE + TILE_SIZE // 2
            
            # If we're close to the center of the tile, we can try to change direction
            # Increasing tolerance from self.speed to self.speed * 1.5 to fix getting stuck
            if abs(self.x - pixel_x) < self.speed * 1.5 and abs(self.y - pixel_y) < self.speed * 1.5:
                # Snap to tile center for precise turning
                self.x = pixel_x
                self.y = pixel_y
                
                # Check if we can move in the intended direction
                next_x = tile_x + self.intended_direction[0]
                next_y = tile_y + self.intended_direction[1]
                
                if maze.can_move_to(next_x, next_y):
                    self.direction = self.intended_direction
        
        # Move in the current direction
        if self.direction != STOP:
            # Check if we can continue moving in the current direction
            next_tile_x = tile_x + self.direction[0]
            next_tile_y = tile_y + self.direction[1]
            
            # Handle wrap-around (tunnels)
            next_tile_x, next_tile_y = maze.handle_wrap_around(next_tile_x, next_tile_y)
            
            # Update position if we can move
            if maze.can_move_to(next_tile_x, next_tile_y):
                self.x += self.direction[0] * self.speed
                self.y += self.direction[1] * self.speed
                
                # Handle wrap-around in pixel coordinates
                if next_tile_x == 0 and self.direction[0] < 0 and tile_x == 0:
                    # Wrapping to right edge
                    self.x = (GRID_WIDTH - 1) * TILE_SIZE + TILE_SIZE // 2
                elif next_tile_x == GRID_WIDTH - 1 and self.direction[0] > 0 and tile_x == GRID_WIDTH - 1:
                    # Wrapping to left edge
                    self.x = TILE_SIZE // 2
    
    def get_tile_pos(self):
        # Convert pixel coordinates to tile coordinates
        tile_x = int(self.x // TILE_SIZE)
        tile_y = int(self.y // TILE_SIZE)
        return tile_x, tile_y
    
    def set_position(self, x, y):
        # Set position in tile coordinates
        self.x = x * TILE_SIZE + TILE_SIZE // 2
        self.y = y * TILE_SIZE + TILE_SIZE // 2
    
    def collides_with(self, other):
        # Check collision with another entity (using circle collision)
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.sqrt(dx*dx + dy*dy)
        return distance < (self.radius + other.radius)


class Pacman(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, PACMAN_SPEED)
        self.lives = INITIAL_LIVES
        self.power_mode = False
        self.power_timer = 0
        self.animation_frame = 0
        self.animation_speed = 0.15  # Controls how fast the mouth animates
        self.angle = 0  # Angle for drawing (based on direction)
    
    def update(self, dt, maze):
        # Update power mode timer
        if self.power_mode and self.power_timer > 0:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.power_mode = False
        
        # Update animation frame
        self.animation_frame += self.animation_speed
        if self.animation_frame >= 4:  # 4 frames in animation cycle
            self.animation_frame = 0
        
        # Update angle based on direction
        if self.direction == RIGHT:
            self.angle = 0
        elif self.direction == LEFT:
            self.angle = 180
        elif self.direction == UP:
            self.angle = 90
        elif self.direction == DOWN:
            self.angle = 270
        
        # Call parent's update method for movement
        super().update(dt, maze)
        
        # Check for pellet consumption
        tile_x, tile_y = self.get_tile_pos()
        return self.check_pellet_collision(maze, tile_x, tile_y)
    
    def handle_input(self, keys):
        # Handle keyboard input to set intended direction
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.intended_direction = UP
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.intended_direction = DOWN
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.intended_direction = LEFT
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.intended_direction = RIGHT
    
    def check_pellet_collision(self, maze, tile_x, tile_y):
        # Check if Pacman has eaten a pellet or power pellet
        pellet_type = maze.check_pellet(tile_x, tile_y)
        
        if pellet_type == PELLET:
            return PELLET_POINTS
        elif pellet_type == POWER_PELLET:
            self.power_mode = True
            self.power_timer = FRIGHTENED_TIME
            return POWER_PELLET_POINTS
        
        return 0  # No points if no pellet eaten
    
    def reset_position(self, maze):
        # Reset Pacman to starting position
        if maze.pacman_start_position:
            self.set_position(*maze.pacman_start_position)
        else:
            # Default position if no start position defined
            self.set_position(GRID_WIDTH // 2, GRID_HEIGHT - 5)
        
        self.direction = STOP
        self.intended_direction = STOP
    
    def draw(self, screen):
        # Draw Pacman with animated mouth
        # Animation frames control how open the mouth is
        mouth_angle = 45 * abs(2 - (self.animation_frame % 4))  # 0, 45, 90, 45 degree mouth opening
        
        # Draw yellow circle
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
        
        # Draw mouth (a pie slice cut out of the circle)
        if self.direction != STOP:  # Only animate mouth when moving
            # Starting point of the mouth arc
            start_angle = self.angle - mouth_angle
            # Ending point of the mouth arc
            end_angle = self.angle + mouth_angle
            
            # Draw wedge for mouth by drawing a pie slice of background color
            # Create points for the mouth wedge
            mouth_points = [(int(self.x), int(self.y))]  # Center point
            
            # Add points around the edge of the circle for the mouth
            for angle in range(int(start_angle), int(end_angle) + 1, 5):
                radians = math.radians(angle)
                mouth_points.append((int(self.x + self.radius * math.cos(radians)),
                                    int(self.y - self.radius * math.sin(radians))))
            
            # Draw the mouth wedge in black (same as background)
            if len(mouth_points) > 2:
                pygame.draw.polygon(screen, BLACK, mouth_points)


class Ghost(Entity):
    def __init__(self, x, y, ghost_type):
        # Different speeds for different states
        super().__init__(x, y, GHOST_SPEED)
        self.ghost_type = ghost_type
        self.current_state = SCATTER
        self.state_timer = SCATTER_TIME
        self.frightened_timer = 0
        self.eaten = False
        self.target_tile = None
        self.base_speed = GHOST_SPEED  # Store original speed
        self.animation_frame = 0
        self.respawn_timer = 0
        
        # Staggered exit times for different ghosts
        # Use index instead of adding directly since ghost_type is a string
        exit_delays = {BLINKY: 1, PINKY: 2, INKY: 3, CLYDE: 4}
        self.exit_timer = FPS * exit_delays.get(ghost_type, 2)  # Default to 2 if ghost type not found
        
        # Set color based on ghost type
        if ghost_type == BLINKY:
            self.color = RED
        elif ghost_type == PINKY:
            self.color = PINK
        elif ghost_type == INKY:
            self.color = CYAN
        elif ghost_type == CLYDE:
            self.color = ORANGE
    
    def update(self, dt, maze, pacman):
        # Update timers and state
        if self.current_state == FRIGHTENED and self.frightened_timer > 0:
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                # Revert to previous state when frightened mode ends
                self.current_state = SCATTER if self.state_timer > 0 else CHASE
                self.speed = self.base_speed
        elif self.current_state == EATEN:
            # If eaten, check if we've reached the ghost house
            tile_x, tile_y = self.get_tile_pos()
            if (tile_x, tile_y) in maze.ghost_house_positions:
                # Respawn after delay
                if self.respawn_timer <= 0:
                    self.current_state = SCATTER
                    self.state_timer = SCATTER_TIME
                    self.speed = self.base_speed
                    self.eaten = False
                else:
                    self.respawn_timer -= 1
                    return  # Don't move while respawning
        else:
            # Toggle between scatter and chase
            self.state_timer -= 1
            if self.state_timer <= 0:
                if self.current_state == SCATTER:
                    self.current_state = CHASE
                    self.state_timer = CHASE_TIME
                else:  # CHASE
                    self.current_state = SCATTER
                    self.state_timer = SCATTER_TIME
        
        # Update animation frame
        self.animation_frame = (self.animation_frame + 0.1) % 2
        
        # Get current tile position
        tile_x, tile_y = self.get_tile_pos()
        
        # Check if ghost is in the ghost house
        in_ghost_house = (tile_x, tile_y) in maze.ghost_house_positions
        
        # Handle ghost house exit logic
        if in_ghost_house and self.exit_timer > 0:
            self.exit_timer -= 1
            if self.exit_timer <= 0 or pacman.power_mode:
                # Time to exit the ghost house
                # Target the exit point (usually directly above the ghost house)
                exit_x, exit_y = min(maze.ghost_house_positions, key=lambda pos: pos[1])
                exit_y -= 2  # Position just above the ghost house
                
                # Set direction toward exit
                dx = 0
                dy = -1  # Move up to exit
                self.direction = (dx, dy)
                return  # Skip normal movement logic
            else:
                # Move randomly inside the ghost house until exit time
                if random.random() < 0.05:  # Occasionally change direction
                    self.direction = random.choice([LEFT, RIGHT, UP, DOWN])
                return  # Skip normal movement logic
        
        # Get target tile based on state
        if self.current_state == FRIGHTENED:
            # Random movement when frightened
            valid_directions = maze.get_valid_directions(tile_x, tile_y, self.direction)
            if valid_directions:
                # Choose random direction if at an intersection
                if maze.is_intersection(tile_x, tile_y) or self.direction == STOP:
                    self.direction = random.choice(valid_directions)
        elif self.current_state == EATEN:
            # Target the ghost house when eaten
            house_pos = random.choice(maze.ghost_house_positions) if maze.ghost_house_positions else (GRID_WIDTH // 2, GRID_HEIGHT // 2)
            self.target_tile = house_pos
            # Find best direction to reach the ghost house
            self.direction = self.get_best_direction(maze, tile_x, tile_y, house_pos)
        else:  # SCATTER or CHASE
            # Set target based on state and ghost type
            self.target_tile = self.get_target_tile(maze, pacman)
            # Find best direction to reach target
            next_direction = self.get_best_direction(maze, tile_x, tile_y, self.target_tile)
            
            # Only change direction at intersections or when hitting a wall
            if maze.is_intersection(tile_x, tile_y) or not maze.can_move_to(tile_x + self.direction[0], tile_y + self.direction[1]):
                self.direction = next_direction
        
        # Call parent's update method for movement
        super().update(dt, maze)
    
    def get_target_tile(self, maze, pacman):
        # Get target tile based on ghost type and current state
        pacman_tile_x, pacman_tile_y = pacman.get_tile_pos()
        
        if self.current_state == SCATTER:
            # Target scatter corner
            return maze.scatter_targets[self.ghost_type]
        
        # CHASE mode targeting logic
        if self.ghost_type == BLINKY:
            # Blinky targets Pacman directly
            return (pacman_tile_x, pacman_tile_y)
        
        elif self.ghost_type == PINKY:
            # Pinky targets 4 tiles ahead of Pacman
            dx, dy = pacman.direction
            return (pacman_tile_x + 4 * dx, pacman_tile_y + 4 * dy)
        
        elif self.ghost_type == INKY:
            # Inky uses Blinky's position
            # First, get position 2 tiles ahead of Pacman
            dx, dy = pacman.direction
            target_x = pacman_tile_x + 2 * dx
            target_y = pacman_tile_y + 2 * dy
            
            # Then, get vector from Blinky to this position and double it
            for ghost in [g for g in GAME_ENTITIES if isinstance(g, Ghost) and g.ghost_type == BLINKY]:
                blinky_x, blinky_y = ghost.get_tile_pos()
                vector_x = target_x - blinky_x
                vector_y = target_y - blinky_y
                return (target_x + vector_x, target_y + vector_y)
            
            # Fallback if Blinky not found
            return (target_x, target_y)
        
        elif self.ghost_type == CLYDE:
            # Clyde targets Pacman directly when far, and scatter corner when close
            clyde_x, clyde_y = self.get_tile_pos()
            distance = math.sqrt((clyde_x - pacman_tile_x)**2 + (clyde_y - pacman_tile_y)**2)
            
            if distance > 8:  # If more than 8 tiles away, chase Pacman
                return (pacman_tile_x, pacman_tile_y)
            else:  # Otherwise, go to scatter corner
                return maze.scatter_targets[self.ghost_type]
    
    def get_best_direction(self, maze, start_x, start_y, target):
        # Simple implementation: choose direction that brings us closest to target
        target_x, target_y = target
        
        # Get all valid directions (excluding reversing)
        valid_directions = maze.get_valid_directions(start_x, start_y, self.direction)
        
        if not valid_directions:
            # If no valid directions (cornered), allow reversing
            valid_directions = [UP, DOWN, LEFT, RIGHT]
            for direction in valid_directions.copy():
                dx, dy = direction
                if not maze.can_move_to(start_x + dx, start_y + dy):
                    valid_directions.remove(direction)
        
        # Find best direction by minimizing distance to target
        best_direction = None
        best_distance = float('inf')
        
        for direction in valid_directions:
            dx, dy = direction
            new_x, new_y = start_x + dx, start_y + dy
            distance = math.sqrt((new_x - target_x)**2 + (new_y - target_y)**2)
            
            if distance < best_distance:
                best_distance = distance
                best_direction = direction
        
        return best_direction or STOP
    
    def set_frightened(self):
        # Set ghost to frightened mode
        if self.current_state != EATEN:  # Only frighten if not already eaten
            self.current_state = FRIGHTENED
            self.frightened_timer = FRIGHTENED_TIME
            self.speed = GHOST_FRIGHTENED_SPEED
            
            # Immediately reverse direction when frightened
            if self.direction != STOP:
                self.direction = (-self.direction[0], -self.direction[1])
    
    def set_eaten(self):
        # Set ghost to eaten mode
        self.current_state = EATEN
        self.eaten = True
        self.speed = GHOST_EATEN_SPEED
        self.frightened_timer = 0
        self.respawn_timer = FPS * 3  # 3 seconds to respawn
    
    def reset_position(self, maze):
        # Reset ghost to starting position in ghost house
        if maze.ghost_house_positions:
            pos = random.choice(maze.ghost_house_positions)
            self.set_position(*pos)
        else:
            # Default position if no ghost house defined
            self.set_position(GRID_WIDTH // 2, GRID_HEIGHT // 2)
        
        self.direction = STOP
        self.current_state = SCATTER
        self.state_timer = SCATTER_TIME
        self.frightened_timer = 0
        self.eaten = False
        self.speed = self.base_speed
    
    def draw(self, screen):
        # Draw ghost body
        if self.current_state == FRIGHTENED:
            # Flashing blue/white when frightened mode is ending
            if self.frightened_timer < FPS * 2 and self.frightened_timer % 20 < 10:
                color = WHITE_FRIGHTENED
            else:
                color = BLUE_FRIGHTENED
        elif self.current_state == EATEN:
            # Just draw eyes when eaten
            self.draw_eyes(screen)
            return
        else:
            color = self.color
        
        # Draw ghost body (circle with rectangle bottom)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.rect(screen, color, 
                        (int(self.x - self.radius), int(self.y), 
                        self.radius * 2, self.radius))
        
        # Draw scalloped bottom (creates the wavy effect at bottom of ghost)
        wave_height = self.radius // 2
        wave_width = self.radius // 2
        bottom_y = int(self.y + self.radius)
        
        for i in range(4):  # Draw 4 waves at bottom
            center_x = int(self.x - self.radius + (i + 0.5) * wave_width)
            # Draw half-circle cutouts at bottom of ghost
            pygame.draw.circle(screen, BLACK, 
                             (center_x, bottom_y), 
                             wave_height // 2)
        
        # Draw eyes
        self.draw_eyes(screen)
    
    def draw_eyes(self, screen):
        # Draw the ghost's eyes based on direction
        eye_radius = self.radius // 3
        eye_offset_x = self.radius // 2
        eye_offset_y = -self.radius // 4
        
        # Left eye position
        left_eye_x = int(self.x - eye_offset_x)
        left_eye_y = int(self.y + eye_offset_y)
        
        # Right eye position
        right_eye_x = int(self.x + eye_offset_x)
        right_eye_y = int(self.y + eye_offset_y)
        
        # Draw white part of eyes
        pygame.draw.circle(screen, WHITE, (left_eye_x, left_eye_y), eye_radius)
        pygame.draw.circle(screen, WHITE, (right_eye_x, right_eye_y), eye_radius)
        
        # Draw pupils based on direction
        pupil_radius = eye_radius // 2
        pupil_offset = eye_radius // 2
        
        # Determine pupil offset based on direction
        pupil_dx, pupil_dy = 0, 0
        if self.direction == LEFT:
            pupil_dx = -pupil_offset
        elif self.direction == RIGHT:
            pupil_dx = pupil_offset
        elif self.direction == UP:
            pupil_dy = -pupil_offset
        elif self.direction == DOWN:
            pupil_dy = pupil_offset
        
        # Draw pupils
        pygame.draw.circle(screen, BLUE, 
                         (left_eye_x + pupil_dx, left_eye_y + pupil_dy), 
                         pupil_radius)
        pygame.draw.circle(screen, BLUE, 
                         (right_eye_x + pupil_dx, right_eye_y + pupil_dy), 
                         pupil_radius)
