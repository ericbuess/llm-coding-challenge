import pygame
from settings import TILE_SIZE

def grid_to_pixel(col, row):
    """Convert grid coordinates to pixel coordinates."""
    return col * TILE_SIZE, row * TILE_SIZE

def pixel_to_grid(x, y):
    """Convert pixel coordinates to grid coordinates."""
    return x // TILE_SIZE, y // TILE_SIZE

def is_grid_aligned(rect):
    """Check if an entity is aligned with the grid (useful for turns)."""
    return rect.x % TILE_SIZE == 0 and rect.y % TILE_SIZE == 0

def get_direction_vector(direction):
    """Convert string direction to vector."""
    directions = {
        'up': pygame.Vector2(0, -1),
        'down': pygame.Vector2(0, 1),
        'left': pygame.Vector2(-1, 0),
        'right': pygame.Vector2(1, 0),
        'none': pygame.Vector2(0, 0)
    }
    return directions.get(direction, pygame.Vector2(0, 0))

def get_opposite_direction(direction):
    """Get the opposite direction."""
    opposites = {
        'up': 'down',
        'down': 'up',
        'left': 'right',
        'right': 'left',
        'none': 'none'
    }
    return opposites.get(direction, 'none') 