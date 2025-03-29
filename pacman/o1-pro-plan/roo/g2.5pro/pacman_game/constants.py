# Constants for the Pac-Man game

# Screen dimensions
TILE_SIZE = 20
GRID_WIDTH = 28
GRID_HEIGHT = 31 # Standard Pac-Man maze height, adjust if using a different layout
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE + 50 # Extra space for score/lives

# Frame Rate
FPS = 60

# Colors (RGB tuples)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255) # Maze wall color
RED = (255, 0, 0)   # Blinky
PINK = (255, 184, 255) # Pinky
CYAN = (0, 255, 255) # Inky
ORANGE = (255, 184, 82)  # Clyde
PELLET_COLOR = (224, 189, 168) # Color for pellets
POWER_PELLET_COLOR = (255, 255, 255) # Color for power pellets
FRIGHTENED_COLOR = (0, 0, 200) # Ghost frightened color
EATEN_COLOR = (100, 100, 255) # Ghost eaten color (eyes)

# Speeds (pixels per second) - Adjust as needed for gameplay feel
PACMAN_SPEED = 80
GHOST_SPEED = 75
GHOST_FRIGHTENED_SPEED = 50
GHOST_EATEN_SPEED = 150

# Time Durations (in seconds)
SCATTER_TIME = 7
CHASE_TIME = 20
FRIGHTENED_TIME = 8 # Duration ghosts stay frightened
GHOST_RESPAWN_TIME = 3 # Time for eaten ghost to respawn

# Ghost States
SCATTER = 0
CHASE = 1
FRIGHTENED = 2
EATEN = 3

# Directions (using vectors for easier movement calculation)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
STOP = (0, 0)

# Scoring
PELLET_SCORE = 10
POWER_PELLET_SCORE = 50
GHOST_SCORES = [200, 400, 800, 1600] # Points for eating 1st, 2nd, 3rd, 4th ghost

# Lives
START_LIVES = 3

# Maze Layout (Example placeholder - will be loaded from maze.py)
MAZE_FILE = "maze1.txt" # Example file name

# Font settings
FONT_NAME = 'arial'
FONT_SIZE = 18