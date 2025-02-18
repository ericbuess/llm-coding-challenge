import pygame
import random

# Initialize Pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 608, 688
BLOCK_SIZE = 32
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Maze layout
maze_layout = [
    "#############################",
    "#..............#..............#",
    "#.####.#####.#.#####.####.#",
    "#...................#................#",
    "#.####.#.#####.###.#.#####.####.#",
    "#....#.#.....#.....#.#.....#....#",
    "####.#.#.### # ###.#.#.### ####",
    "   #.#.# #     # #.#.# #   ",
    "####.#.# # ### # #.#.# ####",
    "#........ # ...#........ #",
    "#.####.### ##### ###.####.#",
    "#...................#................#",
    "#############################"
]

class PacMan:
    def __init__(self):
        self.x = BLOCK_SIZE * 14
        self.y = BLOCK_SIZE * 23
        self.speed = 2
        self.direction = 0  # 0: stop, 1: up, 2: down, 3: left, 4: right
        self.score = 0
        self.lives = 3

    def move(self):
        if self.direction == 1:
            self.y -= self.speed
        elif self.direction == 2:
            self.y += self.speed
        elif self.direction == 3:
            self.x -= self.speed
        elif self.direction == 4:
            self.x += self.speed

class Ghost:
    def __init__(self, color):
        self.x = BLOCK_SIZE * 14
        self.y = BLOCK_SIZE * 11
        self.color = color
        self.speed = 1
        self.direction = random.choice([1, 2, 3, 4])

    def move(self):
        if self.direction == 1:
            self.y -= self.speed
        elif self.direction == 2:
            self.y += self.speed
        elif self.direction == 3:
            self.x -= self.speed
        elif self.direction == 4:
            self.x += self.speed

        # Change direction randomly
        if random.randint(0, 100) < 2:
            self.direction = random.choice([1, 2, 3, 4])

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.pacman = PacMan()
        self.ghosts = [Ghost(RED) for _ in range(4)]
        self.dots = []
        self.load_maze()

    def load_maze(self):
        for row_idx, row in enumerate(maze_layout):
            for col_idx, cell in enumerate(row):
                if cell == '.':
                    self.dots.append((col_idx * BLOCK_SIZE, row_idx * BLOCK_SIZE))

    def check_collision(self):
        # Wall collision (simplified)
        grid_x = self.pacman.x // BLOCK_SIZE
        grid_y = self.pacman.y // BLOCK_SIZE
        
        if maze_layout[grid_y][grid_x] == '#':
            self.pacman.x = self.pacman.x_prev
            self.pacman.y = self.pacman.y_prev

        # Dot collection
        for dot in self.dots[:]:
            if (abs(self.pacman.x - dot[0]) < BLOCK_SIZE and 
                abs(self.pacman.y - dot[1]) < BLOCK_SIZE):
                self.pacman.score += 10
                self.dots.remove(dot)

        # Ghost collision
        for ghost in self.ghosts:
            if (abs(self.pacman.x - ghost.x) < BLOCK_SIZE and 
                abs(self.pacman.y - ghost.y) < BLOCK_SIZE):
                self.pacman.lives -= 1
                self.reset_positions()

    def reset_positions(self):
        self.pacman.x = BLOCK_SIZE * 14
        self.pacman.y = BLOCK_SIZE * 23
        for ghost in self.ghosts:
            ghost.x = BLOCK_SIZE * 14
            ghost.y = BLOCK_SIZE * 11

    def run(self):
        running = True
        while running:
            self.screen.fill(BLACK)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.pacman.direction = 1
                    elif event.key == pygame.K_DOWN:
                        self.pacman.direction = 2
                    elif event.key == pygame.K_LEFT:
                        self.pacman.direction = 3
                    elif event.key == pygame.K_RIGHT:
                        self.pacman.direction = 4

            # Update game state
            self.pacman.move()
            for ghost in self.ghosts:
                ghost.move()
            self.check_collision()

            # Draw maze
            for row_idx, row in enumerate(maze_layout):
                for col_idx, cell in enumerate(row):
                    if cell == '#':
                        pygame.draw.rect(self.screen, BLUE, 
                                       (col_idx*BLOCK_SIZE, row_idx*BLOCK_SIZE,
                                        BLOCK_SIZE, BLOCK_SIZE))

            # Draw dots
            for dot in self.dots:
                pygame.draw.circle(self.screen, WHITE,
                                 (dot[0]+BLOCK_SIZE//2, dot[1]+BLOCK_SIZE//2), 3)

            # Draw characters
            pygame.draw.circle(self.screen, YELLOW,
                             (self.pacman.x + BLOCK_SIZE//2, self.pacman.y + BLOCK_SIZE//2),
                             BLOCK_SIZE//2 - 2)
            
            for ghost in self.ghosts:
                pygame.draw.circle(self.screen, ghost.color,
                                 (ghost.x + BLOCK_SIZE//2, ghost.y + BLOCK_SIZE//2),
                                 BLOCK_SIZE//2 - 2)

            # Draw score and lives
            font = pygame.font.Font(None, 36)
            text = font.render(f"Score: {self.pacman.score}  Lives: {self.pacman.lives}", 
                             True, WHITE)
            self.screen.blit(text, (10, HEIGHT - 40))

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()