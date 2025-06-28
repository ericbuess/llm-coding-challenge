# Pac-Man Game Implementation Plan

## Overview
This document provides a complete implementation plan for a Pac-Man game in Python using Pygame. The plan is designed to be followed step-by-step by any developer or LLM to create a fully functional game.

## Technical Specifications
- **Python Version**: 3.8+
- **Dependencies**: pygame==2.5.0
- **Screen Resolution**: 672x744 pixels (28x31 tiles, 24px per tile)
- **Target FPS**: 60
- **Coordinate System**: Top-left origin (0,0)

## Project Structure
```
pacman/
├── main.py              # Entry point and game loop
├── requirements.txt     # Dependencies
├── game/
│   ├── __init__.py
│   ├── game.py          # GameController class
│   ├── board.py         # Board and maze logic
│   ├── entities.py      # Pacman, Ghost, Pellet classes
│   ├── ai.py            # Ghost AI behaviors
│   ├── constants.py     # Game constants and settings
│   └── utils.py         # Helper functions
├── ui/
│   ├── __init__.py
│   ├── display.py       # Rendering and sprite management
│   └── sounds.py        # Sound effect management
└── assets/
    ├── sprites/         # PNG images (optional)
    └── sounds/          # WAV files (optional)
```

## Core Constants (constants.py)
```python
# Screen dimensions
TILE_SIZE = 24
BOARD_WIDTH = 28
BOARD_HEIGHT = 31
SCREEN_WIDTH = BOARD_WIDTH * TILE_SIZE  # 672
SCREEN_HEIGHT = BOARD_HEIGHT * TILE_SIZE  # 744

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 184, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 184, 82)

# Game settings
FPS = 60
PACMAN_SPEED = 2  # pixels per frame
GHOST_SPEED = 1.5
FRIGHTENED_SPEED = 1
POWER_PELLET_DURATION = 6  # seconds
STARTING_LIVES = 3

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
```

## Maze Representation
The maze is a 28x31 grid where:
- `#` = Wall
- `.` = Pellet
- `o` = Power pellet
- ` ` = Empty space
- `G` = Ghost house
- `P` = Pacman start position
- `-` = Ghost house door

```
############################
#............##............#
#.####.#####.##.#####.####.#
#o#  #.#   #.##.#   #.#  #o#
#.####.#####.##.#####.####.#
#..........................#
#.####.##.########.##.####.#
#.####.##.########.##.####.#
#......##....##....##......#
######.##### ## #####.######
     #.##### ## #####.#     
     #.##          ##.#     
     #.## ###--### ##.#     
######.## #GGGGGG# ##.######
      .   #GGGGGG#   .      
######.## #GGGGGG# ##.######
     #.## ######## ##.#     
     #.##          ##.#     
     #.## ######## ##.#     
######.## ######## ##.######
#............##............#
#.####.#####.##.#####.####.#
#.####.#####.##.#####.####.#
#o..##.......P........##..o#
###.##.##.########.##.##.###
###.##.##.########.##.##.###
#......##....##....##......#
#.##########.##.##########.#
#..........................#
############################
```

## Class Specifications

### 1. Board Class (board.py)
```python
class Board:
    def __init__(self):
        self.maze = []  # 2D list from maze string
        self.pellets = set()  # (x, y) tuples
        self.power_pellets = set()
        self.walls = set()
        self.ghost_house = set()
        self.pacman_start = (14, 23)
        self.ghost_starts = {
            'blinky': (14, 11),
            'pinky': (14, 14),
            'inky': (12, 14),
            'clyde': (16, 14)
        }
    
    def load_maze(self, maze_string: str): pass
    def is_wall(self, x: int, y: int) -> bool: pass
    def is_intersection(self, x: int, y: int) -> bool: pass
    def get_neighbors(self, x: int, y: int) -> list: pass
    def remove_pellet(self, x: int, y: int): pass
```

