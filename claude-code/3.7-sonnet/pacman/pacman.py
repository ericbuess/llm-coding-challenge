import pygame
import random
from pygame.locals import *

# Initialize pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# Game dimensions
CELL_SIZE = 30
WIDTH = 19 * CELL_SIZE
HEIGHT = 21 * CELL_SIZE
FPS = 60

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pacman')
clock = pygame.time.Clock()

# Map layout
# 0 = empty space, 1 = wall, 2 = pellet, 3 = power pellet
layout = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 3, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 3, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 0, 1, 1, 1, 2, 1, 1, 1, 1],
    [0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0],
    [1, 1, 1, 1, 2, 1, 0, 1, 1, 0, 1, 1, 0, 1, 2, 1, 1, 1, 1],
    [0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0],
    [1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1],
    [0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0],
    [1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 3, 2, 1, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 1, 2, 3, 1],
    [1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1],
    [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Initialize game variables
total_pellets = sum(row.count(2) for row in layout) + sum(row.count(3) for row in layout)
score = 0
lives = 3
game_over = False
win = False

# Player class
class Pacman:
    def __init__(self):
        self.row = 15
        self.col = 9
        self.direction = None
        self.next_direction = None
        self.animation_count = 0
        self.mouth_open = True
        self.power_up = False
        self.power_up_timer = 0
    
    def move(self):
        # Try to change direction if requested
        if self.next_direction:
            if self.can_move(self.next_direction):
                self.direction = self.next_direction
            self.next_direction = None
        
        # Move in current direction if possible
        if self.direction and self.can_move(self.direction):
            if self.direction == "UP":
                self.row -= 1
            elif self.direction == "DOWN":
                self.row += 1
            elif self.direction == "LEFT":
                self.col -= 1
            elif self.direction == "RIGHT":
                self.col += 1
        
        # Animate mouth
        self.animation_count += 1
        if self.animation_count >= 5:
            self.mouth_open = not self.mouth_open
            self.animation_count = 0
        
        # Update power up timer
        if self.power_up:
            self.power_up_timer -= 1
            if self.power_up_timer <= 0:
                self.power_up = False
    
    def can_move(self, direction):
        new_row, new_col = self.row, self.col
        
        if direction == "UP":
            new_row -= 1
        elif direction == "DOWN":
            new_row += 1
        elif direction == "LEFT":
            new_col -= 1
        elif direction == "RIGHT":
            new_col += 1
        
        # Tunnel wrap-around
        if new_col < 0:
            new_col = len(layout[0]) - 1
        elif new_col >= len(layout[0]):
            new_col = 0
            
        if new_row < 0:
            new_row = len(layout) - 1
        elif new_row >= len(layout):
            new_row = 0
        
        # Check if the new position is valid (not a wall)
        return layout[new_row][new_col] != 1
    
    def draw(self):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE
        
        # Draw Pacman
        if self.mouth_open:
            if self.direction == "RIGHT" or self.direction is None:
                pygame.draw.circle(screen, YELLOW, (x + CELL_SIZE//2, y + CELL_SIZE//2), CELL_SIZE//2)
                pygame.draw.polygon(screen, BLACK, [
                    (x + CELL_SIZE//2, y + CELL_SIZE//2),
                    (x + CELL_SIZE, y + CELL_SIZE//4),
                    (x + CELL_SIZE, y + CELL_SIZE - CELL_SIZE//4)
                ])
            elif self.direction == "LEFT":
                pygame.draw.circle(screen, YELLOW, (x + CELL_SIZE//2, y + CELL_SIZE//2), CELL_SIZE//2)
                pygame.draw.polygon(screen, BLACK, [
                    (x + CELL_SIZE//2, y + CELL_SIZE//2),
                    (x, y + CELL_SIZE//4),
                    (x, y + CELL_SIZE - CELL_SIZE//4)
                ])
            elif self.direction == "UP":
                pygame.draw.circle(screen, YELLOW, (x + CELL_SIZE//2, y + CELL_SIZE//2), CELL_SIZE//2)
                pygame.draw.polygon(screen, BLACK, [
                    (x + CELL_SIZE//2, y + CELL_SIZE//2),
                    (x + CELL_SIZE//4, y),
                    (x + CELL_SIZE - CELL_SIZE//4, y)
                ])
            elif self.direction == "DOWN":
                pygame.draw.circle(screen, YELLOW, (x + CELL_SIZE//2, y + CELL_SIZE//2), CELL_SIZE//2)
                pygame.draw.polygon(screen, BLACK, [
                    (x + CELL_SIZE//2, y + CELL_SIZE//2),
                    (x + CELL_SIZE//4, y + CELL_SIZE),
                    (x + CELL_SIZE - CELL_SIZE//4, y + CELL_SIZE)
                ])
        else:
            pygame.draw.circle(screen, YELLOW, (x + CELL_SIZE//2, y + CELL_SIZE//2), CELL_SIZE//2)
    
    def eat_pellet(self):
        global score, total_pellets
        
        if layout[self.row][self.col] == 2:  # Regular pellet
            layout[self.row][self.col] = 0
            score += 10
            total_pellets -= 1
        elif layout[self.row][self.col] == 3:  # Power pellet
            layout[self.row][self.col] = 0
            score += 50
            total_pellets -= 1
            self.power_up = True
            self.power_up_timer = FPS * 8  # 8 seconds of power up

# Ghost class
class Ghost:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.frightened = False
        self.home = (row, col)
        self.dead = False
        self.speed_counter = 0
    
    def move(self, pacman):
        self.speed_counter += 1
        if self.speed_counter < 2:  # Ghosts move every other frame (half speed of Pacman)
            return
        
        self.speed_counter = 0
        
        # If dead, move toward home
        if self.dead:
            self.move_to_target(self.home[0], self.home[1])
            
            # If reached home, revive
            if self.row == self.home[0] and self.col == self.home[1]:
                self.dead = False
                self.frightened = False
            return
            
        # If frightened, move randomly
        if self.frightened:
            possible_dirs = []
            
            # Check which directions are valid
            if self.can_move("UP") and self.direction != "DOWN":
                possible_dirs.append("UP")
            if self.can_move("DOWN") and self.direction != "UP":
                possible_dirs.append("DOWN")
            if self.can_move("LEFT") and self.direction != "RIGHT":
                possible_dirs.append("LEFT")
            if self.can_move("RIGHT") and self.direction != "LEFT":
                possible_dirs.append("RIGHT")
                
            # If no valid directions, allow reverse
            if not possible_dirs:
                if self.can_move("UP"):
                    possible_dirs.append("UP")
                if self.can_move("DOWN"):
                    possible_dirs.append("DOWN")
                if self.can_move("LEFT"):
                    possible_dirs.append("LEFT")
                if self.can_move("RIGHT"):
                    possible_dirs.append("RIGHT")
            
            # Choose a random direction
            if possible_dirs:
                self.direction = random.choice(possible_dirs)
                
        else:
            # Chase Pacman (simple AI)
            self.move_to_target(pacman.row, pacman.col)
        
        # Move in chosen direction
        if self.direction == "UP":
            self.row -= 1
        elif self.direction == "DOWN":
            self.row += 1
        elif self.direction == "LEFT":
            self.col -= 1
        elif self.direction == "RIGHT":
            self.col += 1
        
        # Handle tunnel wrap-around
        if self.col < 0:
            self.col = len(layout[0]) - 1
        elif self.col >= len(layout[0]):
            self.col = 0
            
        if self.row < 0:
            self.row = len(layout) - 1
        elif self.row >= len(layout):
            self.row = 0
    
    def move_to_target(self, target_row, target_col):
        # Find the best direction to move toward the target
        possible_dirs = []
        
        # Check which directions are valid
        if self.can_move("UP") and self.direction != "DOWN":
            possible_dirs.append("UP")
        if self.can_move("DOWN") and self.direction != "UP":
            possible_dirs.append("DOWN")
        if self.can_move("LEFT") and self.direction != "RIGHT":
            possible_dirs.append("LEFT")
        if self.can_move("RIGHT") and self.direction != "LEFT":
            possible_dirs.append("RIGHT")
            
        # If no valid directions, allow reverse
        if not possible_dirs:
            if self.can_move("UP"):
                possible_dirs.append("UP")
            if self.can_move("DOWN"):
                possible_dirs.append("DOWN")
            if self.can_move("LEFT"):
                possible_dirs.append("LEFT")
            if self.can_move("RIGHT"):
                possible_dirs.append("RIGHT")
        
        # Calculate distances for each direction
        best_dir = None
        best_dist = float('inf')
        
        for dir in possible_dirs:
            test_row, test_col = self.row, self.col
            
            if dir == "UP":
                test_row -= 1
            elif dir == "DOWN":
                test_row += 1
            elif dir == "LEFT":
                test_col -= 1
            elif dir == "RIGHT":
                test_col += 1
            
            # Handle tunnel wrap-around
            if test_col < 0:
                test_col = len(layout[0]) - 1
            elif test_col >= len(layout[0]):
                test_col = 0
                
            if test_row < 0:
                test_row = len(layout) - 1
            elif test_row >= len(layout):
                test_row = 0
                
            # Calculate Manhattan distance
            dist = abs(test_row - target_row) + abs(test_col - target_col)
            
            if dist < best_dist or (dist == best_dist and random.random() < 0.5):
                best_dist = dist
                best_dir = dir
        
        if best_dir:
            self.direction = best_dir
    
    def can_move(self, direction):
        new_row, new_col = self.row, self.col
        
        if direction == "UP":
            new_row -= 1
        elif direction == "DOWN":
            new_row += 1
        elif direction == "LEFT":
            new_col -= 1
        elif direction == "RIGHT":
            new_col += 1
        
        # Handle tunnel wrap-around
        if new_col < 0:
            new_col = len(layout[0]) - 1
        elif new_col >= len(layout[0]):
            new_col = 0
            
        if new_row < 0:
            new_row = len(layout) - 1
        elif new_row >= len(layout):
            new_row = 0
        
        # Check if the new position is valid (not a wall)
        return layout[new_row][new_col] != 1
    
    def draw(self):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE
        
        color = BLUE
        if self.frightened:
            color = (0, 0, 128)  # Dark blue when frightened
        elif self.dead:
            color = WHITE  # White when dead (eyes only)
        else:
            color = self.color
        
        # Draw ghost body
        if not self.dead:
            pygame.draw.circle(screen, color, (x + CELL_SIZE//2, y + CELL_SIZE//2 - 2), CELL_SIZE//2)
            pygame.draw.rect(screen, color, (x, y + CELL_SIZE//2 - 2, CELL_SIZE, CELL_SIZE//2))
            
            # Draw ghost "skirt"
            skirt_points = 3
            for i in range(skirt_points):
                pygame.draw.polygon(screen, color, [
                    (x + i * (CELL_SIZE // skirt_points), y + CELL_SIZE),
                    (x + (i + 0.5) * (CELL_SIZE // skirt_points), y + CELL_SIZE - 4),
                    (x + (i + 1) * (CELL_SIZE // skirt_points), y + CELL_SIZE)
                ])
        
        # Draw eyes
        eye_radius = CELL_SIZE // 6
        pygame.draw.circle(screen, WHITE, (x + CELL_SIZE//3, y + CELL_SIZE//3), eye_radius)
        pygame.draw.circle(screen, WHITE, (x + CELL_SIZE - CELL_SIZE//3, y + CELL_SIZE//3), eye_radius)
        
        # Draw pupils
        pupil_radius = eye_radius // 2
        pupil_offset = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0)
        }
        
        offset_x, offset_y = pupil_offset.get(self.direction, (0, 0))
        
        pygame.draw.circle(screen, BLACK, 
                          (x + CELL_SIZE//3 + offset_x * pupil_radius, 
                           y + CELL_SIZE//3 + offset_y * pupil_radius), 
                          pupil_radius)
        pygame.draw.circle(screen, BLACK, 
                          (x + CELL_SIZE - CELL_SIZE//3 + offset_x * pupil_radius, 
                           y + CELL_SIZE//3 + offset_y * pupil_radius), 
                          pupil_radius)

# Create player and ghosts
pacman = Pacman()
ghosts = [
    Ghost(10, 9, RED),     # Blinky
    Ghost(9, 8, PINK),     # Pinky
    Ghost(9, 9, CYAN),     # Inky
    Ghost(9, 10, ORANGE)   # Clyde
]

# Main game loop
running = True
while running:
    clock.tick(FPS)
    
    # Process events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                pacman.next_direction = "UP"
            elif event.key == K_DOWN:
                pacman.next_direction = "DOWN"
            elif event.key == K_LEFT:
                pacman.next_direction = "LEFT"
            elif event.key == K_RIGHT:
                pacman.next_direction = "RIGHT"
            elif event.key == K_r and (game_over or win):
                # Reset game
                for row in range(len(layout)):
                    for col in range(len(layout[0])):
                        if layout[row][col] == 0 and (row < 7 or row > 13 or col < 7 or col > 11):
                            layout[row][col] = 2
                
                total_pellets = sum(row.count(2) for row in layout) + sum(row.count(3) for row in layout)
                score = 0
                lives = 3
                game_over = False
                win = False
                pacman = Pacman()
                ghosts = [
                    Ghost(10, 9, RED),
                    Ghost(9, 8, PINK),
                    Ghost(9, 9, CYAN),
                    Ghost(9, 10, ORANGE)
                ]
    
    # Game logic (only if game is still active)
    if not game_over and not win:
        # Move Pacman
        pacman.move()
        
        # Check if Pacman ate a pellet
        pacman.eat_pellet()
        
        # Move ghosts
        for ghost in ghosts:
            ghost.move(pacman)
            
            # Check for collision with Pacman
            if ghost.row == pacman.row and ghost.col == pacman.col:
                if ghost.frightened:
                    ghost.dead = True
                    score += 200
                elif not ghost.dead:
                    lives -= 1
                    if lives <= 0:
                        game_over = True
                    else:
                        # Reset positions
                        pacman = Pacman()
                        for g in ghosts:
                            g.row, g.col = g.home
                            g.frightened = False
                            g.dead = False
        
        # Update ghost frightened state
        for ghost in ghosts:
            ghost.frightened = pacman.power_up and not ghost.dead
        
        # Check win condition
        if total_pellets <= 0:
            win = True
    
    # Draw everything
    screen.fill(BLACK)
    
    # Draw map
    for row in range(len(layout)):
        for col in range(len(layout[0])):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            
            if layout[row][col] == 1:  # Wall
                pygame.draw.rect(screen, BLUE, (x, y, CELL_SIZE, CELL_SIZE))
            elif layout[row][col] == 2:  # Pellet
                pygame.draw.circle(screen, WHITE, (x + CELL_SIZE//2, y + CELL_SIZE//2), 3)
            elif layout[row][col] == 3:  # Power pellet
                pygame.draw.circle(screen, WHITE, (x + CELL_SIZE//2, y + CELL_SIZE//2), 8)
    
    # Draw Pacman
    pacman.draw()
    
    # Draw ghosts
    for ghost in ghosts:
        ghost.draw()
    
    # Draw score and lives
    font = pygame.font.SysFont('Arial', 24)
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (5, 5))
    
    lives_text = font.render(f'Lives: {lives}', True, WHITE)
    screen.blit(lives_text, (WIDTH - lives_text.get_width() - 5, 5))
    
    # Draw game over or win text
    if game_over:
        game_over_font = pygame.font.SysFont('Arial', 48)
        game_over_text = game_over_font.render('GAME OVER', True, RED)
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 24))
        
        restart_font = pygame.font.SysFont('Arial', 24)
        restart_text = restart_font.render('Press R to restart', True, WHITE)
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 24))
    
    if win:
        win_font = pygame.font.SysFont('Arial', 48)
        win_text = win_font.render('YOU WIN!', True, YELLOW)
        screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 24))
        
        restart_font = pygame.font.SysFont('Arial', 24)
        restart_text = restart_font.render('Press R to restart', True, WHITE)
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 24))
    
    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()