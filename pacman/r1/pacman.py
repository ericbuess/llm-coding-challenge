import pygame
from constants import *

class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = (0, 0)
        self.sprites = [
            pygame.image.load("assets/pacman_0.png").convert_alpha(),
            pygame.image.load("assets/pacman_1.png").convert_alpha(),
            pygame.image.load("assets/pacman_2.png").convert_alpha()
        ]
        self.current_sprite = 0
        self.animation_counter = 0
        
    def update(self, maze):
        # Movement
        new_x = self.x + self.direction[0] * PACMAN_SPEED
        new_y = self.y + self.direction[1] * PACMAN_SPEED
        
        # Grid-based collision
        grid_x = int(new_x // TILE_SIZE)
        grid_y = int(new_y // TILE_SIZE)
        
        if 0 <= grid_x < SCREEN_WIDTH//TILE_SIZE and 0 <= grid_y < SCREEN_HEIGHT//TILE_SIZE:
            if maze[grid_y][grid_x] != '1':
                self.x = new_x
                self.y = new_y
        
        # Animation
        self.animation_counter += 1
        if self.animation_counter >= 5:
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.animation_counter = 0
            
    def draw(self, screen):
        rotated_sprite = pygame.transform.rotate(self.sprites[self.current_sprite], 
                                                self.get_rotation_angle())
        screen.blit(rotated_sprite, (self.x - TILE_SIZE//2, self.y - TILE_SIZE//2))
        
    def get_rotation_angle(self):
        if self.direction == (-1, 0):
            return 180
        elif self.direction == (0, -1):
            return 90
        elif self.direction == (0, 1):
            return 270
        return 0 