### 2. Entity Classes (entities.py)
```python
class Entity:
    def __init__(self, x: float, y: float):
        self.x = x  # pixel coordinates
        self.y = y
        self.tile_x = int(x // TILE_SIZE)
        self.tile_y = int(y // TILE_SIZE)
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.speed = 0
    
    def update(self, board: Board): pass
    def can_move(self, board: Board, direction: tuple) -> bool: pass
    def get_center(self) -> tuple: pass

class Pacman(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.speed = PACMAN_SPEED
        self.animation_frame = 0
        self.is_dying = False
    
    def handle_input(self, keys): pass
    def check_pellet_collision(self, board: Board) -> dict: pass

class Ghost(Entity):
    def __init__(self, x: float, y: float, name: str, color: tuple):
        super().__init__(x, y)
        self.name = name
        self.color = color
        self.mode = 'scatter'  # scatter, chase, frightened, eyes
        self.frightened_timer = 0
        self.target_tile = (0, 0)
        self.home_tile = self.get_home_tile()
    
    def get_home_tile(self) -> tuple: pass
    def update_target(self, pacman: Pacman, blinky: 'Ghost' = None): pass
    def move_towards_target(self, board: Board): pass
```

### 3. Game Controller (game.py)
```python
class GameController:
    def __init__(self):
        self.board = Board()
        self.pacman = None
        self.ghosts = {}
        self.score = 0
        self.lives = STARTING_LIVES
        self.level = 1
        self.game_state = 'menu'  # menu, playing, paused, game_over
        self.power_mode_timer = 0
    
    def initialize_level(self): pass
    def update(self, dt: float): pass
    def handle_collisions(self): pass
    def check_win_condition(self) -> bool: pass
    def next_level(self): pass
```

## Implementation Phases

### Phase 1: Foundation (Days 1-2)
**Goal**: Display a static maze with basic rendering

1. Create project structure and install pygame
2. Implement `constants.py` with all constants
3. Create `Board` class with maze loading
4. Implement basic `Display` class in `ui/display.py`:
   ```python
   def draw_maze(self, screen, board):
       for y in range(BOARD_HEIGHT):
           for x in range(BOARD_WIDTH):
               if board.is_wall(x, y):
                   pygame.draw.rect(screen, BLUE, 
                                  (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
   ```
5. Create main game loop in `main.py`

**Acceptance Criteria**:
- Maze displays correctly
- Window stays open at 60 FPS
- All walls render in correct positions

### Phase 2: Pacman Movement (Days 3-4)
**Goal**: Controllable Pacman with smooth movement

1. Implement `Entity` base class with pixel-perfect movement
2. Create `Pacman` class with:
   - Smooth movement between tiles
   - Input buffering for direction changes
   - Wall collision detection
3. Add pellet rendering and collection
4. Implement score display

**Key Algorithm - Smooth Movement**:
```python
def update(self, board):
    # Check if we can turn at current tile center
    if self.next_direction != self.direction:
        if self.is_centered() and self.can_move(board, self.next_direction):
            self.direction = self.next_direction
    
    # Move in current direction
    if self.can_move(board, self.direction):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        self.update_tile_position()
```

**Acceptance Criteria**:
- Pacman moves smoothly at constant speed
- Cannot pass through walls
- Collects pellets and updates score
- Direction changes feel responsive

### Phase 3: Ghost Implementation (Days 5-7)
**Goal**: Four ghosts with unique behaviors

1. Implement `Ghost` base class
2. Create ghost AI behaviors in `ai.py`:
   - **Blinky**: Target Pacman's current tile
   - **Pinky**: Target 4 tiles ahead of Pacman
   - **Inky**: Complex targeting using Blinky's position
   - **Clyde**: Target Pacman when far, scatter when close
3. Implement ghost house exit logic
4. Add mode switching (scatter/chase cycles)

