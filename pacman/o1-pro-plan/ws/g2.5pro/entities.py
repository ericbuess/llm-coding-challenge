# entities.py
# Contains classes for Pacman, Ghost, and a base Entity class.

import pygame
from constants import *
import random # For frightened ghost movement
import pygame.sprite # Import the sprite module
import math

class Entity(pygame.sprite.Sprite): # Inherit from Sprite
    def __init__(self, x, y, speed, color):
        pygame.sprite.Sprite.__init__(self) # Initialize the Sprite base class
        self.x = x * TILE_SIZE # Initial position in pixels
        self.y = y * TILE_SIZE
        self.speed = speed
        self.color = color
        self.direction = STOP
        self.intended_direction = STOP
        self.radius = TILE_SIZE // 2 - 1 # Simple circle representation for now

    def get_tile_pos(self):
        # Calculate the center of the entity for more accurate tile positioning
        center_x = self.x + TILE_SIZE // 2
        center_y = self.y + TILE_SIZE // 2
        tile_x = int(center_x // TILE_SIZE)
        tile_y = int(center_y // TILE_SIZE)
        return tile_x, tile_y

    def is_at_intersection(self):
        # Check if the entity is centered on a tile (allowing turns)
        # Use a small tolerance to account for floating point inaccuracies
        tolerance = self.speed * (1/FPS) / 2 # Tolerance based on movement per frame
        tile_center_x = (self.x + TILE_SIZE / 2) / TILE_SIZE
        tile_center_y = (self.y + TILE_SIZE / 2) / TILE_SIZE
        return abs(tile_center_x - round(tile_center_x)) < tolerance and \
               abs(tile_center_y - round(tile_center_y)) < tolerance

    def snap_to_grid(self):
         # When at an intersection, snap precisely to the grid center
         if self.is_at_intersection():
             tile_x, tile_y = self.get_tile_pos()
             self.x = tile_x * TILE_SIZE
             self.y = tile_y * TILE_SIZE

    def get_next_tile(self, direction):
        current_tile_x, current_tile_y = self.get_tile_pos()
        next_tile_x = current_tile_x + direction[0]
        next_tile_y = current_tile_y + direction[1]
        return next_tile_x, next_tile_y

    def can_move(self, direction, maze):
        next_tile_x, next_tile_y = self.get_next_tile(direction)
        # Handle tunnels
        if next_tile_y == 14: # Assuming tunnel row is 14
             if next_tile_x < 0:
                  return True # Allow moving into left tunnel
             if next_tile_x >= GRID_WIDTH:
                  return True # Allow moving into right tunnel
        return maze.can_move_to(next_tile_x, next_tile_y)

    def handle_tunnels(self):
         # If entity is in the tunnel row and goes off screen, wrap around
         current_tile_x, current_tile_y = self.get_tile_pos()
         if current_tile_y == 14: # Assuming tunnel row is 14
              if self.x < -TILE_SIZE:
                   self.x = (GRID_WIDTH - 1) * TILE_SIZE
              elif self.x > GRID_WIDTH * TILE_SIZE:
                   self.x = -TILE_SIZE + TILE_SIZE # Start slightly off-screen left

    def update_direction(self, maze):
        # Check if at an intersection and intended direction is valid
        if self.is_at_intersection():
            self.snap_to_grid() # Align perfectly before checking turns
            if self.intended_direction != STOP and self.can_move(self.intended_direction, maze):
                self.direction = self.intended_direction
            # If current direction becomes invalid (shouldn't happen often unless maze changes)
            elif not self.can_move(self.direction, maze):
                 self.direction = STOP

    def move(self, dt):
        # Move based on current direction and speed
        if self.direction != STOP:
            delta = self.speed * dt
            self.x += self.direction[0] * delta
            self.y += self.direction[1] * delta
            self.handle_tunnels() # Check for tunnel wrapping after movement

    def update(self, dt, maze):
        self.update_direction(maze)
        self.move(dt)

    def draw(self, screen):
        # Simple circle representation
        center_x = int(self.x + TILE_SIZE // 2)
        center_y = int(self.y + TILE_SIZE // 2)
        pygame.draw.circle(screen, self.color, (center_x, center_y), self.radius)


class Pacman(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, PACMAN_SPEED, YELLOW)
        self.lives = 3
        self.power_mode = False
        self.power_timer = 0
        self.score_multiplier = 0 # For sequential ghost eating
        # Animation properties
        self.animation_timer = 0
        self.animation_frame = 0  # 0-2 for mouth animation (closed, half-open, fully open)
        self.frames_per_second = 10  # Animation speed
        self.mouth_angle = 0  # For the pacman's mouth angle based on direction

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.intended_direction = UP
            elif event.key == pygame.K_DOWN:
                self.intended_direction = DOWN
            elif event.key == pygame.K_LEFT:
                self.intended_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                self.intended_direction = RIGHT

    def update(self, dt, maze, score_manager):
        # Update animation
        if self.direction != STOP:
            self.animation_timer += dt
            if self.animation_timer >= 1.0 / self.frames_per_second:
                self.animation_frame = (self.animation_frame + 1) % 3  # Cycle through 0, 1, 2
                self.animation_timer = 0
        else:
            # Reset animation when not moving
            self.animation_frame = 0
            
        # Set mouth angle based on direction
        if self.direction == RIGHT:
            self.mouth_angle = 0
        elif self.direction == DOWN:
            self.mouth_angle = 90
        elif self.direction == LEFT:
            self.mouth_angle = 180
        elif self.direction == UP:
            self.mouth_angle = 270
            
        super().update(dt, maze)
        self.check_pellet_collision(maze, score_manager)

        # Update power mode timer
        if self.power_mode:
            self.power_timer -= dt
            if self.power_timer <= 0:
                self.power_mode = False
                print("Power mode ended") # Debug
                self.score_multiplier = 0 # Reset ghost score multiplier
                # TODO: Signal ghosts to stop being frightened

    def check_pellet_collision(self, maze, score_manager):
        tile_x, tile_y = self.get_tile_pos()
        eaten_type = maze.eat_pellet(tile_x, tile_y)
        if eaten_type == 'pellet':
            score_manager.add_score(PELLET_POINTS)
            # TODO: Play sound
        elif eaten_type == 'power_pellet':
            score_manager.add_score(POWER_PELLET_POINTS)
            self.activate_power_mode()
            # TODO: Play sound, signal ghosts to become frightened

    def activate_power_mode(self):
        print("Power mode activated!") # Debug
        self.power_mode = True
        self.power_timer = FRIGHTENED_DURATION
        self.score_multiplier = 0 # Reset for the new power pellet sequence

    def lose_life(self):
        self.lives -= 1
        print(f"Lost a life! Lives remaining: {self.lives}") # Debug
        # TODO: Reset position, play death animation/sound
        if self.lives <= 0:
            return True # Game Over
        self.reset_position() # Implement reset_position
        return False

    def reset_position(self):
        # TODO: Define starting position (e.g., from maze data)
        start_x, start_y = 14, 23 # Example starting tile
        self.x = start_x * TILE_SIZE
        self.y = start_y * TILE_SIZE
        self.direction = STOP
        self.intended_direction = STOP

    def draw(self, screen):
        # Draw Pac-Man with animation
        center_x = int(self.x + TILE_SIZE // 2)
        center_y = int(self.y + TILE_SIZE // 2)
        
        # Draw yellow circle
        pygame.draw.circle(screen, YELLOW, (center_x, center_y), self.radius)
        
        # Draw mouth animation based on frame and direction
        if self.animation_frame == 0:
            # Closed mouth (just a full circle)
            pass
        else:
            # Open mouth - angle depends on direction
            # Animation frame determines how wide the mouth opens
            mouth_size = 60 if self.animation_frame == 1 else 90  # Half or fully open
            
            # Draw a pie shape by removing a triangle from the circle
            # The start_angle and stop_angle control the mouth direction and size
            start_angle = (self.mouth_angle - mouth_size // 2) % 360
            stop_angle = (self.mouth_angle + mouth_size // 2) % 360
            
            # Convert angles to radians for pygame
            start_radians = math.radians(start_angle)
            stop_radians = math.radians(stop_angle)
            
            # Draw a black triangle to create the mouth effect
            points = [
                (center_x, center_y),
                (center_x + self.radius * math.cos(start_radians),
                 center_y - self.radius * math.sin(start_radians)),
                (center_x + self.radius * math.cos(stop_radians),
                 center_y - self.radius * math.sin(stop_radians))
            ]
            pygame.draw.polygon(screen, BLACK, points)


class Ghost(Entity):
    # States
    SCATTER = 0
    CHASE = 1
    FRIGHTENED = 2
    EATEN = 3

    def __init__(self, x, y, color, ghost_type):
        speed = GHOST_SPEED # Default speed
        super().__init__(x, y, speed, color) # This now correctly calls Entity.__init__, which calls Sprite.__init__
        self.ghost_type = ghost_type # e.g., 'blinky', 'pinky', etc.
        self.state = Ghost.SCATTER # Initial state
        self.previous_state = Ghost.SCATTER  # For returning from frightened mode
        self.state_timer = 0
        self.frightened_timer = 0
        self.mode_cycle = 0  # To track which scatter/chase cycle we're in
        self.target_tile = None
        self.scatter_target = self._get_scatter_target() # Corner tile
        self.home_tile = (13, 14) # Ghost house entrance/exit approx
        self.respawn_tile = (13, 11) # Inside the ghost house
        
        # Animation frames for different states
        self.animation_timer = 0
        self.animation_frame = 0
        self.frames_per_second = 8  # Animation speed

    def _get_scatter_target(self):
        # Define scatter corners for each ghost
        if self.ghost_type == 'blinky': return (GRID_WIDTH - 2, 0) # Top right
        if self.ghost_type == 'pinky': return (1, 0) # Top left
        if self.ghost_type == 'inky': return (GRID_WIDTH - 2, GRID_HEIGHT - 2) # Bottom right
        if self.ghost_type == 'clyde': return (1, GRID_HEIGHT - 2) # Bottom left
        return (0, 0) # Default

    def update(self, dt, maze, pacman_pos, pacman_dir, blinky_pos=None):
        # Update animation
        self.animation_timer += dt
        if self.animation_timer >= 1.0 / self.frames_per_second:
            self.animation_frame = (self.animation_frame + 1) % 2  # Toggle between 0 and 1
            self.animation_timer = 0
            
        # State Timers
        if self.state == Ghost.FRIGHTENED:
            self.speed = GHOST_SPEED_FRIGHTENED
            self.frightened_timer -= dt
            if self.frightened_timer <= 0:
                self.set_state(self.previous_state) # Revert to scatter/chase
        elif self.state == Ghost.EATEN:
            self.speed = GHOST_SPEED_EATEN
            # Move towards respawn point
            self.target_tile = self.respawn_tile
            current_tile = self.get_tile_pos()
            if current_tile == self.respawn_tile:
                print(f"{self.ghost_type} respawned!") # Debug
                self.set_state(Ghost.SCATTER) # Or chase? Check logic
        else: # Scatter or Chase
            self.speed = GHOST_SPEED
            self.state_timer += dt
            self._update_mode_timer()

        # Determine Target Tile based on State
        if self.state == Ghost.SCATTER:
            self.target_tile = self.scatter_target
        elif self.state == Ghost.CHASE:
            self.target_tile = self._calculate_chase_target(pacman_pos, pacman_dir, blinky_pos)
        elif self.state == Ghost.FRIGHTENED:
            # Move randomly at intersections
            if self.is_at_intersection():
                self.snap_to_grid()
                possible_dirs = [UP, DOWN, LEFT, RIGHT]
                # Don't reverse direction unless it's the only option
                reverse_dir = (-self.direction[0], -self.direction[1])
                valid_moves = []
                for direction in possible_dirs:
                    if direction != reverse_dir and self.can_move(direction, maze):
                         valid_moves.append(direction)
                if not valid_moves: # If trapped, allow reversal
                     if self.can_move(reverse_dir, maze):
                         valid_moves.append(reverse_dir)

                if valid_moves: # Should always find a move unless completely boxed in
                    self.direction = random.choice(valid_moves)
                else: # Stuck - rare case
                    self.direction = STOP

        # Movement Logic (Common for Scatter, Chase, Eaten)
        if self.state != Ghost.FRIGHTENED:
            self._pathfind_to_target(maze)

        # Use the base Entity update for movement
        # Need to adapt base update slightly or override fully
        # Base update checks intended_direction, ghost needs direct direction setting
        self._move_based_on_direction(dt, maze)


    def _move_based_on_direction(self, dt, maze):
         # Simplified move logic directly using self.direction
         if self.is_at_intersection():
             self.snap_to_grid()
             # If the current path is blocked, recalculate (should be handled by pathfind)
             if not self.can_move(self.direction, maze):
                 # This might happen if pathfinding chose a dir that became invalid
                 # Or if state changed mid-tile. Force pathfind again?
                 if self.state != Ghost.FRIGHTENED:
                     self._pathfind_to_target(maze) # Recalculate if blocked
                 else:
                      self.direction = STOP # Frightened ghosts stop if blocked?

         # Actual movement
         if self.can_move(self.direction, maze):
             delta = self.speed * dt
             self.x += self.direction[0] * delta
             self.y += self.direction[1] * delta
             self.handle_tunnels()
         else:
              # If somehow still blocked even after checks, stop
              self.direction = STOP

    def _calculate_chase_target(self, pacman_pos, pacman_dir, blinky_pos):
        # Target calculation based on ghost type
        px, py = pacman_pos
        pdx, pdy = pacman_dir

        if self.ghost_type == 'blinky':
            return pacman_pos # Target Pac-Man directly

        elif self.ghost_type == 'pinky':
            # Target 4 tiles ahead of Pac-Man
            target_x = px + pdx * 4
            target_y = py + pdy * 4
            # Original game had a bug where moving UP also offset 4 tiles left
            if pdx == 0 and pdy == -1: # Moving UP
                target_x -= 4
            return (target_x, target_y)

        elif self.ghost_type == 'inky':
            # Needs Blinky's position (bx, by)
            if blinky_pos is None: return pacman_pos # Fallback if blinky not available
            bx, by = blinky_pos
            # Tile 2 tiles ahead of Pac-Man
            two_ahead_x = px + pdx * 2
            two_ahead_y = py + pdy * 2
            if pdx == 0 and pdy == -1: # Bug replication for UP
                two_ahead_x -= 2
            # Vector from Blinky to two_ahead
            vec_x = two_ahead_x - bx
            vec_y = two_ahead_y - by
            # Double the vector to get target
            target_x = bx + vec_x * 2
            target_y = by + vec_y * 2
            return (int(target_x), int(target_y))

        elif self.ghost_type == 'clyde':
            # If distance > 8 tiles, target Pac-Man; else target scatter corner
            current_x, current_y = self.get_tile_pos()
            dist_sq = (current_x - px)**2 + (current_y - py)**2
            if dist_sq > 8*8:
                return pacman_pos # Chase Pac-Man
            else:
                return self.scatter_target # Go to scatter corner

        return pacman_pos # Default fallback

    def _update_mode_timer(self):
        # Implement the scatter/chase cycle according to classic Pac-Man rules
        if self.mode_cycle == 0:
            if self.state == Ghost.SCATTER and self.state_timer >= SCATTER_TIME_1:
                self.set_state(Ghost.CHASE)
                self.state_timer = 0
            elif self.state == Ghost.CHASE and self.state_timer >= CHASE_TIME_1:
                self.set_state(Ghost.SCATTER)
                self.state_timer = 0
                self.mode_cycle = 1
        elif self.mode_cycle == 1:
            if self.state == Ghost.SCATTER and self.state_timer >= SCATTER_TIME_2:
                self.set_state(Ghost.CHASE)
                self.state_timer = 0
            elif self.state == Ghost.CHASE and self.state_timer >= CHASE_TIME_2:
                self.set_state(Ghost.SCATTER)
                self.state_timer = 0
                self.mode_cycle = 2
        elif self.mode_cycle == 2:
            if self.state == Ghost.SCATTER and self.state_timer >= SCATTER_TIME_3:
                self.set_state(Ghost.CHASE)
                self.state_timer = 0
            elif self.state == Ghost.CHASE and self.state_timer >= CHASE_TIME_3:
                self.set_state(Ghost.SCATTER)
                self.state_timer = 0
                self.mode_cycle = 3
        elif self.mode_cycle == 3:
            if self.state == Ghost.SCATTER and self.state_timer >= SCATTER_TIME_4:
                self.set_state(Ghost.CHASE)
                self.state_timer = 0
                # From here on, ghosts remain in chase mode indefinitely

    def _pathfind_to_target(self, maze):
        # Simple pathfinding: at intersections, choose direction that minimizes
        # straight-line distance to target. Avoid reversing direction.
        if self.is_at_intersection() and self.target_tile is not None:
            self.snap_to_grid()
            possible_dirs = [UP, DOWN, LEFT, RIGHT]
            reverse_dir = (-self.direction[0], -self.direction[1])

            best_dir = STOP
            min_dist_sq = float('inf')

            current_tile_x, current_tile_y = self.get_tile_pos()
            target_x, target_y = self.target_tile

            # Arcade priority: UP > LEFT > DOWN > RIGHT (used as tie-breaker)
            priority_order = [UP, LEFT, DOWN, RIGHT]

            valid_moves = []
            for direction in priority_order:
                if direction != reverse_dir and self.can_move(direction, maze):
                     valid_moves.append(direction)

            if not valid_moves and self.can_move(reverse_dir, maze): # Only reverse if trapped
                 valid_moves.append(reverse_dir)

            if not valid_moves: # Completely stuck
                 self.direction = STOP
                 return

            # Choose the valid move that gets closest to the target
            for direction in valid_moves:
                 next_tile_x, next_tile_y = self.get_next_tile(direction)
                 dist_sq = (next_tile_x - target_x)**2 + (next_tile_y - target_y)**2
                 if dist_sq < min_dist_sq:
                     min_dist_sq = dist_sq
                     best_dir = direction
                 # Tie-breaking already handled by checking in priority order

            self.direction = best_dir


    def set_state(self, state):
        if self.state != state:
            # Store previous state if changing from Scatter/Chase to Frightened/Eaten
            if state == Ghost.FRIGHTENED or state == Ghost.EATEN:
                 if self.state == Ghost.SCATTER or self.state == Ghost.CHASE:
                     self.previous_state = self.state

            self.state = state
            self.state_timer = 0 # Reset timer for the new state
            print(f"{self.ghost_type} changed state to {state}") # Debug

            if state == Ghost.FRIGHTENED:
                self.frightened_timer = FRIGHTENED_DURATION
                # Reverse direction when frightened starts (arcade behavior)
                reverse_dir = (-self.direction[0], -self.direction[1])
                if self.can_move(reverse_dir, maze):
                     self.direction = reverse_dir
            elif state == Ghost.EATEN:
                 self.color = FRIGHTENED_BLUE # Or use an 'eyes' sprite
                 # Set target to home base
                 self.target_tile = self.respawn_tile # Move towards respawn tile
                 self._pathfind_to_target(maze) # Immediately pathfind home
            else: # Scatter or Chase
                 # Reset color if coming from Eaten/Frightened
                 self.color = self._get_original_color()
                 self.speed = GHOST_SPEED


    def _get_original_color(self):
         if self.ghost_type == 'blinky': return RED
         if self.ghost_type == 'pinky': return PINK
         if self.ghost_type == 'inky': return CYAN
         if self.ghost_type == 'clyde': return ORANGE
         return WHITE # Default

    def draw(self, screen):
        # Draw ghost with appropriate color based on state and a more classic ghost shape
        center_x = int(self.x + TILE_SIZE // 2)
        center_y = int(self.y + TILE_SIZE // 2)
        
        # Determine ghost color based on state
        if self.state == Ghost.FRIGHTENED:
            # Flashing white and blue when frightened time is almost up
            if self.frightened_timer < 2.0 and int(self.frightened_timer * 4) % 2 == 0:
                color = FRIGHTENED_WHITE
            else:
                color = FRIGHTENED_BLUE
        elif self.state == Ghost.EATEN:
            # For eaten state, just draw the eyes
            self._draw_eyes(screen, center_x, center_y)
            return
        else:
            color = self.color
        
        # Draw ghost body with a more classic ghost shape
        # Body - semi-circle with wavy bottom
        rect = pygame.Rect(center_x - self.radius, center_y - self.radius, self.radius*2, self.radius*2)
        pygame.draw.rect(screen, color, rect, border_radius=self.radius)  # Rounded top
        
        # Wavy bottom - zigzag pattern at the bottom of the ghost's body
        wave_height = self.radius // 3
        wave_width = self.radius // 2
        wave_base_y = center_y + self.radius - wave_height
        
        wave_points = [
            (center_x - self.radius, wave_base_y),
            (center_x - self.radius + wave_width, wave_base_y + wave_height),
            (center_x, wave_base_y),
            (center_x + wave_width, wave_base_y + wave_height),
            (center_x + self.radius, wave_base_y),
            (center_x + self.radius, center_y - self.radius),  # Top right
            (center_x - self.radius, center_y - self.radius)   # Top left
        ]
        
        pygame.draw.polygon(screen, color, wave_points)
        
        # Draw eyes on top of body
        self._draw_eyes(screen, center_x, center_y)
    
    def _draw_eyes(self, screen, center_x, center_y):
        # Draw eyes
        eye_radius = TILE_SIZE // 6
        eye_offset = TILE_SIZE // 5
        
        # Draw white part of eyes
        pygame.draw.circle(screen, WHITE, (center_x - eye_offset, center_y - eye_offset//2), eye_radius)
        pygame.draw.circle(screen, WHITE, (center_x + eye_offset, center_y - eye_offset//2), eye_radius)
        
        # Draw pupils (look in direction of movement)
        pupil_radius = eye_radius // 2
        pupil_offset_x = 0
        pupil_offset_y = 0
        
        # Adjust pupil position based on direction
        if self.direction == LEFT:
            pupil_offset_x = -pupil_radius
        elif self.direction == RIGHT:
            pupil_offset_x = pupil_radius
        elif self.direction == UP:
            pupil_offset_y = -pupil_radius
        elif self.direction == DOWN:
            pupil_offset_y = pupil_radius
        
        pygame.draw.circle(screen, BLACK, 
                         (center_x - eye_offset + pupil_offset_x, center_y - eye_offset//2 + pupil_offset_y), 
                         pupil_radius)
        pygame.draw.circle(screen, BLACK, 
                         (center_x + eye_offset + pupil_offset_x, center_y - eye_offset//2 + pupil_offset_y), 
                         pupil_radius)
