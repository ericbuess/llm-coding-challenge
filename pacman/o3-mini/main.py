import pygame
import sys
import random

# --- Constants ---
TILE_SIZE = 30
ROWS = 15
COLS = 20
WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE

# --- Maze Creation ---
def create_maze():
    """Creates a simple maze:
       - 0: empty space
       - 1: wall
       - 2: pellet (dot)
    """
    maze = []
    for r in range(ROWS):
        row_tile = []
        for c in range(COLS):
            # Set border walls
            if r == 0 or r == ROWS - 1 or c == 0 or c == COLS - 1:
                row_tile.append(1)
            else:
                # Initialize inner cells with pellets
                row_tile.append(2)
        maze.append(row_tile)

    # Add a horizontal wall in the middle (row 7) from col 3 to col 16
    for col in range(3, 17):
        maze[7][col] = 1

    # Add a vertical wall at col 10 from row 2 to 12
    for row in range(2, 13):
        maze[row][10] = 1

    # Create a passage in the horizontal wall for Pacman to cross
    maze[7][10] = 2

    return maze

# --- Game Entities ---
class Pacman:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = (255, 255, 0)  # Yellow

    def move(self, drow, dcol, maze):
        new_row = self.row + drow
        new_col = self.col + dcol
        # Check for wall collision
        if maze[new_row][new_col] != 1:
            self.row = new_row
            self.col = new_col
            # Eat pellet if present
            if maze[self.row][self.col] == 2:
                maze[self.row][self.col] = 0

class Ghost:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = (255, 0, 0)  # Red
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.current_direction = random.choice(self.directions)

    def move(self, maze):
        # Try moving in the current direction first
        new_row = self.row + self.current_direction[0]
        new_col = self.col + self.current_direction[1]
        if maze[new_row][new_col] != 1:
            self.row = new_row
            self.col = new_col
        else:
            # Choose a new valid direction randomly
            valid_dirs = []
            for d in self.directions:
                r = self.row + d[0]
                c = self.col + d[1]
                if maze[r][c] != 1:
                    valid_dirs.append(d)
            if valid_dirs:
                self.current_direction = random.choice(valid_dirs)
                self.row += self.current_direction[0]
                self.col += self.current_direction[1]

# --- Main Game Loop ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pacman Prototype")
    clock = pygame.time.Clock()

    maze = create_maze()
    # Initialize Pacman near the top-left corner (inside the maze)
    pacman = Pacman(1, 1)
    # Initialize Ghost near the bottom-right corner (inside the maze)
    ghost = Ghost(ROWS - 2, COLS - 2)

    running = True
    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pacman.move(-1, 0, maze)
                elif event.key == pygame.K_DOWN:
                    pacman.move(1, 0, maze)
                elif event.key == pygame.K_LEFT:
                    pacman.move(0, -1, maze)
                elif event.key == pygame.K_RIGHT:
                    pacman.move(0, 1, maze)

        # --- Update Ghost Position ---
        ghost.move(maze)

        # --- Check Collision (Pacman meets Ghost) ---
        if pacman.row == ghost.row and pacman.col == ghost.col:
            print("Game Over!")
            running = False

        # --- Drawing ---
        screen.fill((0, 0, 0))  # Clear screen with black

        # Draw the maze
        for row in range(ROWS):
            for col in range(COLS):
                cell = maze[row][col]
                x = col * TILE_SIZE
                y = row * TILE_SIZE
                if cell == 1:
                    # Draw wall (blue rectangle)
                    pygame.draw.rect(screen, (0, 0, 255), (x, y, TILE_SIZE, TILE_SIZE))
                elif cell == 2:
                    # Draw pellet (small white circle)
                    pygame.draw.circle(
                        screen,
                        (255, 255, 255),
                        (x + TILE_SIZE // 2, y + TILE_SIZE // 2),
                        TILE_SIZE // 6,
                    )

        # Draw Pacman
        pac_x = pacman.col * TILE_SIZE + TILE_SIZE // 2
        pac_y = pacman.row * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, pacman.color, (pac_x, pac_y), TILE_SIZE // 2 - 2)

        # Draw Ghost
        ghost_x = ghost.col * TILE_SIZE + TILE_SIZE // 2
        ghost_y = ghost.row * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, ghost.color, (ghost_x, ghost_y), TILE_SIZE // 2 - 2)

        pygame.display.flip()
        clock.tick(5)  # Limit to 5 frames per second for grid-based movement

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()