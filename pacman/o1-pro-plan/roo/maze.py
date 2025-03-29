"""
Maze module for the Pac-Man game
Handles the maze layout, collision detection, and pellet tracking
"""

import pygame
from constants import *

class Maze:
    def __init__(self):
        """Initialize the maze with a default layout"""
        # The maze layout uses characters to represent different tile types:
        # '#' (WALL): Wall tiles
        # '.' (PELLET): Regular pellets
        # 'o' (POWER_PELLET): Power pellets
        # ' ' (EMPTY): Empty paths
        # 'G' (GHOST_HOUSE): Ghost house area
        # 'P' (PACMAN_START): Pac-Man's starting position
        # 'B', 'p', 'I', 'C': Starting positions for the ghosts
        
        self.layout = [
            "############################",
            "#............##............#",
            "#.####.#####.##.#####.####.#",
            "#o####.#####.##.#####.####o#",
            "#.####.#####.##.#####.####.#",
            "#..........................#",
            "#.####.##.########.##.####.#",
            "#.####.##.########.##.####.#",
            "#......##....##....##......#",
            "######.##### ## #####.######",
            "######.##### ## #####.######",
            "######.##          ##.######",
            "######.## ######## ##.######",
            "######.## #GGGGGG# ##.######",
            "      .   #GBpICG#   .      ",
            "######.## #GGGGGG# ##.######",
            "######.## ######## ##.######",
            "######.##          ##.######",
            "######.## ######## ##.######",
            "######.## ######## ##.######",
            "#............##............#",
            "#.####.#####.##.#####.####.#",
            "#.####.#####.##.#####.####.#",
            "#o..##................##..o#",
            "###.##.##.########.##.##.###",
            "###.##.##.########.##.##.###",
            "#......##....##....##......#",
            "#.##########.##.##########.#",
            "#.##########.##.##########.#",
            "#..........................#",
            "############################"
        ]
        
        # Convert the layout to a 2D grid for easier access
        self.grid = []
        self.total_pellets = 0
        self.pellets_eaten = 0
        
        # Process the layout and create the grid
        for y, row in enumerate(self.layout):
            grid_row = []
            for x, cell in enumerate(row):
                grid_row.append(cell)
                if cell == PELLET or cell == POWER_PELLET:
                    self.total_pellets += 1
            self.grid.append(grid_row)
        
        # Store starting positions for entities
        self.pacman_start = self.find_position(PACMAN_START)
        if not self.pacman_start:
            # Default position if not specified in the layout
            self.pacman_start = (14, 23)
        
        self.ghost_starts = {}
        for ghost_name, ghost_char in GHOST_START.items():
            position = self.find_position(ghost_char)
            if position:
                self.ghost_starts[ghost_name] = position
        
        # If ghost start positions are not specified, set defaults
        if not self.ghost_starts:
            self.ghost_starts = {
                'BLINKY': (14, 14),
                'PINKY': (13, 14),
                'INKY': (15, 14),
                'CLYDE': (16, 14)
            }

    def find_position(self, char):
        """Find the position of a specific character in the layout"""
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                if cell == char:
                    return (x, y)
        return None

    def is_wall(self, x, y):
        """Check if a tile is a wall"""
        # Check if coordinates are out of bounds
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return False  # Allow wrap-around tunnels
        
        return self.grid[y][x] == WALL

    def can_move_to(self, x, y):
        """Check if an entity can move to a specific tile"""
        # Wrap around for tunnels
        if x < 0:
            x = GRID_WIDTH - 1
        elif x >= GRID_WIDTH:
            x = 0
        
        # Normal bounds check for y
        if y < 0 or y >= GRID_HEIGHT:
            return False
        
        return self.grid[y][x] != WALL

    def get_tile_type(self, x, y):
        """Get the type of tile at a specific position"""
        # Wrap around for tunnels
        if x < 0:
            x = GRID_WIDTH - 1
        elif x >= GRID_WIDTH:
            x = 0
        
        # Normal bounds check for y
        if y < 0 or y >= GRID_HEIGHT:
            return WALL  # Treat out of bounds as walls
        
        return self.grid[y][x]

    def eat_pellet(self, x, y):
        """
        Try to eat a pellet at the specified position
        Returns the score earned (0 if no pellet)
        """
        # Wrap around for tunnels
        if x < 0:
            x = GRID_WIDTH - 1
        elif x >= GRID_WIDTH:
            x = 0
        
        # Check if there's a pellet at this position
        tile_type = self.grid[y][x]
        
        if tile_type == PELLET:
            self.grid[y][x] = EMPTY
            self.pellets_eaten += 1
            return PELLET_SCORE
        
        elif tile_type == POWER_PELLET:
            self.grid[y][x] = EMPTY
            self.pellets_eaten += 1
            return POWER_PELLET_SCORE
        
        return 0
    
    def is_pellet(self, x, y):
        """Check if there's a pellet at the specified position"""
        tile_type = self.get_tile_type(x, y)
        return tile_type == PELLET
    
    def is_power_pellet(self, x, y):
        """Check if there's a power pellet at the specified position"""
        tile_type = self.get_tile_type(x, y)
        return tile_type == POWER_PELLET
    
    def all_pellets_eaten(self):
        """Check if all pellets have been eaten"""
        return self.pellets_eaten >= self.total_pellets
    
    def draw(self, screen):
        """Draw the maze, pellets, and power pellets"""
        # Draw the maze walls and other elements
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                # Calculate pixel position
                pixel_x = x * TILE_SIZE
                pixel_y = y * TILE_SIZE
                
                # Draw walls
                if cell == WALL:
                    pygame.draw.rect(screen, BLUE, (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE))
                
                # Draw pellets
                elif cell == PELLET:
                    pygame.draw.circle(screen, WHITE, 
                                      (pixel_x + TILE_SIZE // 2, pixel_y + TILE_SIZE // 2), 
                                      TILE_SIZE // 8)
                
                # Draw power pellets (larger and possibly blinking)
                elif cell == POWER_PELLET:
                    # Blink the power pellet every half second
                    if pygame.time.get_ticks() % 1000 < 500:
                        pygame.draw.circle(screen, WHITE, 
                                          (pixel_x + TILE_SIZE // 2, pixel_y + TILE_SIZE // 2), 
                                          TILE_SIZE // 3)