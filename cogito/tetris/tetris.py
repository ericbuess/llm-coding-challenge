import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 8)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]], # I-piece
    [[1, 1], [1, 1]], # O-piece
    [[1, 1, 1], [0, 1, 0]], # T-piece
    [[1, 1, 1], [1, 0, 0]], # L-piece
    [[1, 1, 1], [0, 0, 1]], # J-piece
    [[1, 1, 0], [0, 1, 1]], # S-piece
    [[0, 1, 1], [1, 1, 0]] # Z-piece
]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.score = 0
        self.level = 1
        self.fall_time = 0
        
    def new_piece(self):
        self.current_piece = {
            'shape': random.choice(SHAPES),
            'x': GRID_WIDTH // 2 - len(self.current_piece['shape'][0]) // 2,
            'y': 0,
            'rotation': 0
        }
        
    def rotate_piece(self):
        if not self.current_piece:
            return
            
        new_rotation = (self.current_piece['rotation'] + 1) % 4
        
        # Calculate new position after rotation
        shape = self.current_piece['shape']
        rotated_shape = [[shape[y][x] for y in range(len(shape)-1, -1, -1)] 
                         for x in range(len(shape[0]))]
        
        if len(rotated_shape) > GRID_HEIGHT:
            return
            
        new_x = self.current_piece['x'] + (len(shape[0]) - len(rotated_shape)) // 2
        
        # Check collision
        if not self.valid_position(new_x, self.current_piece['y'], rotated_shape):
            return
            
        self.current_piece.update({
            'shape': rotated_shape,
            'rotation': new_rotation,
            'x': new_x
        })
        
    def valid_position(self, x, y, shape):
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] == 1:
                    if (y + i < 0 or 
                        y + i >= GRID_HEIGHT or 
                        x + j < 0 or 
                        x + j >= GRID_WIDTH or
                        self.grid[y + i][x + j] != 0):
                        return False
        return True
        
    def move_piece(self, dx):
        new_x = self.current_piece['x'] + dx
        
        if self.valid_position(new_x, self.current_piece['y'], 
                              self.current_piece['shape']):
            self.current_piece['x'] = new_x
            
    def update_grid(self):
        if not self.current_piece:
            return
            
        for i in range(len(self.current_piece['shape'])):
            for j in range(len(self.current_piece['shape'][i])):
                if (self.current_piece['y'] + i < GRID_HEIGHT and 
                    self.current_piece['shape'][i][j] == 1):
                    self.grid[self.current_piece['y'] + i][
                             self.current_piece['x'] + j] = 1
                    
    def check_lines(self):
        lines_cleared = 0
        
        for y in range(GRID_HEIGHT):
            if all(cell == 1 for cell in self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0] * GRID_WIDTH)
                lines_cleared += 1
                
        return lines_cleared
        
    def run(self):
        clock = pygame.time.Clock()
        fall_time = 0
        move_timer = 0
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_piece(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.move_piece(1)
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
                        
            fall_time += clock.get_time()
            move_timer += clock.get_time()
            
            # Move piece down
            if fall_time >= 1000 // self.level:
                fall_time = 0
                if not self.valid_position(self.current_piece['x'], 
                                          self.current_piece['y'] + 1,
                                          self.current_piece['shape']):
                    self.update_grid()
                    
                    lines = self.check_lines()
                    self.score += lines * 100
                    
                    # Increase level every 10 lines
                    if lines > 0:
                        self.level = max(1, (self.score // 1000) + 1)
                        
                    self.new_piece()
                else:
                    self.current_piece['y'] += 1
                    
            # Draw everything
            self.screen.fill(BLACK)
            
            # Draw grid
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    if self.grid[y][x] == 1:
                        pygame.draw.rect(self.screen, WHITE,
                                        (x * BLOCK_SIZE, 
                                         y * BLOCK_SIZE, 
                                         BLOCK_SIZE, 
                                         BLOCK_SIZE))
            
            # Draw current piece
            if self.current_piece:
                shape = self.current_piece['shape']
                for i in range(len(shape)):
                    for j in range(len(shape[i])):
                        if shape[i][j] == 1:
                            pygame.draw.rect(self.screen, WHITE,
                                            ((self.current_piece['x'] + j) * 
                                             BLOCK_SIZE,
                                             (self.current_piece['y'] + i) * 
                                             BLOCK_SIZE,
                                             BLOCK_SIZE, 
                                             BLOCK_SIZE))
            
            # Draw score and level
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {self.score}", True, WHITE)
            level_text = font.render(f"Level: {self.level}", True, WHITE)
            self.screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 10, 10))
            self.screen.blit(level_text, 
                            (GRID_WIDTH * BLOCK_SIZE + 10, 50))
            
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    game = Tetris()
    game.new_piece()
    game.run()
    
pygame.quit()

