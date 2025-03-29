import pygame
from constants import *

class Maze:
    def __init__(self):
        # Define the maze layout as a 2D grid
        self.layout = [
            "############################",
            "############################",
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
            "      .   #GGGGGG#   .      ",
            "######.## #GGGGGG# ##.######",
            "######.## ######## ##.######",
            "######.##          ##.######",
            "######.## ######## ##.######",
            "######.## ######## ##.######",
            "#............##............#",
            "#.####.#####.##.#####.####.#",
            "#.####.#####.##.#####.####.#",
            "#o..##.......P........##..o#",
            "###.##.##.########.##.##.###",
            "###.##.##.########.##.##.###",
            "#......##....##....##......#",
            "#.##########.##.##########.#",
            "#.##########.##.##########.#",
            "#..........................#",
            "############################"
        ]
        
        # Initialize grid with pellets, power pellets, and walls
        self.grid = []
        self.pellet_count = 0
        self.initialize_grid()
        
        # Store ghost house and Pac-Man starting positions
        self.ghost_house_positions = []
        self.pacman_start_position = None
        self.find_special_positions()
        
        # Store scatter corner targets for ghosts
        self.scatter_targets = {
            BLINKY: (GRID_WIDTH - 2, 0),  # Top-right
            PINKY: (1, 0),                # Top-left
            INKY: (GRID_WIDTH - 2, GRID_HEIGHT - 2),  # Bottom-right
            CLYDE: (1, GRID_HEIGHT - 2)   # Bottom-left
        }
    
    def initialize_grid(self):
        # Create a 2D grid from the layout
        for y, row in enumerate(self.layout):
            grid_row = []
            for x, cell in enumerate(row):
                if cell == PELLET:
                    grid_row.append(PELLET)
                    self.pellet_count += 1
                elif cell == POWER_PELLET:
                    grid_row.append(POWER_PELLET)
                    self.pellet_count += 1
                else:
                    grid_row.append(cell)
            self.grid.append(grid_row)
    
    def find_special_positions(self):
        # Find ghost house and Pac-Man starting positions
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == GHOST_HOUSE:
                    self.ghost_house_positions.append((x, y))
                elif cell == PACMAN_START:
                    self.pacman_start_position = (x, y)
                    # Replace Pac-Man marker with empty space in the grid
                    self.grid[y][x] = EMPTY
    
    def is_wall(self, x, y):
        # Check if a position is a wall
        if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0]):
            return self.grid[y][x] == WALL
        return True  # Out of bounds is considered a wall
    
    def can_move_to(self, x, y):
        # Check if a position is navigable (not a wall)
        if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0]):
            return self.grid[y][x] != WALL
        # Handle wrap-around tunnels (left/right edges)
        if y >= 0 and y < len(self.grid):
            if x < 0:
                return not self.is_wall(len(self.grid[0]) - 1, y)
            if x >= len(self.grid[0]):
                return not self.is_wall(0, y)
        return False
    
    def check_pellet(self, x, y):
        # Check if a position has a pellet or power pellet
        # Return the type of pellet (or None) and remove it if found
        if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0]):
            if self.grid[y][x] == PELLET:
                self.grid[y][x] = EMPTY
                self.pellet_count -= 1
                return PELLET
            elif self.grid[y][x] == POWER_PELLET:
                self.grid[y][x] = EMPTY
                self.pellet_count -= 1
                return POWER_PELLET
        return None
    
    def get_tile_type(self, x, y):
        # Get the type of tile at a position
        if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0]):
            return self.grid[y][x]
        return WALL  # Out of bounds is considered a wall
    
    def handle_wrap_around(self, x, y):
        # Handle wrap-around for tunnels
        if y >= 0 and y < len(self.grid):
            if x < 0:
                return len(self.grid[0]) - 1, y
            if x >= len(self.grid[0]):
                return 0, y
        return x, y
    
    def is_intersection(self, x, y):
        # Check if a position is an intersection (more than 2 possible directions)
        if self.is_wall(x, y):
            return False
        
        possible_directions = 0
        for dx, dy in [UP, DOWN, LEFT, RIGHT]:
            if self.can_move_to(x + dx, y + dy):
                possible_directions += 1
        
        return possible_directions > 2
    
    def get_valid_directions(self, x, y, current_direction=None):
        # Get all valid directions from a position
        # Excludes the opposite of current_direction (ghosts can't reverse)
        valid_directions = []
        for direction in [UP, DOWN, LEFT, RIGHT]:
            dx, dy = direction
            # Ghosts can't reverse direction unless forced
            if current_direction and (dx == -current_direction[0] and dy == -current_direction[1]):
                continue
            if self.can_move_to(x + dx, y + dy):
                valid_directions.append(direction)
        return valid_directions
    
    def draw(self, screen):
        # Draw the maze walls, pellets, and power pellets
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                # Draw walls
                if cell == WALL:
                    pygame.draw.rect(screen, MAZE_BLUE, 
                                   (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                # Draw pellets
                elif cell == PELLET:
                    pygame.draw.circle(screen, WHITE,
                                      (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2),
                                      TILE_SIZE // 10)
                # Draw power pellets (larger and possibly blinking)
                elif cell == POWER_PELLET:
                    # Make power pellets blink by checking the frame count
                    if pygame.time.get_ticks() % 500 < 250:  # Blink every half second
                        pygame.draw.circle(screen, WHITE,
                                          (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2),
                                          TILE_SIZE // 3)
