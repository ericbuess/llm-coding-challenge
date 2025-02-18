"""
Global settings and constants for the Pacman game.
"""

# Screen settings
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60
TILE_SIZE = 32

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)

# Speeds (pixels per frame)
PACMAN_SPEED = 3
GHOST_SPEED = 2

# Durations (in milliseconds)
FRIGHTENED_DURATION = 8000
SCATTER_DURATION = 7000
CHASE_DURATION = 20000

# Game States
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAMEOVER = "gameover"

# Scoring
PELLET_SCORE = 10
POWERPELLET_SCORE = 50
GHOST_SCORE = 200
FRUIT_SCORE = 100

# Asset paths
ASSET_DIR = "assets"
IMAGE_DIR = f"{ASSET_DIR}/images"
SOUND_DIR = f"{ASSET_DIR}/sounds"
