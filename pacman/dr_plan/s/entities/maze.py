import pygame
from typing import List, Tuple, Set
from .pellet import Pellet
from .powerpellet import PowerPellet

class Maze:
    def __init__(self, tile_size: int = 20):
        self.tile_size = tile_size
        self.layout = self._create_default_layout()
        self.width = len(self.layout[0])
        self.height = len(self.layout)
        self.walls: Set[Tuple[int, int]] = set()
        self.pellets: List[Pellet] = []
        self.power_pellets: List[PowerPellet] = []
        self._process_layout()

    def _create_default_layout(self) -> List[str]:
        """Create a default maze layout."""
        return [
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "W............WW............W",
            "W.WWWW.WWWW.WW.WWWW.WWWW.W",
            "W*WWWW.WWWW.WW.WWWW.WWWW*W",
            "W.WWWW.WWWW.WW.WWWW.WWWW.W",
            "W..........................W",
            "W.WWWW.WW.WWWWWW.WW.WWWW.W",
            "W.WWWW.WW.WWWWWW.WW.WWWW.W",
            "W......WW....WW....WW....W",
            "WWWWWW.WWWWW WW WWWWW.WWWWW",
            "     W.WWWWW WW WWWWW.W    ",
            "     W.WW          WW.W    ",
            "     W.WW WWW--WWW WW.W    ",
            "WWWWWW.WW W      W WW.WWWWW",
            "      .   W      W   .     ",
            "WWWWWW.WW W      W WW.WWWWW",
            "     W.WW WWWWWWWW WW.W    ",
            "     W.WW          WW.W    ",
            "     W.WW WWWWWWWW WW.W    ",
            "WWWWWW.WW WWWWWWWW WW.WWWWW",
            "W............WW............W",
            "W.WWWW.WWWW.WW.WWWW.WWWW.W",
            "W.WWWW.WWWW.WW.WWWW.WWWW.W",
            "W*..WW................WW..W",
            "WWW.WW.WW.WWWWWW.WW.WW.WWW",
            "WWW.WW.WW.WWWWWW.WW.WW.WWW",
            "W......WW....WW....WW....W",
            "W.WWWWWWWWWW.WW.WWWWWWWW.W",
            "W.WWWWWWWWWW.WW.WWWWWWWW.W",
            "W..........................W",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWW"
        ]

    def _process_layout(self) -> None:
        """Process the layout to create walls and pellets."""
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                # Calculate center position for the current cell
                center_x = x * self.tile_size + self.tile_size // 2
                center_y = y * self.tile_size + self.tile_size // 2

                if cell == 'W':
                    self.walls.add((x, y))
                elif cell == '.':
                    self.pellets.append(Pellet(center_x, center_y))
                elif cell == '*':
                    self.power_pellets.append(PowerPellet(center_x, center_y))

    def check_wall_collision(self, rect: pygame.Rect) -> bool:
        """Check if a rectangle collides with any walls."""
        # Convert pixel coordinates to grid coordinates
        grid_x1 = max(0, rect.left // self.tile_size)
        grid_y1 = max(0, rect.top // self.tile_size)
        grid_x2 = min(self.width - 1, rect.right // self.tile_size)
        grid_y2 = min(self.height - 1, rect.bottom // self.tile_size)

        # Check each grid cell the rectangle might overlap
        for y in range(grid_y1, grid_y2 + 1):
            for x in range(grid_x1, grid_x2 + 1):
                if (x, y) in self.walls:
                    wall_rect = pygame.Rect(x * self.tile_size,
                                         y * self.tile_size,
                                         self.tile_size,
                                         self.tile_size)
                    if rect.colliderect(wall_rect):
                        return True
        return False

    def get_spawn_positions(self) -> dict:
        """Get spawn positions for Pac-Man and ghosts."""
        # These could be marked in the layout, but for now use fixed positions
        return {
            "pacman": (14 * self.tile_size, 23 * self.tile_size),  # Center bottom
            "ghost_house": (14 * self.tile_size, 14 * self.tile_size),  # Center
            "blinky": (14 * self.tile_size, 11 * self.tile_size),
            "pinky": (14 * self.tile_size, 14 * self.tile_size),
            "inky": (12 * self.tile_size, 14 * self.tile_size),
            "clyde": (16 * self.tile_size, 14 * self.tile_size)
        }

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the maze walls."""
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                if cell == 'W':
                    pygame.draw.rect(screen, (0, 0, 255),
                                  (x * self.tile_size,
                                   y * self.tile_size,
                                   self.tile_size,
                                   self.tile_size))

        # Draw pellets
        for pellet in self.pellets:
            pellet.draw(screen)
        
        # Draw power pellets
        for power_pellet in self.power_pellets:
            power_pellet.draw(screen)

    def update(self, dt: float) -> None:
        """Update maze elements (like power pellets animation)."""
        for power_pellet in self.power_pellets:
            power_pellet.update(dt)

    def remove_pellet(self, pellet) -> None:
        """Remove a pellet from the maze."""
        if pellet in self.pellets:
            self.pellets.remove(pellet)
        elif pellet in self.power_pellets:
            self.power_pellets.remove(pellet)

    def reset(self) -> None:
        """Reset the maze to initial state."""
        self.pellets.clear()
        self.power_pellets.clear()
        self._process_layout() 