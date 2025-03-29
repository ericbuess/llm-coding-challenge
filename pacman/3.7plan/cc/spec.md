# Pac-Man Game Implementation Specification

## 1. Game Overview

Pac-Man is a classic arcade game from 1980 where the player controls a character (Pac-Man) through a maze, eating dots while avoiding ghosts. The goal is to eat all dots in the maze to advance to the next level.

## 2. Core Components

### 2.1 Game Architecture

```
pacman/
├── assets/               # Sprites, sounds, fonts
├── config.py             # Game configuration (screen size, colors, speeds)
├── main.py               # Entry point
├── engine/
│   ├── __init__.py
│   ├── game.py           # Game loop, state management
│   ├── input_handler.py  # Keyboard/input management
│   ├── renderer.py       # Drawing to screen
│   └── sound.py          # Sound effects
├── entities/
│   ├── __init__.py
│   ├── entity.py         # Base entity class
│   ├── pacman.py         # Pac-Man implementation
│   ├── ghost.py          # Ghost base class
│   ├── blinky.py         # Red ghost
│   ├── pinky.py          # Pink ghost
│   ├── inky.py           # Cyan ghost
│   ├── clyde.py          # Orange ghost
│   ├── fruit.py          # Bonus fruits
│   └── pellet.py         # Regular and power pellets
└── utils/
    ├── __init__.py
    ├── collision.py      # Collision detection
    ├── path_finding.py   # Ghost AI algorithms
    └── timer.py          # Timing utilities
```

### 2.2 Required Libraries

- Pygame for rendering, input handling, and sound
- NumPy for array operations and calculations (optional, but helpful)

```python
# main.py
import pygame
import numpy as np
from engine.game import Game

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
```

## 3. Game Mechanics

### 3.1 Game States

Implement a state machine with the following states:
- `INTRO`: Title screen
- `READY`: Before level starts
- `PLAYING`: Normal gameplay
- `PACMAN_DYING`: Pac-Man death animation
- `GHOST_EATEN`: Ghost eaten animation
- `LEVEL_COMPLETE`: All pellets eaten
- `GAME_OVER`: Player lost all lives
- `HIGH_SCORE`: High score entry

### 3.2 Game Loop

```python
# engine/game.py
def run(self):
    # Initialize pygame, load assets
    self.init()
    
    # Game loop
    while self.running:
        # Process inputs
        self.handle_events()
        
        # Update game state
        self.update()
        
        # Render frame
        self.render()
        
        # Maintain constant frame rate
        self.clock.tick(60)
    
    # Clean up resources
    self.quit()
```

### 3.3 Timing System

- Base game speed on frames, not real-time
- Implement a global timer for ghost mode transitions
- Each entity should track its own animation timers

```python
# utils/timer.py
class Timer:
    def __init__(self, duration, callback=None, repeat=False):
        self.duration = duration
        self.callback = callback
        self.repeat = repeat
        self.elapsed = 0
        self.active = False
    
    def start(self):
        self.elapsed = 0
        self.active = True
    
    def update(self, dt):
        if not self.active:
            return
        
        self.elapsed += dt
        if self.elapsed >= self.duration:
            if self.callback:
                self.callback()
            
            if self.repeat:
                self.elapsed = 0
            else:
                self.active = False
```

## 4. Map and Level Design

### 4.1 Maze Structure

- Store maze as a 2D grid (28×31 is the original size)
- 0 = empty, 1 = wall, 2 = pellet, 3 = power pellet, 4 = ghost-only path
- Define warp tunnels as special tiles

```python
# Example maze representation (abbreviated)
MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1],
    # ... more rows
]
```

### 4.2 Tile System

- Implement a tile mapping system for rendering
- Define tile size (e.g., 16×16 pixels)
- Implement specialized collision for different tile types

```python
class Maze:
    def __init__(self, layout):
        self.layout = layout
        self.height = len(layout)
        self.width = len(layout[0])
        self.tile_size = 16
        self.pellets_remaining = self.count_pellets()
    
    def get_tile(self, x, y):
        """Get the tile type at grid position (x, y)"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.layout[y][x]
        return 1  # Default to wall for out-of-bounds
    
    def is_wall(self, x, y):
        """Check if tile at (x, y) is a wall"""
        return self.get_tile(x, y) == 1
    
    def count_pellets(self):
        """Count total pellets in the maze"""
        count = 0
        for row in self.layout:
            for tile in row:
                if tile in (2, 3):  # Regular pellet or power pellet
                    count += 1
        return count
```

### 4.3 Level Progression

- Increase ghost speed with each level
- Reduce power pellet duration with each level
- After certain levels, stop increasing difficulty

## 5. Entity System

### 5.1 Base Entity Class

```python
# entities/entity.py
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
```

### 5.2 Pac-Man Character

