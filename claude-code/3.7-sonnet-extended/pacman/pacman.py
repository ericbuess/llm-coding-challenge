import pygame
import math

class Pacman:
    def __init__(self, maze):
        self.maze = maze
        self.radius = 15
        self.color = (255, 255, 0)  # Yellow
        self.speed = 3
        self.direction = "right"
        self.next_direction = None
        self.position = self.get_starting_position()
        self.mouth_angle = 45  # For animation
        self.mouth_change = 5   # Rate of change for mouth animation
        self.mouth_opening = True  # Whether the mouth is opening or closing
    
    def get_starting_position(self):
        # Find pacman's starting position in the maze
        for y, row in enumerate(self.maze.layout):
            for x, cell in enumerate(row):
                if cell == 'P':
                    return [x * self.maze.cell_size + self.maze.cell_size // 2, 
                            y * self.maze.cell_size + self.maze.cell_size // 2]
        # Default position if not found
        return [self.maze.cell_size + self.maze.cell_size // 2, 
                self.maze.cell_size + self.maze.cell_size // 2]
    
    def reset_position(self):
        self.position = self.get_starting_position()
        self.direction = "right"
        self.next_direction = None
    
    def change_direction(self, new_direction):
        # Store the new direction for the next update
        self.next_direction = new_direction
    
    def update(self):
        # Try to change to the next direction if possible
        if self.next_direction:
            if self.can_move(self.next_direction):
                self.direction = self.next_direction
                self.next_direction = None
        
        # Move in the current direction if possible
        if self.can_move(self.direction):
            if self.direction == "up":
                self.position[1] -= self.speed
            elif self.direction == "down":
                self.position[1] += self.speed
            elif self.direction == "left":
                self.position[0] -= self.speed
            elif self.direction == "right":
                self.position[0] += self.speed
        
        # Handle tunnel teleportation
        self.handle_tunnels()
        
        # Update mouth animation
        if self.mouth_opening:
            self.mouth_angle += self.mouth_change
            if self.mouth_angle >= 45:
                self.mouth_opening = False
        else:
            self.mouth_angle -= self.mouth_change
            if self.mouth_angle <= 5:
                self.mouth_opening = True
    
    def can_move(self, direction):
        # Check if Pacman can move in the given direction
        x, y = self.get_grid_position()
        next_x, next_y = x, y
        
        # Calculate the next position based on direction
        if direction == "up":
            next_y -= 1
        elif direction == "down":
            next_y += 1
        elif direction == "left":
            next_x -= 1
        elif direction == "right":
            next_x += 1
        
        # Check if the next position is valid
        return not self.maze.is_wall(next_x, next_y)
    
    def handle_tunnels(self):
        # Check if Pacman is in a tunnel and teleport to the other side
        grid_width = len(self.maze.layout[0])
        grid_height = len(self.maze.layout)
        
        # Left tunnel
        if self.position[0] < 0:
            self.position[0] = grid_width * self.maze.cell_size - 1
        
        # Right tunnel
        elif self.position[0] > grid_width * self.maze.cell_size:
            self.position[0] = 1
        
        # Top tunnel
        if self.position[1] < 0:
            self.position[1] = grid_height * self.maze.cell_size - 1
        
        # Bottom tunnel
        elif self.position[1] > grid_height * self.maze.cell_size:
            self.position[1] = 1
    
    def get_grid_position(self):
        # Convert pixel position to grid position
        return (int(self.position[0] // self.maze.cell_size), 
                int(self.position[1] // self.maze.cell_size))
    
    def eat_dot(self):
        x, y = self.get_grid_position()
        if self.maze.is_dot(x, y):
            self.maze.eat_dot(x, y)
            return True
        return False
    
    def eat_power_pellet(self):
        x, y = self.get_grid_position()
        if self.maze.is_power_pellet(x, y):
            self.maze.eat_power_pellet(x, y)
            return True
        return False
    
    def draw(self, screen):
        # Calculate the angle for the direction Pacman is facing
        direction_angle = 0
        if self.direction == "up":
            direction_angle = 90
        elif self.direction == "down":
            direction_angle = 270
        elif self.direction == "left":
            direction_angle = 180
        
        # Draw Pacman as a circle with a mouth
        pygame.draw.circle(screen, self.color, 
                          (int(self.position[0]), int(self.position[1])), 
                          self.radius)
        
        # Draw the mouth (as a black triangle)
        mouth_points = [
            (self.position[0], self.position[1]),
            (self.position[0] + self.radius * math.cos(math.radians(direction_angle - self.mouth_angle)), 
             self.position[1] - self.radius * math.sin(math.radians(direction_angle - self.mouth_angle))),
            (self.position[0] + self.radius * math.cos(math.radians(direction_angle + self.mouth_angle)), 
             self.position[1] - self.radius * math.sin(math.radians(direction_angle + self.mouth_angle)))
        ]
        pygame.draw.polygon(screen, (0, 0, 0), mouth_points)