import pygame
from . import constants as C

class Maze:
    """
    Represents the game maze, including walls, pellets, power pellets,
    spawn points, and teleport tunnels.
    """
    def __init__(self, layout_file):
        self.layout_file = layout_file
        self.walls = [] # List of (col, row) tuples for wall tiles
        self.pellets = [] # List of (col, row) tuples for pellet tiles
        self.power_pellets = [] # List of (col, row) tuples for power pellet tiles
        self.ghost_spawn_points = [] # List of (col, row) for ghost starting positions
        self.pacman_spawn_point = None # (col, row) for Pac-Man start
        self.teleport_points = {} # Dictionary mapping a teleport tile (col, row) to its destination (col, row)
        self.grid_height = 0
        self.grid_width = 0
        self.total_pellets = 0 # Count of regular pellets + power pellets
        self._load_layout()
        self._identify_teleport_points()

    def _load_layout(self):
        """Loads the maze layout from the specified file."""
        temp_teleports = {} # Store potential teleport points by row {row: [col1, col2]}
        try:
            with open(self.layout_file, 'r') as f:
                for row, line in enumerate(f):
                    self.grid_height = max(self.grid_height, row + 1)
                    self.grid_width = max(self.grid_width, len(line.strip()))
                    for col, char in enumerate(line.strip()):
                        pos = (col, row)
                        if char == '#':
                            self.walls.append(pos)
                        elif char == '.':
                            self.pellets.append(pos)
                            self.total_pellets += 1
                        elif char == 'o':
                            self.power_pellets.append(pos)
                            self.total_pellets += 1
                        elif char == 'P':
                            self.pacman_spawn_point = pos
                        elif char == 'G':
                            self.ghost_spawn_points.append(pos)
                        elif char == 'T': # Mark potential teleport points
                            if row not in temp_teleports:
                                temp_teleports[row] = []
                            temp_teleports[row].append(col)
                        # Add other characters if needed (e.g., ghost house door '-')
        except FileNotFoundError:
            print(f"Error: Maze file not found at {self.layout_file}")
            # Handle error appropriately, maybe raise exception or exit
            raise SystemExit(f"Error: Maze file not found at {self.layout_file}")

        # Ensure grid dimensions match constants if needed, or update constants
        # Note: The loaded grid dimensions might differ from constants if the file changes.
        # Consider adding a check or dynamically setting constants based on loaded size.
        if self.grid_width != C.GRID_WIDTH or self.grid_height != C.GRID_HEIGHT:
             print(f"Warning: Maze dimensions ({self.grid_width}x{self.grid_height}) "
                   f"differ from constants ({C.GRID_WIDTH}x{C.GRID_HEIGHT}).")
             # Adjust constants or handle mismatch based on design choice
             # For now, we'll proceed with loaded dimensions for logic,
             # but rendering might use constant dimensions.

        # Store teleport points found
        self.raw_teleport_coords = temp_teleports


    def _identify_teleport_points(self):
        """Connects pairs of teleport points found on the same row."""
        for row, cols in self.raw_teleport_coords.items():
            if len(cols) == 2:
                # Assume the two 'T's on the same row are connected
                p1 = (cols[0], row)
                p2 = (cols[1], row)
                self.teleport_points[p1] = p2
                self.teleport_points[p2] = p1
            elif len(cols) > 2:
                print(f"Warning: Found more than two teleport markers 'T' on row {row}. Teleportation might be unpredictable.")
            # If only one 'T' on a row, it's ignored as it needs a pair.

    def is_wall(self, col, row):
        """Checks if the given tile coordinates correspond to a wall."""
        return (col, row) in self.walls

    def get_pellet_type(self, col, row):
        """Checks if a tile contains a pellet or power pellet."""
        pos = (col, row)
        if pos in self.pellets:
            return "pellet"
        if pos in self.power_pellets:
            return "power_pellet"
        return None

    def remove_pellet(self, col, row):
        """Removes a pellet or power pellet from the maze."""
        pos = (col, row)
        removed = False
        if pos in self.pellets:
            self.pellets.remove(pos)
            removed = True
        elif pos in self.power_pellets:
            self.power_pellets.remove(pos)
            removed = True

        if removed:
            self.total_pellets -= 1 # Decrement remaining count
        return removed

    def get_teleport_destination(self, col, row):
        """Returns the destination tile if the current tile is a teleport point."""
        return self.teleport_points.get((col, row))

    def draw(self, screen):
        """Draws the maze elements (walls, pellets, power pellets) onto the screen."""
        # Draw Walls
        wall_color = C.BLUE # Use color from constants
        for wall_pos in self.walls:
            rect = pygame.Rect(wall_pos[0] * C.TILE_SIZE, wall_pos[1] * C.TILE_SIZE,
                               C.TILE_SIZE, C.TILE_SIZE)
            pygame.draw.rect(screen, wall_color, rect)

        # Draw Pellets
        pellet_color = C.PELLET_COLOR
        pellet_radius = C.TILE_SIZE // 6 # Small radius for pellets
        for pellet_pos in self.pellets:
            center_x = int(pellet_pos[0] * C.TILE_SIZE + C.TILE_SIZE / 2)
            center_y = int(pellet_pos[1] * C.TILE_SIZE + C.TILE_SIZE / 2)
            pygame.draw.circle(screen, pellet_color, (center_x, center_y), pellet_radius)

        # Draw Power Pellets
        power_pellet_color = C.POWER_PELLET_COLOR
        power_pellet_radius = C.TILE_SIZE // 3 # Larger radius
        # Add blinking effect? Could use pygame.time.get_ticks()
        for pp_pos in self.power_pellets:
            center_x = int(pp_pos[0] * C.TILE_SIZE + C.TILE_SIZE / 2)
            center_y = int(pp_pos[1] * C.TILE_SIZE + C.TILE_SIZE / 2)
            pygame.draw.circle(screen, power_pellet_color, (center_x, center_y), power_pellet_radius)

    def all_pellets_eaten(self):
        """Checks if all pellets and power pellets have been consumed."""
        # Check based on the count rather than list emptiness for efficiency
        return self.total_pellets <= 0

# Example usage (for testing purposes, remove later)
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Test")
    clock = pygame.time.Clock()

    # Assuming maze1.txt is in the same directory or correct path is given
    maze = Maze('maze1.txt')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(C.BLACK)
        maze.draw(screen)
        pygame.display.flip()
        clock.tick(C.FPS)

    pygame.quit()
    print("Pacman Spawn:", maze.pacman_spawn_point)
    print("Ghost Spawns:", maze.ghost_spawn_points)
    print("Teleport Points:", maze.teleport_points)
    print("Total Pellets:", maze.total_pellets) # Initial count