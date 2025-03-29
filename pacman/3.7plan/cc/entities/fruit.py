import pygame
from entities.entity import Entity
import config

class Fruit(Entity):
    def __init__(self, x, y, maze, level):
        super().__init__(x, y, maze)
        self.level = level
        self.points = self.get_points()
        
        # For initial implementation, just use a colored circle
        self.color = config.GREEN
        self.radius = maze.tile_size // 2 - 2
    
    def get_points(self):
        """Return the point value based on the level"""
        points = [100, 300, 500, 700, 1000, 2000, 3000, 5000]
        index = min(self.level - 1, len(points) - 1)
        return points[index]
    
    def update(self, dt):
        # No movement or special behavior yet
        pass
    
    def render(self, screen, offset_x=0, offset_y=0):
        """Render the fruit"""
        center_x = int(self.x + self.maze.tile_size // 2 + offset_x)
        center_y = int(self.y + self.maze.tile_size // 2 + offset_y)
        
        pygame.draw.circle(screen, self.color, (center_x, center_y), self.radius)