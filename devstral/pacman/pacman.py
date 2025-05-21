import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 640, 480
TILE_SIZE = 32

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

# Load assets
pacman_image = pygame.image.load('pacman.png')
ghost_image = pygame.image.load('ghost.png')

# Scaling images to fit tile size
pacman_image = pygame.transform.scale(pacman_image, (TILE_SIZE, TILE_SIZE))
ghost_image = pygame.transform.scale(ghost_image, (TILE_SIZE, TILE_SIZE))

# Game variables
clock = pygame.time.Clock()
player_pos = [WIDTH // 2, HEIGHT // 2]
direction = None

# Sample maze layout (0 is empty space, 1 is wall)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

def draw_maze():
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, WHITE, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_pacman():
    screen.blit(pacman_image, player_pos)

def draw_ghosts(ghosts):
    for ghost in ghosts:
        screen.blit(ghost_image, ghost)

def move_player(direction):
    global player_pos
    
    if direction is None:
        return

    x, y = player_pos
    new_x, new_y = x, y

    if direction == 'UP':
        new_y -= TILE_SIZE
    elif direction == 'DOWN':
        new_y += TILE_SIZE
    elif direction == 'LEFT':
        new_x -= TILE_SIZE
    elif direction == 'RIGHT':
        new_x += TILE_SIZE

    # Check if position is within bounds
    row, col = new_y // TILE_SIZE, new_x // TILE_SIZE
    if 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col] != 1:
        player_pos = [new_x, new_y]

def main():
    global direction
    ghosts = [[TILE_SIZE * 5, TILE_SIZE * 3], [TILE_SIZE * 9, TILE_SIZE * 4]]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = 'UP'
                elif event.key == pygame.K_DOWN:
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    direction = 'RIGHT'

        move_player(direction)
        screen.fill(BLACK)
        draw_maze()
        draw_pacman()
        draw_ghosts(ghosts)

        pygame.display.flip()
        clock.tick(10)  # Frames per second

if __name__ == "__main__":
    main()