import pygame
from sprites import Wall, Pellet, PowerPellet
from constants import *

class Maze:
    def __init__(self):
        self.walls = pygame.sprite.Group()
        self.pellets = pygame.sprite.Group()
        self.power_pellets = pygame.sprite.Group()
        self.ghost_positions = []
        self.pacman_position = None
        self.load_maze()

    def load_maze(self):
        for row in range(len(MAZE_LAYOUT)):
            for col in range(len(MAZE_LAYOUT[row])):
                cell = MAZE_LAYOUT[row][col]
                if cell == 1:  # Wall
                    wall = Wall(col, row)
                    self.walls.add(wall)
                elif cell == 2:  # Pellet
                    pellet = Pellet(col, row)
                    self.pellets.add(pellet)
                elif cell == 3:  # Power Pellet
                    power_pellet = PowerPellet(col, row)
                    self.power_pellets.add(power_pellet)
                elif cell == 4:  # Pacman start
                    self.pacman_position = (col, row)
                elif cell in [5, 6, 7, 8]:  # Ghost starts
                    self.ghost_positions.append((col, row))

    def draw(self, screen):
        self.walls.draw(screen)
        self.pellets.draw(screen)
        self.power_pellets.draw(screen)

    def get_pacman_start(self):
        return self.pacman_position

    def get_ghost_starts(self):
        return self.ghost_positions

    def remaining_pellets(self):
        return len(self.pellets) + len(self.power_pellets)