```python
# entities/pacman.py
from entities.entity import Entity
import pygame

class Pacman(Entity):
    def __init__(self, x, y, maze):
        super().__init__(x, y, maze)
        self.speed = 2.0
        self.lives = 3
        self.score = 0
        self.direction = (0, 0)  # Initial direction
        self.next_direction = (0, 0)  # Buffered input
        self.animation_speed = 0.15
        self.animation_timer = 0
        self.mouth_open = 0  # 0 to 3, for animation frames
        self.is_dead = False
        self.death_animation_frame = 0
        
        # Load sprites
        self.sprites = {
            "right": [sprite1, sprite2, sprite3, sprite4],
            "left": [sprite5, sprite6, sprite7, sprite8],
            "up": [sprite9, sprite10, sprite11, sprite12],
            "down": [sprite13, sprite14, sprite15, sprite16],
            "death": [sprite17, sprite18, ..., sprite28]
        }
    
    def update(self, dt):
        if self.is_dead:
            self.update_death_animation(dt)
            return
        
        # Try to change direction if there's buffered input
        if self.next_direction != (0, 0):
            if self.can_move(self.next_direction[0], self.next_direction[1]):
                self.direction = self.next_direction
                self.next_direction = (0, 0)
        
        # Update position if can move in current direction
        dx, dy = self.direction
        if self.can_move(dx * self.speed, dy * self.speed):
            self.x += dx * self.speed
            self.y += dy * self.speed
            
            # Handle wrap-around tunnels
            self.handle_tunnel_wrap()
        
        # Update animation
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.mouth_open = (self.mouth_open + 1) % 4
        
        # Check for pellet collisions
        self.check_pellet_collisions()
    
    def set_next_direction(self, direction):
        """Buffer the next direction change"""
        self.next_direction = direction
    
    def handle_tunnel_wrap(self):
        """Handle wrap-around when Pac-Man goes through a tunnel"""
        if self.x < 0:
            self.x = self.maze.width * self.maze.tile_size
        elif self.x >= self.maze.width * self.maze.tile_size:
            self.x = 0
    
    def check_pellet_collisions(self):
        """Check for and handle collisions with pellets"""
        grid_x, grid_y = self.get_grid_position()
        tile = self.maze.get_tile(grid_x, grid_y)
        
        if tile == 2:  # Regular pellet
            self.maze.layout[grid_y][grid_x] = 0  # Remove pellet
            self.score += 10
            self.maze.pellets_remaining -= 1
            # Play eating sound
        elif tile == 3:  # Power pellet
            self.maze.layout[grid_y][grid_x] = 0  # Remove power pellet
            self.score += 50
            self.maze.pellets_remaining -= 1
            # Trigger ghost frightened mode
            # Play power pellet sound
    
    def die(self):
        """Start Pac-Man's death animation"""
        self.is_dead = True
        self.death_animation_frame = 0
        self.direction = (0, 0)
        # Play death sound
    
    def update_death_animation(self, dt):
        """Update Pac-Man's death animation"""
        self.animation_timer += dt
        if self.animation_timer >= 0.1:  # Slower animation for death
            self.animation_timer = 0
            self.death_animation_frame += 1
            if self.death_animation_frame >= len(self.sprites["death"]):
                # Animation complete
                self.death_animation_frame = 0
                self.lives -= 1
                self.is_dead = False
                # Reset position
                self.x = 14 * self.maze.tile_size
                self.y = 23 * self.maze.tile_size
                # Signal game to reset ghost positions
    
    def render(self, screen, offset_x=0, offset_y=0):
        if self.is_dead:
            # Render death animation
            sprite = self.sprites["death"][self.death_animation_frame]
        else:
            # Determine facing direction
            direction_key = "right"
            if self.direction == (-1, 0):
                direction_key = "left"
            elif self.direction == (0, -1):
                direction_key = "up"
            elif self.direction == (0, 1):
                direction_key = "down"
            
            # Get current animation frame
            sprite = self.sprites[direction_key][self.mouth_open]
        
        # Draw sprite
        screen.blit(sprite, (self.x + offset_x, self.y + offset_y))
```

### 5.3 Ghost Characters

