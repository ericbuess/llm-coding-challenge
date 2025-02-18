"""
Helper functions for the Pacman game.
"""
import pygame
from settings import TILE_SIZE

def grid_to_pixel(col: int, row: int) -> tuple[int, int]:
    """Convert grid coordinates to pixel coordinates."""
    return col * TILE_SIZE, row * TILE_SIZE

def pixel_to_grid(x: int, y: int) -> tuple[int, int]:
    """Convert pixel coordinates to grid coordinates."""
    return x // TILE_SIZE, y // TILE_SIZE

def get_direction_vector(direction: str) -> pygame.Vector2:
    """Convert a direction string to a Vector2."""
    directions = {
        'up': pygame.Vector2(0, -1),
        'down': pygame.Vector2(0, 1),
        'left': pygame.Vector2(-1, 0),
        'right': pygame.Vector2(1, 0),
    }
    return directions.get(direction, pygame.Vector2(0, 0))

def can_move_in_direction(entity: pygame.sprite.Sprite, direction: pygame.Vector2, 
                         wall_group: pygame.sprite.Group) -> bool:
    """Check if an entity can move in a given direction without hitting a wall."""
    test_rect = entity.rect.copy()
    test_rect.x += direction.x
    test_rect.y += direction.y
    return not pygame.sprite.spritecollide(entity, wall_group, False, 
                                         collided=lambda s1, s2: test_rect.colliderect(s2.rect))

def get_valid_directions(entity: pygame.sprite.Sprite, 
                        wall_group: pygame.sprite.Group) -> list[pygame.Vector2]:
    """Get list of valid directions an entity can move."""
    valid = []
    for direction in [pygame.Vector2(0, -1), pygame.Vector2(0, 1), 
                     pygame.Vector2(-1, 0), pygame.Vector2(1, 0)]:
        if can_move_in_direction(entity, direction, wall_group):
            valid.append(direction)
    return valid
