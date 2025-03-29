import pygame
import random
from constants import *
from maze import Maze # Needed for maze interactions
import math

# --- Helper Functions ---
def pixel_to_tile(pixel_pos):
    """Converts pixel coordinates (Vector2) to tile coordinates (tuple)."""
    return int(pixel_pos.x / TILE_SIZE), int(pixel_pos.y / TILE_SIZE)

def tile_center_pixel(tile_x, tile_y):
    """Gets the pixel coordinates of the center of a tile."""
    return pygame.Vector2(tile_x * TILE_SIZE + TILE_SIZE / 2, tile_y * TILE_SIZE + TILE_SIZE / 2)

# --- Base Entity Class ---
class Entity(pygame.sprite.Sprite):
    def __init__(self, x_tile, y_tile, speed):
        super().__init__()
        self.pos = tile_center_pixel(x_tile, y_tile) # Pixel coordinates (Vector2)
        self.speed = speed
        self.direction = STOP # Current movement vector
        self.intended_direction = STOP # Desired movement vector (from input or AI)
        self.radius = TILE_SIZE // 2 - 1 # Collision radius
        self.image = pygame.Surface([self.radius*2, self.radius*2]) # Placeholder image
        self.image.fill(WHITE) # Default color
        self.rect = self.image.get_rect(center=self.pos)

    def get_tile_pos(self):
        """Returns the (col, row) tuple of the tile the entity is currently mostly in."""
        # Simple division, center-based might be better but requires care
        return pixel_to_tile(self.pos)

    def get_current_tile_center(self):
        """Returns the pixel coordinates of the center of the current tile."""
        tile_x, tile_y = self.get_tile_pos()
        return tile_center_pixel(tile_x, tile_y)

    def is_aligned_with_tile(self, tolerance=1):
        """Checks if the entity is close to the center of its current tile."""
        center_pixel = self.get_current_tile_center()
        return abs(self.pos.x - center_pixel.x) < tolerance and abs(self.pos.y - center_pixel.y) < tolerance

    def move(self, dt, maze):
        """Moves the entity based on its current direction, handling wall collisions and alignment."""
        dist_to_move = self.speed * dt

        # Check for potential wrap-around (tunnels)
        current_tile_x, current_tile_y = self.get_tile_pos()
        if self.direction == LEFT and current_tile_x == 0 and maze.layout_str[current_tile_y][0] == TUNNEL:
             # Check if past the threshold to wrap
             if self.pos.x < -TILE_SIZE / 2:
                 self.pos.x = (GRID_WIDTH - 0.5) * TILE_SIZE
        elif self.direction == RIGHT and current_tile_x == GRID_WIDTH - 1 and maze.layout_str[current_tile_y][GRID_WIDTH-1] == TUNNEL:
             if self.pos.x > (GRID_WIDTH - 0.5) * TILE_SIZE:
                 self.pos.x = -TILE_SIZE / 2

        # --- Movement and Turning Logic ---
        if self.is_aligned_with_tile():
            # Snap to center to prevent drift
            self.pos = self.get_current_tile_center()

            current_tile_x, current_tile_y = self.get_tile_pos()

            # Check if the intended direction is valid from the current tile
            next_tile_x = current_tile_x + int(self.intended_direction.x)
            next_tile_y = current_tile_y + int(self.intended_direction.y)

            if maze.can_move_to(next_tile_x, next_tile_y):
                self.direction = self.intended_direction # Commit to the intended turn
            else:
                # If intended direction is blocked, check if current direction is still valid
                next_tile_x_current = current_tile_x + int(self.direction.x)
                next_tile_y_current = current_tile_y + int(self.direction.y)
                if not maze.can_move_to(next_tile_x_current, next_tile_y_current):
                    self.direction = STOP # Hit a wall, stop

        # Move the entity if direction is not STOP
        if self.direction != STOP:
            self.pos += self.direction * dist_to_move

        self.rect.center = self.pos

    def update(self, dt, maze):
        self.move(dt, maze)

    def draw(self, screen):
        # Basic drawing, override in subclasses for animations
        screen.blit(self.image, self.rect.topleft)