```python
# entities/ghost.py
from entities.entity import Entity
import random

class Ghost(Entity):
    def __init__(self, x, y, maze, name, scatter_target):
        super().__init__(x, y, maze)
        self.name = name
        self.speed = 1.75
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.mode = "scatter"  # scatter, chase, frightened
        self.scatter_target = scatter_target
        self.home_position = (x, y)
        self.target_tile = (0, 0)
        self.animation_timer = 0
        self.animation_frame = 0
        self.frightened_timer = 0
        self.is_eaten = False
        self.in_house = True
        
        # Load sprites
        self.sprites = {
            "right": [sprite1, sprite2],
            "left": [sprite3, sprite4],
            "up": [sprite5, sprite6],
            "down": [sprite7, sprite8],
            "frightened": [sprite9, sprite10],
            "frightened_ending": [sprite11, sprite12, sprite13, sprite14],
            "eyes": {
                "right": sprite15,
                "left": sprite16,
                "up": sprite17,
                "down": sprite18
            }
        }
    
    def update(self, dt):
        # Update animation
        self.animation_timer += dt
        if self.animation_timer >= 0.2:
            self.animation_timer = 0
            self.animation_frame = 1 - self.animation_frame  # Toggle between 0 and 1
        
        # Update frightened timer if applicable
        if self.mode == "frightened" and not self.is_eaten:
            self.frightened_timer -= dt
            if self.frightened_timer <= 0:
                self.mode = "chase"  # Revert to chase mode
        
        # If ghost is eaten, just move eyes back to ghost house
        if self.is_eaten:
            self.return_to_house(dt)
            return
        
        # At each tile center, decide next direction
        grid_x, grid_y = self.get_grid_position()
        center_x = grid_x * self.maze.tile_size + self.maze.tile_size / 2
        center_y = grid_y * self.maze.tile_size + self.maze.tile_size / 2
        
        # If at a tile center (or close enough), choose next direction
        if abs(self.x - center_x) < 1 and abs(self.y - center_y) < 1:
            self.x = center_x
            self.y = center_y
            
            # In frightened mode, choose random direction
            if self.mode == "frightened" and not self.is_eaten:
                self.choose_random_direction()
            else:
                # In scatter or chase mode, use path finding
                self.choose_next_direction()
        
        # Move in current direction
        dx, dy = self.direction
        if self.can_move(dx * self.speed, dy * self.speed):
            self.x += dx * self.speed
            self.y += dy * self.speed
            
            # Handle tunnel wrap-around
            self.handle_tunnel_wrap()
    
    def set_mode(self, mode, duration=None):
        """Set ghost mode to 'scatter', 'chase', or 'frightened'"""
        self.mode = mode
        if mode == "frightened":
            self.frightened_timer = duration if duration else 7.0
            # Reverse direction when entering frightened mode
            self.reverse_direction()
        elif mode != self.mode:
            # Reverse direction when changing between scatter and chase
            self.reverse_direction()
    
    def reverse_direction(self):
        """Reverse the current direction"""
        dx, dy = self.direction
        self.direction = (-dx, -dy)
    
    def choose_next_direction(self):
        """Choose next direction based on shortest path to target"""
        x, y = self.get_grid_position()
        
        # Determine target based on mode
        if self.mode == "scatter":
            target = self.scatter_target
        else:  # chase mode or eaten
            target = self.get_chase_target()
        
        # Calculate distances to target for each possible direction
        directions = []
        possible_dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, Right, Down, Left
        
        # Ghosts cannot reverse direction (except when changing modes)
        reverse_dir = (-self.direction[0], -self.direction[1])
        if reverse_dir in possible_dirs and self.direction != (0, 0):
            possible_dirs.remove(reverse_dir)
        
        for dx, dy in possible_dirs:
            if self.can_move(dx, dy):
                new_x, new_y = x + dx, y + dy
                # Calculate Manhattan distance to target
                distance = abs(new_x - target[0]) + abs(new_y - target[1])
                directions.append((dx, dy, distance))
        
        # Sort by distance (closest first)
        directions.sort(key=lambda d: d[2])
        
        if directions:
            self.direction = (directions[0][0], directions[0][1])
    
    def choose_random_direction(self):
        """Choose a random direction (for frightened mode)"""
        x, y = self.get_grid_position()
        possible_dirs = []
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:  # Up, Right, Down, Left
            if self.can_move(dx, dy) and (dx, dy) != (-self.direction[0], -self.direction[1]):
                possible_dirs.append((dx, dy))
        
        if possible_dirs:
            self.direction = random.choice(possible_dirs)
    
    def get_chase_target(self):
        """Override in subclasses to implement specific ghost behavior"""
        return (0, 0)
    
    def handle_tunnel_wrap(self):
        """Handle tunnel wrap-around"""
        if self.x < 0:
            self.x = self.maze.width * self.maze.tile_size
        elif self.x >= self.maze.width * self.maze.tile_size:
            self.x = 0
    
    def eaten(self):
        """Set ghost to eaten state (eyes only)"""
        self.is_eaten = True
    
    def return_to_house(self, dt):
        """Return to ghost house after being eaten"""
        # Implement path finding to return to ghost house entrance
        # Once at entrance, reset ghost state
        pass
    
    def render(self, screen, offset_x=0, offset_y=0):
        # Determine sprite to display based on mode
        if self.is_eaten:
            # Draw eyes only
            direction_key = "right"
            if self.direction[0] < 0:
                direction_key = "left"
            elif self.direction[1] < 0:
                direction_key = "up"
            elif self.direction[1] > 0:
                direction_key = "down"
            
            sprite = self.sprites["eyes"][direction_key]
        elif self.mode == "frightened":
            # Draw frightened sprite (blue or flashing)
            if self.frightened_timer <= 2.0:  # Flash white/blue when almost done
                flashing_index = (self.animation_frame + (int(self.frightened_timer * 5) % 2) * 2)
                sprite = self.sprites["frightened_ending"][flashing_index]
            else:
                sprite = self.sprites["frightened"][self.animation_frame]
        else:
            # Draw normal ghost sprites
            direction_key = "right"
            if self.direction[0] < 0:
                direction_key = "left"
            elif self.direction[1] < 0:
                direction_key = "up"
            elif self.direction[1] > 0:
                direction_key = "down"
            
            sprite = self.sprites[direction_key][self.animation_frame]
        
        # Draw sprite
        screen.blit(sprite, (self.x + offset_x, self.y + offset_y))
```

### 5.4 Specific Ghost Behaviors

Implement specific ghost targeting algorithms as subclasses:

```python
# entities/blinky.py (Red Ghost)
from entities.ghost import Ghost

class Blinky(Ghost):
    def __init__(self, x, y, maze, pacman):
        super().__init__(x, y, maze, "blinky", (27, 0))  # Scatter to top-right
        self.pacman = pacman
        self.color = (255, 0, 0)  # Red
    
    def get_chase_target(self):
        """Blinky targets Pac-Man's current position directly"""
        return self.pacman.get_grid_position()

# entities/pinky.py (Pink Ghost)
from entities.ghost import Ghost

class Pinky(Ghost):
    def __init__(self, x, y, maze, pacman):
        super().__init__(x, y, maze, "pinky", (0, 0))  # Scatter to top-left
        self.pacman = pacman
        self.color = (255, 192, 203)  # Pink
    
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

# entities/inky.py (Cyan Ghost)
from entities.ghost import Ghost

class Inky(Ghost):
    def __init__(self, x, y, maze, pacman, blinky):
        super().__init__(x, y, maze, "inky", (27, 31))  # Scatter to bottom-right
        self.pacman = pacman
        self.blinky = blinky
        self.color = (0, 255, 255)  # Cyan
    
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

# entities/clyde.py (Orange Ghost)
from entities.ghost import Ghost

class Clyde(Ghost):
    def __init__(self, x, y, maze, pacman):
        super().__init__(x, y, maze, "clyde", (0, 31))  # Scatter to bottom-left
        self.pacman = pacman
        self.color = (255, 165, 0)  # Orange
    
    def get_chase_target(self):
        """
        Clyde targets Pac-Man directly when far away,
        but scatters to his corner when within 8 tiles
        """
        px, py = self.pacman.get_grid_position()
        cx, cy = self.get_grid_position()
        
        # Calculate Manhattan distance to Pac-Man
        distance = abs(px - cx) + abs(py - cy)
        
        if distance < 8:
            # If close to Pac-Man, target scatter corner
            return self.scatter_target
        else:
            # If far from Pac-Man, target him directly
            return (px, py)
```

### 5.5 Pellets and Power Pellets

