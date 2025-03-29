import pygame
from constants import *

class Maze:
    def __init__(self):
        # Maze representation:
        # 0 = empty space, 1 = wall, 2 = pellet, 3 = power pellet, 4 = ghost house
        self.layout = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
            [1, 3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1],
            [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
            [1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 1, 1, 1, 4, 4, 1, 1, 1, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
            [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
            [1, 3, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 3, 1],
            [1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1],
            [1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
            [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        
        # Count initial pellets
        self.total_pellets = 0
        for row in self.layout:
            for cell in row:
                if cell == 2 or cell == 3:  # Pellet or power pellet
                    self.total_pellets += 1
        
        # Define spawn locations
        self.pacman_spawn = (14, 23)  # (x, y) in tile coordinates
        self.ghost_spawns = {
            "blinky": (14, 11),
            "pinky": (14, 13),
            "inky": (12, 13),
            "clyde": (16, 13)
        }
        
        # Ghost scatter targets (corners)
        self.scatter_targets = {
            "blinky": (25, 0),  # Top-right
            "pinky": (2, 0),    # Top-left
            "inky": (27, 30),   # Bottom-right
            "clyde": (0, 30)    # Bottom-left
        }
    
    def is_wall(self, x, y):
        """Check if the given tile is a wall."""
        # Check if tile is within bounds
        if not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT):
            return True  # Treat out of bounds as walls
        
        return self.layout[y][x] == 1
    
    def can_move_to(self, x, y):
        """Check if a character can move to the given tile."""
        # Check if tile is within bounds
        if not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT):
            # Special case for wrap-around tunnels
            if y == 14:  # Middle row
                if x < 0:  # Left tunnel
                    return True
                if x >= GRID_WIDTH:  # Right tunnel
                    return True
            return False  # Otherwise out of bounds
        
        return self.layout[y][x] != 1  # Not a wall
    
    def get_tile_type(self, x, y):
        """Get the type of tile at the given coordinates."""
        if not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT):
            return 0  # Out of bounds is empty
        
        return self.layout[y][x]
    
    def eat_pellet(self, x, y):
        """Eat a pellet at the given coordinates and return the points earned."""
        tile_type = self.get_tile_type(x, y)
        
        if tile_type == 2:  # Regular pellet
            self.layout[y][x] = 0  # Remove pellet
            return PELLET_POINTS
        elif tile_type == 3:  # Power pellet
            self.layout[y][x] = 0  # Remove power pellet
            return POWER_PELLET_POINTS
        
        return 0  # No points if no pellet
    
    def get_remaining_pellets(self):
        """Count the remaining pellets in the maze."""
        count = 0
        for row in self.layout:
            for cell in row:
                if cell == 2 or cell == 3:  # Pellet or power pellet
                    count += 1
        return count
    
    def is_ghost_house(self, x, y):
        """Check if the given tile is part of the ghost house."""
        if not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT):
            return False
        
        return self.layout[y][x] == 4
    
    def draw(self, screen):
        """Draw the maze walls, pellets, and power pellets."""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                # Draw walls
                if self.layout[y][x] == 1:
                    pygame.draw.rect(screen, BLUE, 
                                   (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                
                # Draw pellets
                elif self.layout[y][x] == 2:
                    pygame.draw.circle(screen, WHITE, 
                                     (x * TILE_SIZE + TILE_SIZE//2, 
                                      y * TILE_SIZE + TILE_SIZE//2), 
                                     TILE_SIZE//8)
                
                # Draw power pellets
                elif self.layout[y][x] == 3:
                    pygame.draw.circle(screen, WHITE, 
                                     (x * TILE_SIZE + TILE_SIZE//2, 
                                      y * TILE_SIZE + TILE_SIZE//2), 
                                     TILE_SIZE//3)
