from entities.ghost import Ghost
import config

class Inky(Ghost):
    def __init__(self, x, y, maze, pacman, blinky):
        super().__init__(x, y, maze, "inky", (27, 31))  # Scatter to bottom-right
        self.pacman = pacman
        self.blinky = blinky
        self.color = config.CYAN  # Cyan
    
    def get_chase_target(self):
        """
        Inky uses a two-step process:
        1. Find the position 2 tiles in front of Pac-Man
        2. Draw a vector from Blinky to this position, then double it
        """
        px, py = self.pacman.get_grid_position()
        dx, dy = self.pacman.direction
        
        # Get position 2 tiles in front of Pac-Man
        # With the same bug as Pinky's targeting
        if dx == 0 and dy == -1:
            intermediate_x, intermediate_y = px - 2, py - 2
        else:
            intermediate_x, intermediate_y = px + dx * 2, py + dy * 2
        
        # Get Blinky's position
        bx, by = self.blinky.get_grid_position()
        
        # Calculate vector from Blinky to intermediate position and double it
        target_x = 2 * intermediate_x - bx
        target_y = 2 * intermediate_y - by
        
        return (target_x, target_y)