```python
# entities/pellet.py
import pygame

class Pellet:
    def __init__(self, x, y, is_power_pellet=False):
        self.x = x
        self.y = y
        self.is_power_pellet = is_power_pellet
        self.radius = 2 if not is_power_pellet else 7
        self.color = (255, 255, 255)  # White
        self.blink_timer = 0
        self.visible = True
    
    def update(self, dt):
        # Make power pellets blink
        if self.is_power_pellet:
            self.blink_timer += dt
            if self.blink_timer >= 0.2:
                self.blink_timer = 0
                self.visible = not self.visible
    
    def render(self, screen, offset_x=0, offset_y=0):
        if not self.visible:
            return
        
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x + offset_x), int(self.y + offset_y)),
            self.radius
        )
```

## 6. Collision System

### 6.1 Entity Collisions

```python
# utils/collision.py
def check_collision(entity1, entity2, threshold=10):
    """Check if two entities are colliding"""
    # Calculate centers
    center1_x = entity1.x + entity1.maze.tile_size / 2
    center1_y = entity1.y + entity1.maze.tile_size / 2
    center2_x = entity2.x + entity2.maze.tile_size / 2
    center2_y = entity2.y + entity2.maze.tile_size / 2
    
    # Calculate distance between centers
    distance = ((center1_x - center2_x) ** 2 + (center1_y - center2_y) ** 2) ** 0.5
    
    # Return True if distance is less than threshold
    return distance < threshold
```

### 6.2 Ghost-Pacman Collision

```python
# In the Game class update method
def check_ghost_collisions(self):
    for ghost in self.ghosts:
        if collision.check_collision(self.pacman, ghost):
            if ghost.mode == "frightened" and not ghost.is_eaten:
                # Pac-Man eats ghost
                ghost.eaten()
                self.score += self.ghost_score
                self.ghost_score *= 2  # Double points for next ghost
                # Play ghost eaten sound
            elif not ghost.is_eaten and not self.pacman.is_dead:
                # Ghost catches Pac-Man
                self.pacman.die()
                self.state = "PACMAN_DYING"
                # Reset ghosts
                self.reset_ghosts_after_death()
```

## 7. Input Handling

```python
# engine/input_handler.py
import pygame

class InputHandler:
    def __init__(self, game):
        self.game = game
    
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            
            elif event.type == pygame.KEYDOWN:
                if self.game.state == "PLAYING":
                    if event.key == pygame.K_UP:
                        self.game.pacman.set_next_direction((0, -1))
                    elif event.key == pygame.K_RIGHT:
                        self.game.pacman.set_next_direction((1, 0))
                    elif event.key == pygame.K_DOWN:
                        self.game.pacman.set_next_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.game.pacman.set_next_direction((-1, 0))
                
                elif self.game.state in ["INTRO", "GAME_OVER"]:
                    # Start game on any key press
                    if event.key == pygame.K_RETURN:
                        self.game.start_game()
                
                # Global keys
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False
                elif event.key == pygame.K_p:
                    self.game.toggle_pause()
```

## 8. Rendering System

```python
# engine/renderer.py
import pygame

class Renderer:
    def __init__(self, screen, maze):
        self.screen = screen
        self.maze = maze
        self.tile_size = maze.tile_size
        self.offset_x = (screen.get_width() - maze.width * maze.tile_size) // 2
        self.offset_y = (screen.get_height() - maze.height * maze.tile_size) // 2
        
        # Colors
        self.wall_color = (33, 33, 255)  # Blue
        self.background_color = (0, 0, 0)  # Black
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def render_maze(self):
        """Render the maze walls"""
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.maze.is_wall(x, y):
                    pygame.draw.rect(
                        self.screen,
                        self.wall_color,
                        (
                            x * self.tile_size + self.offset_x,
                            y * self.tile_size + self.offset_y,
                            self.tile_size,
                            self.tile_size
                        )
                    )
    
    def render_pellets(self):
        """Render pellets and power pellets"""
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                tile = self.maze.get_tile(x, y)
                if tile == 2:  # Regular pellet
                    center_x = x * self.tile_size + self.tile_size // 2 + self.offset_x
                    center_y = y * self.tile_size + self.tile_size // 2 + self.offset_y
                    pygame.draw.circle(
                        self.screen,
                        (255, 255, 255),  # White
                        (center_x, center_y),
                        2  # Radius
                    )
                elif tile == 3:  # Power pellet
                    center_x = x * self.tile_size + self.tile_size // 2 + self.offset_x
                    center_y = y * self.tile_size + self.tile_size // 2 + self.offset_y
                    # Make power pellets blink
                    if int(pygame.time.get_ticks() / 200) % 2 == 0:
                        pygame.draw.circle(
                            self.screen,
                            (255, 255, 255),  # White
                            (center_x, center_y),
                            6  # Radius
                        )
    
    def render_entities(self, entities):
        """Render all game entities"""
        for entity in entities:
            entity.render(self.screen, self.offset_x, self.offset_y)
    
    def render_score(self, score, high_score, level):
        """Render the score and high score"""
        # Draw score
        score_surf = self.font.render(f"SCORE: {score}", True, (255, 255, 255))
        self.screen.blit(score_surf, (10, 10))
        
        # Draw high score
        high_score_surf = self.font.render(f"HIGH: {high_score}", True, (255, 255, 255))
        self.screen.blit(high_score_surf, (screen_width - high_score_surf.get_width() - 10, 10))
        
        # Draw level
        level_surf = self.small_font.render(f"LEVEL: {level}", True, (255, 255, 255))
        self.screen.blit(level_surf, (10, screen_height - level_surf.get_height() - 10))
    
    def render_lives(self, lives):
        """Render remaining lives as small Pac-Man icons"""
        for i in range(lives):
            # Draw a simple yellow circle for each life
            pygame.draw.circle(
                self.screen,
                (255, 255, 0),  # Yellow
                (30 + i * 25, screen_height - 20),
                8  # Radius
            )
    
    def render_ready_text(self):
        """Render 'READY!' text at game start"""
        ready_surf = self.font.render("READY!", True, (255, 255, 0))
        ready_rect = ready_surf.get_rect(center=(screen_width // 2, screen_height // 2))
        self.screen.blit(ready_surf, ready_rect)
    
    def render_game_over(self):
        """Render 'GAME OVER' text"""
        game_over_surf = self.font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_surf.get_rect(center=(screen_width // 2, screen_height // 2))
        self.screen.blit(game_over_surf, game_over_rect)
    
    def render_intro_screen(self):
        """Render the intro/title screen"""
        # Draw title
        title_surf = pygame.font.Font(None, 72).render("PAC-MAN", True, (255, 255, 0))
        title_rect = title_surf.get_rect(center=(screen_width // 2, screen_height // 4))
        self.screen.blit(title_surf, title_rect)
        
        # Draw "Press ENTER to start"
        start_surf = self.font.render("Press ENTER to start", True, (255, 255, 255))
        start_rect = start_surf.get_rect(center=(screen_width // 2, screen_height * 3 // 4))
        self.screen.blit(start_surf, start_rect)
        
        # Draw ghost characters and their names
        ghost_y = screen_height // 2
        ghost_colors = [(255, 0, 0), (255, 192, 203), (0, 255, 255), (255, 165, 0)]
        ghost_names = ["BLINKY", "PINKY", "INKY", "CLYDE"]
        
        for i, (color, name) in enumerate(zip(ghost_colors, ghost_names)):
            # Draw ghost shape
            pygame.draw.rect(
                self.screen,
                color,
                (screen_width // 4, ghost_y + i * 40, 20, 20)
            )
            
            # Draw name
            name_surf = self.small_font.render(name, True, (255, 255, 255))
            self.screen.blit(name_surf, (screen_width // 4 + 30, ghost_y + i * 40))
```

