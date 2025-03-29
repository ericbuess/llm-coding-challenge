class Entity:
    def __init__(self, x, y, maze):
        self.x = x
        self.y = y
        self.maze = maze
        self.direction = (0, 0)  # (dx, dy)
        self.speed = 1.0
        self.animation_frame = 0
        self.sprite = None
    
    def update(self, dt):
        # Base update method
        pass
    
    def render(self, screen, offset_x=0, offset_y=0):
        # Base render method
        pass
    
    def get_position(self):
        return (self.x, self.y)
    
    def get_grid_position(self):
        """Convert pixel position to grid position"""
        tile_size = self.maze.tile_size
        return (int(self.x // tile_size), int(self.y // tile_size))
    
    def can_move(self, dx, dy):
        """Check if movement in direction (dx, dy) is possible"""
        tile_size = self.maze.tile_size
        next_x = self.x + dx
        next_y = self.y + dy
        
        # Check each corner of the entity's bounding box
        corners = [
            (next_x, next_y),
            (next_x + tile_size - 1, next_y),
            (next_x, next_y + tile_size - 1),
            (next_x + tile_size - 1, next_y + tile_size - 1)
        ]
        
        for corner_x, corner_y in corners:
            grid_x = int(corner_x // tile_size)
            grid_y = int(corner_y // tile_size)
            if self.maze.is_wall(grid_x, grid_y):
                return False
        
        return True