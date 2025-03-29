import pygame

# --- Screen Dimensions ---
TILE_SIZE = 16
GRID_WIDTH = 28
GRID_HEIGHT = 31 # Standard Pac-Man maze height, adjust if using a different layout
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE + 50 # Extra space for score/lives display

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255) # Maze walls
RED = (255, 0, 0)   # Blinky
PINK = (255, 184, 255) # Pinky
CYAN = (0, 255, 255) # Inky
ORANGE = (255, 184, 82) # Clyde
FRIGHTENED_BLUE = (0, 0, 200)
FRIGHTENED_WHITE = (224, 224, 224)

# --- Game Settings ---
FPS = 60
PACMAN_SPEED = 80 # Pixels per second
GHOST_SPEED = 75  # Pixels per second
GHOST_FRIGHTENED_SPEED = 40 # Pixels per second
GHOST_EATEN_SPEED = 160 # Pixels per second

# --- Time Durations (in seconds) ---
SCATTER_TIME_1 = 7
CHASE_TIME_1 = 20
SCATTER_TIME_2 = 7
CHASE_TIME_2 = 20
SCATTER_TIME_3 = 5
CHASE_TIME_3 = 20
SCATTER_TIME_4 = 5
# Chase indefinitely after this point in many versions

FRIGHTENED_DURATION = 8 # How long ghosts stay frightened
FRIGHTENED_FLASH_DURATION = 2 # How long ghosts flash before returning to normal

# --- Points ---
PELLET_SCORE = 10
POWER_PELLET_SCORE = 50
GHOST_SCORES = [200, 400, 800, 1600] # For eating 1, 2, 3, 4 ghosts in one power pellet

# --- Maze Elements (Character Representations) ---
WALL = '#'
PELLET = '.'
POWER_PELLET = 'o'
EMPTY = ' '
GHOST_HOUSE = 'G' # Placeholder, might need specific handling
TUNNEL = 'T' # For wrap-around tunnels

# --- Directions ---
UP = pygame.Vector2(0, -1)
DOWN = pygame.Vector2(0, 1)
LEFT = pygame.Vector2(-1, 0)
RIGHT = pygame.Vector2(1, 0)
STOP = pygame.Vector2(0, 0)

# --- Ghost States ---
SCATTER = 0
CHASE = 1
FRIGHTENED = 2
EATEN = 3

# --- Ghost Types (for targeting logic) ---
BLINKY = 0
PINKY = 1
INKY = 2
CLYDE = 3 