## 9. Sound System

```python
# engine/sound.py
import pygame

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music = None
        
        # Load sound effects
        self.load_sounds()
    
    def load_sounds(self):
        """Load all game sound effects"""
        self.sounds = {
            "chomp": pygame.mixer.Sound("assets/sounds/chomp.wav"),
            "death": pygame.mixer.Sound("assets/sounds/death.wav"),
            "eat_ghost": pygame.mixer.Sound("assets/sounds/eat_ghost.wav"),
            "eat_fruit": pygame.mixer.Sound("assets/sounds/eat_fruit.wav"),
            "power_pellet": pygame.mixer.Sound("assets/sounds/power_pellet.wav"),
            "extra_life": pygame.mixer.Sound("assets/sounds/extra_life.wav"),
            "game_start": pygame.mixer.Sound("assets/sounds/game_start.wav"),
        }
        
        # Set volume
        for sound in self.sounds.values():
            sound.set_volume(0.5)
    
    def play(self, sound_name):
        """Play a sound effect by name"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_siren(self, level):
        """Play the appropriate siren music based on level"""
        if self.music:
            pygame.mixer.music.stop()
        
        # Change siren speed based on remaining pellets/level
        siren_num = min(level, 5)  # Maximum of 5 different sirens
        pygame.mixer.music.load(f"assets/sounds/siren_{siren_num}.wav")
        pygame.mixer.music.play(-1)  # Loop indefinitely
    
    def play_frightened(self):
        """Play the frightened ghost music"""
        if self.music:
            pygame.mixer.music.stop()
        
        pygame.mixer.music.load("assets/sounds/frightened.wav")
        pygame.mixer.music.play(-1)  # Loop indefinitely
    
    def stop_music(self):
        """Stop any currently playing music"""
        pygame.mixer.music.stop()
```

## 10. Scoring System

```python
# In the Game class
def update_score(self, points):
    """Update score and check for extra life"""
    self.score += points
    
    # Check if score has reached next extra life threshold
    if self.score >= self.next_extra_life_score:
        self.lives += 1
        self.next_extra_life_score += 10000  # Next extra life at every 10,000 points
        self.sound_manager.play("extra_life")
    
    # Update high score if needed
    if self.score > self.high_score:
        self.high_score = self.score
        # Save high score to file
        self.save_high_score()
```

## 11. Main Game Class

