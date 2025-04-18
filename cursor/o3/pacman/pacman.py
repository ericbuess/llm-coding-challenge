import pygame
import sys
import random

# Constants
CELL_SIZE = 24
MAZE_LAYOUT = [
    "####################",  # 20 columns
    "#........##........#",
    "#.##.###.##.###.##.#",
    "#o##.###.##.###.##o#",
    "#.##.###.##.###.##.#",
    "#..................#",
    "#.##.#.######.#.##.#",
    "#.##.#.######.#.##.#",
    "#....#....##....#...#",
    "####.### ## ###.####",
    "   #.#   GG   #.#   ",  # 9th index spaces for tunnel
    "####.# ###### #.####",
    "#........##........#",
    "#.##.###.##.###.##.#",
    "#o.......P........o#",
    "####################"
]
ROWS = len(MAZE_LAYOUT)
COLS = len(MAZE_LAYOUT[0])
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
FPS = 60

# Colors
BLACK = (0, 0, 0)
BLUE = (33, 33, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
PINK = (255, 105, 180)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

GHOST_COLORS = [RED, PINK, CYAN, ORANGE]

# Helper functions

def load_maze():
    walls = []
    dots = []
    energizers = []
    pacman_start = None
    ghost_starts = []
    for row, line in enumerate(MAZE_LAYOUT):
        for col, ch in enumerate(line):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if ch == "#":
                walls.append(rect)
            elif ch == ".":
                dots.append(rect.inflate(-CELL_SIZE // 2, -CELL_SIZE // 2))  # smaller dot
            elif ch == "o":
                energizers.append(rect.inflate(-CELL_SIZE // 4, -CELL_SIZE // 4))
            elif ch == "P":
                pacman_start = rect.center
            elif ch == "G":
                ghost_starts.append(rect.center)
    return walls, dots, energizers, pacman_start, ghost_starts

class Entity:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.dir = pygame.Vector2(0, 0)
        self.speed = 2
        self.color = color

    def move(self, walls):
        new_x = self.x + self.dir.x * self.speed
        new_y = self.y + self.dir.y * self.speed
        rect = pygame.Rect(new_x - CELL_SIZE // 2, new_y - CELL_SIZE // 2, CELL_SIZE, CELL_SIZE)
        # Check collision with walls
        for wall in walls:
            if rect.colliderect(wall):
                return  # blocked
        self.x, self.y = new_x, new_y

    @property
    def pos(self):
        return pygame.Vector2(self.x, self.y)

    def rect(self):
        return pygame.Rect(self.x - CELL_SIZE // 2, self.y - CELL_SIZE // 2, CELL_SIZE, CELL_SIZE)

class Pacman(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, YELLOW)
        self.mouth_open = True
        self.mouth_timer = 0
        self.score = 0
        self.lives = 3

    def update(self, walls):
        self.move(walls)
        self.mouth_timer += 1
        if self.mouth_timer % 10 == 0:
            self.mouth_open = not self.mouth_open

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), CELL_SIZE // 2)
        # Draw mouth by overlaying background triangle
        if self.mouth_open and self.dir.length_squared() != 0:
            angle = 0
            if self.dir.x > 0:
                angle = 0
            elif self.dir.x < 0:
                angle = 180
            elif self.dir.y < 0:
                angle = 90
            elif self.dir.y > 0:
                angle = 270
            mouth_rect = pygame.Rect(0,0,CELL_SIZE,CELL_SIZE)
            mouth_rect.center = (self.x, self.y)
            start_angle = angle - 30
            end_angle = angle + 30
            pygame.draw.arc(screen, BLACK, mouth_rect, start_angle * (3.14/180), end_angle * (3.14/180), CELL_SIZE)

class Ghost(Entity):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.speed = 2
        # initial random direction
        self.dir = random.choice([pygame.Vector2(1,0), pygame.Vector2(-1,0), pygame.Vector2(0,1), pygame.Vector2(0,-1)])

    def update(self, walls):
        # attempt to move; if blocked choose new direction
        old_pos = (self.x, self.y)
        self.move(walls)
        if (self.x, self.y) == old_pos:
            dirs = [pygame.Vector2(1,0), pygame.Vector2(-1,0), pygame.Vector2(0,1), pygame.Vector2(0,-1)]
            random.shuffle(dirs)
            for d in dirs:
                self.dir = d
                old_pos = (self.x, self.y)
                self.move(walls)
                if (self.x, self.y) != old_pos:
                    break

    def draw(self, screen):
        rect = pygame.Rect(self.x - CELL_SIZE//2, self.y - CELL_SIZE//2, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, self.color, rect, border_radius=8)
        # eyes
        eye_offset_x = CELL_SIZE//6
        eye_offset_y = CELL_SIZE//6
        eye_radius = CELL_SIZE//10
        pygame.draw.circle(screen, WHITE, (int(self.x - eye_offset_x), int(self.y - eye_offset_y)), eye_radius)
        pygame.draw.circle(screen, WHITE, (int(self.x + eye_offset_x), int(self.y - eye_offset_y)), eye_radius)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man")
    clock = pygame.time.Clock()

    walls, dots, energizers, pac_start, ghost_starts = load_maze()
    pacman = Pacman(*pac_start)
    ghosts = [Ghost(*ghost_starts[i % len(ghost_starts)], GHOST_COLORS[i % len(GHOST_COLORS)]) for i in range(4)]

    font = pygame.font.SysFont(None, 24)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pacman.dir = pygame.Vector2(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    pacman.dir = pygame.Vector2(1, 0)
                elif event.key == pygame.K_UP:
                    pacman.dir = pygame.Vector2(0, -1)
                elif event.key == pygame.K_DOWN:
                    pacman.dir = pygame.Vector2(0, 1)

        # Update
        pacman.update(walls)
        for ghost in ghosts:
            ghost.update(walls)

        # Check dot collisions
        pac_rect = pacman.rect()
        dots = [d for d in dots if not pac_rect.colliderect(d)]
        pacman.score = (len(MAZE_LAYOUT) * len(MAZE_LAYOUT[0]) - len(dots))

        # Check ghost collisions
        for ghost in ghosts:
            if pac_rect.colliderect(ghost.rect()):
                pacman.lives -= 1
                pacman.x, pacman.y = pac_start
                if pacman.lives <= 0:
                    running = False

        # Render
        screen.fill(BLACK)
        # draw walls
        for wall in walls:
            pygame.draw.rect(screen, BLUE, wall)
        # dots
        for d in dots:
            pygame.draw.circle(screen, WHITE, d.center, 3)
        # energizers (draw slightly larger)
        for e in energizers:
            pygame.draw.circle(screen, WHITE, e.center, 6)
        # entities
        pacman.draw(screen)
        for ghost in ghosts:
            ghost.draw(screen)

        score_surf = font.render(f"Score: {pacman.score}", True, WHITE)
        lives_surf = font.render(f"Lives: {pacman.lives}", True, WHITE)
        screen.blit(score_surf, (5, HEIGHT - 40))
        screen.blit(lives_surf, (WIDTH - 100, HEIGHT - 40))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main() 