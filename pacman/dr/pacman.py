import pygame
from settings import TILE_SIZE, YELLOW

# PacMan class handles the player's character.
class PacMan(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        # For simplicity, we use colored circles for animation.
        self.images = {
            'left': pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA),
            'right': pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA),
            'up': pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA),
            'down': pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        }
        for key in self.images:
            pygame.draw.circle(self.images[key], YELLOW, (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2)
        self.image = self.images['left']
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.direction = pygame.math.Vector2(0, 0)
        # next_direction stores the intended direction from user input.
        self.next_direction = pygame.math.Vector2(0, 0)

    def update(self, walls):
        # If possible, update to the next direction.
        if self.can_move(self.next_direction, walls):
            self.direction = self.next_direction

        # Move Pac-Man if there’s no wall in the direction.
        if self.can_move(self.direction, walls):
            self.rect.x += self.direction.x * self.speed
            self.rect.y += self.direction.y * self.speed

        # Set the appropriate image based on movement direction.
        if self.direction.x < 0:
            self.image = self.images['left']
        elif self.direction.x > 0:
            self.image = self.images['right']
        elif self.direction.y < 0:
            self.image = self.images['up']
        elif self.direction.y > 0:
            self.image = self.images['down']

    def can_move(self, direction, walls):
        if direction.length_squared() == 0:
            return False
        new_rect = self.rect.copy()
        new_rect.x += direction.x * self.speed
        new_rect.y += direction.y * self.speed
        for wall in walls:
            if new_rect.colliderect(wall.rect):
                return False
        return True
