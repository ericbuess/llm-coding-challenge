import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
SCREEN_SIZE = (800, 600)
BLOCK_SIZE = 20
SPEED = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize the screen
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Snake Game")

# Snake and food initialization
snake = [(5 * BLOCK_SIZE, 5 * BLOCK_SIZE)]
dx = BLOCK_SIZE  # Initial direction (right)
dy = 0

def place_food():
    x = random.randint(0, (SCREEN_SIZE[0] - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    y = random.randint(0, (SCREEN_SIZE[1] - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    # Make sure food doesn't appear on snake
    for segment in snake:
        if x == segment[0] and y == segment[1]:
            return place_food()
    return (x, y)

food = place_food()

# Game loop
game_over = False
clock = pygame.time.Clock()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Handle keyboard input to control the snake
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if dx == 0:  # Prevent reverse direction
                    dx = -BLOCK_SIZE
                    dy = 0
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if dx == 0:
                    dx = BLOCK_SIZE
                    dy = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                if dy == 0:
                    dx = 0
                    dy = -BLOCK_SIZE
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if dy == 0:
                    dx = 0
                    dy = BLOCK_SIZE

    # Move the snake
    head = (snake[0][0] + dx, snake[0][1] + dy)
    
    # Check for collisions with walls or self
    if head[0] < 0 or head[0] >= SCREEN_SIZE[0] - BLOCK_SIZE:
        game_over = True
    if head[1] < 0 or head[1] >= SCREEN_SIZE[1] - BLOCK_SIZE:
        game_over = True
    for segment in snake:
        if head == segment:
            game_over = True

    if not game_over:
        # Add new head to the snake
        snake.insert(0, head)
        
        # Check if food is eaten
        if head[0] == food[0] and head[1] == food[1]:
            food = place_food()
        else:
            # Remove the tail (if not eating food)
            snake.pop()

    # Draw everything on screen
    screen.fill(BLACK)  # Background
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK_SIZE-2, BLOCK_SIZE-2))
    pygame.draw.circle(screen, RED, (food[0] + BLOCK_SIZE//2, food[1] + BLOCK_SIZE//2), BLOCK_SIZE//2)

    # Update the display
    pygame.display.flip()
    
    # Control game speed
    clock.tick(SPEED)

# Game over message
while True:
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over!", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2))
    screen.blit(text, text_rect)
    
    # Allow the player to quit or restart
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                sys.exit()
            elif event.key == pygame.K_RETURN or event.key == pygame.K_r:
                # Reset the game
                snake = [(5 * BLOCK_SIZE, 5 * BLOCK_SIZE)]
                dx = BLOCK_SIZE
                dy = 0
                food = place_food()
                game_over = False
                break
    
    pygame.display.flip()