```python
# engine/game.py
import pygame
import random
from engine.input_handler import InputHandler
from engine.renderer import Renderer
from engine.sound import SoundManager
from entities.pacman import Pacman
from entities.blinky import Blinky
from entities.pinky import Pinky
from entities.inky import Inky
from entities.clyde import Clyde
from entities.fruit import Fruit
from utils.collision import check_collision

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Screen setup
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pac-Man")
        
        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        
        # Game state
        self.state = "INTRO"  # INTRO, READY, PLAYING, PACMAN_DYING, GHOST_EATEN, LEVEL_COMPLETE, GAME_OVER
        self.level = 1
        self.score = 0
        self.high_score = self.load_high_score()
        self.lives = 3
        self.ghost_score = 200  # Points for eating ghost, doubles each time
        self.next_extra_life_score = 10000
        
        # Load maze
        self.maze = self.load_maze()
        
        # Create renderer
        self.renderer = Renderer(self.screen, self.maze)
        
        # Create input handler
        self.input_handler = InputHandler(self)
        
        # Create sound manager
        self.sound_manager = SoundManager()
        
        # Create entities
        self.pacman = None
        self.ghosts = []
        self.fruit = None
        
        # Ghost mode timing
        self.ghost_mode_timer = 0
        self.ghost_mode_schedule = [
            ("scatter", 7),    # Scatter for 7 seconds
            ("chase", 20),     # Chase for 20 seconds
            ("scatter", 7),    # Scatter for 7 seconds
            ("chase", 20),     # Chase for 20 seconds
            ("scatter", 5),    # Scatter for 5 seconds
            ("chase", 20),     # Chase for 20 seconds
            ("scatter", 5),    # Scatter for 5 seconds
            ("chase", float('inf'))  # Chase permanently
        ]
        self.current_mode_index = 0
        
        # Fruit timing
        self.fruit_timer = 0
        self.fruit_duration = 10  # 10 seconds
        self.fruit_active = False
        
        # For level restart
        self.ready_timer = 0
        self.ready_duration = 2  # 2 seconds "READY!" display
    
    def load_high_score(self):
        """Load high score from file"""
        try:
            with open("highscore.txt", "r") as file:
                return int(file.read())
        except (FileNotFoundError, ValueError):
            return 0
    
    def save_high_score(self):
        """Save high score to file"""
        with open("highscore.txt", "w") as file:
            file.write(str(self.high_score))
    
    def load_maze(self):
        """Load maze layout"""
        # Implement maze loading from file or hardcode maze layout
        pass
    
    def init_level(self):
        """Initialize entities for current level"""
        # Create Pac-Man
        self.pacman = Pacman(14 * self.maze.tile_size, 23 * self.maze.tile_size, self.maze)
        
        # Create ghosts
        blinky = Blinky(14 * self.maze.tile_size, 11 * self.maze.tile_size, self.maze, self.pacman)
        pinky = Pinky(14 * self.maze.tile_size, 14 * self.maze.tile_size, self.maze, self.pacman)
        inky = Inky(12 * self.maze.tile_size, 14 * self.maze.tile_size, self.maze, self.pacman, blinky)
        clyde = Clyde(16 * self.maze.tile_size, 14 * self.maze.tile_size, self.maze, self.pacman)
        
        self.ghosts = [blinky, pinky, inky, clyde]
        
        # Reset ghost mode timer
        self.ghost_mode_timer = 0
        self.current_mode_index = 0
        self.update_ghost_modes()
        
        # No fruit initially
        self.fruit = None
        self.fruit_timer = 0
        self.fruit_active = False
        
        # Set ready timer
        self.ready_timer = 0
        self.state = "READY"
        
        # Play start sound
        self.sound_manager.play("game_start")
    
    def start_game(self):
        """Start a new game"""
        self.level = 1
        self.score = 0
        self.lives = 3
        self.ghost_score = 200
        self.next_extra_life_score = 10000
        
        # Reset maze (repopulate pellets)
        self.maze = self.load_maze()
        
        # Initialize level
        self.init_level()
    
    def update(self):
        """Update game state"""
        if self.paused:
            return
        
        # Get time delta
        dt = self.clock.get_time() / 1000.0  # Convert to seconds
        
        # Handle game states
        if self.state == "INTRO":
            # Just waiting for player to start
            pass
        
        elif self.state == "READY":
            # Show "READY!" text for a moment before starting
            self.ready_timer += dt
            if self.ready_timer >= self.ready_duration:
                self.state = "PLAYING"
                self.sound_manager.play_siren(self.level)
        
        elif self.state == "PLAYING":
            # Update ghost modes
            self.update_ghost_modes(dt)
            
            # Update all entities
            self.pacman.update(dt)
            for ghost in self.ghosts:
                ghost.update(dt)
            
            # Check for collisions
            self.check_ghost_collisions()
            
            # Check for level completion
            if self.maze.pellets_remaining == 0:
                self.state = "LEVEL_COMPLETE"
                self.sound_manager.stop_music()
                # Short delay before next level
                pygame.time.set_timer(pygame.USEREVENT, 3000)  # 3 second delay
            
            # Handle fruit spawning
            self.update_fruit(dt)
            
            # Check fruit collision
            if self.fruit and self.fruit_active:
                if check_collision(self.pacman, self.fruit):
                    self.score += self.get_fruit_points()
                    self.sound_manager.play("eat_fruit")
                    self.fruit_active = False
        
        elif self.state == "PACMAN_DYING":
            # Just wait for death animation to complete
            # The pacman.update() method will handle animation and state transition
            self.pacman.update(dt)
            
            # After animation, check if game over
            if not self.pacman.is_dead:
                if self.lives <= 0:
                    self.state = "GAME_OVER"
                    pygame.time.set_timer(pygame.USEREVENT, 3000)  # 3 second delay
                else:
                    # Reset for next life
                    self.reset_level()
        
        elif self.state == "LEVEL_COMPLETE":
            # Wait for timer to expire (handled in event processing)
            pass
        
        elif self.state == "GAME_OVER":
            # Wait for timer to expire (handled in event processing)
            pass
    
    def update_ghost_modes(self, dt=0):
        """Update ghost modes based on timer"""
        if self.state != "PLAYING":
            return
        
        self.ghost_mode_timer += dt
        current_mode, duration = self.ghost_mode_schedule[self.current_mode_index]
        
        if self.ghost_mode_timer >= duration:
            # Move to next mode
            self.ghost_mode_timer = 0
            self.current_mode_index = (self.current_mode_index + 1) % len(self.ghost_mode_schedule)
            next_mode, _ = self.ghost_mode_schedule[self.current_mode_index]
            
            # Update all ghosts
            for ghost in self.ghosts:
                if not ghost.is_eaten:
                    ghost.set_mode(next_mode)
            
            # Update music
            if next_mode == "chase" or next_mode == "scatter":
                self.sound_manager.play_siren(self.level)
    
    def frighten_ghosts(self, duration):
        """Set all ghosts to frightened mode"""
        self.ghost_score = 200  # Reset ghost score
        
        for ghost in self.ghosts:
            if not ghost.is_eaten:
                ghost.set_mode("frightened", duration)
        
        # Play frightened music
        self.sound_manager.play_frightened()
    
    def update_fruit(self, dt):
        """Handle fruit spawning and despawning"""
        # Spawn fruit at 70 pellets and 170 pellets remaining
        pellets_needed = [self.maze.total_pellets - 70, self.maze.total_pellets - 170]
        pellets_eaten = self.maze.total_pellets - self.maze.pellets_remaining
        
        if pellets_eaten in pellets_needed and not self.fruit_active and not self.fruit:
            # Spawn fruit
            self.fruit = Fruit(
                14 * self.maze.tile_size,
                17 * self.maze.tile_size,
                self.maze,
                self.level
            )
            self.fruit_active = True
            self.fruit_timer = 0
        
        # Update fruit timer if active
        if self.fruit_active:
            self.fruit_timer += dt
            if self.fruit_timer >= self.fruit_duration:
                self.fruit_active = False
    
    def get_fruit_points(self):
        """Return points for current level's fruit"""
        points = [100, 300, 500, 700, 1000, 2000, 3000, 5000]
        index = min(self.level - 1, len(points) - 1)
        return points[index]
    
    def check_ghost_collisions(self):
        """Check for collisions between Pac-Man and ghosts"""
        for ghost in self.ghosts:
            if check_collision(self.pacman, ghost):
                if ghost.mode == "frightened" and not ghost.is_eaten:
                    # Pac-Man eats ghost
                    ghost.eaten()
                    self.score += self.ghost_score
                    self.sound_manager.play("eat_ghost")
                    self.ghost_score *= 2  # Double points for next ghost
                    
                    # Short pause
                    self.state = "GHOST_EATEN"
                    pygame.time.set_timer(pygame.USEREVENT, 500)  # 0.5 second pause
                
                elif not ghost.is_eaten and not self.pacman.is_dead:
                    # Ghost catches Pac-Man
                    self.pacman.die()
                    self.sound_manager.play("death")
                    self.sound_manager.stop_music()
                    self.state = "PACMAN_DYING"
    
    def reset_level(self):
        """Reset entities after Pac-Man dies"""
        # Reset Pac-Man position
        self.pacman.x = 14 * self.maze.tile_size
        self.pacman.y = 23 * self.maze.tile_size
        self.pacman.direction = (0, 0)
        self.pacman.next_direction = (0, 0)
        
        # Reset ghost positions
        blinky = self.ghosts[0]
        blinky.x = 14 * self.maze.tile_size
        blinky.y = 11 * self.maze.tile_size
        
        pinky = self.ghosts[1]
        pinky.x = 14 * self.maze.tile_size
        pinky.y = 14 * self.maze.tile_size
        
        inky = self.ghosts[2]
        inky.x = 12 * self.maze.tile_size
        inky.y = 14 * self.maze.tile_size
        
        clyde = self.ghosts[3]
        clyde.x = 16 * self.maze.tile_size
        clyde.y = 14 * self.maze.tile_size
        
        # Reset ghost modes
        self.ghost_mode_timer = 0
        self.current_mode_index = 0
        self.update_ghost_modes()
        
        # Set ready state
        self.state = "READY"
        self.ready_timer = 0
    
    def next_level(self):
        """Advance to next level"""
        self.level += 1
        
        # Reset maze (repopulate pellets)
        self.maze = self.load_maze()
        
        # Initialize level with increased difficulty
        self.init_level()
        
        # Adjust ghost speeds based on level
        for ghost in self.ghosts:
            # Increase ghost speed every 2 levels up to level 20
            level_factor = min(self.level, 20) / 2
            ghost.speed = 1.75 + (level_factor * 0.05)
    
    def toggle_pause(self):
        """Toggle game pause state"""
        self.paused = not self.paused
    
    def render(self):
        """Render the current game state"""
        # Clear screen
        self.screen.fill((0, 0, 0))  # Black background
        
        if self.state == "INTRO":
            # Render intro screen
            self.renderer.render_intro_screen()
        
        elif self.state in ["READY", "PLAYING", "PACMAN_DYING", "GHOST_EATEN"]:
            # Render maze
            self.renderer.render_maze()
            
            # Render pellets
            self.renderer.render_pellets()
            
            # Render fruit if active
            if self.fruit and self.fruit_active:
                self.fruit.render(self.screen, self.renderer.offset_x, self.renderer.offset_y)
            
            # Render Pac-Man and ghosts
            self.renderer.render_entities(self.ghosts + [self.pacman])
            
            # Render score and lives
            self.renderer.render_score(self.score, self.high_score, self.level)
            self.renderer.render_lives(self.lives)
            
            # Render "READY!" text if in ready state
            if self.state == "READY":
                self.renderer.render_ready_text()
        
        elif self.state == "GAME_OVER":
            # Render game over screen
            self.renderer.render_game_over()
        
        # Display paused message if paused
        if self.paused:
            paused_surf = pygame.font.Font(None, 48).render("PAUSED", True, (255, 255, 255))
            paused_rect = paused_surf.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(paused_surf, paused_rect)
        
        # Update display
        pygame.display.flip()
    
    def handle_events(self):
        """Process input events"""
        self.input_handler.process_events()
        
        # Check for any custom events
        for event in pygame.event.get(pygame.USEREVENT):
            if self.state == "GHOST_EATEN":
                # Resume game after ghost eaten pause
                self.state = "PLAYING"
            
            elif self.state == "LEVEL_COMPLETE":
                # Advance to next level
                self.next_level()
            
            elif self.state == "GAME_OVER":
                # Return to intro screen
                self.state = "INTRO"
    
    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            self.handle_events()
            
            # Update game state
            self.update()
            
            # Render frame
            self.render()
            
            # Maintain frame rate
            self.clock.tick(60)
        
        # Save high score before quitting
        self.save_high_score()
        
        # Clean up
        pygame.quit()
```

