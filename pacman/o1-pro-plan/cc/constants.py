# Game constants

# Screen and grid dimensions
TILE_SIZE = 20
GRID_WIDTH = 28
GRID_HEIGHT = 31
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE + 50  # Extra space for score

# Game speeds
FPS = 60
PACMAN_SPEED = 80  # pixels per second
GHOST_SPEED = 75  # pixels per second
FRIGHTENED_SPEED = 40  # pixels per second
EATEN_SPEED = 150  # pixels per second

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Directions
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)
STOP = (0, 0)

# Timer durations (in milliseconds)
SCATTER_TIME = 7000
CHASE_TIME = 20000
FRIGHTENED_TIME = 8000

# Scoring
PELLET_POINTS = 10
POWER_PELLET_POINTS = 50
GHOST_POINTS = [200, 400, 800, 1600]  # Points for eating ghosts

# Game states
START = 0
PLAY = 1
PAUSE = 2
GAME_OVER = 3
WIN = 4

# Initial lives
INITIAL_LIVES = 3
