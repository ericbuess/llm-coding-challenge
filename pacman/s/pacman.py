import pygame
import sys
from constants import *

class Pacman:
    def __init__(self):
        self.row = 9
        self.col = 9
        self.direction = [0, 0]
        self.next_direction = [0, 0]
        self.score = 0

class Ghost:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.direction = [0, 1]

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pacman")
        self.clock = pygame.time.Clock()
        self.maze = [row[:] for row in MAZE]
        self.pacman = Pacman()
        self.ghosts = [Ghost(9, 10, RED)]
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.pacman.next_direction = [-1, 0]
                elif event.key == pygame.K_DOWN:
                    self.pacman.next_direction = [1, 0]
                elif event.key == pygame.K_LEFT:
                    self.pacman.next_direction = [0, -1]
                elif event.key == pygame.K_RIGHT:
                    self.pacman.next_direction = [0, 1]
        return True

    def update(self):
        # Try to move in the next_direction if possible
        next_row = self.pacman.row + self.pacman.next_direction[0]
        next_col = self.pacman.col + self.pacman.next_direction[1]
        
        if 0 <= next_row < ROWS and 0 <= next_col < COLS and self.maze[next_row][next_col] != 1:
            self.pacman.direction = self.pacman.next_direction
        
        # Move Pacman
        new_row = self.pacman.row + self.pacman.direction[0]
        new_col = self.pacman.col + self.pacman.direction[1]
        
        if 0 <= new_row < ROWS and 0 <= new_col < COLS and self.maze[new_row][new_col] != 1:
            self.pacman.row = new_row
            self.pacman.col = new_col
            if self.maze[new_row][new_col] == 0:
                self.maze[new_row][new_col] = 2
                self.pacman.score += 10

        # Move ghosts (simple movement)
        for ghost in self.ghosts:
            new_row = ghost.row + ghost.direction[0]
            new_col = ghost.col + ghost.direction[1]
            
            if 0 <= new_row < ROWS and 0 <= new_col < COLS and self.maze[new_row][new_col] != 1:
                ghost.row = new_row
                ghost.col = new_col
            else:
                ghost.direction[0], ghost.direction[1] = -ghost.direction[1], ghost.direction[0]

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw maze
        for row in range(ROWS):
            for col in range(COLS):
                x = col * BLOCK_SIZE
                y = row * BLOCK_SIZE
                if self.maze[row][col] == 1:
                    pygame.draw.rect(self.screen, BLUE, (x, y, BLOCK_SIZE, BLOCK_SIZE))
                elif self.maze[row][col] == 0:
                    pygame.draw.circle(self.screen, WHITE, 
                                    (x + BLOCK_SIZE//2, y + BLOCK_SIZE//2), 
                                    BLOCK_SIZE//6)

        # Draw Pacman
        pygame.draw.circle(self.screen, YELLOW,
                         (self.pacman.col * BLOCK_SIZE + BLOCK_SIZE//2,
                          self.pacman.row * BLOCK_SIZE + BLOCK_SIZE//2),
                         BLOCK_SIZE//2)

        # Draw ghosts
        for ghost in self.ghosts:
            pygame.draw.circle(self.screen, ghost.color,
                             (ghost.col * BLOCK_SIZE + BLOCK_SIZE//2,
                              ghost.row * BLOCK_SIZE + BLOCK_SIZE//2),
                             BLOCK_SIZE//2)

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.pacman.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 