import pygame
from settings import TILE_SIZE
from entities.wall import Wall
from entities.pellet import Pellet
from entities.powerpellet import PowerPellet
from entities.pacman import Pacman
from entities.ghost import Ghost

class Level:
    def __init__(self, game):
        self.game = game
        # Example level layout as a list of strings
        # '#' = wall, '.' = pellet, 'O' = power pellet
        # 'P' = pacman start, 'R' = red ghost, 'B' = blue ghost
        # 'K' = pink ghost, 'O' = orange ghost
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
            "     #.##    B     ##.#     ",
            "######.## ###--### ##.######",
            "      .   #RPKO#   .       ",
            "######.## ######## ##.######",
            "     #.##          ##.#     ",
            "     #.## ######## ##.#     ",
            "     #.## ######## ##.#     ",
            "######.## ######## ##.######",
            "#............##............#",
            "#.####.#####.##.#####.####.#",
            "#O..##................##..O#",
            "###.##.##.########.##.##.###",
            "#......##....##....##......#",
            "#.##########.##.##########.#",
            "#..........................#",
            "############################"
        ]
        
        # Store entity positions for reset
        self.pacman_start = None
        self.ghost_starts = {
            'red': None,
            'pink': None,
            'blue': None,
            'orange': None
        }
        
    def load(self):
        """Load the level layout and create all game entities."""
        for row_index, row in enumerate(self.layout):
            for col_index, char in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                
                if char == '#':
                    wall = Wall(x, y)
                    self.game.wall_group.add(wall)
                    self.game.all_sprites.add(wall)
                elif char == '.':
                    pellet = Pellet(x, y)
                    self.game.pellet_group.add(pellet)
                    self.game.all_sprites.add(pellet)
                elif char == 'O':
                    power = PowerPellet(x, y)
                    self.game.powerpellet_group.add(power)
                    self.game.all_sprites.add(power)
                elif char == 'P':
                    self.pacman_start = (x, y)
                    pacman = Pacman(x, y)
                    self.game.pacman_group.add(pacman)
                    self.game.all_sprites.add(pacman)
                    self.game.pacman = pacman
                elif char in ['R', 'B', 'K', 'O']:
                    ghost_color = self._get_ghost_color(char)
                    self.ghost_starts[ghost_color] = (x, y)
                    ghost = Ghost(x, y, ghost_color)
                    self.game.ghost_group.add(ghost)
                    self.game.all_sprites.add(ghost)
                    
    def reset_positions(self):
        """Reset all movable entities to their starting positions."""
        if self.pacman_start and self.game.pacman:
            self.game.pacman.set_position(*self.pacman_start)
            self.game.pacman.direction = pygame.Vector2(0, 0)
            self.game.pacman.stored_direction = None
            
        for ghost in self.game.ghost_group:
            if self.ghost_starts[ghost.color]:
                ghost.set_position(*self.ghost_starts[ghost.color])
                ghost.direction = pygame.Vector2(0, 0)
                ghost.state = 'scatter'
                ghost._draw_ghost(ghost.base_color)
                
    def _get_ghost_color(self, char):
        """Convert character to ghost color."""
        colors = {
            'R': 'red',
            'B': 'blue',
            'K': 'pink',
            'O': 'orange'
        }
        return colors.get(char, 'red')
        
    def get_pellet_count(self):
        """Return the total number of pellets and power pellets remaining."""
        return len(self.game.pellet_group) + len(self.game.powerpellet_group) 