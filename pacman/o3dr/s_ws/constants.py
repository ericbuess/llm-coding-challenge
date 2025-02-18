"""Global constants for the Pac-Man game."""
from enum import Enum, auto

# Display Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "Pac-Man"
FPS = 60

# Game Constants
TILE_SIZE = 32  # Size of each tile in pixels
PLAYER_SPEED = 200  # Pixels per second
GHOST_SPEED = 180  # Pixels per second
INITIAL_LIVES = 3

# Scoring Constants
SCORE_PELLET = 10
SCORE_POWER_PELLET = 50
SCORE_GHOST = [200, 400, 800, 1600]  # Consecutive ghost scores during power mode

# Timing Constants (in seconds)
POWER_PELLET_DURATION = 6.0
GHOST_FRIGHTENED_SPEED = 100  # Slower speed when frightened
GHOST_MODE_DURATIONS = [
    7.0,   # Scatter
    20.0,  # Chase
    7.0,   # Scatter
    20.0,  # Chase
    5.0,   # Scatter
    20.0,  # Chase
    5.0,   # Scatter
    float('inf')  # Chase forever
]

# Direction Vectors
class Direction(Enum):
    NONE = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

# Direction to vector mapping
DIRECTION_VECTORS = {
    Direction.NONE: (0, 0),
    Direction.UP: (0, 1),
    Direction.DOWN: (0, -1),
    Direction.LEFT: (-1, 0),
    Direction.RIGHT: (1, 0)
}

# Ghost States
class GhostState(Enum):
    SCATTER = auto()
    CHASE = auto()
    FRIGHTENED = auto()
    EATEN = auto()  # When returning to the ghost house

# Colors (RGBA)
COLOR_BLACK = (0, 0, 0, 255)
COLOR_WHITE = (255, 255, 255, 255)
COLOR_BLUE = (0, 0, 255, 255)
COLOR_YELLOW = (255, 255, 0, 255)
COLOR_RED = (255, 0, 0, 255)

# UI Constants
FONT_SIZE = 24
SCORE_POSITION = (10, SCREEN_HEIGHT - 30)
LIVES_POSITION = (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 30)
