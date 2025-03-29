from entities.ghost import Ghost
import config

class Blinky(Ghost):
    def __init__(self, x, y, maze, pacman):
        super().__init__(x, y, maze, "blinky", (27, 0))  # Scatter to top-right
        self.pacman = pacman
        self.color = config.RED  # Red
    
    def get_chase_target(self):
        """Blinky targets Pac-Man's current position directly"""
        return self.pacman.get_grid_position()