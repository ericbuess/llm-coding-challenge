# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Game speed
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Tile size
TILE_SIZE = 16

# Ghost speeds for each level (baseline, increases with level)
GHOST_SPEEDS = {
    'normal': 1.75,
    'tunnel': 0.5,
    'frightened': 0.8
}

# Ghost mode durations for each level
GHOST_MODE_DURATIONS = [
    # Level 1
    {
        'scatter': [7, 7, 5, 5],
        'chase': [20, 20, 20, float('inf')]
    },
    # Level 2 (shorter scatter times)
    {
        'scatter': [7, 7, 5, 1],
        'chase': [20, 20, 1033, float('inf')]
    },
    # Level 3+ (minimal scatter)
    {
        'scatter': [5, 5, 5, 1],
        'chase': [20, 20, 1037, float('inf')]
    }
]

# Power pellet durations (seconds)
POWER_PELLET_DURATIONS = [
    8,    # Level 1
    7,    # Level 2
    6,    # Level 3
    5,    # Level 4
    4,    # Level 5
    3,    # Level 6
    2,    # Level 7
    1,    # Level 8+
]