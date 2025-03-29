import pygame
import math
import random
from constants import *

class Entity:
    def __init__(self, x, y, speed):
        # Position in pixel coordinates
        self.x = x * TILE_SIZE + TILE_SIZE // 2
        self.y = y * TILE_SIZE + TILE_SIZE // 2
        self.speed = speed
        self.direction = STOP
        self.next_direction = STOP
        self.radius = TILE_SIZE // 2 - 2
    
    def get_tile_pos(self):
        """Convert pixel coordinates to tile coordinates."""
        return (int(self.x // TILE_SIZE), int(self.y // TILE_SIZE))
    
    def is_at_intersection(self):
        """Check if entity is at a tile center (for direction changes)."""
        # Check if entity is close to the center of a tile
        pixel_x = self.x % TILE_SIZE
        pixel_y = self.y % TILE_SIZE
        return abs(pixel_x - TILE_SIZE//2) < 3 and abs(pixel_y - TILE_SIZE//2) < 3
    
    def handle_wrap_around(self):
        """Handle wrap-around tunnels on the left and right of the maze."""
        # Wrap around horizontally (tunnels)
        if self.y // TILE_SIZE == 14:  # Middle row with tunnels
            if self.x < 0:  # Left tunnel
                self.x = SCREEN_WIDTH - 1
            elif self.x >= SCREEN_WIDTH:  # Right tunnel
                self.x = 0
    
    def move(self, dt, maze):
        """Move the entity according to its direction and speed."""
        # Calculate distance to move
        dist = self.speed * dt / 1000  # Convert milliseconds to seconds
        
        # Try to change direction, even if not exactly at an intersection
        if self.next_direction != STOP and self.next_direction != self.direction:
            # Get current and next tile positions
            current_tile = self.get_tile_pos()
            next_tile = (current_tile[0] + self.next_direction[0], 
                        current_tile[1] + self.next_direction[1])
            
            # Try to change direction if possible
            if maze.can_move_to(*next_tile):
                # For Pacman's smoother turning, we should be at/near an intersection
                # or along the same axis as the turn
                can_turn = self.is_at_intersection()
                
                # Allow turning at any point along the same axis
                # (e.g., going left/right and want to go up/down at a column)
                if (self.direction[0] != 0 and self.next_direction[0] == 0 and 
                    abs(self.x % TILE_SIZE - TILE_SIZE//2) < 5):
                    can_turn = True
                # Going up/down and want to go left/right at a row
                elif (self.direction[1] != 0 and self.next_direction[1] == 0 and 
                      abs(self.y % TILE_SIZE - TILE_SIZE//2) < 5):
                    can_turn = True
                
                if can_turn:
                    # Correct position to align with the grid when turning
                    if self.next_direction[0] == 0:  # turning to go up/down
                        self.x = current_tile[0] * TILE_SIZE + TILE_SIZE//2
                    if self.next_direction[1] == 0:  # turning to go left/right
                        self.y = current_tile[1] * TILE_SIZE + TILE_SIZE//2
                        
                    self.direction = self.next_direction
        
        # Move according to current direction
        new_x = self.x + self.direction[0] * dist
        new_y = self.y + self.direction[1] * dist
        
        # Check if movement in current direction is valid
        next_tile = (int(new_x // TILE_SIZE), int(new_y // TILE_SIZE))
        if maze.can_move_to(*next_tile):
            self.x = new_x
            self.y = new_y
        else:
            # Allow trying the queued direction instead of stopping
            if self.next_direction != STOP and self.next_direction != self.direction:
                # Try the next direction
                alt_x = self.x + self.next_direction[0] * dist
                alt_y = self.y + self.next_direction[1] * dist
                alt_tile = (int(alt_x // TILE_SIZE), int(alt_y // TILE_SIZE))
                
                if maze.can_move_to(*alt_tile):
                    self.direction = self.next_direction
                    self.x = alt_x
                    self.y = alt_y
            # Only stop if we can't move in either direction
            else:
                # Don't completely stop at walls, just prevent movement
                pass
        
        # Handle tunnels
        self.handle_wrap_around()

class Pacman(Entity):
    def __init__(self, maze):
        super().__init__(*maze.pacman_spawn, PACMAN_SPEED)
        self.lives = INITIAL_LIVES
        self.power_mode = False
        self.power_timer = 0
        self.mouth_open = True
        self.animation_timer = 0
        self.stuck_timer = 0  # Track how long Pacman has been stuck
    
    def update(self, dt, maze, score_manager):
        """Update Pac-Man's position and state."""
        # Save current position to check if we actually moved
        prev_x, prev_y = self.x, self.y
        
        # Update movement
        self.move(dt, maze)
        
        # Check if Pacman is stuck (hasn't moved and tried to move)
        if self.direction != STOP and abs(self.x - prev_x) < 0.1 and abs(self.y - prev_y) < 0.1:
            self.stuck_timer += dt
            # If stuck for more than 200ms, try to align to grid
            if self.stuck_timer > 200:
                # Align to grid to help unstick
                tile_x, tile_y = self.get_tile_pos()
                self.x = tile_x * TILE_SIZE + TILE_SIZE // 2
                self.y = tile_y * TILE_SIZE + TILE_SIZE // 2
                # Try alternate direction if available
                if self.next_direction != STOP and self.next_direction != self.direction:
                    # Check if next direction is valid
                    next_tile = (tile_x + self.next_direction[0], tile_y + self.next_direction[1])
                    if maze.can_move_to(*next_tile):
                        self.direction = self.next_direction
                self.stuck_timer = 0
        else:
            # Reset stuck timer if moving
            self.stuck_timer = 0
        
        # Handle pellet collisions
        self.check_pellet_collision(maze, score_manager)
        
        # Update power mode timer
        if self.power_mode:
            self.power_timer -= dt
            if self.power_timer <= 0:
                self.power_mode = False
                self.power_timer = 0
        
        # Update animation
        self.animation_timer += dt
        if self.animation_timer >= 150:  # Change every 150ms
            self.mouth_open = not self.mouth_open
            self.animation_timer = 0
    
    def handle_input(self, keys):
        """Process keyboard input for direction changes."""
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.next_direction = UP
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.next_direction = DOWN
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.next_direction = LEFT
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.next_direction = RIGHT
    
    def check_pellet_collision(self, maze, score_manager):
        """Check if Pac-Man is on a pellet and consume it."""
        tile_x, tile_y = self.get_tile_pos()
        points = maze.eat_pellet(tile_x, tile_y)
        
        if points > 0:
            score_manager.add_points(points)
            
            # Check if it was a power pellet
            if points == POWER_PELLET_POINTS:
                self.power_mode = True
                self.power_timer = FRIGHTENED_TIME
                return True  # Signal that a power pellet was eaten
        
        return False
    
    def reset_position(self, maze):
        """Reset Pac-Man to starting position."""
        self.x = maze.pacman_spawn[0] * TILE_SIZE + TILE_SIZE // 2
        self.y = maze.pacman_spawn[1] * TILE_SIZE + TILE_SIZE // 2
        self.direction = STOP
        self.next_direction = STOP
    
    def draw(self, screen):
        """Draw Pac-Man with proper orientation and animation."""
        # Calculate angle based on direction
        angle = 0
        if self.direction == RIGHT:
            angle = 0
        elif self.direction == DOWN:
            angle = 90
        elif self.direction == LEFT:
            angle = 180
        elif self.direction == UP:
            angle = 270
        
        # Draw Pac-Man's circle
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
        
        # Draw mouth if open (as a triangle to create the pie shape)
        if self.mouth_open and self.direction != STOP:
            # Start angle and span angle (in radians)
            start_angle = math.radians(angle - 45)
            end_angle = math.radians(angle + 45)
            
            # Calculate points for the triangle (mouth)
            points = [
                (self.x, self.y),
                (self.x + self.radius * math.cos(start_angle),
                 self.y + self.radius * math.sin(start_angle)),
                (self.x + self.radius * math.cos(end_angle),
                 self.y + self.radius * math.sin(end_angle))
            ]
            
            # Draw the triangle in black (creating the mouth effect)
            pygame.draw.polygon(screen, BLACK, points)

class Ghost(Entity):
    # Ghost states
    SCATTER = 0
    CHASE = 1
    FRIGHTENED = 2
    EATEN = 3
    
    def __init__(self, ghost_type, maze):
        self.ghost_type = ghost_type
        spawn_pos = maze.ghost_spawns[ghost_type]
        super().__init__(*spawn_pos, GHOST_SPEED)
        
        # Set initial state
        self.current_state = self.SCATTER
        self.state_timer = SCATTER_TIME
        self.frightened_timer = 0
        self.eaten_timer = 0
        
        # Set color based on ghost type
        if ghost_type == "blinky":
            self.color = RED
        elif ghost_type == "pinky":
            self.color = PINK
        elif ghost_type == "inky":
            self.color = CYAN
        elif ghost_type == "clyde":
            self.color = ORANGE
    
    def update(self, dt, maze, pacman):
        """Update ghost state and movement."""
        # Save current position to check if we actually moved
        prev_x, prev_y = self.x, self.y
        prev_tile = self.get_tile_pos()
        
        # If ghost is stuck with STOP direction in ghost house, initialize movement
        if self.direction == STOP and maze.is_ghost_house(*prev_tile):
            # Choose a valid initial direction to exit the ghost house
            exit_directions = [UP, LEFT, RIGHT]  # Prefer UP to exit
            for d in exit_directions:
                next_tile = (prev_tile[0] + d[0], prev_tile[1] + d[1])
                if maze.can_move_to(*next_tile):
                    self.direction = d
                    self.next_direction = d
                    break
        
        # Update state timers
        if self.current_state == self.FRIGHTENED:
            self.frightened_timer -= dt
            if self.frightened_timer <= 0:
                self.set_state(self.SCATTER)
        elif self.current_state == self.EATEN:
            self.eaten_timer -= dt
            if self.eaten_timer <= 0:
                self.set_state(self.SCATTER)
        else:  # SCATTER or CHASE
            self.state_timer -= dt
            if self.state_timer <= 0:
                # Toggle between scatter and chase
                if self.current_state == self.SCATTER:
                    self.set_state(self.CHASE)
                else:
                    self.set_state(self.SCATTER)
        
        # Determine target based on current state
        target = self.get_target_tile(maze, pacman)
        
        # Choose direction either at intersections or if currently stopped
        if self.is_at_intersection() or self.direction == STOP:
            self.choose_direction(maze, target)
        # Also choose new direction if we're about to hit a wall
        else:
            next_tile = (
                int((self.x + self.direction[0] * 5) // TILE_SIZE),
                int((self.y + self.direction[1] * 5) // TILE_SIZE)
            )
            if not maze.can_move_to(*next_tile):
                self.choose_direction(maze, target)
        
        # Move the ghost
        # Override the speed based on state
        original_speed = self.speed
        if self.current_state == self.FRIGHTENED:
            self.speed = FRIGHTENED_SPEED
        elif self.current_state == self.EATEN:
            self.speed = EATEN_SPEED
        
        self.move(dt, maze)
        
        # Check if ghost is stuck (hasn't moved)
        current_tile = self.get_tile_pos()
        if (abs(self.x - prev_x) < 0.1 and abs(self.y - prev_y) < 0.1 and
            self.direction != STOP):
            # Align to grid to help unstick
            self.x = current_tile[0] * TILE_SIZE + TILE_SIZE // 2
            self.y = current_tile[1] * TILE_SIZE + TILE_SIZE // 2
            
            # Try a different direction
            possible_dirs = [UP, DOWN, LEFT, RIGHT]
            random.shuffle(possible_dirs)  # Randomize to break patterns
            
            for d in possible_dirs:
                next_tile = (current_tile[0] + d[0], current_tile[1] + d[1])
                if maze.can_move_to(*next_tile) and d != self.direction:
                    self.direction = d
                    self.next_direction = d
                    break
        
        # Restore original speed
        self.speed = original_speed
        
        # Check if eaten ghost reached the ghost house
        if self.current_state == self.EATEN and maze.is_ghost_house(*self.get_tile_pos()):
            self.set_state(self.SCATTER)
    
    def set_state(self, state, timer=None):
        """Change the ghost's state and reset appropriate timers."""
        # Don't change state if already in that state
        if self.current_state == state:
            return
        
        self.current_state = state
        
        # Set appropriate timer
        if state == self.SCATTER:
            self.state_timer = timer or SCATTER_TIME
        elif state == self.CHASE:
            self.state_timer = timer or CHASE_TIME
        elif state == self.FRIGHTENED:
            self.frightened_timer = timer or FRIGHTENED_TIME
            # Reverse direction when entering frightened mode
            if self.direction != STOP:
                self.reverse_direction()
        elif state == self.EATEN:
            self.eaten_timer = 5000  # 5 seconds to return to ghost house
    
    def reverse_direction(self):
        """Reverse the ghost's current direction."""
        self.direction = (-self.direction[0], -self.direction[1])
        self.next_direction = self.direction
    
    def get_target_tile(self, maze, pacman):
        """Determine the target tile based on ghost type and state."""
        # If in ghost house and not eaten, target exit point above ghost house
        if maze.is_ghost_house(*self.get_tile_pos()) and self.current_state != self.EATEN:
            # A point above the ghost house to encourage ghosts to leave
            return (14, 11)  # Exit point above ghost house
        
        if self.current_state == self.FRIGHTENED:
            # Random target when frightened but don't target walls
            while True:
                target = (random.randint(1, GRID_WIDTH-2), random.randint(1, GRID_HEIGHT-2))
                if not maze.is_wall(*target):
                    return target
        
        elif self.current_state == self.EATEN:
            # Target is the ghost house when eaten
            return maze.ghost_spawns[self.ghost_type]
        
        elif self.current_state == self.SCATTER:
            # Target the ghost's corner in scatter mode
            return maze.scatter_targets[self.ghost_type]
        
        else:  # CHASE mode - each ghost has different targeting strategy
            pacman_tile = pacman.get_tile_pos()
            
            if self.ghost_type == "blinky":  # Red - direct chase
                return pacman_tile
            
            elif self.ghost_type == "pinky":  # Pink - ahead of Pacman
                # Target 4 tiles ahead of Pacman
                target_x = pacman_tile[0] + 4 * pacman.direction[0]
                target_y = pacman_tile[1] + 4 * pacman.direction[1]
                
                # Special case for the infamous "up" bug in the original game
                if pacman.direction == UP:
                    target_x -= 4  # Shift left by 4 tiles
                
                # Make sure target is within bounds
                target_x = max(0, min(GRID_WIDTH-1, target_x))
                target_y = max(0, min(GRID_HEIGHT-1, target_y))
                
                return (target_x, target_y)
            
            elif self.ghost_type == "inky":  # Cyan - uses Blinky's position
                # Find Blinky's position (if we can)
                blinky_pos = None
                from main import PacmanGame
                for ghost in pacman.ghosts if hasattr(pacman, 'ghosts') else []:
                    if ghost.ghost_type == "blinky":
                        blinky_pos = ghost.get_tile_pos()
                        break
                
                # If we can't find Blinky, use fixed position
                if not blinky_pos:
                    blinky_x, blinky_y = (14, 11)  # Center of maze
                else:
                    blinky_x, blinky_y = blinky_pos
                
                # Target is based on a vector from Blinky to a point ahead of Pacman
                ahead_x = pacman_tile[0] + 2 * pacman.direction[0]
                ahead_y = pacman_tile[1] + 2 * pacman.direction[1]
                
                # Special case for the "up" bug
                if pacman.direction == UP:
                    ahead_x -= 2
                
                # The target is the reflection of the ahead point about Blinky
                target_x = 2 * ahead_x - blinky_x
                target_y = 2 * ahead_y - blinky_y
                
                # Make sure target is within bounds
                target_x = max(0, min(GRID_WIDTH-1, target_x))
                target_y = max(0, min(GRID_HEIGHT-1, target_y))
                
                return (target_x, target_y)
            
            elif self.ghost_type == "clyde":  # Orange - shy
                # Target Pacman directly if far away, otherwise go to scatter corner
                pacman_dist = math.sqrt((self.x - pacman.x)**2 + (self.y - pacman.y)**2)
                if pacman_dist > 8 * TILE_SIZE:  # If more than 8 tiles away
                    return pacman_tile
                else:
                    return maze.scatter_targets[self.ghost_type]
        
        # Default failsafe
        return pacman.get_tile_pos()
    
    def choose_direction(self, maze, target):
        """Choose the best direction to reach the target."""
        current_tile = self.get_tile_pos()
        
        # Special case for ghost house - prioritize moving upward to exit
        if maze.is_ghost_house(*current_tile) and self.current_state != self.EATEN:
            # First try UP to exit
            next_tile = (current_tile[0], current_tile[1] - 1)
            if maze.can_move_to(*next_tile):
                self.next_direction = UP
                return
        
        # Possible directions (excluding the opposite of current direction)
        possible_dirs = [UP, DOWN, LEFT, RIGHT]
        
        # Remove the opposite direction to prevent backtracking
        # (unless stopped, in frightened mode, or stuck)
        if (self.direction != STOP and 
            self.current_state != self.FRIGHTENED):
            opposite = (-self.direction[0], -self.direction[1])
            if opposite in possible_dirs:
                possible_dirs.remove(opposite)
        
        # Filter out invalid directions (walls)
        valid_dirs = []
        for d in possible_dirs:
            next_tile = (current_tile[0] + d[0], current_tile[1] + d[1])
            if maze.can_move_to(*next_tile):
                valid_dirs.append(d)
        
        # If no valid directions (should rarely happen), allow backing up
        if not valid_dirs:
            # Try again with all directions
            for d in [UP, DOWN, LEFT, RIGHT]:
                next_tile = (current_tile[0] + d[0], current_tile[1] + d[1])
                if maze.can_move_to(*next_tile):
                    valid_dirs.append(d)
        
        # Still no valid directions (should never happen)
        if not valid_dirs:
            # Just maintain current direction or stop if that's not possible
            next_tile = (current_tile[0] + self.direction[0], current_tile[1] + self.direction[1])
            if maze.can_move_to(*next_tile):
                self.next_direction = self.direction
            else:
                self.next_direction = STOP
            return
        
        if self.current_state == self.FRIGHTENED:
            # Choose a random valid direction when frightened
            # But with small chance to make better choice to avoid getting stuck
            if random.random() < 0.8:  # 80% chance for random move
                self.next_direction = random.choice(valid_dirs)
            else:
                # 20% chance to move toward a valid target
                # Choose the direction that gets closest to pacman's opposite side
                best_dir = None
                best_dist = -float('inf')  # Note: maximizing distance in frightened mode
                
                for d in valid_dirs:
                    next_tile = (current_tile[0] + d[0], current_tile[1] + d[1])
                    dist = math.sqrt((next_tile[0] - target[0])**2 + 
                                    (next_tile[1] - target[1])**2)
                    
                    if dist > best_dist:
                        best_dist = dist
                        best_dir = d
                
                self.next_direction = best_dir
        else:
            # Choose the direction that gets closest to the target
            best_dir = None
            best_dist = float('inf')
            
            for d in valid_dirs:
                next_tile = (current_tile[0] + d[0], current_tile[1] + d[1])
                dist = math.sqrt((next_tile[0] - target[0])**2 + 
                                (next_tile[1] - target[1])**2)
                
                if dist < best_dist:
                    best_dist = dist
                    best_dir = d
            
            self.next_direction = best_dir
    
    def draw(self, screen):
        """Draw the ghost with the appropriate color and state."""
        # Draw different colors based on state
        if self.current_state == self.FRIGHTENED:
            # Draw blue ghost (frightened)
            color = BLUE
        elif self.current_state == self.EATEN:
            # Draw eyes only
            color = None
        else:
            color = self.color
        
        # Draw ghost body
        if color:  # Skip body for EATEN state
            # Draw ghost shape (semi-circle + rectangle with wavy bottom)
            # Semi-circle for top half
            pygame.draw.circle(screen, color, (int(self.x), int(self.y) - TILE_SIZE//6), 
                             self.radius)
            
            # Rectangle for bottom half
            pygame.draw.rect(screen, color, 
                          (int(self.x) - self.radius, int(self.y) - TILE_SIZE//6, 
                           2 * self.radius, self.radius + TILE_SIZE//6))
        
        # Draw eyes (white circles with black pupils)
        eye_offset_x = 4
        if self.direction == LEFT:
            eye_offset_x = -4
        
        # Eye positions
        left_eye_pos = (int(self.x) - eye_offset_x - 3, int(self.y) - 4)
        right_eye_pos = (int(self.x) + eye_offset_x + 3, int(self.y) - 4)
        
        # Draw eyes (white with black pupils)
        pygame.draw.circle(screen, WHITE, left_eye_pos, 3)
        pygame.draw.circle(screen, WHITE, right_eye_pos, 3)
        
        # Eye direction
        pupil_offset_x = 1
        pupil_offset_y = 0
        
        if self.direction == LEFT:
            pupil_offset_x = -1
        elif self.direction == UP:
            pupil_offset_x = 0
            pupil_offset_y = -1
        elif self.direction == DOWN:
            pupil_offset_x = 0
            pupil_offset_y = 1
        
        # Draw pupils
        pygame.draw.circle(screen, BLACK, 
                         (left_eye_pos[0] + pupil_offset_x, 
                          left_eye_pos[1] + pupil_offset_y), 1)
        pygame.draw.circle(screen, BLACK, 
                         (right_eye_pos[0] + pupil_offset_x, 
                          right_eye_pos[1] + pupil_offset_y), 1)
