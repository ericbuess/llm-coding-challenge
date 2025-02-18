from pygame.math import Vector2
from entities.pellet import Pellet

class Maze:
    def __init__(self):
        self.tile_size = 20  # pixels per tile
        self.width = 28      # standard Pac-Man maze width
        self.height = 31     # standard Pac-Man maze height
        
        # Initialize empty maze with the correct dimensions
        self.layout = None  # Will be set in load_default_maze
        self.walls = set()
        self.pellets = []
        
        # Spawn positions
        self.pacman_start = Vector2(14, 23)  # Center bottom area
        self.ghost_start = Vector2(14, 11)   # Ghost house
        self.ghost_exit = Vector2(14, 11)    # Just outside ghost house
        
        # Load the default maze
        self.load_default_maze()

    def load_default_maze(self):
        """Load the classic Pac-Man maze layout"""
        # This is a simplified version of the maze layout
        # 0 = empty, 1 = wall, 2 = pellet, 3 = power pellet
        self.layout = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
            [1,3,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,3,1],
            [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
            [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
            [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
            [1,1,1,1,1,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,1,1,1,1,1],
            [1,1,1,1,1,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,1,1,1,1,1],
            [1,1,1,1,1,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,1,1,1,1,1],
            [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
            [1,1,1,1,1,1,2,1,1,0,1,0,0,0,0,0,0,1,0,1,1,2,1,1,1,1,1,1],
            [0,0,0,0,0,0,2,0,0,0,1,0,0,0,0,0,0,1,0,0,0,2,0,0,0,0,0,0],
            [1,1,1,1,1,1,2,1,1,0,1,0,0,0,0,0,0,1,0,1,1,2,1,1,1,1,1,1],
            [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
            [1,1,1,1,1,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,1,1,1,1,1],
            [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
            [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
            [1,3,2,2,1,1,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,1,1,2,2,3,1],
            [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
            [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
            [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1],
            [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]
        
        # Process the layout to create walls and pellets
        self.process_layout()

    def process_layout(self):
        """Process the layout to create walls and pellets lists"""
        self.walls.clear()
        self.pellets.clear()
        
        for y, row in enumerate(self.layout):
            for x, tile in enumerate(row):
                if tile == 1:  # Wall
                    self.walls.add((x, y))
                elif tile == 2:  # Regular pellet
                    self.pellets.append(Pellet(
                        Vector2(x * self.tile_size + self.tile_size/2,
                               y * self.tile_size + self.tile_size/2),
                        False
                    ))
                elif tile == 3:  # Power pellet
                    self.pellets.append(Pellet(
                        Vector2(x * self.tile_size + self.tile_size/2,
                               y * self.tile_size + self.tile_size/2),
                        True
                    ))

    def is_wall(self, x, y):
        """Check if given pixel coordinates contain a wall"""
        # Convert pixel coordinates to grid coordinates
        grid_x = int(x / self.tile_size)
        grid_y = int(y / self.tile_size)
        
        # Check bounds
        if grid_x < 0 or grid_x >= self.width or grid_y < 0 or grid_y >= self.height:
            return True  # Out of bounds counts as wall
            
        return (grid_x, grid_y) in self.walls

    def wrap_position(self, position):
        """Handle position wrapping (for tunnel)"""
        x, y = position.x, position.y
        
        # Wrap horizontally (tunnel)
        if x < 0:
            x = self.width * self.tile_size
        elif x > self.width * self.tile_size:
            x = 0
            
        return Vector2(x, y)

    def remove_pellet(self, pellet):
        """Remove a pellet from the maze"""
        if pellet in self.pellets:
            self.pellets.remove(pellet)

    def reset(self):
        """Reset the maze to initial state"""
        self.load_default_maze()
