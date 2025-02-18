import pygame
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 20
PACMAN_SPEED = 2
GHOST_SPEED = 1.5

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 0  # 0: right, 1: up, 2: left, 3: down
        self.mouth_open = True
        self.score = 0

    def move(self, direction, walls):
        new_x, new_y = self.x, self.y
        
        if direction == 0:  # Right
            new_x += PACMAN_SPEED
        elif direction == 1:  # Up
            new_y -= PACMAN_SPEED
        elif direction == 2:  # Left
            new_x -= PACMAN_SPEED
        elif direction == 3:  # Down
            new_y += PACMAN_SPEED

        # Check wall collisions
        can_move = True
        for wall in walls:
            if (new_x + CELL_SIZE > wall.x and 
                new_x < wall.x + CELL_SIZE and 
                new_y + CELL_SIZE > wall.y and 
                new_y < wall.y + CELL_SIZE):
                can_move = False
                break

        if can_move:
            self.x = new_x
            self.y = new_y
            self.direction = direction

        # Screen wrapping
        if self.x < 0:
            self.x = WINDOW_WIDTH - CELL_SIZE
        elif self.x > WINDOW_WIDTH - CELL_SIZE:
            self.x = 0
        if self.y < 0:
            self.y = WINDOW_HEIGHT - CELL_SIZE
        elif self.y > WINDOW_HEIGHT - CELL_SIZE:
            self.y = 0

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.direction = random.randint(0, 3)

    def move(self, pacman, walls):
        # Simple ghost AI: move towards Pacman with some randomness
        if random.random() < 0.05:
            self.direction = random.randint(0, 3)

        new_x, new_y = self.x, self.y
        
        if self.direction == 0:
            new_x += GHOST_SPEED
        elif self.direction == 1:
            new_y -= GHOST_SPEED
        elif self.direction == 2:
            new_x -= GHOST_SPEED
        elif self.direction == 3:
            new_y += GHOST_SPEED

        # Check wall collisions
        can_move = True
        for wall in walls:
            if (new_x + CELL_SIZE > wall.x and 
                new_x < wall.x + CELL_SIZE and 
                new_y + CELL_SIZE > wall.y and 
                new_y < wall.y + CELL_SIZE):
                can_move = False
                self.direction = random.randint(0, 3)
                break

        if can_move:
            self.x = new_x
            self.y = new_y

        # Screen wrapping
        if self.x < 0:
            self.x = WINDOW_WIDTH - CELL_SIZE
        elif self.x > WINDOW_WIDTH - CELL_SIZE:
            self.x = 0
        if self.y < 0:
            self.y = WINDOW_HEIGHT - CELL_SIZE
        elif self.y > WINDOW_HEIGHT - CELL_SIZE:
            self.y = 0

class Pellet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def create_maze():
    walls = []
    pellets = []
    
    # Create basic maze layout
    for i in range(0, WINDOW_WIDTH, CELL_SIZE):
        walls.append(Wall(i, 0))
        walls.append(Wall(i, WINDOW_HEIGHT - CELL_SIZE))
    
    for i in range(0, WINDOW_HEIGHT, CELL_SIZE):
        walls.append(Wall(0, i))
        walls.append(Wall(WINDOW_WIDTH - CELL_SIZE, i))

    # Add some internal walls
    for i in range(100, 700, CELL_SIZE * 3):
        for j in range(100, 500, CELL_SIZE * 3):
            walls.append(Wall(i, j))

    # Add pellets
    for i in range(CELL_SIZE, WINDOW_WIDTH - CELL_SIZE, CELL_SIZE * 2):
        for j in range(CELL_SIZE, WINDOW_HEIGHT - CELL_SIZE, CELL_SIZE * 2):
            add_pellet = True
            for wall in walls:
                if (i == wall.x and j == wall.y):
                    add_pellet = False
                    break
            if add_pellet:
                pellets.append(Pellet(i, j))

    return walls, pellets

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Pacman')
    clock = pygame.time.Clock()

    # Create game objects
    pacman = Pacman(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    ghosts = [
        Ghost(100, 100, RED),
        Ghost(WINDOW_WIDTH - 100, 100, (255, 192, 203)),
        Ghost(100, WINDOW_HEIGHT - 100, (0, 255, 255)),
        Ghost(WINDOW_WIDTH - 100, WINDOW_HEIGHT - 100, (255, 165, 0))
    ]
    walls, pellets = create_maze()

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Move Pacman based on key input
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]:
            pacman.move(0, walls)
        elif keys[K_UP]:
            pacman.move(1, walls)
        elif keys[K_LEFT]:
            pacman.move(2, walls)
        elif keys[K_DOWN]:
            pacman.move(3, walls)

        # Move ghosts
        for ghost in ghosts:
            ghost.move(pacman, walls)

        # Check pellet collection
        for pellet in pellets[:]:
            if (abs(pacman.x - pellet.x) < CELL_SIZE and 
                abs(pacman.y - pellet.y) < CELL_SIZE):
                pellets.remove(pellet)
                pacman.score += 10

        # Check ghost collision
        for ghost in ghosts:
            if (abs(pacman.x - ghost.x) < CELL_SIZE and 
                abs(pacman.y - ghost.y) < CELL_SIZE):
                running = False

        # Draw everything
        screen.fill(BLACK)
        
        # Draw walls
        for wall in walls:
            pygame.draw.rect(screen, BLUE, 
                           (wall.x, wall.y, CELL_SIZE, CELL_SIZE))

        # Draw pellets
        for pellet in pellets:
            pygame.draw.circle(screen, WHITE, 
                             (pellet.x + CELL_SIZE//2, pellet.y + CELL_SIZE//2), 3)

        # Draw Pacman
        pygame.draw.circle(screen, YELLOW, 
                         (int(pacman.x + CELL_SIZE//2), 
                          int(pacman.y + CELL_SIZE//2)), CELL_SIZE//2)

        # Draw ghosts
        for ghost in ghosts:
            pygame.draw.circle(screen, ghost.color, 
                             (int(ghost.x + CELL_SIZE//2), 
                              int(ghost.y + CELL_SIZE//2)), CELL_SIZE//2)

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {pacman.score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()