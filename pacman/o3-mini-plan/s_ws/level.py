"""
Level loader and manager.
"""
import pygame
from settings import TILE_SIZE
from entities.wall import Wall
from entities.pacman import Pacman
from entities.ghost import Ghost
from entities.pellet import Pellet
from entities.powerpellet import PowerPellet

class Level:
    def __init__(self, game):
        """Initialize level."""
        self.game = game
        self.layout = [
            "############################",
            "#............##............#",
            "#.####.#####.##.#####.####.#",
            "#O####.#####.##.#####.####O#",
            "#..........................#",
            "#.####.##.########.##.####.#",
            "#......##....##....##......#",
            "######.##### ## #####.######",
            "     #.##### ## #####.#     ",
            "     #.##    G     ##.#     ",
            "     #.## ###--### ##.#     ",
            "######.## #      # ##.######",
            "      .   #      #   .      ",
            "######.## #      # ##.######",
            "     #.## ######## ##.#     ",
            "     #.##    P     ##.#     ",
            "     #.## ######## ##.#     ",
            "######.## ######## ##.######",
            "#............##............#",
            "#.####.#####.##.#####.####.#",
            "#O..##................##..O#",
            "###.##.##.########.##.##.###",
            "#......##....##....##......#",
            "#.##########.##.##########.#",
            "#..........................#",
            "############################",
        ]
        
        # Store initial positions
        self.pacman_start = None
        self.ghost_starts = []
        
    def load(self):
        """Load level from layout."""
        ghost_colors = ["red", "pink", "blue", "orange"]
        ghost_count = 0
        
        for row_index, row in enumerate(self.layout):
            for col_index, char in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                
                if char == "#":
                    wall = Wall(x, y)
                    self.game.wall_group.add(wall)
                    self.game.all_sprites.add(wall)
                elif char == ".":
                    pellet = Pellet(x, y)
                    self.game.pellet_group.add(pellet)
                    self.game.all_sprites.add(pellet)
                elif char == "O":
                    power = PowerPellet(x, y)
                    self.game.powerpellet_group.add(power)
                    self.game.all_sprites.add(power)
                elif char == "P":
                    self.pacman_start = (x, y)
                    pacman = Pacman(x, y)
                    self.game.pacman_group.add(pacman)
                    self.game.all_sprites.add(pacman)
                    self.game.pacman = pacman
                elif char == "G" and ghost_count < len(ghost_colors):
                    self.ghost_starts.append((x, y))
                    ghost = Ghost(x, y, ghost_colors[ghost_count])
                    self.game.ghost_group.add(ghost)
                    self.game.all_sprites.add(ghost)
                    ghost_count += 1
    
    def reset_positions(self):
        """Reset all entities to their starting positions."""
        if self.pacman_start and self.game.pacman:
            self.game.pacman.reset_position(*self.pacman_start)
        
        for ghost, start_pos in zip(self.game.ghost_group.sprites(), self.ghost_starts):
            ghost.reset_position(*start_pos)
    
    def is_complete(self) -> bool:
        """Check if level is complete (all pellets collected)."""
        return len(self.game.pellet_group) == 0 and len(self.game.powerpellet_group) == 0
