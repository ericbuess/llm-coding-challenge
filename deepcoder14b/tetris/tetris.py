import pygame
import random
from pygame.locals import *

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)

# Board dimensions
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Block size in pixels
BLOCK_SIZE = 30

# Screen dimensions
SCREEN_WIDTH = BOARD_WIDTH * BLOCK_SIZE + 200  # Adding space for score
SCREEN_HEIGHT = BOARD_HEIGHT * BLOCK_SIZE

# Tetromino shapes and colors
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'L': [[0, 1, 0], [0, 1, 0], [1, 1, 1]],
    'J': [[0, 1, 0], [0, 1, 0], [-1, -1, -1]],  # Using negative indices for rotation
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]]
}

COLORS = {
    'I': CYAN,
    'O': YELLOW,
    'T': RED,
    'L': GREEN,
    'J': BLUE,
    'S': MAGENTA,
    'Z': MAGENTA
}

class Tetris:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")

        # Clock for game timing
        self.clock = pygame.time.Clock()

        # Game state
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.score = 0

        # Current piece
        self.current_piece = None
        self.current_color = None
        self.current_x = 0
        self.current_y = 0

    def new_piece(self):
        # Select a random shape and color
        shape_keys = list(SHAPES.keys())
        self.current_piece = SHAPES[random.choice(shape_keys)]
        self.current_color = COLORS[shape_keys.index(self.current_piece)]

        # Calculate starting position
        self.current_x = (BOARD_WIDTH - len(self.current_piece[0])) // 2
        self.current_y = 0

    def draw(self):
        # Clear screen with black background
        self.screen.fill(BLACK)

        # Draw the board
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board[y][x]:
                    # Calculate position on screen
                    pos_x = x * BLOCK_SIZE + 200  # Adding offset for score panel
                    pos_y = y * BLOCK_SIZE

                    # Draw the block
                    pygame.draw.rect(self.screen, self.board[y][x],
                                   (pos_x, pos_y, BLOCK_SIZE-1, BLOCK_SIZE-1))

        # Draw current piece
        if self.current_piece:
            for y in range(len(self.current_piece)):
                for x in range(len(self.current_piece[0])):
                    if self.current_piece[y][x]:
                        pos_x = (self.current_x + x) * BLOCK_SIZE + 200
                        pos_y = (self.current_y + y) * BLOCK_SIZE

                        # Draw the block
                        pygame.draw.rect(self.screen, self.current_color,
                                       (pos_x, pos_y, BLOCK_SIZE-1, BLOCK_SIZE-1))

        # Draw score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(text, (BOARD_WIDTH * BLOCK_SIZE + 20, 20))

    def collision(self):
        # Check if current piece is out of bounds or collides with the board
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[0])):
                if self.current_piece[y][x]:
                    # Calculate absolute positions
                    abs_x = self.current_x + x
                    abs_y = self.current_y + y

                    # Check boundaries
                    if abs_x < 0 or abs_x >= BOARD_WIDTH:
                        return True
                    if abs_y >= BOARD_HEIGHT:
                        return True

                    # Check collision with existing blocks
                    if abs_y >= 0 and self.board[abs_y][abs_x]:
                        return True

        return False

    def merge(self):
        # Merge current piece into the board
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[0])):
                if self.current_piece[y][x]:
                    self.board[self.current_y + y][self.current_x + x] = self.current_color

    def rotate(self):
        # Rotate current piece 90 degrees
        new_shape = []
        for i in range(len(self.current_piece[0])):
            row = []
            for j in reversed(range(len(self.current_piece))):
                row.append(self.current_piece[j][i])
            new_shape.append(row)

        # Check if rotation is possible
        temp_x = self.current_x
        temp_y = self.current_y
        old_piece = self.current_piece

        # Update the piece and position for trial
        self.current_piece = new_shape
        collision = self.collision()
        self.current_piece = old_piece

        # If no collision, rotate
        if not collision:
            # Adjust position after rotation
            # This might need more logic depending on how the pieces are structured
    def move_down(self):
        # Move piece down by one row
        if self.current_y + 1 < BOARD_HEIGHT - len(self.current_piece):
            self.current_y += 1
        else:
            # If can't move down, merge into board and create new piece
            self.merge()
            self.clear_lines()
            self.new_piece()

    def clear_lines(self):
        # Clear complete lines in the board
        for y in range(BOARD_HEIGHT):
            if all(self.board[y][x] != 0 for x in range(BOARD_WIDTH)):
                del self.board[y]
                self.board.insert(0, [0] * BOARD_WIDTH)
                self.score += 100

    def handle_input(self, event):
        # Handle keyboard events
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                # Move piece left
                if self.current_x > 0:
                    self.current_x -= 1
            elif event.key == K_RIGHT:
                # Move piece right
                if self.current_x < BOARD_WIDTH - len(self.current_piece[0]):
                    self.current_x += 1
            elif event.key == K_DOWN:
                # Move piece down faster
                self.move_down()
            elif event.key == K_UP:
                # Rotate piece
                self.rotate()

    def run(self):
        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    return
                else:
                    self.handle_input(event)

            # Update game state
            self.move_down()  # Auto-move down

            # Draw everything
            self.draw()

            # Update screen
            pygame.display.flip()

            # Control frame rate
            self.clock.tick(5)

if __name__ == "__main__":
    game = Tetris()
    game.run()
