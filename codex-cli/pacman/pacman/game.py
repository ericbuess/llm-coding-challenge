#!/usr/bin/env python3
"""
Core game loop and map loading for Pac-Man.
"""
import sys

import pygame

from pacman.settings import TILE_SIZE, FPS, BLACK, MAP_FILE
from pacman.settings import WHITE
from pacman.sprites import Wall, Pellet, Pacman, Ghost


class Game:
    def __init__(self):
        pygame.init()
        self.walls = pygame.sprite.Group()
        self.pellets = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.pacman = None
        self.score = 0
        self.load_map()

        width = self.cols * TILE_SIZE
        height = self.rows * TILE_SIZE
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()

    def load_map(self):
        with open(MAP_FILE) as f:
            lines = [line.rstrip("\n") for line in f]
        self.rows = len(lines)
        self.cols = len(lines[0]) if self.rows > 0 else 0
        for y, line in enumerate(lines):
            for x, ch in enumerate(line):
                pos = (x * TILE_SIZE, y * TILE_SIZE)
                if ch == '#':
                    wall = Wall(pos)
                    self.walls.add(wall)
                    self.all_sprites.add(wall)
                elif ch == '.':
                    pellet = Pellet(pos)
                    self.pellets.add(pellet)
                    self.all_sprites.add(pellet)
                elif ch == 'P':
                    self.pacman = Pacman(pos)
                    self.all_sprites.add(self.pacman)
                elif ch == 'G':
                    ghost = Ghost(pos)
                    self.ghosts.add(ghost)
                    self.all_sprites.add(ghost)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.pacman.direction = pygame.math.Vector2(-1, 0)
        elif keys[pygame.K_RIGHT]:
            self.pacman.direction = pygame.math.Vector2(1, 0)
        elif keys[pygame.K_UP]:
            self.pacman.direction = pygame.math.Vector2(0, -1)
        elif keys[pygame.K_DOWN]:
            self.pacman.direction = pygame.math.Vector2(0, 1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.handle_input()
            self.pacman.update(self.walls)
            for ghost in self.ghosts:
                ghost.update(self.walls)

            eaten = pygame.sprite.spritecollide(self.pacman, self.pellets, dokill=True)
            self.score += len(eaten)

            self.screen.fill(BLACK)
            for sprite in self.all_sprites:
                self.screen.blit(sprite.image, sprite.rect)

            font = pygame.font.SysFont(None, 24)
            score_surf = font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_surf, (5, 5))

            pygame.display.flip()
            self.clock.tick(FPS)