import pygame
import sys
import random

# Constants
TILE_SIZE = 24
SPEED = 2

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 105, 180)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)

# Simple map: #=wall, .=pellet, o=power pellet (not implemented)
MAP = [
    "################",
    "#..............#",
    "#.#.###.###.#..#",
    "#..............#",
    "#.##.#####.##..#",
    "#..............#",
    "################"
]

class Maze:
    def __init__(self):
        self.grid = MAP
        self.walls = []
        self.pellets = []
        for j, row in enumerate(self.grid):
            for i, char in enumerate(row):
                x, y = i * TILE_SIZE, j * TILE_SIZE
                if char == '#':
                    self.walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                elif char == '.':
                    self.pellets.append(pygame.Rect(x+TILE_SIZE//4, y+TILE_SIZE//4, TILE_SIZE//2, TILE_SIZE//2))

    def draw(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, BLUE, wall)
        for pellet in self.pellets:
            pygame.draw.circle(screen, WHITE, pellet.center, TILE_SIZE//8)

class Pacman:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.dir_x = 0
        self.dir_y = 0
        self.next_dir = (0, 0)
        self.speed = SPEED

    def update(self, maze):
        # Try to turn
        if self.next_dir != (0, 0):
            new_rect = self.rect.move(self.next_dir[0]*self.speed, self.next_dir[1]*self.speed)
            if not any(new_rect.colliderect(w) for w in maze.walls):
                self.dir_x, self.dir_y = self.next_dir
        # Move
        new_rect = self.rect.move(self.dir_x*self.speed, self.dir_y*self.speed)
        if not any(new_rect.colliderect(w) for w in maze.walls):
            self.rect = new_rect
        # Eat pellets
        for pellet in maze.pellets[:]:
            if self.rect.colliderect(pellet):
                maze.pellets.remove(pellet)

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, self.rect.center, TILE_SIZE//2)

class Ghost:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.color = color
        self.dir_x = 0
        self.dir_y = 0
        self.speed = SPEED

    def update(self, maze):
        # At junction, pick new dir
        if self.rect.x % TILE_SIZE == 0 and self.rect.y % TILE_SIZE == 0:
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(directions)
            for d in directions:
                new_rect = self.rect.move(d[0]*self.speed, d[1]*self.speed)
                if not any(new_rect.colliderect(w) for w in maze.walls):
                    self.dir_x, self.dir_y = d
                    break
        # Move
        new_rect = self.rect.move(self.dir_x*self.speed, self.dir_y*self.speed)
        if not any(new_rect.colliderect(w) for w in maze.walls):
            self.rect = new_rect

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


def game_over(screen, score):
    font = pygame.font.SysFont(None, 48)
    text = font.render("GAME OVER", True, WHITE)
    rect = text.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
    screen.blit(text, rect)
    subfont = pygame.font.SysFont(None, 36)
    subtext = subfont.render(f"Score: {score}", True, WHITE)
    subrect = subtext.get_rect(center=(screen.get_width()//2, screen.get_height()//2+50))
    screen.blit(subtext, subrect)
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()


def main():
    pygame.init()
    width = len(MAP[0]) * TILE_SIZE
    height = len(MAP) * TILE_SIZE
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pac-Man Clone")
    clock = pygame.time.Clock()

    maze = Maze()
    pacman = Pacman(TILE_SIZE, TILE_SIZE)
    ghosts = [
        Ghost((len(MAP[0]) - 2) * TILE_SIZE, TILE_SIZE, RED),
        Ghost((len(MAP[0]) - 2) * TILE_SIZE, (len(MAP) - 2) * TILE_SIZE, PINK),
        Ghost(TILE_SIZE, (len(MAP) - 2) * TILE_SIZE, CYAN)
    ]

    score = 0
    font = pygame.font.SysFont(None, 24)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pacman.next_dir = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    pacman.next_dir = (1, 0)
                elif event.key == pygame.K_UP:
                    pacman.next_dir = (0, -1)
                elif event.key == pygame.K_DOWN:
                    pacman.next_dir = (0, 1)

        # Update
        pellets_before = len(maze.pellets)
        pacman.update(maze)
        pellets_after = len(maze.pellets)
        score += (pellets_before - pellets_after) * 10
        for ghost in ghosts:
            ghost.update(maze)
            if pacman.rect.colliderect(ghost.rect):
                running = False

        # Draw
        screen.fill(BLACK)
        maze.draw(screen)
        pacman.draw(screen)
        for ghost in ghosts:
            ghost.draw(screen)
        score_surf = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (5, 5))

        pygame.display.flip()
        clock.tick(60)

    game_over(screen, score)

if __name__ == '__main__':
    main()
