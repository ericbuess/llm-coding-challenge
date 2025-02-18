import pygame
import random

# --- Constants ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 480
TILE_SIZE = 20
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# --- Game Objects ---

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.direction = (0, 0)  # (dx, dy)

    def update(self, maze):
        # Store current position for collision check
        old_x = self.rect.x
        old_y = self.rect.y

        # Update position based on direction
        self.rect.x += self.direction[0] * TILE_SIZE
        self.rect.y += self.direction[1] * TILE_SIZE

        # Collision check with maze walls
        tile_x = self.rect.x // TILE_SIZE
        tile_y = self.rect.y // TILE_SIZE

        if maze[tile_y][tile_x] == 1:
            # Reset to old position if collision
            self.rect.x = old_x
            self.rect.y = old_y

    def set_direction(self, direction):
        self.direction = direction

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.direction = (0, 0)

    def update(self, maze):
        # Store current position
        old_x = self.rect.x
        old_y = self.rect.y

        # Randomly choose a direction
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Up, Down, Left, Right
        self.direction = random.choice(directions)

        # Update position
        self.rect.x += self.direction[0] * TILE_SIZE
        self.rect.y += self.direction[1] * TILE_SIZE

        # Collision check
        tile_x = self.rect.x // TILE_SIZE
        tile_y = self.rect.y // TILE_SIZE

        if maze[tile_y][tile_x] == 1:
            self.rect.x = old_x
            self.rect.y = old_y

class Pellet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([TILE_SIZE // 4, TILE_SIZE // 4])  # Smaller than tile
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2)

# --- Maze ---
# 0: Empty, 1: Wall, 2: Pellet
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 0, 0, 0, 2, 1, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 0, 0, 0, 2, 1, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# --- Game Initialization ---

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man Prototype")
clock = pygame.time.Clock()

# --- Sprite Groups ---
all_sprites = pygame.sprite.Group()
pellets = pygame.sprite.Group()

# --- Create Objects ---
player = Player(1, 1)  # Start at (1, 1)
all_sprites.add(player)

ghost = Ghost(9, 4)  # Start at (9, 4)
all_sprites.add(ghost)

# Create pellets based on maze data
for row_index, row in enumerate(maze):
    for col_index, cell in enumerate(row):
        if cell == 2:
            pellet = Pellet(col_index, row_index)
            all_sprites.add(pellet)
            pellets.add(pellet)

# --- Game Loop ---

running = True
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.set_direction((0, -1))
            if event.key == pygame.K_DOWN:
                player.set_direction((0, 1))
            if event.key == pygame.K_LEFT:
                player.set_direction((-1, 0))
            if event.key == pygame.K_RIGHT:
                player.set_direction((1, 0))

    # --- Updates ---
    player.update(maze)
    ghost.update(maze)

    # Pellet collection
    collected_pellets = pygame.sprite.spritecollide(player, pellets, True)  # Remove collected pellets

    # --- Drawing ---
    screen.fill(BLACK)

    # Draw maze
    for row_index, row in enumerate(maze):
        for col_index, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, BLUE, (col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    all_sprites.draw(screen)  # Draw all sprites (player, ghost, pellets)

    pygame.display.flip()

    # --- Win Condition ---
    if not pellets:  # If pellets group is empty
        print("You Win!")
        running = False

    # --- Clock Tick ---
    clock.tick(FPS)

pygame.quit() 