# maze.py
# Contains the Maze class responsible for:
# - Loading the maze layout
# - Storing pellet state
# - Collision detection
# - Rendering the maze

import pygame
from constants import *

class Maze:
    def __init__(self, layout_filepath):
        self.layout = []
        self.pellets = []
        self.power_pellets = []
        self.walls = []
        self.ghost_house_access = [] # Points ghosts can enter/exit the house
        self._load_layout(layout_filepath)
        self._parse_layout()

    def _load_layout(self, filepath):
        # TODO: Load layout from a text file
        # Example simplified layout (replace with file loading)
        self.layout = [
            "############################",
            "#............##............#",
            "#.####.#####.##.#####.####.#",
            "#o####.#####.##.#####.####o#", # o for power pellet
            "#.####.#####.##.#####.####.#",
            "#..........................#",
            "#.####.##.########.##.####.#",
            "#.####.##.########.##.####.#",
            "#......##....##....##......#",
            "######.##### ## #####.######",
            "     #.##### ## #####.#     ",
            "     #.##   G  G   ##.#     ", # G for Ghost area (simplified)
            "     #.## ######## ##.#     ",
            "######.## ######## ##.######",
            "T     .   ########   .     T", # T for Tunnel
            "######.## ######## ##.######",
            "     #.## ######## ##.#     ",
            "     #.##   G  G   ##.#     ",
            "     #.## ######## ##.#     ",
            "######.## ######## ##.######",
            "#............##............#",
            "#.####.#####.##.#####.####.#",
            "#.####.#####.##.#####.####.#",
            "#o..##.......  .......##..o#",
            "###.##.##.########.##.##.###",
            "###.##.##.########.##.##.###",
            "#......##....##....##......#",
            "#.##########.##.##########.#",
            "#.##########.##.##########.#",
            "#..........................#",
            "############################"
        ]
        # Ensure grid dimensions match layout
        # assert len(self.layout[0]) == GRID_WIDTH
        # assert len(self.layout) == GRID_HEIGHT
        # Note: Need to handle potential mismatch or adjust constants


    def _parse_layout(self):
        # Iterate through the loaded layout and populate walls, pellets etc.
        for r, row in enumerate(self.layout):
            for c, char in enumerate(row):
                pos = (c, r)
                if char == '#':
                    self.walls.append(pos)
                elif char == '.':
                    self.pellets.append(pos)
                elif char == 'o':
                    self.power_pellets.append(pos)
                # Add logic for Ghost house 'G', Tunnels 'T', etc.
                # Store player start position, ghost start positions maybe?

    def is_wall(self, tile_x, tile_y):
        return (tile_x, tile_y) in self.walls

    def can_move_to(self, tile_x, tile_y):
        # Check boundaries and if it's not a wall
        if 0 <= tile_x < GRID_WIDTH and 0 <= tile_y < GRID_HEIGHT:
            return not self.is_wall(tile_x, tile_y)
        return False

    def get_pellet_at(self, tile_x, tile_y):
        pos = (tile_x, tile_y)
        if pos in self.pellets:
            return 'pellet'
        if pos in self.power_pellets:
            return 'power_pellet'
        return None

    def eat_pellet(self, tile_x, tile_y):
        pos = (tile_x, tile_y)
        eaten_type = None
        if pos in self.pellets:
            self.pellets.remove(pos)
            eaten_type = 'pellet'
        elif pos in self.power_pellets:
            self.power_pellets.remove(pos)
            eaten_type = 'power_pellet'
        return eaten_type # Return type of pellet eaten, or None

    def all_pellets_eaten(self):
        return not self.pellets and not self.power_pellets

    def draw(self, screen):
        # Draw Walls
        for wall_pos in self.walls:
            rect = pygame.Rect(wall_pos[0] * TILE_SIZE, wall_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, BLUE, rect)

        # Draw Pellets
        pellet_radius = TILE_SIZE // 8
        for pellet_pos in self.pellets:
            center_x = pellet_pos[0] * TILE_SIZE + TILE_SIZE // 2
            center_y = pellet_pos[1] * TILE_SIZE + TILE_SIZE // 2
            pygame.draw.circle(screen, WHITE, (center_x, center_y), pellet_radius)

        # Draw Power Pellets (larger, maybe blinking later)
        power_pellet_radius = TILE_SIZE // 4
        for pp_pos in self.power_pellets:
            center_x = pp_pos[0] * TILE_SIZE + TILE_SIZE // 2
            center_y = pp_pos[1] * TILE_SIZE + TILE_SIZE // 2
            pygame.draw.circle(screen, WHITE, (center_x, center_y), power_pellet_radius)

