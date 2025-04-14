# entities.py
# Pac-Man and Ghost classes

import pygame
import random
import math
from constants import *

DIRECTIONS = [(1,0), (0,-1), (-1,0), (0,1)]  # Right, Up, Left, Down

class Entity:
    def __init__(self, x, y, color, speed):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.direction = (0, 0)
        self.next_direction = (0, 0)

    def move(self, maze):
        nx, ny = self.x + self.direction[0], self.y + self.direction[1]
        if not maze.is_wall(nx, ny):
            self.x, self.y = nx, ny
        elif self.next_direction != self.direction and not maze.is_wall(self.x + self.next_direction[0], self.y + self.next_direction[1]):
            self.direction = self.next_direction
            self.x += self.direction[0]
            self.y += self.direction[1]

    def set_direction(self, direction):
        self.next_direction = direction

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2)

class PacMan(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, YELLOW, PACMAN_SPEED)
        self.alive = True
        self.mouth_open = True

    def update(self, maze):
        if self.alive:
            self.move(maze)
            self.mouth_open = not self.mouth_open

    def draw(self, screen):
        # Simple mouth animation
        center = (self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2)
        if self.mouth_open:
            pygame.draw.circle(screen, self.color, center, TILE_SIZE // 2)
        else:
            pygame.draw.arc(screen, self.color, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), math.radians(30), math.radians(330), TILE_SIZE // 2)

class Ghost(Entity):
    def __init__(self, x, y, color, ghost_type):
        super().__init__(x, y, color, GHOST_SPEED)
        self.ghost_type = ghost_type
        self.state = 'scatter'  # scatter, chase, frightened, eaten
        self.scatter_target = self.get_scatter_target()
        self.frightened_timer = 0

    def get_scatter_target(self):
        if self.ghost_type == 'blinky':
            return (27, 0)
        elif self.ghost_type == 'pinky':
            return (0, 0)
        elif self.ghost_type == 'inky':
            return (27, 35)
        elif self.ghost_type == 'clyde':
            return (0, 35)
        return (0, 0)

    def update(self, maze, pacman, ghosts):
        if self.state == 'frightened':
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                self.state = 'chase'
        if self.state == 'eaten':
            # Return to ghost house
            self.move_towards((13, 17), maze)
            if (self.x, self.y) == (13, 17):
                self.state = 'chase'
        elif self.state == 'frightened':
            self.random_move(maze)
        else:
            self.ai_move(maze, pacman, ghosts)

    def ai_move(self, maze, pacman, ghosts):
        # Simple AI: chase Pac-Man or scatter
        if self.state == 'scatter':
            self.move_towards(self.scatter_target, maze)
        elif self.state == 'chase':
            if self.ghost_type == 'blinky':
                self.move_towards((pacman.x, pacman.y), maze)
            elif self.ghost_type == 'pinky':
                target = (pacman.x + 4 * pacman.direction[0], pacman.y + 4 * pacman.direction[1])
                self.move_towards(target, maze)
            elif self.ghost_type == 'inky':
                # Inky's target: vector from Blinky to 2 tiles in front of Pac-Man
                blinky = next(g for g in ghosts if g.ghost_type == 'blinky')
                vec_x = pacman.x + 2 * pacman.direction[0] - blinky.x
                vec_y = pacman.y + 2 * pacman.direction[1] - blinky.y
                target = (blinky.x + 2 * vec_x, blinky.y + 2 * vec_y)
                self.move_towards(target, maze)
            elif self.ghost_type == 'clyde':
                dist = math.hypot(self.x - pacman.x, self.y - pacman.y)
                if dist > 8:
                    self.move_towards((pacman.x, pacman.y), maze)
                else:
                    self.move_towards(self.scatter_target, maze)

    def move_towards(self, target, maze):
        # Choose the direction that minimizes distance to target
        min_dist = float('inf')
        best_dir = self.direction
        for d in DIRECTIONS:
            nx, ny = self.x + d[0], self.y + d[1]
            if not maze.is_wall(nx, ny):
                dist = math.hypot(target[0] - nx, target[1] - ny)
                if dist < min_dist:
                    min_dist = dist
                    best_dir = d
        self.direction = best_dir
        self.move(maze)

    def random_move(self, maze):
        random.shuffle(DIRECTIONS)
        for d in DIRECTIONS:
            nx, ny = self.x + d[0], self.y + d[1]
            if not maze.is_wall(nx, ny):
                self.direction = d
                self.move(maze)
                break

    def frighten(self):
        self.state = 'frightened'
        self.frightened_timer = FRIGHTENED_DURATION * 60

    def eaten(self):
        self.state = 'eaten'

    def draw(self, screen):
        color = BLUE if self.state == 'frightened' else self.color
        pygame.draw.circle(screen, color, (self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2)
