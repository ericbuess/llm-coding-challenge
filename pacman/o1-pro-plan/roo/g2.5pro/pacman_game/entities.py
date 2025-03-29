import pygame
import math
from . import constants as C

# Helper function to convert tile coordinates to pixel coordinates (center of tile)
def tile_to_pixel(tile_x, tile_y):
    return (tile_x * C.TILE_SIZE + C.TILE_SIZE / 2,
            tile_y * C.TILE_SIZE + C.TILE_SIZE / 2)

# Helper function to convert pixel coordinates to tile coordinates
def pixel_to_tile(pixel_x, pixel_y):
    return (int(pixel_x // C.TILE_SIZE), int(pixel_y // C.TILE_SIZE))

class Entity:
    """Base class for Pacman and Ghosts."""
    def __init__(self, start_tile_x, start_tile_y, speed):
        self.start_tile = (start_tile_x, start_tile_y)
        self.x, self.y = tile_to_pixel(start_tile_x, start_tile_y) # Pixel coordinates
        self.speed = speed
        self.direction = C.STOP # Current direction vector (e.g., C.LEFT, C.RIGHT)
        self.target_tile = None # The next tile we are moving towards
        self.current_tile = self.start_tile # The tile the entity is currently centered on or just left

    def get_tile_pos(self):
        """Returns the integer tile coordinates (col, row) based on pixel position."""
        return pixel_to_tile(self.x, self.y)

    def set_pixel_pos(self, tile_pos):
        """Sets the entity's pixel position to the center of the given tile."""
        self.x, self.y = tile_to_pixel(tile_pos[0], tile_pos[1])
        self.current_tile = tile_pos

    def is_at_tile_center(self, tolerance=1):
        """Checks if the entity is close to the center of its current target tile."""
        if not self.target_tile:
            # If no target, consider it centered on its current tile based on pixel pos
            current_center_x, current_center_y = tile_to_pixel(self.current_tile[0], self.current_tile[1])
            return abs(self.x - current_center_x) < tolerance and abs(self.y - current_center_y) < tolerance

        target_center_x, target_center_y = tile_to_pixel(self.target_tile[0], self.target_tile[1])
        return abs(self.x - target_center_x) < tolerance and abs(self.y - target_center_y) < tolerance

    def move(self, dt):
        """Moves the entity based on its direction and speed."""
        if self.direction != C.STOP:
            distance = self.speed * dt
            self.x += self.direction[0] * distance
            self.y += self.direction[1] * distance

    def update(self, dt, maze):
        """Basic update logic: move and handle reaching the target tile."""
        self.move(dt)

        # Check if we've reached or passed the center of the target tile
        if self.target_tile:
            target_px, target_py = tile_to_pixel(self.target_tile[0], self.target_tile[1])
            moved_past = False
            if self.direction == C.LEFT and self.x <= target_px: moved_past = True
            elif self.direction == C.RIGHT and self.x >= target_px: moved_past = True
            elif self.direction == C.UP and self.y <= target_py: moved_past = True
            elif self.direction == C.DOWN and self.y >= target_py: moved_past = True

            if moved_past:
                # Snap to target tile center
                self.x, self.y = target_px, target_py
                self.current_tile = self.target_tile
                self.target_tile = None # Reached target, ready for next decision
                # Stop movement momentarily until a new direction/target is set
                # self.direction = C.STOP # Optional: Stop exactly at center? Or allow continuous movement?

    def reset_position(self):
        """Resets the entity to its starting position and state."""
        self.set_pixel_pos(self.start_tile)
        self.direction = C.STOP
        self.target_tile = None
        self.current_tile = self.start_tile

    def draw(self, screen):
        """Placeholder draw method."""
        pygame.draw.circle(screen, C.WHITE, (int(self.x), int(self.y)), C.TILE_SIZE // 3)


class Pacman(Entity):
    """Represents the player character, Pac-Man."""
    def __init__(self, start_tile_x, start_tile_y):
        super().__init__(start_tile_x, start_tile_y, C.PACMAN_SPEED)
        self.lives = C.START_LIVES
        self.power_mode_timer = 0 # Time remaining in power mode (seconds)
        self.intended_direction = C.STOP # Direction player wants to go next
        self.score = 0 # Pacman's score, managed here or by a ScoreManager
        self.ghosts_eaten_in_power_mode = 0

        # Animation attributes
        self.anim_timer = 0
        self.anim_frame = 0
        self.mouth_open = True # Simple 2-state animation

    def handle_input(self, key):
        """Sets the intended direction based on key presses."""
        if key == pygame.K_UP or key == pygame.K_w:
            self.intended_direction = C.UP
        elif key == pygame.K_DOWN or key == pygame.K_s:
            self.intended_direction = C.DOWN
        elif key == pygame.K_LEFT or key == pygame.K_a:
            self.intended_direction = C.LEFT
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.intended_direction = C.RIGHT

    def _can_move_in_direction(self, direction, maze):
        """Checks if the next tile in the given direction is walkable."""
        if direction == C.STOP:
            return False
        next_tile_x = self.current_tile[0] + direction[0]
        next_tile_y = self.current_tile[1] + direction[1]
        return not maze.is_wall(next_tile_x, next_tile_y)

    def update(self, dt, maze):
        """Updates Pac-Man's state, movement, and handles collisions."""
        # Handle direction changes only when at the center of a tile
        if self.is_at_tile_center():
            # Snap to center precisely if slightly off
            self.set_pixel_pos(self.current_tile)

            # Check for teleportation
            teleport_dest = maze.get_teleport_destination(self.current_tile[0], self.current_tile[1])
            if teleport_dest:
                self.set_pixel_pos(teleport_dest)
                # Continue moving in the same direction if possible after teleporting
                if not self._can_move_in_direction(self.direction, maze):
                     # If blocked after teleport, try intended, else stop
                     if self._can_move_in_direction(self.intended_direction, maze):
                         self.direction = self.intended_direction
                     else:
                         self.direction = C.STOP
                # Set target based on new position and direction
                if self.direction != C.STOP:
                     self.target_tile = (self.current_tile[0] + self.direction[0], self.current_tile[1] + self.direction[1])
                else:
                     self.target_tile = None # Stop if blocked immediately after teleport

            else: # Not teleporting, normal movement logic
                # Try to apply intended direction
                if self.intended_direction != C.STOP and self._can_move_in_direction(self.intended_direction, maze):
                    if self.intended_direction != self.direction:
                        self.direction = self.intended_direction
                        self.target_tile = (self.current_tile[0] + self.direction[0], self.current_tile[1] + self.direction[1])
                # If intended direction is blocked, check if current direction is still valid
                elif not self._can_move_in_direction(self.direction, maze):
                    # Current path blocked, stop movement
                    self.direction = C.STOP
                    self.target_tile = None
                # If current direction is valid, continue moving
                elif self.direction != C.STOP:
                     self.target_tile = (self.current_tile[0] + self.direction[0], self.current_tile[1] + self.direction[1])


        # Update power mode timer
        if self.power_mode_timer > 0:
            self.power_mode_timer -= dt
            if self.power_mode_timer <= 0:
                self.power_mode_timer = 0
                self.ghosts_eaten_in_power_mode = 0 # Reset count when power mode ends
                # print("Power mode ended") # Debug

        # Call base Entity update to handle movement towards target
        # Only move if a target is set (i.e., not blocked)
        if self.target_tile:
             super().update(dt, maze)
        else:
             # If no target, ensure snapped to current tile center
             self.set_pixel_pos(self.current_tile)


        # Check for pellet collision at the current tile position
        self.check_pellet_collision(maze)

        # Update animation
        self.update_animation(dt)


    def check_pellet_collision(self, maze):
        """Checks for and handles collisions with pellets and power pellets."""
        tile_x, tile_y = self.get_tile_pos() # Use current tile position for collision check
        pellet_type = maze.get_pellet_type(tile_x, tile_y)

        if pellet_type:
            if maze.remove_pellet(tile_x, tile_y): # Ensure pellet exists before scoring
                if pellet_type == "pellet":
                    self.score += C.PELLET_SCORE
                    # Play pellet sound
                elif pellet_type == "power_pellet":
                    self.score += C.POWER_PELLET_SCORE
                    self.activate_power_mode()
                    # Play power pellet sound / start frightened music

    def activate_power_mode(self):
        """Activates power mode (frightened state for ghosts)."""
        self.power_mode_timer = C.FRIGHTENED_TIME
        self.ghosts_eaten_in_power_mode = 0 # Reset counter for this power pellet
        # print("Power mode activated!") # Debug
        # Need to signal ghosts to enter FRIGHTENED state (handled in main game loop or Ghost class)

    def eat_ghost(self):
        """Called when Pac-Man eats a frightened ghost."""
        if self.power_mode_timer > 0:
            score_index = min(self.ghosts_eaten_in_power_mode, len(C.GHOST_SCORES) - 1)
            self.score += C.GHOST_SCORES[score_index]
            self.ghosts_eaten_in_power_mode += 1
            # Play ghost eaten sound
            return True # Successfully ate ghost
        return False # Cannot eat ghost if not in power mode

    def lose_life(self):
        """Decrements life count."""
        self.lives -= 1
        print(f"Lost a life! Lives remaining: {self.lives}") # Debug
        # Play death sound

    def reset_position(self):
        """Resets Pac-Man after losing a life or starting a new level."""
        super().reset_position()
        self.intended_direction = C.STOP
        self.power_mode_timer = 0
        self.ghosts_eaten_in_power_mode = 0

    def update_animation(self, dt):
        """Updates the animation frame based on time."""
        if self.direction == C.STOP:
            self.anim_frame = 0 # Static frame when stopped
            self.mouth_open = True
            return

        self.anim_timer += dt
        anim_speed = 0.1 # Time between frame changes (seconds)
        if self.anim_timer >= anim_speed:
            self.anim_timer = 0
            self.mouth_open = not self.mouth_open
            # Could use more frames: self.anim_frame = (self.anim_frame + 1) % num_frames

    def draw(self, screen):
        """Draws Pac-Man on the screen."""
        # Simple circle representation for now
        radius = C.TILE_SIZE // 2 - 1 # Slightly smaller than tile

        # Basic animation: open/close mouth based on direction
        if self.direction == C.STOP and not self.mouth_open: # Keep mouth closed when stopped
             start_angle = 0
             end_angle = 2 * math.pi
        elif not self.mouth_open: # Closed mouth frame
             start_angle = 0
             end_angle = 2 * math.pi
        else: # Open mouth frame
            angle_offset = math.pi / 4 # How wide the mouth opens
            if self.direction == C.RIGHT:
                start_angle = angle_offset
                end_angle = 2 * math.pi - angle_offset
            elif self.direction == C.LEFT:
                start_angle = math.pi + angle_offset
                end_angle = math.pi - angle_offset
            elif self.direction == C.UP:
                start_angle = math.pi / 2 + angle_offset
                end_angle = math.pi / 2 - angle_offset
            elif self.direction == C.DOWN:
                start_angle = 3 * math.pi / 2 + angle_offset
                end_angle = 3 * math.pi / 2 - angle_offset
            else: # Default case (e.g., stopped but mouth open)
                 start_angle = angle_offset
                 end_angle = 2 * math.pi - angle_offset

        # Draw Pac-Man body (arc for mouth)
        center_pos = (int(self.x), int(self.y))
        pygame.draw.arc(screen, C.YELLOW,
                        (self.x - radius, self.y - radius, radius * 2, radius * 2),
                        start_angle, end_angle, radius)

        # Draw a filled circle if mouth is closed (or use a different sprite)
        if not self.mouth_open:
             pygame.draw.circle(screen, C.YELLOW, center_pos, radius)


import random

class Ghost(Entity):
    """Represents a ghost enemy."""
    def __init__(self, start_tile_x, start_tile_y, ghost_type, color, scatter_target):
        speed = C.GHOST_SPEED # Initial speed
        super().__init__(start_tile_x, start_tile_y, speed)
        self.ghost_type = ghost_type
        self.color = color
        self.scatter_target = scatter_target # Tile (col, row) for scatter mode
        self.current_state = C.SCATTER # Initial state
        self.state_timer = 0 # Timer for current state duration
        self.frightened_timer = 0 # Timer for frightened duration
        self.eaten_timer = 0 # Timer used for visual effect after being eaten? Or respawn?
        self.target_tile = None # The tile the ghost is aiming for
        self.home_tile = self.start_tile # Ghost house entrance/respawn point
        self.is_in_ghost_house = True # Ghosts start inside initially (optional logic)
        self.exit_house_timer = random.uniform(0, 3) # Staggered exit times

        # Define scatter targets for each ghost (adjust as needed based on maze layout)
        # These should ideally be outside the maze boundaries or specific corners
        if ghost_type == 'blinky': self.scatter_target = (C.GRID_WIDTH - 2, 0) # Top right
        elif ghost_type == 'pinky': self.scatter_target = (1, 0) # Top left
        elif ghost_type == 'inky': self.scatter_target = (C.GRID_WIDTH - 2, C.GRID_HEIGHT - 2) # Bottom right
        elif ghost_type == 'clyde': self.scatter_target = (1, C.GRID_HEIGHT - 2) # Bottom left


    def set_state(self, new_state):
        """Changes the ghost's state and resets relevant timers."""
        # print(f"{self.ghost_type} changing from {self.current_state} to {new_state}") # Debug
        self.current_state = new_state
        self.state_timer = 0 # Reset timer for scatter/chase cycles
        if new_state == C.FRIGHTENED:
            self.frightened_timer = C.FRIGHTENED_TIME
            self.speed = C.GHOST_FRIGHTENED_SPEED
            # Reverse direction when entering frightened mode (classic behavior)
            self.reverse_direction()
        elif new_state == C.EATEN:
            self.speed = C.GHOST_EATEN_SPEED
            self.frightened_timer = 0 # No longer frightened
            # Target is now the ghost house
        elif new_state == C.SCATTER or new_state == C.CHASE:
            self.speed = C.GHOST_SPEED
            self.frightened_timer = 0
            # Determine target based on the new state immediately
            # self.target_tile = self._get_target_tile(pacman) # Requires pacman ref

    def reverse_direction(self):
        """Reverses the ghost's current direction if moving."""
        if self.direction == C.UP: self.direction = C.DOWN
        elif self.direction == C.DOWN: self.direction = C.UP
        elif self.direction == C.LEFT: self.direction = C.RIGHT
        elif self.direction == C.RIGHT: self.direction = C.LEFT
        # Update target tile based on reversed direction if possible
        next_tile_x = self.current_tile[0] + self.direction[0]
        next_tile_y = self.current_tile[1] + self.direction[1]
        # Simple check, assumes maze ref is available or handled in update
        # if not maze.is_wall(next_tile_x, next_tile_y):
        self.target_tile = (next_tile_x, next_tile_y)
        # else: handle being blocked after reversing


    def update(self, dt, maze, pacman, blinky=None): # Pass pacman and potentially blinky (for Inky)
        """Updates the ghost's state, target, and movement."""

        # Handle timers
        self.state_timer += dt
        if self.frightened_timer > 0:
            self.frightened_timer -= dt
            if self.frightened_timer <= 0:
                self.frightened_timer = 0
                if self.current_state == C.FRIGHTENED: # Only switch if still frightened
                     self.set_state(C.CHASE) # Or scatter based on game cycle logic

        # --- Ghost House Logic (Simplified) ---
        if self.is_in_ghost_house:
            if self.exit_house_timer > 0:
                self.exit_house_timer -= dt
                return # Stay inside until timer expires
            else:
                # Logic to move out of the house (e.g., move towards a specific exit tile)
                # For now, just mark as exited and place at spawn point ready to move
                self.is_in_ghost_house = False
                self.set_pixel_pos(self.start_tile) # Ensure at start tile center
                self.current_state = C.SCATTER # Start with scatter usually
                # print(f"{self.ghost_type} exiting house.")


        # --- State-based Logic ---
        if self.current_state == C.EATEN:
            # Move towards home tile
            self.target_tile = self.home_tile # Target is always home when eaten
            if self.is_at_tile_center() and self.current_tile == self.home_tile:
                # Reached home, respawn
                self.is_in_ghost_house = True # Go back inside
                self.exit_house_timer = C.GHOST_RESPAWN_TIME # Wait before exiting again
                self.set_state(C.SCATTER) # Or chase depending on global state
                self.speed = C.GHOST_SPEED
                # print(f"{self.ghost_type} respawned.")
            else:
                 # Move towards home using pathfinding
                 self._move_towards_target(maze)

        elif self.current_state == C.FRIGHTENED:
            # Move randomly at intersections
            if self.is_at_tile_center():
                 self.set_pixel_pos(self.current_tile) # Snap
                 self._choose_random_direction(maze)

        elif self.current_state == C.SCATTER or self.current_state == C.CHASE:
            # Determine target tile based on state
            self.target_tile = self._get_target_tile(pacman, blinky)
            # Move towards target using pathfinding logic at intersections
            if self.is_at_tile_center():
                 self.set_pixel_pos(self.current_tile) # Snap
                 self._move_towards_target(maze)


        # --- Movement ---
        # Only move if a target is set and not blocked immediately
        if self.target_tile and self.direction != C.STOP:
             super().update(dt, maze) # Use base class movement
        elif self.is_at_tile_center(): # If stopped at center, ensure snapped
             self.set_pixel_pos(self.current_tile)


    def _get_target_tile(self, pacman, blinky):
        """Calculates the target tile based on the ghost's state and type."""
        if self.current_state == C.SCATTER:
            return self.scatter_target
        elif self.current_state == C.CHASE:
            pacman_tile = pacman.get_tile_pos()
            pacman_direction = pacman.direction

            if self.ghost_type == 'blinky':
                # Target Pac-Man's current tile
                return pacman_tile
            elif self.ghost_type == 'pinky':
                # Target 4 tiles ahead of Pac-Man
                target_x = pacman_tile[0] + pacman_direction[0] * 4
                target_y = pacman_tile[1] + pacman_direction[1] * 4
                # Special case for 'UP' direction bug in original game
                if pacman_direction == C.UP:
                    target_x -= 4 # Move 4 tiles left as well
                return (target_x, target_y)
            elif self.ghost_type == 'inky':
                # Target based on Blinky and Pac-Man's position
                if not blinky: return pacman_tile # Failsafe if blinky ref is missing

                pacman_ahead_tile_x = pacman_tile[0] + pacman_direction[0] * 2
                pacman_ahead_tile_y = pacman_tile[1] + pacman_direction[1] * 2
                # Special case for 'UP'
                if pacman_direction == C.UP:
                     pacman_ahead_tile_x -= 2

                blinky_tile = blinky.get_tile_pos()
                vec_x = pacman_ahead_tile_x - blinky_tile[0]
                vec_y = pacman_ahead_tile_y - blinky_tile[1]

                target_x = pacman_ahead_tile_x + vec_x
                target_y = pacman_ahead_tile_y + vec_y
                return (target_x, target_y)

            elif self.ghost_type == 'clyde':
                # Target Pac-Man if far, scatter if close
                my_tile = self.get_tile_pos()
                dist_sq = (my_tile[0] - pacman_tile[0])**2 + (my_tile[1] - pacman_tile[1])**2
                if dist_sq > 8*8: # If distance squared > 64 (dist > 8)
                    return pacman_tile # Chase Pac-Man
                else:
                    return self.scatter_target # Go to scatter corner

        # Default fallback (e.g., for FRIGHTENED or EATEN handled elsewhere)
        return self.current_tile # Stay put or handled by state logic


    def _get_valid_directions(self, maze):
        """Returns a list of valid directions (not walls, not reversing) from the current tile."""
        valid_dirs = []
        current_tile = self.current_tile # Use the snapped tile position
        possible_dirs = [C.UP, C.DOWN, C.LEFT, C.RIGHT]

        # Prevent reversing direction unless forced (at dead end)
        reverse_dir = (-self.direction[0], -self.direction[1])

        for d in possible_dirs:
            # Don't allow immediate reversal if other options exist
            if d == reverse_dir and len(valid_dirs) > 0 and self.current_state != C.FRIGHTENED: # Frightened can reverse
                 continue

            next_tile_x = current_tile[0] + d[0]
            next_tile_y = current_tile[1] + d[1]

            # Check bounds and walls
            if 0 <= next_tile_x < maze.grid_width and 0 <= next_tile_y < maze.grid_height:
                 # Ghosts generally cannot enter the ghost house unless EATEN
                 # Add specific logic here if needed to prevent entry
                 # is_ghost_house_door = ...

                 if not maze.is_wall(next_tile_x, next_tile_y): # and not is_ghost_house_door:
                     valid_dirs.append(d)

        # If only the reverse direction is valid (dead end), allow it
        if not valid_dirs and reverse_dir != (0,0) and not maze.is_wall(current_tile[0] + reverse_dir[0], current_tile[1] + reverse_dir[1]):
             valid_dirs.append(reverse_dir)

        # If truly stuck (shouldn't happen in standard maze), return empty or STOP
        if not valid_dirs:
             # print(f"Warning: {self.ghost_type} is stuck at {current_tile}!") # Debug
             return [C.STOP] # Or handle error

        return valid_dirs


    def _choose_direction_towards_target(self, valid_dirs, target_tile):
        """Chooses the valid direction that minimizes distance to the target tile."""
        if not valid_dirs:
            return C.STOP # Should not happen if _get_valid_directions works

        if len(valid_dirs) == 1:
            return valid_dirs[0] # Only one way to go

        best_dir = C.STOP
        min_dist_sq = float('inf')

        current_tile = self.current_tile
        target_x, target_y = target_tile

        # Arcade priority: Up > Left > Down > Right (when distances are equal)
        priority_order = [C.UP, C.LEFT, C.DOWN, C.RIGHT]

        # Filter valid_dirs based on priority order for tie-breaking
        ordered_valid_dirs = [d for d in priority_order if d in valid_dirs]


        for d in ordered_valid_dirs:
            next_tile_x = current_tile[0] + d[0]
            next_tile_y = current_tile[1] + d[1]
            dist_sq = (next_tile_x - target_x)**2 + (next_tile_y - target_y)**2

            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                best_dir = d

        # Failsafe if no direction chosen (shouldn't happen with ordered list)
        if best_dir == C.STOP and ordered_valid_dirs:
             best_dir = ordered_valid_dirs[0]

        return best_dir


    def _move_towards_target(self, maze):
        """Determines the next direction based on target and valid moves."""
        valid_dirs = self._get_valid_directions(maze)

        if not valid_dirs or valid_dirs == [C.STOP]:
            self.direction = C.STOP
            self.target_tile = None
            return

        chosen_dir = self._choose_direction_towards_target(valid_dirs, self.target_tile)
        self.direction = chosen_dir

        # Set the next tile as the immediate target for movement
        if self.direction != C.STOP:
             self.target_tile = (self.current_tile[0] + self.direction[0], self.current_tile[1] + self.direction[1])
        else:
             self.target_tile = None # Stop if chosen direction is STOP


    def _choose_random_direction(self, maze):
        """Chooses a random valid direction (used in FRIGHTENED state)."""
        valid_dirs = self._get_valid_directions(maze)

        if not valid_dirs or valid_dirs == [C.STOP]:
            self.direction = C.STOP
            self.target_tile = None
            return

        # Filter out the reverse direction if possible
        reverse_dir = (-self.direction[0], -self.direction[1])
        possible_dirs = [d for d in valid_dirs if d != reverse_dir]

        if not possible_dirs: # If only reverse is possible (dead end)
             possible_dirs = valid_dirs # Allow reversal

        self.direction = random.choice(possible_dirs)

        # Set the next tile as the immediate target
        if self.direction != C.STOP:
             self.target_tile = (self.current_tile[0] + self.direction[0], self.current_tile[1] + self.direction[1])
        else:
             self.target_tile = None


    def draw(self, screen):
        """Draws the ghost on the screen based on its state."""
        radius = C.TILE_SIZE // 2 - 2 # Slightly smaller than Pac-Man

        draw_color = self.color
        is_eaten = False

        if self.current_state == C.FRIGHTENED:
            # Blinking effect when frightened time is low
            if self.frightened_timer < 3 and int(self.frightened_timer * 4) % 2 == 0:
                 draw_color = C.WHITE # Blink white
            else:
                 draw_color = C.FRIGHTENED_COLOR
        elif self.current_state == C.EATEN:
            draw_color = C.EATEN_COLOR # Draw eyes only
            is_eaten = True


        # Simple circle representation
        center_pos = (int(self.x), int(self.y))

        if not is_eaten:
            # Draw main body
            pygame.draw.circle(screen, draw_color, center_pos, radius)
            # Draw "skirt" (rectangle below circle)
            skirt_rect = pygame.Rect(self.x - radius, self.y, radius * 2, radius)
            pygame.draw.rect(screen, draw_color, skirt_rect)
            # Add wavy bottom? (more complex drawing)

        # Draw eyes (always white, adjust position based on direction)
        eye_radius = radius // 4
        eye_offset_x = radius // 2.5
        eye_offset_y = -radius // 3 # Position eyes slightly up

        # Adjust eye position based on direction
        pupil_offset_x = 0
        pupil_offset_y = 0
        pupil_radius = eye_radius // 2

        if not is_eaten: # Normal eyes
             if self.direction == C.LEFT: pupil_offset_x = -eye_radius / 2
             elif self.direction == C.RIGHT: pupil_offset_x = eye_radius / 2
             elif self.direction == C.UP: pupil_offset_y = -eye_radius / 2
             elif self.direction == C.DOWN: pupil_offset_y = eye_radius / 2

             # Left eye
             left_eye_pos = (int(center_pos[0] - eye_offset_x), int(center_pos[1] + eye_offset_y))
             pygame.draw.circle(screen, C.WHITE, left_eye_pos, eye_radius)
             pygame.draw.circle(screen, C.BLACK, (int(left_eye_pos[0] + pupil_offset_x), int(left_eye_pos[1] + pupil_offset_y)), pupil_radius)

             # Right eye
             right_eye_pos = (int(center_pos[0] + eye_offset_x), int(center_pos[1] + eye_offset_y))
             pygame.draw.circle(screen, C.WHITE, right_eye_pos, eye_radius)
             pygame.draw.circle(screen, C.BLACK, (int(right_eye_pos[0] + pupil_offset_x), int(right_eye_pos[1] + pupil_offset_y)), pupil_radius)

        else: # Eaten eyes (just white squares or circles)
             eye_size = eye_radius * 1.5
             # Left eye
             left_eye_rect = pygame.Rect(center_pos[0] - eye_offset_x - eye_size/2, center_pos[1] + eye_offset_y - eye_size/2, eye_size, eye_size)
             pygame.draw.rect(screen, C.WHITE, left_eye_rect)
             # Right eye
             right_eye_rect = pygame.Rect(center_pos[0] + eye_offset_x - eye_size/2, center_pos[1] + eye_offset_y - eye_size/2, eye_size, eye_size)
             pygame.draw.rect(screen, C.WHITE, right_eye_rect)


    def reset_position(self):
        """Resets ghost to starting position and state."""
        super().reset_position()
        self.current_state = C.SCATTER # Or initial state logic
        self.frightened_timer = 0
        self.is_in_ghost_house = True # Reset to inside
        self.exit_house_timer = random.uniform(1, 4) # Reset exit timer
        self.speed = C.GHOST_SPEED


# Example usage (for testing purposes, remove later)
if __name__ == '__main__':
    # This part needs more setup to test ghosts effectively (maze, pacman)
    print("Entity classes defined: Entity, Pacman, Ghost")
    # Need to instantiate Maze and Pacman to test Ghost update fully
    # maze = Maze('maze1.txt')
    # pacman = Pacman(maze.pacman_spawn_point[0], maze.pacman_spawn_point[1])
    # blinky = Ghost(maze.ghost_spawn_points[0][0], maze.ghost_spawn_points[0][1], 'blinky', C.RED, (C.GRID_WIDTH-2, 0))
    # ... setup pygame loop ...