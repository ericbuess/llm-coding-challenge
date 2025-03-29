"""
Constants for Pac-Man game
"""

# Screen Constants
TILE_SIZE = 20
GRID_WIDTH = 28
GRID_HEIGHT = 31
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE + 50  # Extra space for score display

# Game Constants
FPS = 60
LIVES = 3

# Speed Constants (pixels per frame)
PACMAN_SPEED = 2
GHOST_SPEED = 2
GHOST_FRIGHTENED_SPEED = 1
GHOST_EATEN_SPEED = 4

# Timer Constants (in frames at 60 FPS)
SCATTER_TIME = [420, 420, 300, 300, 240, 240, 180, -1]  # 7s, 7s, 5s, 5s, 4s, 4s, 3s, permanent (at 60 FPS)
CHASE_TIME = [1200, 1200, 1200, 1200, 1200, -1]  # 20s, 20s, 20s, 20s, 20s, permanent (at 60 FPS)
FRIGHTENED_TIME = 480  # 8 seconds at 60 FPS

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
STOP = (0, 0)

# Color Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
FRIGHTENED_COLOR = (0, 0, 255)
FRIGHTENED_END_COLOR = (255, 255, 255)

# Score Constants
PELLET_SCORE = 10
POWER_PELLET_SCORE = 50
GHOST_SCORE = [200, 400, 800, 1600]  # Sequential ghost scores

# Maze Character Codes
WALL = '#'
PELLET = '.'
POWER_PELLET = 'o'
EMPTY = ' '
GHOST_HOUSE = 'G'
PACMAN_START = 'P'
GHOST_START = 'B'  # B, I, P, C for different ghosts

# Ghost Names
BLINKY = "blinky"
PINKY = "pinky"
INKY = "inky"
CLYDE = "clyde"

# Ghost States
SCATTER = "scatter"
CHASE = "chase"
FRIGHTENED = "frightened"
EATEN = "eaten"

# Game States
START = "start"
PLAYING = "playing"
PAUSED = "paused"
GAME_OVER = "game_over"
WIN = "win" 