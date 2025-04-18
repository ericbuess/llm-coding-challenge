import pygame
import math
import random

class Ghost:
    def __init__(self, maze, color, behavior):
        self.maze = maze
        self.color = color
        self.radius = 15
        self.speed = 2
        self.behavior = behavior  # "chase", "ambush", "random", "patrol"
        self.position = self.get_starting_position()
        self.direction = random.choice(["up", "down", "left", "right"])
        self.frightened = False
        self.frightened_timer = 0
        self.frightened_duration = 400  # About 7 seconds at 60 fps
        self.target_tile = None
        self.patrol_points = self.generate_patrol_points()
        self.current_patrol_index = 0
    
    def get_starting_position(self):
        # Find ghost's starting position in the maze
        for y, row in enumerate(self.maze.layout):
            for x, cell in enumerate(row):
                if cell == 'G':
                    return [x * self.maze.cell_size + self.maze.cell_size // 2, 
                            y * self.maze.cell_size + self.maze.cell_size // 2]
        # Default position if not found
        return [self.maze.cell_size * 10 + self.maze.cell_size // 2, 
                self.maze.cell_size * 10 + self.maze.cell_size // 2]
    
    def reset_position(self):
        self.position = self.get_starting_position()
        self.direction = random.choice(["up", "down", "left", "right"])
        self.frightened = False
        self.frightened_timer = 0
    
    def set_frightened(self):
        self.frightened = True
        self.frightened_timer = self.frightened_duration
        # Reverse direction when frightened
        if self.direction == "up":
            self.direction = "down"
        elif self.direction == "down":
            self.direction = "up"
        elif self.direction == "left":
            self.direction = "right"
        elif self.direction == "right":
            self.direction = "left"
    
    def is_frightened(self):
        return self.frightened
    
    def generate_patrol_points(self):
        # Generate 4 patrol points at corners of the maze
        width = len(self.maze.layout[0])
        height = len(self.maze.layout)
        points = [
            (1, 1),  # Top-left
            (width - 2, 1),  # Top-right
            (width - 2, height - 2),  # Bottom-right
            (1, height - 2)  # Bottom-left
        ]
        return points
    
    def increase_speed(self, level):
        # Increase ghost speed with level
        self.speed = 2 + level * 0.1
    
    def update(self, pacman):
        # Handle frightened state
        if self.frightened:
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                self.frightened = False
        
        # Move the ghost
        self.move(pacman)
    
    def move(self, pacman):
        # Ghost movement depends on behavior and frightened state
        if self.frightened:
            self.random_move()
        else:
            if self.behavior == "chase":
                self.chase_move(pacman)
            elif self.behavior == "ambush":
                self.ambush_move(pacman)
            elif self.behavior == "random":
                self.random_move()
            elif self.behavior == "patrol":
                self.patrol_move()
    
    def chase_move(self, pacman):
        # Chase directly toward Pacman
        pacman_grid = pacman.get_grid_position()
        self.target_tile = pacman_grid
        self.move_toward_target()
    
    def ambush_move(self, pacman):
        # Try to cut off Pacman by targeting a position ahead of him
        pacman_grid = pacman.get_grid_position()
        pacman_direction = pacman.direction
        
        # Calculate a position 4 tiles ahead of Pacman
        target_x, target_y = pacman_grid
        if pacman_direction == "up":
            target_y -= 4
        elif pacman_direction == "down":
            target_y += 4
        elif pacman_direction == "left":
            target_x -= 4
        elif pacman_direction == "right":
            target_x += 4
        
        self.target_tile = (target_x, target_y)
        self.move_toward_target()
    
    def random_move(self):
        # Only choose a new direction at intersections or when blocked
        if not self.can_move(self.direction) or self.at_intersection():
            available_directions = []
            for direction in ["up", "down", "left", "right"]:
                if self.can_move(direction):
                    available_directions.append(direction)
            
            # Don't turn around unless necessary
            opposite = self.get_opposite_direction(self.direction)
            if len(available_directions) > 1 and opposite in available_directions:
                available_directions.remove(opposite)
            
            if available_directions:
                self.direction = random.choice(available_directions)
        
        # Move in the current direction
        self.move_in_direction()
    
    def patrol_move(self):
        # Move toward the current patrol point
        patrol_point = self.patrol_points[self.current_patrol_index]
        self.target_tile = patrol_point
        
        # If close to the patrol point, move to the next one
        ghost_grid = self.get_grid_position()
        if abs(ghost_grid[0] - patrol_point[0]) <= 1 and abs(ghost_grid[1] - patrol_point[1]) <= 1:
            self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)
        
        self.move_toward_target()
    
    def move_toward_target(self):
        if not self.target_tile:
            self.random_move()
            return
        
        # Only choose a new direction at intersections or when blocked
        if not self.can_move(self.direction) or self.at_intersection():
            ghost_grid = self.get_grid_position()
            
            # Calculate the distance to the target for each direction
            distances = {}
            for direction in ["up", "down", "left", "right"]:
                if self.can_move(direction):
                    next_pos = self.get_next_position(direction)
                    distance = self.calculate_distance(next_pos, self.target_tile)
                    distances[direction] = distance
            
            # Don't turn around unless necessary
            opposite = self.get_opposite_direction(self.direction)
            if len(distances) > 1 and opposite in distances:
                del distances[opposite]
            
            # Choose the direction with the shortest distance
            if distances:
                self.direction = min(distances, key=distances.get)
        
        # Move in the current direction
        self.move_in_direction()
    
    def move_in_direction(self):
        # Actual movement in the current direction
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
    
    def can_move(self, direction):
        # Check if the ghost can move in the given direction
        x, y = self.get_grid_position()
        next_x, next_y = x, y
        
        if direction == "up":
            next_y -= 1
        elif direction == "down":
            next_y += 1
        elif direction == "left":
            next_x -= 1
        elif direction == "right":
            next_x += 1
        
        return not self.maze.is_wall(next_x, next_y)
    
    def at_intersection(self):
        # Check if the ghost is at an intersection (more than 2 possible directions)
        possible_directions = 0
        for direction in ["up", "down", "left", "right"]:
            if self.can_move(direction):
                possible_directions += 1
        
        return possible_directions > 2
    
    def get_opposite_direction(self, direction):
        if direction == "up":
            return "down"
        elif direction == "down":
            return "up"
        elif direction == "left":
            return "right"
        elif direction == "right":
            return "left"
        return direction
    
    def get_next_position(self, direction):
        x, y = self.get_grid_position()
        if direction == "up":
            y -= 1
        elif direction == "down":
            y += 1
        elif direction == "left":
            x -= 1
        elif direction == "right":
            x += 1
        return (x, y)
    
    def calculate_distance(self, pos1, pos2):
        # Manhattan distance
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def handle_tunnels(self):
        # Check if the ghost is in a tunnel and teleport to the other side
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
    
    def collides_with(self, pacman):
        # Check if the ghost collides with Pacman
        distance = math.sqrt((self.position[0] - pacman.position[0]) ** 2 + 
                            (self.position[1] - pacman.position[1]) ** 2)
        return distance < self.radius + pacman.radius
    
    def draw(self, screen):
        # Draw the ghost
        if self.frightened:
            # Flashing blue/white during frightened mode
            if self.frightened_timer < 100 and self.frightened_timer % 20 < 10:
                ghost_color = (255, 255, 255)  # White
            else:
                ghost_color = (0, 0, 255)  # Blue
        else:
            ghost_color = self.color
        
        # Draw the main body (circle for now)
        pygame.draw.circle(screen, ghost_color, 
                         (int(self.position[0]), int(self.position[1])), 
                         self.radius)
        
        # Draw the bottom part (skirt)
        bottom_rect = pygame.Rect(self.position[0] - self.radius, 
                                 self.position[1], 
                                 self.radius * 2, 
                                 self.radius)
        pygame.draw.rect(screen, ghost_color, bottom_rect)
        
        # Draw eyes
        eye_radius = 4
        eye_offset = 6
        
        # White of the eyes
        pygame.draw.circle(screen, (255, 255, 255), 
                         (int(self.position[0] - eye_offset), int(self.position[1] - 2)), 
                         eye_radius)
        pygame.draw.circle(screen, (255, 255, 255), 
                         (int(self.position[0] + eye_offset), int(self.position[1] - 2)), 
                         eye_radius)
        
        # Pupils (looking in the direction of movement)
        pupil_offset = 2
        pupil_x1, pupil_y1 = self.position[0] - eye_offset, self.position[1] - 2
        pupil_x2, pupil_y2 = self.position[0] + eye_offset, self.position[1] - 2
        
        if self.direction == "up":
            pupil_y1 -= pupil_offset
            pupil_y2 -= pupil_offset
        elif self.direction == "down":
            pupil_y1 += pupil_offset
            pupil_y2 += pupil_offset
        elif self.direction == "left":
            pupil_x1 -= pupil_offset
            pupil_x2 -= pupil_offset
        elif self.direction == "right":
            pupil_x1 += pupil_offset
            pupil_x2 += pupil_offset
        
        pygame.draw.circle(screen, (0, 0, 0), 
                         (int(pupil_x1), int(pupil_y1)), 
                         eye_radius // 2)
        pygame.draw.circle(screen, (0, 0, 0), 
                         (int(pupil_x2), int(pupil_y2)), 
                         eye_radius // 2)