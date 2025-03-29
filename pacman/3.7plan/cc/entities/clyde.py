from entities.ghost import Ghost
import config

class Clyde(Ghost):
    def __init__(self, x, y, maze, pacman):
        super().__init__(x, y, maze, "clyde", (0, 31))  # Scatter to bottom-left
        self.pacman = pacman
        self.color = config.ORANGE  # Orange
    
    def get_chase_target(self):
        """
        Clyde targets Pac-Man directly when far away,
        but scatters to his corner when within 8 tiles
        """
        px, py = self.pacman.get_grid_position()
        cx, cy = self.get_grid_position()
        
        # Calculate Manhattan distance to Pac-Man
        distance = abs(px - cx) + abs(py - cy)
        
        if distance < 8:
            # If close to Pac-Man, target scatter corner
            return self.scatter_target
        else:
            # If far from Pac-Man, target him directly
            return (px, py)