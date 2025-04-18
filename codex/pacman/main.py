#!/usr/bin/env python3
"""
Simple Pacman clone in Python using pygame.
Controls: Arrow keys to move Pacman.
"""
import sys
import random
import math
import pygame

# Game settings
TILE_SIZE = 32
FPS = 60

# Map layout: '#' wall, '.' pellet, ' ' empty
level = [
    "##########",
    "#........#",
    "#.####.#.#",
    "#........#",
    "##########",
]

def load_map(level):
    walls = []
    pellets = set()
    for row_idx, line in enumerate(level):
        row = []
        for col_idx, ch in enumerate(line):
            if ch == '#':
                row.append(True)
            else:
                row.append(False)
                if ch == '.':
                    pellets.add((col_idx, row_idx))
        walls.append(row)
    return walls, pellets

class Entity:
    def __init__(self, col, row, color):
        self.x = col * TILE_SIZE + TILE_SIZE // 2
        self.y = row * TILE_SIZE + TILE_SIZE // 2
        self.color = color
        self.dir = (0, 0)
        self.next_dir = (0, 0)
        self.speed = 4

    def move(self, walls):
        # Try to change direction if possible
        if self.next_dir != self.dir:
            nx = self.x + self.next_dir[0] * self.speed
            ny = self.y + self.next_dir[1] * self.speed
            if not self.collides(nx, ny, walls):
                self.dir = self.next_dir
        # Move in current direction
        nx = self.x + self.dir[0] * self.speed
        ny = self.y + self.dir[1] * self.speed
        if not self.collides(nx, ny, walls):
            self.x = nx
            self.y = ny

    def collides(self, x, y, walls):
        # Check four corners for wall collision
        radius = TILE_SIZE // 2 - 2
        for dx in (-radius, radius):
            for dy in (-radius, radius):
                px = x + dx
                py = y + dy
                col = int(px // TILE_SIZE)
                row = int(py // TILE_SIZE)
                if row < 0 or row >= len(walls) or col < 0 or col >= len(walls[0]):
                    return True
                if walls[row][col]:
                    return True
        return False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,
                           (int(self.x), int(self.y)), TILE_SIZE // 2 - 2)

def main():
    pygame.init()
    walls, pellets = load_map(level)
    cols = len(level[0])
    rows = len(level)
    screen = pygame.display.set_mode((cols * TILE_SIZE, rows * TILE_SIZE))
    pygame.display.set_caption('Pacman')
    clock = pygame.time.Clock()

    # Initialize entities
    pacman = Entity(1, 1, (255, 255, 0))
    ghosts = [Entity(5, 3, (255, 0, 0))]
    # Random initial directions for ghosts
    for g in ghosts:
        g.dir = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
    # Remove pellet at Pacman's starting cell
    start_cell = (int(pacman.x) // TILE_SIZE, int(pacman.y) // TILE_SIZE)
    pellets.discard(start_cell)

    score = 0
    font = pygame.font.SysFont(None, 24)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pacman.next_dir = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    pacman.next_dir = (1, 0)
                elif event.key == pygame.K_UP:
                    pacman.next_dir = (0, -1)
                elif event.key == pygame.K_DOWN:
                    pacman.next_dir = (0, 1)

        # Update pacman
        pacman.move(walls)
        # Consume pellets
        pc = int(pacman.x // TILE_SIZE)
        pr = int(pacman.y // TILE_SIZE)
        if (pc, pr) in pellets:
            pellets.remove((pc, pr))
            score += 10

        # Update ghosts
        for g in ghosts:
            # change direction at tile center
            if ((int(g.x) - TILE_SIZE // 2) % TILE_SIZE == 0 and
                (int(g.y) - TILE_SIZE // 2) % TILE_SIZE == 0):
                # choose random valid direction
                options = []
                for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx = g.x + d[0] * g.speed
                    ny = g.y + d[1] * g.speed
                    if not g.collides(nx, ny, walls):
                        options.append(d)
                if options:
                    g.dir = random.choice(options)
            g.move(walls)

        # Check collisions with ghosts
        for g in ghosts:
            dist2 = (pacman.x - g.x) ** 2 + (pacman.y - g.y) ** 2
            if dist2 < (TILE_SIZE // 2) ** 2:
                print('Game Over! Score:', score)
                running = False
                break

        # Check win
        if not pellets:
            print('You Win! Score:', score)
            running = False

        # Draw
        screen.fill((0, 0, 0))
        # Draw walls and pellets
        for row_idx, row in enumerate(walls):
            for col_idx, is_wall in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                if is_wall:
                    pygame.draw.rect(screen, (33, 33, 255),
                                     (x, y, TILE_SIZE, TILE_SIZE))
                elif (col_idx, row_idx) in pellets:
                    pygame.draw.circle(screen, (200, 200, 200),
                                       (x + TILE_SIZE // 2, y + TILE_SIZE // 2), 4)
        # Draw entities
        pacman.draw(screen)
        for g in ghosts:
            g.draw(screen)

        # Draw score
        text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(text, (5, 5))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()