"""
Maze module for Pac-Man game
"""
import pygame
from constants import *

class Maze:
    """
    Handles the maze layout, collision detection, and pellet management
    """
    
    def __init__(self):
        """Initialize the maze with layout and pellet tracking"""
        # The maze layout represents the classic Pac-Man maze
        # # = wall, . = pellet, o = power pellet, space = empty path
        # G = ghost house area, P = Pac-Man start position
        # B, I, P, C = Ghost start positions (Blinky, Inky, Pinky, Clyde)
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
            "######.## ###GG### ##.######",
            "######.## #BGIPC# ##.######",
            "      .   #GGGGG#   .      ",  # Tunnel
            "######.## ####### ##.######",
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
            "#..........P...............#",
            "############################"
        ]
        
        # Track pellets that are still in the maze
        self.pellets = {}  # (x,y) -> True/False for pellet existence
        self.power_pellets = {}  # (x,y) -> True/False for power pellet existence
        self.total_pellets = 0
        self.remaining_pellets = 0
        
        # Parse layout and track spawn positions
        self.pacman_spawn = None
        self.ghost_spawns = {
            BLINKY: None,
            PINKY: None,
            INKY: None,
            CLYDE: None
        }
        self.ghost_house_positions = []
        
        self._parse_layout()
        
        # Create rect for wall collision
        self.wall_rects = []
        self._create_wall_rects()

    def _parse_layout(self):
        """Parse the layout to identify walls, pellets, and spawn positions"""
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                if cell == PELLET:
                    self.pellets[(x, y)] = True
                    self.total_pellets += 1
                    self.remaining_pellets += 1
                elif cell == POWER_PELLET:
                    self.power_pellets[(x, y)] = True
                    self.total_pellets += 1
                    self.remaining_pellets += 1
                elif cell == PACMAN_START:
                    # Store Pacman's spawn position in tile coordinates
                    self.pacman_spawn = (x * TILE_SIZE + TILE_SIZE // 2, 
                                         y * TILE_SIZE + TILE_SIZE // 2)
                    # This position should also be an empty path (not a wall)
                    # Don't place a pellet here
                elif cell == 'B':
                    self.ghost_spawns[BLINKY] = (x * TILE_SIZE + TILE_SIZE // 2, 
                                                y * TILE_SIZE + TILE_SIZE // 2)
                elif cell == 'P':
                    self.ghost_spawns[PINKY] = (x * TILE_SIZE + TILE_SIZE // 2, 
                                               y * TILE_SIZE + TILE_SIZE // 2)
                elif cell == 'I':
                    self.ghost_spawns[INKY] = (x * TILE_SIZE + TILE_SIZE // 2, 
                                              y * TILE_SIZE + TILE_SIZE // 2)
                elif cell == 'C':
                    self.ghost_spawns[CLYDE] = (x * TILE_SIZE + TILE_SIZE // 2, 
                                               y * TILE_SIZE + TILE_SIZE // 2)
                elif cell == GHOST_HOUSE:
                    self.ghost_house_positions.append((x, y))

        # Print debug info about Pacman spawn
        print(f"Pacman spawn position: {self.pacman_spawn}")
                    
        # If specific spawn points weren't defined, use default positions
        if not self.pacman_spawn:
            self.pacman_spawn = (GRID_WIDTH // 2 * TILE_SIZE + TILE_SIZE // 2, 
                                 (GRID_HEIGHT - 3) * TILE_SIZE + TILE_SIZE // 2)
            print(f"Using default Pacman spawn: {self.pacman_spawn}")
        
        # Default ghost spawn points if not specified
        for ghost in [BLINKY, PINKY, INKY, CLYDE]:
            if not self.ghost_spawns[ghost]:
                self.ghost_spawns[ghost] = (GRID_WIDTH // 2 * TILE_SIZE + TILE_SIZE // 2, 
                                           (GRID_HEIGHT // 2 - 2) * TILE_SIZE + TILE_SIZE // 2)

    def _create_wall_rects(self):
        """Create pygame Rects for wall collision detection"""
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                if cell == WALL:
                    self.wall_rects.append(pygame.Rect(
                        x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE
                    ))

    def is_wall(self, x, y):
        """Check if the given tile coordinates contain a wall"""
        # Convert pixel coordinates to tile coordinates if needed
        if x >= TILE_SIZE or y >= TILE_SIZE:
            tile_x, tile_y = x // TILE_SIZE, y // TILE_SIZE
        else:
            tile_x, tile_y = x, y
            
        # Check bounds
        if (tile_x < 0 or tile_x >= GRID_WIDTH or 
            tile_y < 0 or tile_y >= GRID_HEIGHT):
            return True  # Out of bounds is considered a wall
        
        # Log wall checks for debugging
        cell = self.layout[tile_y][tile_x]
        is_wall_result = cell == WALL
        if is_wall_result:
            print(f"Wall detected at ({tile_x}, {tile_y})")
            
        return is_wall_result

    def is_intersection(self, x, y):
        """
        Check if the given tile is an intersection (has more than 2 directions to move)
        Used for ghost AI decision making
        """
        tile_x, tile_y = x // TILE_SIZE, y // TILE_SIZE
        
        # Count available directions
        directions = 0
        for direction in [UP, DOWN, LEFT, RIGHT]:
            next_x, next_y = tile_x + direction[0], tile_y + direction[1]
            if not self.is_wall(next_x, next_y):
                directions += 1
        
        return directions > 2

    def get_valid_directions(self, x, y, current_direction=None):
        """
        Get all valid directions from the current position
        Excludes the opposite of current_direction to prevent 180-degree turns
        """
        tile_x, tile_y = x // TILE_SIZE, y // TILE_SIZE
        valid_directions = []
        
        for direction in [UP, DOWN, LEFT, RIGHT]:
            # Skip the opposite direction if current_direction is provided
            if (current_direction and direction[0] == -current_direction[0] and 
                direction[1] == -current_direction[1]):
                continue
                
            next_x, next_y = tile_x + direction[0], tile_y + direction[1]
            if not self.is_wall(next_x, next_y):
                valid_directions.append(direction)
        
        return valid_directions

    def check_wrap_around(self, x, y):
        """Check and handle the wrap-around tunnels at the edges"""
        # Left to right wrap
        if x < 0:
            return GRID_WIDTH * TILE_SIZE, y
        # Right to left wrap
        elif x >= GRID_WIDTH * TILE_SIZE:
            return 0, y
        # No wrap needed
        return x, y

    def consume_pellet(self, x, y):
        """
        Try to consume a pellet at the given position
        Returns the score gained (0 if no pellet was consumed)
        """
        tile_x, tile_y = x // TILE_SIZE, y // TILE_SIZE
        pos = (tile_x, tile_y)
        
        # Check for regular pellet
        if pos in self.pellets and self.pellets[pos]:
            self.pellets[pos] = False
            self.remaining_pellets -= 1
            return PELLET_SCORE
            
        # Check for power pellet
        if pos in self.power_pellets and self.power_pellets[pos]:
            self.power_pellets[pos] = False
            self.remaining_pellets -= 1
            return POWER_PELLET_SCORE
            
        return 0

    def is_power_pellet(self, x, y):
        """Check if the given position has a power pellet"""
        tile_x, tile_y = x // TILE_SIZE, y // TILE_SIZE
        pos = (tile_x, tile_y)
        return pos in self.power_pellets and self.power_pellets[pos]

    def draw(self, screen):
        """Draw the maze walls, pellets, and power pellets"""
        # Fill background
        screen.fill(BLACK)
        
        # Draw walls
        for rect in self.wall_rects:
            pygame.draw.rect(screen, BLUE, rect)
        
        # Draw pellets
        for pos, exists in self.pellets.items():
            if exists:
                x, y = pos
                pygame.draw.circle(
                    screen, 
                    WHITE, 
                    (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), 
                    2
                )
        
        # Draw power pellets (slightly larger, possibly blinking)
        for pos, exists in self.power_pellets.items():
            if exists:
                x, y = pos
                # Blink on even seconds
                if pygame.time.get_ticks() // 500 % 2 == 0:
                    pygame.draw.circle(
                        screen, 
                        WHITE, 
                        (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), 
                        6
                    ) 