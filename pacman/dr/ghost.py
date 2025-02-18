import pygame
import random
from settings import TILE_SIZE

# Ghost class implements a simple AI: chasing Pac-Man when normal and moving randomly when vulnerable.
class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, color):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.color = color
        pygame.draw.circle(self.image, self.color, (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.direction = pygame.math.Vector2(0, 0)
        self.vulnerable = False
        self.vulnerable_timer = 0

    def update(self, walls, pacman):
        if self.vulnerable:
            self.random_move(walls)
            # Count down the vulnerable timer.
            self.vulnerable_timer -= 1
            if self.vulnerable_timer <= 0:
                self.vulnerable = False
                # Restore original appearance.
                self.image.fill((0, 0, 0, 0))
                pygame.draw.circle(self.image, self.color, (self.rect.width//2, self.rect.height//2), self.rect.width//2)
        else:
            self.chase_pacman(walls, pacman)

    def chase_pacman(self, walls, pacman):
        # Simple chase: compute a vector toward Pac-Man.
        target = pygame.math.Vector2(pacman.rect.center)
        current = pygame.math.Vector2(self.rect.center)
        if (target - current).length() != 0:
            direction = (target - current).normalize()
        else:
            direction = pygame.math.Vector2(0, 0)
        self.try_move(direction, walls)

    def random_move(self, walls):
        directions = [
            pygame.math.Vector2(1, 0),
            pygame.math.Vector2(-1, 0),
            pygame.math.Vector2(0, 1),
            pygame.math.Vector2(0, -1)
        ]
        random.shuffle(directions)
        for d in directions:
            if self.can_move(d, walls):
                self.direction = d
                break
        self.move(walls)

    def try_move(self, direction, walls):
        if self.can_move(direction, walls):
            self.direction = direction
        self.move(walls)

    def move(self, walls):
        if self.can_move(self.direction, walls):
            self.rect.x += self.direction.x * self.speed
            self.rect.y += self.direction.y * self.speed

    def can_move(self, direction, walls):
        new_rect = self.rect.copy()
        new_rect.x += direction.x * self.speed
        new_rect.y += direction.y * self.speed
        for wall in walls:
            if new_rect.colliderect(wall.rect):
                return False
        return True

    def set_vulnerable(self, timer):
        self.vulnerable = True
        self.vulnerable_timer = timer
        # Change appearance to indicate vulnerability.
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, (0, 0, 255), (self.rect.width//2, self.rect.height//2), self.rect.width//2)
