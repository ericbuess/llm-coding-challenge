import pygame
import math
from .constants import *
from .ai import GhostAI

class Entity:
    """Base class for all game entities (Pacman and Ghosts)"""
    def __init__(self, x: float, y: float):
        self.x = x  # pixel coordinates
        self.y = y
        self.tile_x = int(x // TILE_SIZE)
        self.tile_y = int(y // TILE_SIZE)
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.speed = 0
    
    def update_tile_position(self):
        """Update tile position based on pixel position"""
        self.tile_x = int(self.x // TILE_SIZE)
        self.tile_y = int(self.y // TILE_SIZE)
    
    def get_center(self) -> tuple:
        """Get the center pixel coordinates of the entity"""
        return (self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2)
    
    def is_centered(self) -> bool:
        """Check if entity is centered on a tile"""
        center_x = self.tile_x * TILE_SIZE + TILE_SIZE // 2
        center_y = self.tile_y * TILE_SIZE + TILE_SIZE // 2
        tolerance = 2  # pixels
        return (abs(self.x + TILE_SIZE // 2 - center_x) < tolerance and
                abs(self.y + TILE_SIZE // 2 - center_y) < tolerance)
    
    def can_move(self, board, direction: tuple) -> bool:
        """Check if entity can move in given direction"""
        if direction == (0, 0):
            return False
        
        # Calculate the position we're trying to move to
        next_x = self.x + direction[0] * self.speed
        next_y = self.y + direction[1] * self.speed
        
        # Special case for tunnel - allow movement off screen edges at row 14
        if self.tile_y == 14:
            if (direction == LEFT and self.x <= 0) or (direction == RIGHT and self.x >= SCREEN_WIDTH - TILE_SIZE):
                return True  # Allow movement through tunnel
        
        # Check all four corners of the entity's bounding box
        margin = 1  # Small margin to prevent getting too close to walls
        corners = [
            (next_x + margin, next_y + margin),  # Top-left
            (next_x + TILE_SIZE - margin, next_y + margin),  # Top-right
            (next_x + margin, next_y + TILE_SIZE - margin),  # Bottom-left
            (next_x + TILE_SIZE - margin, next_y + TILE_SIZE - margin)  # Bottom-right
        ]
        
        # Check if any corner would be in a wall
        for corner_x, corner_y in corners:
            # Skip boundary check for tunnel
            if corner_x < 0 or corner_x >= SCREEN_WIDTH:
                if self.tile_y == 14:  # Tunnel row
                    continue
                else:
                    return False
            
            tile_x = int(corner_x // TILE_SIZE)
            tile_y = int(corner_y // TILE_SIZE)
            if board.is_wall(tile_x, tile_y):
                return False
        
        return True
    
    def update(self, board):
        """Update entity position - to be overridden by subclasses"""
        pass
    
    def handle_tunnel_wrap(self):
        """Handle tunnel wrapping at screen edges"""
        # Check for horizontal wrap (tunnels are at row 14)
        if self.tile_y == 14:  # Tunnel row
            if self.x < -TILE_SIZE:  # Went off left edge
                self.x = SCREEN_WIDTH
                self.update_tile_position()
            elif self.x > SCREEN_WIDTH:  # Went off right edge
                self.x = -TILE_SIZE
                self.update_tile_position()


class Pacman(Entity):
    """Pacman character class"""
    def __init__(self, x: float, y: float):
        # Convert tile coordinates to pixel coordinates
        super().__init__(x * TILE_SIZE, y * TILE_SIZE)
        self.speed = PACMAN_SPEED
        self.animation_frame = 0
        self.is_dying = False
        self.is_moving = False
    
    def handle_input(self, keys):
        """Handle keyboard input for Pacman movement"""
        # Store the desired direction based on key press
        if keys[pygame.K_UP]:
            self.next_direction = UP
        elif keys[pygame.K_DOWN]:
            self.next_direction = DOWN
        elif keys[pygame.K_LEFT]:
            self.next_direction = LEFT
        elif keys[pygame.K_RIGHT]:
            self.next_direction = RIGHT
    
    def update(self, board):
        """Update Pacman's position with smooth movement"""
        # Check if we can turn at current tile center
        if self.next_direction != self.direction:
            if self.is_centered() and self.can_move(board, self.next_direction):
                self.direction = self.next_direction
        
        # Move in current direction
        if self.can_move(board, self.direction):
            self.x += self.direction[0] * self.speed
            self.y += self.direction[1] * self.speed
            self.update_tile_position()
            self.is_moving = True
            
            # Handle tunnel wrapping
            self.handle_tunnel_wrap()
        else:
            self.is_moving = False
        
        # Animate if moving
        if self.is_moving:
            self.animation_frame = (self.animation_frame + 1) % 30
    
    def check_pellet_collision(self, board) -> dict:
        """Check if Pacman is on a pellet and collect it"""
        result = {'pellet': False, 'power_pellet': False, 'points': 0}
        
        # Check if we're centered enough on a tile to collect its pellet
        if self.is_centered():
            collected = board.remove_pellet(self.tile_x, self.tile_y)
            if collected['pellet']:
                result['pellet'] = True
                result['points'] = 10
            elif collected['power_pellet']:
                result['power_pellet'] = True
                result['points'] = 50
        
        return result


class Ghost(Entity):
    """Ghost character class with AI behaviors"""
    def __init__(self, x: float, y: float, name: str, color: tuple):
        # Convert tile coordinates to pixel coordinates
        super().__init__(x * TILE_SIZE, y * TILE_SIZE)
        self.name = name
        self.color = color
        self.mode = 'scatter'  # scatter, chase, frightened, eyes
        self.frightened_timer = 0
        self.target_tile = (0, 0)
        self.home_tile = self.get_home_tile()
        self.speed = GHOST_SPEED
        self.spawn_tile = (x, y)  # Remember spawn position
        self.mode_timer = 0  # For scatter/chase switching
        self.in_ghost_house = True  # Start in ghost house
        self.exit_timer = 0  # Delay before leaving ghost house
        # Give ghosts an initial direction to prevent getting stuck
        if self.name == 'blinky':
            self.direction = LEFT
        else:
            self.direction = UP
    
    def get_home_tile(self) -> tuple:
        """Get the home corner tile for this ghost"""
        # Each ghost has a different home corner for scatter mode
        if self.name == 'blinky':
            return (BOARD_WIDTH - 3, 0)  # Top-right
        elif self.name == 'pinky':
            return (2, 0)  # Top-left
        elif self.name == 'inky':
            return (BOARD_WIDTH - 1, BOARD_HEIGHT - 1)  # Bottom-right
        elif self.name == 'clyde':
            return (0, BOARD_HEIGHT - 1)  # Bottom-left
        return (0, 0)
    
    def update_target(self, pacman, blinky=None):
        """Update target tile based on current mode and ghost type"""
        pacman_tile = (pacman.tile_x, pacman.tile_y)
        
        if self.mode == 'frightened':
            # No specific target when frightened (random movement)
            self.target_tile = None
        elif self.mode == 'eyes':
            # Return to spawn position
            self.target_tile = self.spawn_tile
        elif self.mode == 'scatter':
            # Go to home corner
            self.target_tile = self.home_tile
        elif self.mode == 'chase':
            # Each ghost has different chase behavior
            if self.name == 'blinky':
                self.target_tile = GhostAI.get_blinky_target(pacman_tile)
            elif self.name == 'pinky':
                self.target_tile = GhostAI.get_pinky_target(pacman_tile, pacman.direction)
            elif self.name == 'inky' and blinky:
                blinky_tile = (blinky.tile_x, blinky.tile_y)
                self.target_tile = GhostAI.get_inky_target(pacman_tile, pacman.direction, blinky_tile)
            elif self.name == 'clyde':
                self.target_tile = GhostAI.get_clyde_target(pacman_tile, 
                                                           (self.tile_x, self.tile_y), 
                                                           self.home_tile)
    
    def update(self, board, pacman=None, blinky=None):
        """Update ghost position and behavior"""
        # Handle ghost house exit
        if self.in_ghost_house:
            self.exit_timer += 1
            # Different ghosts exit at different times
            exit_delays = {'blinky': 0, 'pinky': 60, 'inky': 120, 'clyde': 180}
            if self.exit_timer > exit_delays.get(self.name, 0):
                self.in_ghost_house = False
                # Move to just outside ghost house
                self.y -= TILE_SIZE * 3
                self.update_tile_position()
                # Set initial direction
                self.direction = UP
        
        # Update mode timer (for scatter/chase switching)
        if self.mode in ['scatter', 'chase']:
            self.mode_timer += 1
            # Switch modes every 7 seconds (420 frames at 60 FPS)
            if self.mode_timer > 420:
                self.mode = 'chase' if self.mode == 'scatter' else 'scatter'
                self.mode_timer = 0
        
        # Update frightened timer
        if self.mode == 'frightened':
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                self.mode = 'scatter'
                self.speed = GHOST_SPEED
        
        # Check if reached spawn position when eyes
        if self.mode == 'eyes' and self.is_centered():
            if self.tile_x == self.spawn_tile[0] and self.tile_y == self.spawn_tile[1]:
                self.mode = 'scatter'
                self.speed = GHOST_SPEED
                self.in_ghost_house = True
                self.exit_timer = 30  # Brief delay before re-emerging
        
        # Ensure proper speed for current mode
        if self.mode == 'frightened':
            self.speed = FRIGHTENED_SPEED
        elif self.mode == 'eyes':
            self.speed = GHOST_SPEED * 2
        else:
            self.speed = GHOST_SPEED
        
        # Update target
        if pacman and not self.in_ghost_house:
            self.update_target(pacman, blinky)
        
        # Move towards target
        if not self.in_ghost_house:
            self.move_towards_target(board)
    
    def move_towards_target(self, board):
        """Move ghost towards its target tile"""
        # Always try to update direction when centered on a tile
        if self.is_centered():
            current_tile = (self.tile_x, self.tile_y)
            
            if self.mode == 'frightened':
                # Random movement when frightened
                new_direction = GhostAI.get_frightened_direction(current_tile, board, self.direction)
            elif self.target_tile:
                # Normal pathfinding towards target
                new_direction = GhostAI.get_next_direction(current_tile, self.target_tile, 
                                                          board, self.direction)
            else:
                new_direction = self.direction
            
            # Update direction if we can move that way
            if new_direction != (0, 0) and self.can_move(board, new_direction):
                self.direction = new_direction
            elif self.direction == (0, 0) or not self.can_move(board, self.direction):
                # If we have no direction or can't move, try all directions
                for test_dir in [UP, DOWN, LEFT, RIGHT]:
                    if self.can_move(board, test_dir):
                        self.direction = test_dir
                        break
        
        # Move in current direction
        if self.direction != (0, 0) and self.can_move(board, self.direction):
            self.x += self.direction[0] * self.speed
            self.y += self.direction[1] * self.speed
            self.update_tile_position()
            
            # Handle tunnel wrapping
            self.handle_tunnel_wrap()
    
    def set_frightened(self, duration):
        """Set ghost to frightened mode"""
        if self.mode != 'eyes':  # Can't frighten eyes
            self.mode = 'frightened'
            self.frightened_timer = duration
            self.speed = FRIGHTENED_SPEED
            # Reverse direction
            self.direction = (-self.direction[0], -self.direction[1])