# --- Pacman Class ---
class Pacman(Entity):
    def __init__(self, x_tile, y_tile):
        super().__init__(x_tile, y_tile, PACMAN_SPEED)
        self.lives = 3
        self.power_mode = False
        self.power_timer = 0
        self.image.fill(YELLOW) # Pac-Man color
        self.animation_timer = 0
        self.mouth_open = True # For animation
        self.last_non_stop_direction = RIGHT # Default facing direction

    def handle_input(self, event):
        """Updates intended_direction based on key presses."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.intended_direction = UP
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.intended_direction = DOWN
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.intended_direction = LEFT
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.intended_direction = RIGHT

    def update(self, dt, maze, score_manager):
        """Extends Entity update to handle pellet collision and power mode timer."""
        super().update(dt, maze)

        # Update facing direction for drawing
        if self.direction != STOP:
            self.last_non_stop_direction = self.direction

        # Check for pellet collision only when aligned with tile center for accuracy
        if self.is_aligned_with_tile():
             tile_pos_vec = pygame.Vector2(self.get_tile_pos())
             score_gain, is_power_pellet = maze.check_pellet_collision(tile_pos_vec)
             if score_gain > 0:
                 score_manager.add_score(score_gain)
                 if is_power_pellet:
                     self.activate_power_mode()
                     # Notify ghosts (will be handled in main loop or via observer pattern)
                     return True # Indicate power pellet was eaten

        # Update power mode timer
        if self.power_mode:
            self.power_timer -= dt
            if self.power_timer <= 0:
                self.deactivate_power_mode()

        # Update animation
        self.update_animation(dt)
        return False # Indicate no power pellet eaten this frame

    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer > 0.1: # Change frame every 100ms
            self.mouth_open = not self.mouth_open
            self.animation_timer = 0
        self.draw_sprite()

    def draw_sprite(self):
        """Draws Pac-Man with animated mouth facing the correct direction."""
        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE], pygame.SRCALPHA) # Use SRCALPHA for transparency
        self.image.fill((0,0,0,0)) # Transparent background
        center = (TILE_SIZE // 2, TILE_SIZE // 2)
        radius = TILE_SIZE // 2 - 1

        if self.direction == STOP and not self.mouth_open:
             # Draw closed mouth when stopped
            pygame.draw.circle(self.image, YELLOW, center, radius)
            return

        if self.mouth_open and self.direction != STOP:
            # Calculate mouth angle based on direction
            if self.last_non_stop_direction == RIGHT:
                start_angle = math.radians(45)
                end_angle = math.radians(315)
            elif self.last_non_stop_direction == LEFT:
                start_angle = math.radians(225)
                end_angle = math.radians(135)
            elif self.last_non_stop_direction == UP:
                start_angle = math.radians(135)
                end_angle = math.radians(45)
            elif self.last_non_stop_direction == DOWN:
                start_angle = math.radians(315)
                end_angle = math.radians(225)
            else: # Default to right facing if somehow still STOP
                 start_angle = math.radians(45)
                 end_angle = math.radians(315)

            pygame.draw.arc(self.image, YELLOW, (0, 0, TILE_SIZE, TILE_SIZE), start_angle, end_angle, radius)
            # Fill the arc shape
            points = [center]
            for angle in range(int(math.degrees(start_angle)), int(math.degrees(end_angle)), 1):
                rad = math.radians(angle)
                points.append((center[0] + radius * math.cos(rad), center[1] - radius * math.sin(rad)))
            if len(points) > 2:
                 # Hacky way to fill arc - draw lines from center for Pacman shape
                 # Better way: Use polygon fill if points are ordered correctly or draw.arc + lines
                 # For simplicity, draw circle and cover mouth with black triangle? No, draw arc is better.
                 # Need to handle the geometry correctly. pygame.draw.arc doesn't fill.
                 # Let's try drawing a filled circle and then cutting out the mouth wedge.
                 pygame.draw.circle(self.image, YELLOW, center, radius) # Draw full circle first
                 mouth_points = [center,
                                 (center[0] + radius * math.cos(start_angle), center[1] - radius * math.sin(start_angle)),
                                 (center[0] + radius * math.cos(end_angle), center[1] - radius * math.sin(end_angle))]
                 pygame.draw.polygon(self.image, (0,0,0,0), mouth_points) # Cut wedge with transparent color
        else:
             # Draw closed mouth (full circle)
            pygame.draw.circle(self.image, YELLOW, center, radius)

    def lose_life(self):
        self.lives -= 1
        # Reset position, etc. (handled in game logic typically)

    def reset_position(self, x_tile, y_tile):
        self.pos = tile_center_pixel(x_tile, y_tile)
        self.direction = STOP
        self.intended_direction = STOP
        self.last_non_stop_direction = RIGHT
        self.rect.center = self.pos

    def activate_power_mode(self):
        self.power_mode = True
        self.power_timer = FRIGHTENED_DURATION

    def deactivate_power_mode(self):
        self.power_mode = False
        self.power_timer = 0

# --- Ghost Class ---
class Ghost(Entity):
    def __init__(self, x_tile, y_tile, ghost_type, color):
        super().__init__(x_tile, y_tile, GHOST_SPEED)
        self.ghost_type = ghost_type
        self.color = color
        self.current_state = SCATTER # Initial state
        self.state_timer = 0 # Tracks time in current Scatter/Chase cycle
        self.frightened_timer = 0 # Tracks time remaining in Frightened mode
        self.eaten_timer = 0 # Tracks time since eaten (for respawn logic)
        self.scatter_target = self.get_scatter_target() # Tile coordinates
        self.image.fill(self.color)
        self.target_tile = None # Tile coordinates (col, row)

    def get_scatter_target(self):
        # Define fixed scatter corners for each ghost
        if self.ghost_type == BLINKY:
            return (GRID_WIDTH - 2, 1) # Top right
        elif self.ghost_type == PINKY:
            return (1, 1) # Top left
        elif self.ghost_type == INKY:
            return (GRID_WIDTH - 2, GRID_HEIGHT - 2) # Bottom right
        elif self.ghost_type == CLYDE:
            return (1, GRID_HEIGHT - 2) # Bottom left
        return (1, 1) # Default

    def set_state(self, state):
        self.current_state = state
        # Reset timers or adjust speed based on new state
        if state == FRIGHTENED:
            self.speed = GHOST_FRIGHTENED_SPEED
            self.frightened_timer = FRIGHTENED_DURATION
            self.direction *= -1 # Reverse direction immediately
            self.intended_direction = self.direction # Keep moving away initially
        elif state == EATEN:
            self.speed = GHOST_EATEN_SPEED
            # Target logic will guide it back to the ghost house
            self.target_tile = (13, 14) # Example ghost house entrance tile
        else: # SCATTER or CHASE
            self.speed = GHOST_SPEED
            self.frightened_timer = 0
            # Determine target based on Scatter/Chase
            if state == SCATTER:
                self.target_tile = self.scatter_target
            # Chase target is dynamic, set in update

    def update(self, dt, maze, pacman):
        """Updates ghost state, target, and movement."""
        # Update state timers
        if self.current_state == FRIGHTENED:
            self.frightened_timer -= dt
            if self.frightened_timer <= 0:
                self.set_state(CHASE) # Revert to chase (or scatter based on main timer)
            else:
                 # Flash when time is low
                if self.frightened_timer < FRIGHTENED_FLASH_DURATION:
                    flash_interval = 0.2
                    if int(self.frightened_timer / flash_interval) % 2 == 0:
                        self.image.fill(FRIGHTENED_WHITE)
                    else:
                        self.image.fill(FRIGHTENED_BLUE)
                else:
                    self.image.fill(FRIGHTENED_BLUE)

        elif self.current_state != EATEN:
            # Update scatter/chase timer (controlled externally in Game class)
            # self.state_timer += dt
            # if self.state_timer > appropriate_duration:
            #     switch state (scatter <-> chase)
            #     self.state_timer = 0
            self.image.fill(self.color) # Ensure correct color

        # Determine target tile based on state
        if self.current_state == CHASE:
            self.target_tile = self.get_chase_target(pacman)
        elif self.current_state == SCATTER:
            self.target_tile = self.scatter_target
        elif self.current_state == FRIGHTENED:
            # Choose random direction at intersections
            if self.is_aligned_with_tile():
                self.choose_random_direction(maze)
        elif self.current_state == EATEN:
             self.image.fill(WHITE) # Draw eyes only (simplified)
             # Check if reached ghost house target
             current_tile = self.get_tile_pos()
             if current_tile == self.target_tile:
                 # Respawn logic (change state back) - handled externally or here
                 self.set_state(SCATTER) # Or Chase, depending on game mode cycle
                 # Need to place it correctly inside the house
                 self.pos = tile_center_pixel(13, 14) # TODO: Proper ghost house spawn logic
             else:
                 # Move towards ghost house entrance
                 self.choose_next_direction(maze, self.target_tile)

        # Choose next move direction only when aligned and not frightened (random) or eaten (fixed path)
        if self.is_aligned_with_tile() and self.current_state not in [FRIGHTENED, EATEN]:
             if self.target_tile:
                 self.choose_next_direction(maze, self.target_tile)
             else:
                 # Failsafe if target is somehow None
                 self.intended_direction = STOP

        # Standard movement inherited from Entity
        super().update(dt, maze)

    def get_chase_target(self, pacman):
        """Calculate the target tile based on ghost type and Pac-Man's position/direction."""
        pacman_tile = pacman.get_tile_pos()
        pacman_dir = pacman.last_non_stop_direction

        if self.ghost_type == BLINKY: # Target Pac-Man directly
            return pacman_tile

        elif self.ghost_type == PINKY: # Target 4 tiles ahead of Pac-Man
            target_x = pacman_tile[0] + int(pacman_dir.x * 4)
            target_y = pacman_tile[1] + int(pacman_dir.y * 4)
            # Special case for UP direction (arcade bug emulation - also moves 4 left)
            if pacman_dir == UP:
                target_x -= 4
            return (target_x, target_y)

        elif self.ghost_type == INKY: # Complex targeting using Blinky
            # Requires access to Blinky's position - needs modification
            # Simplified: Target opposite side of Pacman from a fixed point (e.g., corner)
            # Placeholder: Target 2 tiles ahead for now
            target_x = pacman_tile[0] + int(pacman_dir.x * 2)
            target_y = pacman_tile[1] + int(pacman_dir.y * 2)
            return (target_x, target_y)

        elif self.ghost_type == CLYDE: # Target Pac-Man if far, scatter if close
            dist_sq = (self.pos.x - pacman.pos.x)**2 + (self.pos.y - pacman.pos.y)**2
            if dist_sq > (8 * TILE_SIZE)**2:
                return pacman_tile # Chase Pac-Man
            else:
                return self.scatter_target # Go to scatter corner

        return pacman_tile # Default failsafe

    def choose_next_direction(self, maze, target_tile):
        """Chooses the best direction to move towards the target tile, avoiding walls and reversing."""
        possible_directions = [UP, LEFT, DOWN, RIGHT] # Priority order (Arcade style: Up > Left > Down > Right)
        current_tile_x, current_tile_y = self.get_tile_pos()
        best_dir = STOP
        min_dist_sq = float('inf')

        # Don't allow reversing direction unless at a dead end
        opposite_direction = self.direction * -1

        valid_moves = []
        for direction in possible_directions:
            if direction == opposite_direction:
                 continue # Don't allow U-turns unless forced

            next_tile_x = current_tile_x + int(direction.x)
            next_tile_y = current_tile_y + int(direction.y)

            if maze.can_move_to(next_tile_x, next_tile_y):
                valid_moves.append(direction)
                # Calculate distance squared to target from the *next* tile
                dist_sq = (next_tile_x - target_tile[0])**2 + (next_tile_y - target_tile[1])**2
                if dist_sq < min_dist_sq:
                    min_dist_sq = dist_sq
                    best_dir = direction

        if best_dir != STOP:
            self.intended_direction = best_dir
        elif valid_moves: # If target logic failed but moves are possible (e.g., target unreachable)
             # As a fallback, just pick the first valid move that isn't reversing
             self.intended_direction = valid_moves[0]
        else: # Only option is reversing (dead end)
             next_tile_x = current_tile_x + int(opposite_direction.x)
             next_tile_y = current_tile_y + int(opposite_direction.y)
             if maze.can_move_to(next_tile_x, next_tile_y):
                  self.intended_direction = opposite_direction
             else:
                  self.intended_direction = STOP # Completely stuck?

    def choose_random_direction(self, maze):
        """Used in Frightened mode. Chooses a random valid direction at an intersection."""
        possible_directions = [UP, DOWN, LEFT, RIGHT]
        random.shuffle(possible_directions)
        current_tile_x, current_tile_y = self.get_tile_pos()
        opposite_direction = self.direction * -1

        for direction in possible_directions:
            if direction == opposite_direction:
                continue # Don't reverse unless necessary

            next_tile_x = current_tile_x + int(direction.x)
            next_tile_y = current_tile_y + int(direction.y)
            if maze.can_move_to(next_tile_x, next_tile_y):
                self.intended_direction = direction
                return # Found a valid random direction

        # If only reversing is possible
        next_tile_x = current_tile_x + int(opposite_direction.x)
        next_tile_y = current_tile_y + int(opposite_direction.y)
        if maze.can_move_to(next_tile_x, next_tile_y):
             self.intended_direction = opposite_direction
        else:
             self.intended_direction = STOP # Stuck

    def draw(self, screen):
         # Use self.image which is updated in update() for state/animation
        if self.current_state == EATEN:
             # Draw simple eyes (two white squares)
             eye_size = TILE_SIZE // 4
             eye_offset = TILE_SIZE // 8
             eye_y = self.rect.centery - eye_size // 2
             eye1_rect = pygame.Rect(self.rect.centerx - eye_size - eye_offset // 2, eye_y, eye_size, eye_size)
             eye2_rect = pygame.Rect(self.rect.centerx + eye_offset // 2, eye_y, eye_size, eye_size)
             pygame.draw.rect(screen, WHITE, eye1_rect)
             pygame.draw.rect(screen, WHITE, eye2_rect)
        else:
            screen.blit(self.image, self.rect.topleft) 