#!/usr/bin/env python3
"""
Global settings and constants for the Pac-Man game.
"""
import os

# Frame rate (frames per second)
FPS = 10

# Size of each tile (square) in pixels
TILE_SIZE = 24

# Path to the map layout file
MAP_FILE = os.path.join(os.path.dirname(__file__), "map.txt")

# Color definitions (R, G, B)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)