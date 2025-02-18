import pygame
from constants import *

class Pacman(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (15, 15), 15)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = PACMAN_SPEED
        self.direction = pygame.math.Vector2()
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        self.direction = pygame.math.Vector2()
        
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
            
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        
        # Keep Pacman within screen bounds
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (15, 15), 15)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = GHOST_SPEED
        self.direction = pygame.math.Vector2(1, 0)  # Start moving right

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        
        # Bounce off screen edges
        screen_rect = pygame.display.get_surface().get_rect()
        if not screen_rect.contains(self.rect):
            if self.rect.left < 0 or self.rect.right > screen_rect.right:
                self.direction.x *= -1
            if self.rect.top < 0 or self.rect.bottom > screen_rect.bottom:
                self.direction.y *= -1
            self.rect.clamp_ip(screen_rect)

class Pellet(pygame.sprite.Sprite):
    def __init__(self, x, y, is_power_pellet=False):
        super().__init__()
        size = POWER_PELLET_SIZE if is_power_pellet else PELLET_SIZE
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (size//2, size//2), size//2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_power_pellet = is_power_pellet
        self.points = POWER_PELLET_POINTS if is_power_pellet else PELLET_POINTS
