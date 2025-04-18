import pygame
import random
import sys

# Constants
TILE_SIZE = 24
GRID_WIDTH = 15
GRID_HEIGHT = 15
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE + 40  # extra for score display
FPS = 10

# Colors
BLACK = (0, 0, 0)
BLUE = (33, 33, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Maze layout (#=wall, .=pellet)
maze = [
    "###############",
    "#.............#",
    "#.###########.#",
    "#.#.........#.#",
    "#.#.#######.#.#",
    "#.#.#.....#.#.#",
    "#.#.#.###.#.#.#",
    "#.............#",
    "#.#.#.###.#.#.#",
    "#.#.#.....#.#.#",
    "#.#.#######.#.#",
    "#.#.........#.#",
    "#.###########.#",
    "#.............#",
    "###############",
]

def draw_maze(screen):
    for r, row in enumerate(maze):
        for c, ch in enumerate(row):
            if ch == '#':
                pygame.draw.rect(screen, BLUE,
                                 (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE))

class Pacman:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * TILE_SIZE
        self.y = row * TILE_SIZE
        self.dx = 0
        self.dy = 0

    def change_direction(self, key):
        if key == pygame.K_LEFT:
            self.dx, self.dy = -1, 0
        elif key == pygame.K_RIGHT:
            self.dx, self.dy = 1, 0
        elif key == pygame.K_UP:
            self.dx, self.dy = 0, -1
        elif key == pygame.K_DOWN:
            self.dx, self.dy = 0, 1

    def move(self):
        # Check for wall collision
        new_col = self.col + self.dx
        new_row = self.row + self.dy
        if 0 <= new_row < GRID_HEIGHT and 0 <= new_col < GRID_WIDTH:
            if maze[new_row][new_col] != '#':
                self.col = new_col
                self.row = new_row
                self.x = self.col * TILE_SIZE
                self.y = self.row * TILE_SIZE

    def eat(self, pellets):
        if (self.x + TILE_SIZE//2, self.y + TILE_SIZE//2) in pellets:
            pellets.remove((self.x + TILE_SIZE//2, self.y + TILE_SIZE//2))
            return True
        return False

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW,
                           (self.x + TILE_SIZE//2, self.y + TILE_SIZE//2), TILE_SIZE//2)

class Ghost:
    def __init__(self, row, col, color=RED):
        self.row = row
        self.col = col
        self.x = col * TILE_SIZE
        self.y = row * TILE_SIZE
        self.dx, self.dy = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        self.color = color

    def move(self):
        # At center, choose new direction if blocked or at tile center
        if self.x % TILE_SIZE == 0 and self.y % TILE_SIZE == 0:
            dirs = [(1,0),(-1,0),(0,1),(0,-1)]
            valid = []
            for dx, dy in dirs:
                nr, nc = self.row + dy, self.col + dx
                if 0 <= nr < GRID_HEIGHT and 0 <= nc < GRID_WIDTH:
                    if maze[nr][nc] != '#':
                        valid.append((dx, dy))
            if valid:
                self.dx, self.dy = random.choice(valid)
            self.row += self.dy
            self.col += self.dx
            self.x = self.col * TILE_SIZE
            self.y = self.row * TILE_SIZE
        else:
            # move pixel by pixel towards next tile
            self.row += self.dy
            self.col += self.dx
            self.x += self.dx * TILE_SIZE
            self.y += self.dy * TILE_SIZE

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,
                           (self.x + TILE_SIZE//2, self.y + TILE_SIZE//2), TILE_SIZE//2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pac-Man in Python")
    clock = pygame.time.Clock()

    # Initialize pellets (center positions)
    pellets = []
    for r, row in enumerate(maze):
        for c, ch in enumerate(row):
            if ch == '.':
                pellets.append((c * TILE_SIZE + TILE_SIZE//2,
                                r * TILE_SIZE + TILE_SIZE//2))

    pacman = Pacman(1, 1)
    ghost = Ghost(GRID_HEIGHT - 2, GRID_WIDTH - 2)
    score = 0

    font = pygame.font.SysFont(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                pacman.change_direction(event.key)

        pacman.move()
        if pacman.eat(pellets):
            score += 10
        ghost.move()

        screen.fill(BLACK)
        draw_maze(screen)
        for p in pellets:
            pygame.draw.circle(screen, WHITE, p, TILE_SIZE//8)
        pacman.draw(screen)
        ghost.draw(screen)

        # Draw score
        score_surf = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (10, SCREEN_HEIGHT - 35))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main() 