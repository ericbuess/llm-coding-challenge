import pygame
import math
from constants import *

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tile_x = x // TILE_SIZE
        self.tile_y = y // TILE_SIZE
        self.direction = None
        self.next_direction = None
        self.speed = 0
        
    def get_center(self):
        return (self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2)
    
    def update_tile_position(self):
        self.tile_x = int((self.x + TILE_SIZE // 2) / TILE_SIZE)
        self.tile_y = int((self.y + TILE_SIZE // 2) / TILE_SIZE)

class Pacman(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = PACMAN_SPEED
        self.lives = LIVES
        self.score = 0
        self.mouth_open = True
        self.animation_counter = 0
        
    def update(self, maze):
        # Animation
        self.animation_counter += 1
        if self.animation_counter % 5 == 0:
            self.mouth_open = not self.mouth_open
            
        # Movement
        if self.next_direction is not None:
            if self.can_move(self.next_direction, maze):
                self.direction = self.next_direction
                self.next_direction = None
                
        if self.direction is not None and self.can_move(self.direction, maze):
            if self.direction == UP:
                self.y -= self.speed
            elif self.direction == DOWN:
                self.y += self.speed
            elif self.direction == LEFT:
                self.x -= self.speed
            elif self.direction == RIGHT:
                self.x += self.speed
                
        self.update_tile_position()
        
    def can_move(self, direction, maze):
        next_x, next_y = self.x, self.y
        
        if direction == UP:
            next_y -= self.speed
        elif direction == DOWN:
            next_y += self.speed
        elif direction == LEFT:
            next_x -= self.speed
        elif direction == RIGHT:
            next_x += self.speed
            
        # Check corners
        corners = [
            (next_x, next_y),
            (next_x + TILE_SIZE - 1, next_y),
            (next_x, next_y + TILE_SIZE - 1),
            (next_x + TILE_SIZE - 1, next_y + TILE_SIZE - 1)
        ]
        
        for cx, cy in corners:
            tile_x = cx // TILE_SIZE
            tile_y = cy // TILE_SIZE
            
            if tile_x < 0 or tile_x >= MAZE_WIDTH or tile_y < 0 or tile_y >= MAZE_HEIGHT:
                return False
                
            if maze[tile_y][tile_x] == '#':
                return False
                
        return True
        
    def draw(self, screen):
        if self.mouth_open:
            # Draw Pacman with mouth open
            angle_offset = 0
            if self.direction == UP:
                angle_offset = 90
            elif self.direction == DOWN:
                angle_offset = 270
            elif self.direction == LEFT:
                angle_offset = 180
            elif self.direction == RIGHT:
                angle_offset = 0
                
            points = []
            center_x = self.x + TILE_SIZE // 2
            center_y = self.y + TILE_SIZE // 2
            radius = TILE_SIZE // 2 - 2
            
            # Create pie shape
            for angle in range(30, 330):
                rad = math.radians(angle + angle_offset)
                px = center_x + radius * math.cos(rad)
                py = center_y - radius * math.sin(rad)
                points.append((px, py))
            points.append((center_x, center_y))
            
            pygame.draw.polygon(screen, YELLOW, points)
        else:
            # Draw full circle
            pygame.draw.circle(screen, YELLOW, 
                             (self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2), 
                             TILE_SIZE // 2 - 2)

class Ghost(Entity):
    def __init__(self, x, y, color, name):
        super().__init__(x, y)
        self.color = color
        self.name = name
        self.speed = GHOST_SPEED
        self.state = SCATTER
        self.frightened_timer = 0
        self.home_x = x
        self.home_y = y
        self.scatter_target = None
        self.release_timer = 0
        self.in_house = True
        
    def update(self, pacman, maze, blinky=None):
        # Update frightened timer
        if self.state == FRIGHTENED:
            self.frightened_timer -= 1000 / FPS
            if self.frightened_timer <= 0:
                self.state = CHASE
                self.speed = GHOST_SPEED
                
        # Release from ghost house
        if self.in_house:
            self.release_timer += 1
            if self.release_timer > 60:  # 1 second at 60 FPS
                self.in_house = False
                self.y -= TILE_SIZE * 3
                
        if not self.in_house:
            # Get target based on state and ghost type
            target = self.get_target(pacman, blinky)
            
            # Simple pathfinding - move towards target
            self.move_towards_target(target, maze)
            
        self.update_tile_position()
        
    def get_target(self, pacman, blinky):
        if self.state == FRIGHTENED:
            # Random movement when frightened
            return (self.tile_x, self.tile_y)
        elif self.state == SCATTER:
            return self.scatter_target
        else:  # CHASE
            if self.name == "Blinky":
                # Red ghost - targets Pacman directly
                return (pacman.tile_x, pacman.tile_y)
            elif self.name == "Pinky":
                # Pink ghost - targets 4 tiles ahead of Pacman
                target_x, target_y = pacman.tile_x, pacman.tile_y
                if pacman.direction == UP:
                    target_y -= 4
                elif pacman.direction == DOWN:
                    target_y += 4
                elif pacman.direction == LEFT:
                    target_x -= 4
                elif pacman.direction == RIGHT:
                    target_x += 4
                return (target_x, target_y)
            elif self.name == "Inky" and blinky:
                # Cyan ghost - complex targeting
                pivot_x, pivot_y = pacman.tile_x, pacman.tile_y
                if pacman.direction == UP:
                    pivot_y -= 2
                elif pacman.direction == DOWN:
                    pivot_y += 2
                elif pacman.direction == LEFT:
                    pivot_x -= 2
                elif pacman.direction == RIGHT:
                    pivot_x += 2
                    
                target_x = 2 * pivot_x - blinky.tile_x
                target_y = 2 * pivot_y - blinky.tile_y
                return (target_x, target_y)
            elif self.name == "Clyde":
                # Orange ghost - targets Pacman when far, scatters when close
                distance = math.sqrt((pacman.tile_x - self.tile_x)**2 + 
                                   (pacman.tile_y - self.tile_y)**2)
                if distance > 8:
                    return (pacman.tile_x, pacman.tile_y)
                else:
                    return self.scatter_target
                    
        return (pacman.tile_x, pacman.tile_y)
        
    def move_towards_target(self, target, maze):
        # Simple movement towards target
        dx = target[0] * TILE_SIZE - self.x
        dy = target[1] * TILE_SIZE - self.y
        
        # Normalize and apply speed
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            dx = dx / distance * self.speed
            dy = dy / distance * self.speed
            
            # Try to move
            next_x = self.x + dx
            next_y = self.y + dy
            
            # Check collision
            if self.can_move_to(next_x, next_y, maze):
                self.x = next_x
                self.y = next_y
                
    def can_move_to(self, x, y, maze):
        # Check corners
        corners = [
            (x, y),
            (x + TILE_SIZE - 1, y),
            (x, y + TILE_SIZE - 1),
            (x + TILE_SIZE - 1, y + TILE_SIZE - 1)
        ]
        
        for cx, cy in corners:
            tile_x = int(cx // TILE_SIZE)
            tile_y = int(cy // TILE_SIZE)
            
            if tile_x < 0 or tile_x >= MAZE_WIDTH or tile_y < 0 or tile_y >= MAZE_HEIGHT:
                return False
                
            if maze[tile_y][tile_x] == '#':
                return False
                
        return True
        
    def make_frightened(self):
        if self.state != EATEN:
            self.state = FRIGHTENED
            self.speed = FRIGHTENED_SPEED
            self.frightened_timer = FRIGHTENED_DURATION
            
    def draw(self, screen):
        if self.state == FRIGHTENED:
            color = BLUE if self.frightened_timer > 2000 else WHITE
        else:
            color = self.color
            
        # Ghost body
        pygame.draw.circle(screen, color,
                         (self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2),
                         TILE_SIZE // 2 - 2)
        pygame.draw.rect(screen, color,
                        (self.x + 2, self.y + TILE_SIZE // 2,
                         TILE_SIZE - 4, TILE_SIZE // 2 - 2))
                         
        # Eyes
        if self.state != FRIGHTENED:
            eye_y = self.y + TILE_SIZE // 3
            pygame.draw.circle(screen, WHITE, (self.x + 7, eye_y), 3)
            pygame.draw.circle(screen, WHITE, (self.x + TILE_SIZE - 7, eye_y), 3)
            pygame.draw.circle(screen, BLACK, (self.x + 7, eye_y), 1)
            pygame.draw.circle(screen, BLACK, (self.x + TILE_SIZE - 7, eye_y), 1)

class Pellet:
    def __init__(self, x, y, is_power=False):
        self.x = x
        self.y = y
        self.is_power = is_power
        self.eaten = False
        
    def draw(self, screen):
        if not self.eaten:
            if self.is_power:
                pygame.draw.circle(screen, WHITE,
                                 (self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2),
                                 TILE_SIZE // 4)
            else:
                pygame.draw.circle(screen, WHITE,
                                 (self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2),
                                 2)