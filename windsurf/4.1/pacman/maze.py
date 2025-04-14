# maze.py
# Maze layout and collision detection for Pac-Man

import pygame
from constants import TILE_SIZE, MAZE_LAYOUT_FILE, WALL, PELLET, POWER_PELLET

WALL = 'X'
PELLET = '.'
POWER_PELLET = 'o'
EMPTY = ' '

class Maze:
    def __init__(self):
        self.layout = []
        self.pellets = set()
        self.power_pellets = set()
        self.load_maze()

    def load_maze(self):
        with open(MAZE_LAYOUT_FILE, 'r') as f:
            for y, line in enumerate(f):
                row = []
                for x, ch in enumerate(line.strip('\n')):
                    row.append(ch)
                    if ch == PELLET:
                        self.pellets.add((x, y))
                    elif ch == POWER_PELLET:
                        self.power_pellets.add((x, y))
                self.layout.append(row)

    def draw(self, screen):
        for y, row in enumerate(self.layout):
            for x, ch in enumerate(row):
                if ch == WALL:
                    pygame.draw.rect(screen, (33, 33, 255), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif ch == PELLET and (x, y) in self.pellets:
                    pygame.draw.circle(screen, (255, 255, 255), (x * TILE_SIZE + TILE_SIZE//2, y * TILE_SIZE + TILE_SIZE//2), 2)
                elif ch == POWER_PELLET and (x, y) in self.power_pellets:
                    pygame.draw.circle(screen, (255, 255, 255), (x * TILE_SIZE + TILE_SIZE//2, y * TILE_SIZE + TILE_SIZE//2), 5)

    def is_wall(self, x, y):
        if 0 <= y < len(self.layout) and 0 <= x < len(self.layout[y]):
            return self.layout[y][x] == WALL
        return True

    def eat_pellet(self, x, y):
        if (x, y) in self.pellets:
            self.pellets.remove((x, y))
            return 'pellet'
        elif (x, y) in self.power_pellets:
            self.power_pellets.remove((x, y))
            return 'power_pellet'
        return None

    def pellets_left(self):
        return len(self.pellets) + len(self.power_pellets)