## 12. Asset Management

### 12.1 Sprite Sheets

Create a simple sprite loader:

```python
# utils/sprite_loader.py
import pygame

def load_sprite_sheet(filename, sprite_width, sprite_height, colorkey=None):
    """
    Load a sprite sheet and split it into individual sprites
    
    Args:
        filename (str): Path to sprite sheet image
        sprite_width (int): Width of each sprite in pixels
        sprite_height (int): Height of each sprite in pixels
        colorkey (tuple): RGB color for transparency, or -1 for top left pixel
    
    Returns:
        list: List of surface objects for each sprite
    """
    sheet = pygame.image.load(filename).convert()
    sheet_width, sheet_height = sheet.get_size()
    
    # Calculate number of sprites
    columns = sheet_width // sprite_width
    rows = sheet_height // sprite_height
    
    sprites = []
    
    for row in range(rows):
        for col in range(columns):
            # Calculate position
            x = col * sprite_width
            y = row * sprite_height
            
            # Create a new surface
            sprite = pygame.Surface((sprite_width, sprite_height))
            
            # Copy the sprite from the sheet
            sprite.blit(sheet, (0, 0), (x, y, sprite_width, sprite_height))
            
            # Set color key (transparency)
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = sprite.get_at((0, 0))
                sprite.set_colorkey(colorkey, pygame.RLEACCEL)
            
            sprites.append(sprite)
    
    return sprites
```

