# Constants for the Pac-Man game

# Display settings
TILE_SIZE = 20
GRID_WIDTH = 28
GRID_HEIGHT = 31
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE + 50  # Extra space for score display
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
BLUE_FRIGHTENED = (0, 0, 255)
WHITE_FRIGHTENED = (255, 255, 255)
MAZE_BLUE = (33, 33, 255)

# Game speeds (pixels per frame)
PACMAN_SPEED = 2
GHOST_SPEED = 1.75
GHOST_FRIGHTENED_SPEED = 1
GHOST_EATEN_SPEED = 4

# Time constants (in frames)
SCATTER_TIME = 7 * FPS  # 7 seconds in frames
CHASE_TIME = 20 * FPS   # 20 seconds in frames
FRIGHTENED_TIME = 8 * FPS  # 8 seconds in frames
GHOST_HOUSE_TIME = 5 * FPS  # Time ghosts stay in house before initial release

# Direction vectors
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
STOP = (0, 0)

# Scoring
PELLET_POINTS = 10
POWER_PELLET_POINTS = 50
GHOST_POINTS = [200, 400, 800, 1600]  # Points for eating each ghost in sequence
FRUIT_POINTS = 100

# Initial lives
INITIAL_LIVES = 3

# Tile types
WALL = '#'
PELLET = '.'
POWER_PELLET = 'o'
EMPTY = ' '
GHOST_HOUSE = 'G'
PACMAN_START = 'P'

# Ghost types
BLINKY = 'blinky'
PINKY = 'pinky'
INKY = 'inky'
CLYDE = 'clyde'

# Ghost states
SCATTER = 'scatter'
CHASE = 'chase'
FRIGHTENED = 'frightened'
EATEN = 'eaten'

# Game states
START = 'start'
PLAY = 'play'
PAUSE = 'pause'
GAME_OVER = 'game_over'
WIN = 'win'
