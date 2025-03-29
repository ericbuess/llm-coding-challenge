from entities.ghost import Ghost
import config

class Pinky(Ghost):
    def __init__(self, x, y, maze, pacman):
        super().__init__(x, y, maze, "pinky", (0, 0))  # Scatter to top-left
        self.pacman = pacman
        self.color = config.PINK  # Pink
    
    def get_chase_target(self):
        """Pinky targets 4 tiles ahead of Pac-Man's current direction"""
        px, py = self.pacman.get_grid_position()
        dx, dy = self.pacman.direction
        
        # Implement the targeting bug from the original game
        # If Pac-Man is facing up, target 4 tiles up and 4 tiles left
        if dx == 0 and dy == -1:
            return (px - 4, py - 4)
        
        # Otherwise, target 4 tiles in front of Pac-Man
        return (px + dx * 4, py + dy * 4)