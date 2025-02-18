import pygame
import sys
import random

# Initialize pygame
pygame.init()

# --------------------------
# Game settings and globals
# --------------------------
TILE_SIZE = 24
FPS = 10  # grid-based movement, so a lower FPS makes movement more “stepwise”

# Colors (R, G, B)
BLACK   = (0, 0, 0)
BLUE    = (0, 0, 255)
YELLOW  = (255, 255, 0)
RED     = (255, 0, 0)
WHITE   = (255, 255, 255)

# Maze layout:
#
# Legend:
#   '#'  Wall
#   '.'  Pellet
#   ' '  Empty space
#
# For simplicity Pacman and the ghost will start at hard-coded positions.
maze_layout = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "############################"
]

ROWS = len(maze_layout)
COLS = len(maze_layout[0])
SCREEN_WIDTH = COLS * TILE_SIZE
SCREEN_HEIGHT = ROWS * TILE_SIZE

# Movement delays (in milliseconds)
MOVE_DELAY = 150       # delay for Pacman moves
GHOST_MOVE_DELAY = 300 # ghost moves every 300ms

# --------------------------
# Utility functions
# --------------------------
def is_wall(grid_x, grid_y):
    """Return True if the cell (grid_x, grid_y) is a wall or out of bounds."""
    if grid_y < 0 or grid_y >= ROWS or grid_x < 0 or grid_x >= COLS:
        return True
    return maze_layout[grid_y][grid_x] == '#'

# --------------------------
# Game objects
# --------------------------
class Pacman:
    def __init__(self, grid_x, grid_y):
        self.x = grid_x
        self.y = grid_y
        self.color = YELLOW
        self.last_move_time = 0

    def move(self, dx, dy, current_time):
        if current_time - self.last_move_time < MOVE_DELAY:
            return
        new_x = self.x + dx
        new_y = self.y + dy
        if not is_wall(new_x, new_y):
            self.x = new_x
            self.y = new_y
            self.last_move_time = current_time

    def draw(self, surface):
        # draw Pacman as a circle centered in its tile
        center = (self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2)
        pygame.draw.circle(surface, self.color, center, TILE_SIZE // 2 - 2)

class Ghost:
    def __init__(self, grid_x, grid_y):
        self.x = grid_x
        self.y = grid_y
        self.color = RED
        self.last_move_time = 0

    def update(self, current_time):
        if current_time - self.last_move_time < GHOST_MOVE_DELAY:
            return
        # possible directions: up, down, left, right
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        possible_moves = []
        for dx, dy in directions:
            new_x = self.x + dx
            new_y = self.y + dy
            if not is_wall(new_x, new_y):
                possible_moves.append((dx, dy))
        if possible_moves:
            dx, dy = random.choice(possible_moves)
            self.x += dx
            self.y += dy
            self.last_move_time = current_time

    def draw(self, surface):
        # draw Ghost as a circle centered in its tile
        center = (self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2)
        pygame.draw.circle(surface, self.color, center, TILE_SIZE // 2 - 2)

# --------------------------
# Main game loop
# --------------------------
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pacman in Python")
    clock = pygame.time.Clock()

    # Create pellet set from the maze layout (each pellet is at a cell with '.')
    pellets = set()
    for row in range(ROWS):
        for col in range(COLS):
            if maze_layout[row][col] == '.':
                pellets.add((col, row))

    # Create game objects.
    # For this example, we choose starting positions that are not walls.
    pacman = Pacman(1, 1)   # Top-left-ish position
    ghost = Ghost(COLS - 2, ROWS - 2)  # Bottom-right-ish position

    score = 0
    font = pygame.font.SysFont("Arial", 18)

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle key presses for Pacman movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            pacman.move(-1, 0, current_time)
        elif keys[pygame.K_RIGHT]:
            pacman.move(1, 0, current_time)
        elif keys[pygame.K_UP]:
            pacman.move(0, -1, current_time)
        elif keys[pygame.K_DOWN]:
            pacman.move(0, 1, current_time)

        # Update ghost movement
        ghost.update(current_time)

        # Check for pellet collision
        pacman_pos = (pacman.x, pacman.y)
        if pacman_pos in pellets:
            pellets.remove(pacman_pos)
            score += 10

        # Check for collision with ghost
        if pacman.x == ghost.x and pacman.y == ghost.y:
            print("Game Over! Final Score:", score)
            running = False

        # Drawing section
        screen.fill(BLACK)

        # Draw maze walls and pellets
        for row in range(ROWS):
            for col in range(COLS):
                cell = maze_layout[row][col]
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if cell == '#':
                    pygame.draw.rect(screen, BLUE, rect)
                # Note: pellets are drawn from our set so that if eaten they disappear.
                if (col, row) in pellets:
                    pellet_center = (col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2)
                    pygame.draw.circle(screen, WHITE, pellet_center, 3)

        # Draw game objects
        pacman.draw(screen)
        ghost.draw(screen)

        # Draw score
        score_surface = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surface, (10, SCREEN_HEIGHT - 30))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
