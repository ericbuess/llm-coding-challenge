# constants.py
# Game configuration values for Pac-Man

# Screen dimensions
SCREEN_WIDTH = 448  # 28 tiles * 16px
SCREEN_HEIGHT = 576  # 36 tiles * 16px
TILE_SIZE = 16

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 184, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 184, 82)
BLUE = (0, 0, 255)

# Game speeds
PACMAN_SPEED = 2
GHOST_SPEED = 2
FRIGHTENED_SPEED = 1

# Ghost modes durations (in seconds)
SCATTER_DURATION = 7
CHASE_DURATION = 20
FRIGHTENED_DURATION = 6

# Ghost house exit delays (in seconds)
GHOST_EXIT_DELAYS = {
    'blinky': 0,
    'pinky': 2,
    'inky': 4,
    'clyde': 6
}

# Score values
PELLET_SCORE = 10
POWER_PELLET_SCORE = 50
GHOST_SCORE = 200

# Maze layout file
MAZE_LAYOUT_FILE = "maze.txt"

# Sound filenames (to be added by user)
SOUND_CHOMP = "chomp.wav"
SOUND_EAT_GHOST = "eat_ghost.wav"
SOUND_POWER_PELLET = "power_pellet.wav"
SOUND_DEATH = "death.wav"
SOUND_START = "start.wav"

# High score file
HIGH_SCORE_FILE = "highscore.txt"
