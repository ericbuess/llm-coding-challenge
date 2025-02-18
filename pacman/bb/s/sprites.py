import pygame
import math
from constants import *

class Pacman(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.Surface([CELL_SIZE - 4, CELL_SIZE - 4], pygame.SRCALPHA)
        self.image = self.original_image.copy()
        self.angle = 0
        self.mouth_speed = 3
        self.mouth_opening = True
        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE
        self.direction = None
        self.speed = PACMAN_SPEED
        self.next_direction = None

    def update(self, maze):
        # Update mouth animation
        if self.mouth_opening:
            self.angle += self.mouth_speed
            if self.angle >= 45:
                self.mouth_opening = False
        else:
            self.angle -= self.mouth_speed
            if self.angle <= 0:
                self.mouth_opening = True

        # Draw Pacman with current mouth angle
        self.image = self.original_image.copy()
        pygame.draw.circle(self.image, YELLOW, ((CELL_SIZE-4)//2, (CELL_SIZE-4)//2), (CELL_SIZE-4)//2)
        if self.direction:
            # Calculate mouth points
            center = ((CELL_SIZE-4)//2, (CELL_SIZE-4)//2)
            radius = (CELL_SIZE-4)//2
            start_angle = self.angle
            end_angle = 360 - self.angle
            
            # Draw mouth (clear a triangle)
            points = [center]
            points.append((center[0] + radius * math.cos(math.radians(start_angle)),
                         center[1] - radius * math.sin(math.radians(start_angle))))
            points.append((center[0] + radius * math.cos(math.radians(end_angle)),
                         center[1] - radius * math.sin(math.radians(end_angle))))
            pygame.draw.polygon(self.image, (0, 0, 0, 0), points)
            
            # Rotate Pacman based on direction
            rotation = 0
            if self.direction == UP:
                rotation = 90
            elif self.direction == DOWN:
                rotation = 270
            elif self.direction == LEFT:
                rotation = 180
            self.image = pygame.transform.rotate(self.image, rotation)
        if self.next_direction:
            # Try to change direction
            next_pos = self.get_next_position(self.next_direction)
            if not self.will_collide(next_pos, maze):
                self.direction = self.next_direction
                self.next_direction = None

        if self.direction:
            next_pos = self.get_next_position(self.direction)
            if not self.will_collide(next_pos, maze):
                self.rect.x = next_pos[0]
                self.rect.y = next_pos[1]

    def get_next_position(self, direction):
        x, y = self.rect.x, self.rect.y
        if direction == UP:
            return (x, y - self.speed)
        elif direction == DOWN:
            return (x, y + self.speed)
        elif direction == LEFT:
            return (x - self.speed, y)
        elif direction == RIGHT:
            return (x + self.speed, y)
        return (x, y)

    def will_collide(self, next_pos, maze):
        next_rect = pygame.Rect(next_pos[0], next_pos[1], CELL_SIZE, CELL_SIZE)
        return any(wall.rect.colliderect(next_rect) for wall in maze.walls)

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface([CELL_SIZE - 4, CELL_SIZE - 4], pygame.SRCALPHA)
        # Make ghosts more ghost-like with a curved top and wavy bottom
        ghost_rect = pygame.Rect(0, 0, CELL_SIZE - 4, CELL_SIZE - 4)
        pygame.draw.ellipse(self.image, color, ghost_rect)
        # Add wave pattern at bottom
        wave_height = 4
        for i in range(3):
            x = i * ((CELL_SIZE-4) // 2)
            pygame.draw.circle(self.image, color, (x, CELL_SIZE-4), wave_height)
        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE
        self.start_x = x * CELL_SIZE
        self.start_y = y * CELL_SIZE
        self.direction = RIGHT
        self.speed = GHOST_SPEED
        self.color = color
        self.vulnerable = False

    def update(self, maze, pacman):
        if not self.vulnerable:
            self.chase_pacman(maze, pacman)
        else:
            self.random_movement(maze)

    def chase_pacman(self, maze, pacman):
        # Simple chase AI - move towards Pacman
        dx = pacman.rect.x - self.rect.x
        dy = pacman.rect.y - self.rect.y
        
        if abs(dx) > abs(dy):
            if dx > 0:
                next_pos = self.get_next_position(RIGHT)
                if not self.will_collide(next_pos, maze):
                    self.direction = RIGHT
            else:
                next_pos = self.get_next_position(LEFT)
                if not self.will_collide(next_pos, maze):
                    self.direction = LEFT
        else:
            if dy > 0:
                next_pos = self.get_next_position(DOWN)
                if not self.will_collide(next_pos, maze):
                    self.direction = DOWN
            else:
                next_pos = self.get_next_position(UP)
                if not self.will_collide(next_pos, maze):
                    self.direction = UP

        next_pos = self.get_next_position(self.direction)
        if not self.will_collide(next_pos, maze):
            self.rect.x = next_pos[0]
            self.rect.y = next_pos[1]

    def random_movement(self, maze):
        # List of possible directions
        directions = [UP, DOWN, LEFT, RIGHT]
        
        # Try a random direction if current direction is blocked
        next_pos = self.get_next_position(self.direction)
        if self.will_collide(next_pos, maze):
            # Filter out directions that would lead to collision
            valid_directions = [d for d in directions if not self.will_collide(self.get_next_position(d), maze)]
            if valid_directions:
                self.direction = valid_directions[pygame.time.get_ticks() % len(valid_directions)]
        
        # Move in current direction if possible
        next_pos = self.get_next_position(self.direction)
        if not self.will_collide(next_pos, maze):
            self.rect.x = next_pos[0]
            self.rect.y = next_pos[1]

    def get_next_position(self, direction):
        x, y = self.rect.x, self.rect.y
        if direction == UP:
            return (x, y - self.speed)
        elif direction == DOWN:
            return (x, y + self.speed)
        elif direction == LEFT:
            return (x - self.speed, y)
        elif direction == RIGHT:
            return (x + self.speed, y)
        return (x, y)

    def will_collide(self, next_pos, maze):
        next_rect = pygame.Rect(next_pos[0], next_pos[1], CELL_SIZE, CELL_SIZE)
        return any(wall.rect.colliderect(next_rect) for wall in maze.walls)

    def make_vulnerable(self):
        self.vulnerable = True
        self.image.fill(BLUE)
        self.speed = GHOST_SPEED * 0.5

    def reset_vulnerability(self):
        self.vulnerable = False
        self.image.fill(self.color)
        self.speed = GHOST_SPEED

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([CELL_SIZE, CELL_SIZE])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE

class Pellet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([CELL_SIZE // 3, CELL_SIZE // 3])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x * CELL_SIZE + CELL_SIZE // 2
        self.rect.centery = y * CELL_SIZE + CELL_SIZE // 2

class PowerPellet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([CELL_SIZE // 2, CELL_SIZE // 2], pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (CELL_SIZE//4, CELL_SIZE//4), CELL_SIZE//4)
        self.rect = self.image.get_rect()
        self.rect.centerx = x * CELL_SIZE + CELL_SIZE // 2
        self.rect.centery = y * CELL_SIZE + CELL_SIZE // 2
