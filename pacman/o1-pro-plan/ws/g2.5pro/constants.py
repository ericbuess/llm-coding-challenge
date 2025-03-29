\
# --- Constants and Configuration ---

# Tile Size
TILE_SIZE = 16  # Pixels per tile

# Grid Dimensions (based on typical Pac-Man layout)
GRID_WIDTH = 28
GRID_HEIGHT = 31

# Window Size
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE  # 28 * 16 = 448
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE # 31 * 16 = 496

# Frame Rate
FPS = 60

# Colors (RGB tuples)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0) # Pac-Man color
BLUE = (0, 0, 255)   # Maze wall color
RED = (255, 0, 0)     # Blinky
PINK = (255, 184, 255) # Pinky
CYAN = (0, 255, 255)  # Inky
ORANGE = (255, 184, 82) # Clyde
FRIGHTENED_BLUE = (50, 50, 255)
FRIGHTENED_WHITE = (200, 200, 200)

# Speeds (adjust as needed)
PACMAN_SPEED = 80 # pixels per second
GHOST_SPEED = 75  # pixels per second
GHOST_SPEED_FRIGHTENED = 50 # pixels per second
GHOST_SPEED_EATEN = 150 # pixels per second

# Time Durations (in seconds)
SCATTER_TIME_1 = 7
CHASE_TIME_1 = 20
SCATTER_TIME_2 = 7
CHASE_TIME_2 = 20
SCATTER_TIME_3 = 5
CHASE_TIME_3 = 20 # Often becomes indefinite after this
SCATTER_TIME_4 = 5
FRIGHTENED_DURATION = 8 # Duration of power pellet effect

# Score Values
PELLET_POINTS = 10
POWER_PELLET_POINTS = 50
GHOST_POINTS = [200, 400, 800, 1600] # Points for eating 1st, 2nd, 3rd, 4th ghost

# Entity Directions (using vectors for simplicity)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
STOP = (0, 0)

# Game States
START = 0
PLAYING = 1
PAUSED = 2
GAME_OVER = 3
WIN = 4