**Ghost AI Pseudocode**:
```python
def update_target(self, pacman, blinky=None):
    if self.mode == 'scatter':
        self.target_tile = self.home_tile
    elif self.mode == 'chase':
        if self.name == 'blinky':
            self.target_tile = (pacman.tile_x, pacman.tile_y)
        elif self.name == 'pinky':
            # Target 4 tiles ahead of Pacman
            offset_x = pacman.direction[0] * 4
            offset_y = pacman.direction[1] * 4
            self.target_tile = (pacman.tile_x + offset_x, pacman.tile_y + offset_y)
        # ... etc for other ghosts
```

**Acceptance Criteria**:
- Each ghost exhibits unique behavior
- Ghosts navigate maze without getting stuck
- Mode switching works on timer

### Phase 4: Game Mechanics (Days 8-9)
**Goal**: Complete game rules

1. Implement power pellets and frightened mode
2. Add collision detection between Pacman and ghosts
3. Implement lives system and death animation
4. Add level progression
5. Create game over and win conditions

**Collision Detection**:
```python
def check_ghost_collision(pacman, ghost):
    distance = math.sqrt((pacman.x - ghost.x)**2 + (pacman.y - ghost.y)**2)
    return distance < TILE_SIZE * 0.75  # 75% of tile size for tolerance
```

**Acceptance Criteria**:
- Power pellets make ghosts vulnerable
- Eating ghosts gives points and sends them home
- Death removes a life and resets positions
- Level advances when all pellets eaten

### Phase 5: Polish (Days 10-11)
**Goal**: Game feel and polish

1. Add animation frames for Pacman (mouth opening/closing)
2. Implement ghost animations (eyes looking in direction)
3. Add sound effects (optional)
4. Create start menu and game over screen
5. Implement high score tracking

**Animation Example**:
```python
def draw_pacman(self, screen, pacman):
    # Animate mouth based on movement
    if pacman.is_moving():
        pacman.animation_frame = (pacman.animation_frame + 1) % 30
        mouth_angle = abs(pacman.animation_frame - 15) * 2
        
        # Draw pac-man with animated mouth
        start_angle = math.radians(mouth_angle)
        end_angle = math.radians(360 - mouth_angle)
        # ... pygame arc drawing code
```

## Testing Strategy

### Unit Tests (for each phase)
- Board: Test wall detection, pellet removal, pathfinding
- Entities: Test movement, collision detection
- Game logic: Test scoring, lives, level progression

### Integration Tests
- Full game loop without display
- Save/load game state
- Performance (maintain 60 FPS)

### Manual Testing Checklist
- [ ] Can navigate entire maze without getting stuck
- [ ] All pellets are reachable
- [ ] Ghosts don't overlap inappropriately
- [ ] Power pellet timing feels right
- [ ] Death animation plays correctly
- [ ] Score calculates correctly
- [ ] Game difficulty increases with levels

## Common Pitfalls to Avoid

1. **Pixel-perfect collision**: Use tolerance ranges, not exact pixel matching
2. **Ghost house exits**: Implement proper queueing system
3. **Corner cutting**: Pacman should cut corners slightly for smooth feel
4. **Input lag**: Buffer next direction for responsive controls
5. **Ghost AI loops**: Add randomness to prevent predictable patterns

## Debugging Tips

1. Add visual debugging:
   ```python
   # Draw target tiles for ghosts
   if DEBUG_MODE:
       pygame.draw.circle(screen, ghost.color, 
                         (ghost.target_tile[0] * TILE_SIZE + TILE_SIZE//2,
                          ghost.target_tile[1] * TILE_SIZE + TILE_SIZE//2), 5)
   ```

2. Log state transitions
3. Implement frame-by-frame stepping for debugging
4. Save/load specific game states for testing

## Success Criteria

The implementation is complete when:
1. All core mechanics work as in original Pac-Man
2. Game runs at steady 60 FPS
3. No crashes or stuck states
4. Ghosts exhibit distinct personalities
5. Game is challenging but fair
6. Code is modular and well-organized

## Optional Enhancements

After core implementation:
- Fruit bonuses
- Cutscenes between levels
- Multiple maze layouts
- Two-player mode
- AI difficulty settings