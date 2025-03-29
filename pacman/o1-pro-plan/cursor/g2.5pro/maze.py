import pygame
from constants import *

# Example Maze Layout (Reduced size for simplicity initially)
# We'll use a standard Pac-Man layout later or load from file
DEFAULT_MAZE = [
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
    "     #.##### ## #####.#     ",
    "     #.##   G  G   ##.#     ", # G = Ghost House area (not navigable initially)
    "     #.## ######## ##.#     ",
    "######.## ######## ##.######",
    "T......   ########   ......T", # T = Tunnel
    "######.## ######## ##.######",
    "     #.## ######## ##.#     ",
    "     #.##   G  G   ##.#     ",
    "     #.## ######## ##.#     ",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#o..##.......  .......##..o#", # Bottom row with power pellets
    "###.##.##.########.##.##.###",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#.##########.##.##########.#",
    "#..........................#",
    "############################"
]


class Maze:
    def __init__(self, layout=DEFAULT_MAZE):
        self.layout_str = layout
        self.grid_height = len(layout)
        self.grid_width = len(layout[0])
        self.walls = []
        self.pellets = []
        self.power_pellets = []
        self.pellet_count = 0
        self.parse_layout()

        # Pre-render maze surface for performance
        self.background = self.create_background()

    def parse_layout(self):
        """Parses the layout string to populate walls, pellets, etc."""
        for row_idx, row in enumerate(self.layout_str):
            for col_idx, char in enumerate(row):
                pos = pygame.Vector2(col_idx, row_idx)
                if char == WALL:
                    self.walls.append(pos)
                elif char == PELLET:
                    self.pellets.append(pos)
                    self.pellet_count += 1
                elif char == POWER_PELLET:
                    self.power_pellets.append(pos)
                    self.pellet_count += 1
                # Add handling for Ghost House 'G' or Tunnel 'T' if needed for logic
                # Currently, 'G' and 'T' are treated as empty navigable space by default

    def is_wall(self, tile_x, tile_y):
        """Check if a given TILE coordinate is a wall."""
        # Check bounds first
        if 0 <= tile_x < self.grid_width and 0 <= tile_y < self.grid_height:
            return pygame.Vector2(tile_x, tile_y) in self.walls
        return True # Treat out-of-bounds as walls

    def can_move_to(self, tile_x, tile_y):
        """Check if a given TILE coordinate is navigable (not a wall)."""
        # Consider tunnels for wrap-around
        if tile_x < 0 or tile_x >= self.grid_width: # Horizontal wrap
             if 0 <= tile_y < self.grid_height and self.layout_str[tile_y][0 if tile_x < 0 else self.grid_width-1] == TUNNEL:
                 return True # Allow movement into the tunnel exit tile

        if 0 <= tile_x < self.grid_width and 0 <= tile_y < self.grid_height:
            char = self.layout_str[tile_y][tile_x]
            # Basic check: not a wall. Add checks for ghost house doors later if needed.
            return char != WALL #and char != GHOST_HOUSE # Modify later for ghost house logic
        return False # Out of bounds and not a tunnel entrance

    def check_pellet_collision(self, tile_pos):
        """Check if a tile position contains a pellet or power pellet. Remove it if found."""
        if tile_pos in self.pellets:
            self.pellets.remove(tile_pos)
            self.pellet_count -= 1
            return PELLET_SCORE, False # Score, is_power_pellet
        elif tile_pos in self.power_pellets:
            self.power_pellets.remove(tile_pos)
            self.pellet_count -= 1
            return POWER_PELLET_SCORE, True # Score, is_power_pellet
        return 0, False

    def get_pellet_count(self):
        return self.pellet_count

    def create_background(self):
        """Pre-renders the static parts of the maze (walls)."""
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - 50)).convert() # Adjust height for score area
        background.fill(BLACK)
        wall_color = BLUE

        for wall_pos in self.walls:
            rect = pygame.Rect(wall_pos.x * TILE_SIZE, wall_pos.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(background, wall_color, rect)
        return background

    def draw(self, screen):
        """Draws the maze walls (from pre-rendered surface) and pellets."""
        # Draw the pre-rendered background (walls)
        screen.blit(self.background, (0, 0))

        # Draw remaining pellets
        pellet_color = WHITE
        pellet_radius = TILE_SIZE // 8
        for pellet_pos in self.pellets:
            center_x = int(pellet_pos.x * TILE_SIZE + TILE_SIZE / 2)
            center_y = int(pellet_pos.y * TILE_SIZE + TILE_SIZE / 2)
            pygame.draw.circle(screen, pellet_color, (center_x, center_y), pellet_radius)

        # Draw remaining power pellets (larger, maybe flashing later)
        power_pellet_color = WHITE
        power_pellet_radius = TILE_SIZE // 4
        for pp_pos in self.power_pellets:
            center_x = int(pp_pos.x * TILE_SIZE + TILE_SIZE / 2)
            center_y = int(pp_pos.y * TILE_SIZE + TILE_SIZE / 2)
            pygame.draw.circle(screen, power_pellet_color, (center_x, center_y), power_pellet_radius) 