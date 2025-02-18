import pygame
from settings import TILE_SIZE, MAZE_LAYOUT, BLUE

# A simple Wall sprite for maze boundaries.
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))

# Maze class that creates walls and places pellets based on MAZE_LAYOUT.
class Maze:
    def __init__(self):
        self.wall_group = pygame.sprite.Group()
        self.pellet_group = pygame.sprite.Group()
        self.power_pellet_group = pygame.sprite.Group()
        self.load_maze()

    def load_maze(self):
        # Walk through the layout and add sprites accordingly.
        for row_idx, row in enumerate(MAZE_LAYOUT):
            for col_idx, char in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                if char == '#':
                    wall = Wall(x, y)
                    self.wall_group.add(wall)
                elif char == '.':
                    # Import Pellet here to avoid circular imports.
                    from pellet import Pellet
                    pellet = Pellet(x + TILE_SIZE // 2, y + TILE_SIZE // 2)
                    self.pellet_group.add(pellet)
                elif char == 'o':
                    from pellet import PowerPellet
                    power = PowerPellet(x + TILE_SIZE // 2, y + TILE_SIZE // 2)
                    self.power_pellet_group.add(power)

    def draw(self, screen):
        self.wall_group.draw(screen)
        self.pellet_group.draw(screen)
        self.power_pellet_group.draw(screen)
