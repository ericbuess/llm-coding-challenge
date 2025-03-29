"""
Constants used throughout the Pac-Man game
"""

# Tile and grid settings
TILE_SIZE = 20
GRID_WIDTH = 28
GRID_HEIGHT = 31
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE + 50  # Extra space for score display

# Game settings
FPS = 60
LIVES = 3

# Entity speeds (in pixels per frame)
PACMAN_SPEED = 2
GHOST_NORMAL_SPEED = 1.75
GHOST_FRIGHTENED_SPEED = 1
GHOST_EATEN_SPEED = 4

# Ghost timing constants (in milliseconds)
SCATTER_TIMES = [7000, 7000, 5000, 5000]  # Four scatter phases
CHASE_TIMES = [20000, 20000, 20000, -1]  # Last chase is indefinite
FRIGHTENED_TIME = 8000
GHOST_RELEASE_TIME = 5000  # Time to wait before releasing a ghost

# Score values
PELLET_SCORE = 10
POWER_PELLET_SCORE = 50
GHOST_SCORE = [200, 400, 800, 1600]  # Sequential ghost scores

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
FRIGHTENED_COLOR = (0, 0, 255)

# Direction vectors
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
STOP = (0, 0)

# Tile types
WALL = '#'
PELLET = '.'
POWER_PELLET = 'o'
EMPTY = ' '
GHOST_HOUSE = 'G'
PACMAN_START = 'P'
GHOST_START = {
    'BLINKY': 'B',
    'PINKY': 'p',
    'INKY': 'I',
    'CLYDE': 'C'
}