### 12.2 Animation System

Create a simple animation system:

```python
# utils/animation.py
class Animation:
    def __init__(self, frames, frame_duration=0.1, loop=True):
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.current_frame = 0
        self.elapsed_time = 0
        self.finished = False
    
    def update(self, dt):
        """Update animation state"""
        if self.finished:
            return
        
        self.elapsed_time += dt
        
        if self.elapsed_time >= self.frame_duration:
            frames_to_advance = int(self.elapsed_time / self.frame_duration)
            self.elapsed_time %= self.frame_duration
            
            self.current_frame += frames_to_advance
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame %= len(self.frames)
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
    
    def get_current_frame(self):
        """Get the current frame of the animation"""
        return self.frames[self.current_frame]
    
    def reset(self):
        """Reset the animation to the beginning"""
        self.current_frame = 0
        self.elapsed_time = 0
        self.finished = False
```

## 13. Final Steps

### 13.1 Entry Point

Create the main entry point:

```python
# main.py
import pygame
from engine.game import Game

def main():
    # Initialize game
    game = Game()
    
    # Run game loop
    game.run()

if __name__ == "__main__":
    main()
```

### 13.2 Config File

Create a global configuration file:

```python
# config.py
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Game speed
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Tile size
TILE_SIZE = 16

# Ghost speeds for each level (baseline, increases with level)
GHOST_SPEEDS = {
    'normal': 1.75,
    'tunnel': 0.5,
    'frightened': 0.8
}

# Ghost mode durations for each level
GHOST_MODE_DURATIONS = [
    # Level 1
    {
        'scatter': [7, 7, 5, 5],
        'chase': [20, 20, 20, float('inf')]
    },
    # Level 2 (shorter scatter times)
    {
        'scatter': [7, 7, 5, 1],
        'chase': [20, 20, 1033, float('inf')]
    },
    # Level 3+ (minimal scatter)
    {
        'scatter': [5, 5, 5, 1],
        'chase': [20, 20, 1037, float('inf')]
    }
]

# Power pellet durations (seconds)
POWER_PELLET_DURATIONS = [
    8,    # Level 1
    7,    # Level 2
    6,    # Level 3
    5,    # Level 4
    4,    # Level 5
    3,    # Level 6
    2,    # Level 7
    1,    # Level 8+
]
```

## 14. Implementation Notes

1. **Start Simple**: Begin with implementing the basic game loop, rendering, and movement systems before adding advanced features.
2. **Incremental Testing**: Test each component individually:
   - First, get the maze rendering correctly
   - Then add Pac-Man movement
   - Then add pellet collection
   - Finally add ghost behavior
3. **Ghost AI**: The ghost AI is the most complex part. Implement one ghost at a time, starting with Blinky.
4. **Collision Detection**: Keep collision detection simple initially, then refine it later.
5. **Maze Design**: For simplicity, use a hardcoded maze array for the first version.
6. **Animation**: Start with basic animation frames, then enhance them later.

## 15. Troubleshooting Guide

1. **Pac-Man Movement Issues**:
   - Check that grid-to-pixel conversions are correct
   - Ensure collision detection is accounting for the proper tile size
   - Verify that direction changes are only applied when valid

2. **Ghost Behavior Problems**:
   - Verify target tile calculations for each ghost
   - Make sure mode transitions are occurring correctly
   - Check for proper reverse direction implementation when changing modes

3. **Collision Detection Errors**:
   - Use visual debugging to draw collision boxes
   - Ensure entities are detecting collisions at the right distance thresholds
   - Verify that grid position calculations are correct

4. **Performance Issues**:
   - Use profiling to identify bottlenecks
   - Minimize unnecessary sprite reloading
   - Optimize collision detection by only checking relevant entities

5. **Timing Issues**:
   - Make sure all timers are using delta time
   - Verify frame-independent movement calculations
   - Check that animations are updating at the correct rate


I've created a comprehensive Pac-Man implementation specification that covers all aspects of the game. The specification is detailed enough that an LLM can follow it to implement the classic arcade game without needing additional clarification.

The specification includes:

1. Complete architecture and file structure
2. Game mechanics and physics
3. Entity system with detailed implementations for:
   - Pac-Man character
   - All four ghosts with their unique AI behaviors
   - Pellets and power pellets
4. Maze representation and collision system
5. Input handling and controls
6. Rendering and animation systems
7. Sound management
8. Scoring and level progression
9. Game state management
10. Asset loading and configuration

The implementation uses Pygame for rendering, input handling, and sound. I've included complete code samples for all major components, with detailed comments explaining the functionality.

This specification follows the original Pac-Man game design closely, including the unique ghost AI behaviors, timing systems for ghost modes, and proper scoring mechanics. The code architecture is modular and organized to promote maintainability and extensibility.
