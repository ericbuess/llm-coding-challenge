#!/usr/bin/env python3
"""
Sprite definitions for walls, pellets, Pac-Man, and ghosts.
"""
import random

import pygame

from pacman.settings import TILE_SIZE, BLUE, YELLOW, WHITE, RED, PINK, CYAN, ORANGE


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=pos)


class Pellet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        radius = TILE_SIZE // 8
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(
            self.image,
            WHITE,
            (TILE_SIZE // 2, TILE_SIZE // 2),
            radius,
        )
        self.rect = self.image.get_rect(topleft=pos)


class Pacman(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(
            self.image,
            YELLOW,
            (TILE_SIZE // 2, TILE_SIZE // 2),
            TILE_SIZE // 2,
        )
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = TILE_SIZE // 4

    def update(self, walls):
        if self.direction.length_squared() == 0:
            return
        new_rect = self.rect.move(
            self.direction.x * self.speed,
            self.direction.y * self.speed,
        )
        if not any(wall.rect.colliderect(new_rect) for wall in walls):
            self.rect = new_rect


class Ghost(pygame.sprite.Sprite):
    COLORS = [RED, PINK, CYAN, ORANGE]

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        color = random.choice(self.COLORS)
        pygame.draw.circle(
            self.image,
            color,
            (TILE_SIZE // 2, TILE_SIZE // 2),
            TILE_SIZE // 2,
        )
        self.rect = self.image.get_rect(topleft=pos)
        dirs = [
            pygame.math.Vector2(1, 0),
            pygame.math.Vector2(-1, 0),
            pygame.math.Vector2(0, 1),
            pygame.math.Vector2(0, -1),
        ]
        self.direction = random.choice(dirs)
        self.speed = TILE_SIZE // 4

    def update(self, walls):
        dirs = [
            pygame.math.Vector2(1, 0),
            pygame.math.Vector2(-1, 0),
            pygame.math.Vector2(0, 1),
            pygame.math.Vector2(0, -1),
        ]
        if random.random() < 0.1:
            self.direction = random.choice(dirs)
        new_rect = self.rect.move(
            self.direction.x * self.speed,
            self.direction.y * self.speed,
        )
        if any(wall.rect.colliderect(new_rect) for wall in walls):
            self.direction = random.choice(dirs)
        else:
            self.rect = new_rect