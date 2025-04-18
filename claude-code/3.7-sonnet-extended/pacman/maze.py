import pygame

class Maze:
    def __init__(self):
        self.cell_size = 20  # Reduced cell size for better fit
        self.wall_color = (0, 0, 255)  # Blue
        self.dot_color = (255, 255, 255)  # White
        self.power_pellet_color = (255, 255, 255)  # White
        self.dot_radius = 2
        self.power_pellet_radius = 6
        self.layout = self.generate_maze()
        self.original_layout = [row[:] for row in self.layout]  # Deep copy for reset
        # Calculate maze dimensions for the game
        self.width = len(self.layout[0]) * self.cell_size
        self.height = len(self.layout) * self.cell_size
        
    def generate_maze(self):
        # 1 = wall, 0 = empty space, . = dot, o = power pellet, P = Pacman start, G = Ghost start
        # Make sure all rows are the same length
        return [
            "1111111111111111111111111111",
            "1............11............1",
            "1.1111.11111.11.11111.1111.1",
            "1o1111.11111.11.11111.1111o1",
            "1.1111.11111.11.11111.1111.1",
            "1..........................1",
            "1.1111.11.11111111.11.1111.1",
            "1.1111.11.11111111.11.1111.1",
            "1......11....11....11......1",
            "111111.11111.11.11111.111111",
            "111111.11111.11.11111.111111",
            "111111.11..........11.111111",
            "111111.11.111GG111.11.111111",
            "111111.11.1      1.11.111111",
            "000000....1      1....000000",
            "111111.11.1      1.11.111111",
            "111111.11.11111111.11.111111",
            "111111.11..........11.111111",
            "111111.11.11111111.11.111111",
            "111111.11.11111111.11.111111",
            "1............11............1",
            "1.1111.11111.11.11111.1111.1",
            "1.1111.11111.11.11111.1111.1",
            "1o..11................11..o1",
            "111.11.11.11111111.11.11.111",
            "111.11.11.11111111.11.11.111",
            "1......11....P.....11......1",
            "1.1111111111.11.1111111111.1",
            "1.1111111111.11.1111111111.1",
            "1..........................1",
            "1111111111111111111111111111"
        ]
    
    def is_wall(self, x, y):
        # Check if a given grid position is a wall
        if x < 0 or y < 0 or y >= len(self.layout) or x >= len(self.layout[0]):
            return False  # Allow movement through tunnels
        
        return self.layout[y][x] == '1'
    
    def is_dot(self, x, y):
        # Check if a given grid position has a dot
        if 0 <= y < len(self.layout) and 0 <= x < len(self.layout[0]):
            return self.layout[y][x] == '.'
        return False
    
    def is_power_pellet(self, x, y):
        # Check if a given grid position has a power pellet
        if 0 <= y < len(self.layout) and 0 <= x < len(self.layout[0]):
            return self.layout[y][x] == 'o'
        return False
    
    def eat_dot(self, x, y):
        # Remove a dot from the maze
        if self.is_dot(x, y):
            self.layout[y] = self.layout[y][:x] + ' ' + self.layout[y][x+1:]
    
    def eat_power_pellet(self, x, y):
        # Remove a power pellet from the maze
        if self.is_power_pellet(x, y):
            self.layout[y] = self.layout[y][:x] + ' ' + self.layout[y][x+1:]
    
    def dots_remaining(self):
        # Count how many dots are left in the maze
        dot_count = 0
        for row in self.layout:
            dot_count += row.count('.') + row.count('o')
        return dot_count
    
    def reset_dots(self):
        # Reset all dots and power pellets
        self.layout = [row[:] for row in self.original_layout]
    
    def draw(self, screen):
        # Draw the maze
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                # Calculate the position for this cell
                pos_x = x * self.cell_size
                pos_y = y * self.cell_size
                
                # Draw walls
                if cell == '1':
                    pygame.draw.rect(screen, self.wall_color, 
                                   (pos_x, pos_y, self.cell_size, self.cell_size))
                
                # Draw dots
                elif cell == '.':
                    pygame.draw.circle(screen, self.dot_color, 
                                     (pos_x + self.cell_size // 2, pos_y + self.cell_size // 2), 
                                     self.dot_radius)
                
                # Draw power pellets
                elif cell == 'o':
                    pygame.draw.circle(screen, self.power_pellet_color, 
                                     (pos_x + self.cell_size // 2, pos_y + self.cell_size // 2), 
                                     self.power_pellet_radius)