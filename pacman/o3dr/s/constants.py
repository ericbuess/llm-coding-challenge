"""Game constants and configuration."""
from enum import Enum, auto

# Display Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "Pac-Man"
FPS = 60

# Game Constants
TILE_SIZE = 32
PLAYER_SPEED = 200  # pixels per second
GHOST_SPEED = 180   # pixels per second
INITIAL_LIVES = 3

# Scoring
PELLET_SCORE = 10
POWER_PELLET_SCORE = 50
GHOST_SCORE = 200

# Timing (in seconds)
POWER_PELLET_DURATION = 8.0
GHOST_FRIGHTENED_SPEED = 100  # slower when frightened

# Directions as (x, y) vectors
class Direction:
    NONE = (0, 0)
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class GhostState(Enum):
    SCATTER = auto()
    CHASE = auto()
    FRIGHTENED = auto()

# Colors (RGBA)
BACKGROUND_COLOR = (0, 0, 0, 255)
WALL_COLOR = (33, 33, 255, 255)
PELLET_COLOR = (255, 255, 255, 255)
TEXT_COLOR = (255, 255, 255, 255)

# Added transparent color constant (RGBA)
TRANSPARENT = (0, 0, 0, 0) 