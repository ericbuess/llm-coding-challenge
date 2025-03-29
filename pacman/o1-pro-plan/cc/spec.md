Below is an extensive **technical specification** for creating a Pac-Man game in Python from scratch, suitable for direct consumption by an LLM or a developer. The specification includes details on game structure, modules, class definitions, data flow, logic for movement and collision, ghost AI modes, scoring, audio, and more. It is designed so the implementing system needs no further clarifications.

---

## 1. Overview

Pac-Man is a tile-based arcade maze game. The player navigates Pac-Man through a grid containing pellets, power pellets, walls, and four ghost enemies. The objective is to consume all the pellets and avoid being caught by the ghosts. Eating power pellets causes the ghosts to become vulnerable for a short duration, allowing Pac-Man to eat them for extra points.

### 1.1 Key Requirements

1. **Tile-based Maze**: A 2D grid representing walls, paths, pellets, and power pellets.
2. **Player Entity (Pac-Man)**: Controlled by arrow keys (or WASD) with smooth movement on a grid.
3. **Ghosts**:
   - Four ghosts, each with distinct colors and personalities: Blinky (red), Pinky (pink), Inky (cyan), and Clyde (orange).
   - Each ghost has a scatter mode, chase mode, frightened mode (when a power pellet is active), and a brief transition mode between scatter/chase.
4. **Scoring**: Eating pellets, power pellets, ghosts (when frightened), bonus fruit, and tracking high scores.
5. **Game States**: Start screen, playing, pausing, losing a life, game over, winning (when all pellets are consumed).
6. **Animations**: Sprites for Pac-Man’s mouth movement, ghosts’ animations, frightened mode flicker, etc.
7. **Audio**: Basic sound effects for pellet munching, ghost eaten, death jingle, etc. (Optional if needed).

---

## 2. Project Structure

The code can be structured into multiple Python modules or remain in a single file. A recommended approach is to have at least these components:

1. **`main.py`** (or a single-file approach):
   - Entry point for the game.
   - Defines the main game loop.
   - Creates and coordinates all main objects (Pac-Man, Ghosts, Maze, Score).
2. **`constants.py`** (optional, can be in `main.py` if a single-file approach):
   - Holds global constants: screen size, tile size, frame rate, colors, ghost speeds, etc.
3. **`maze.py`**:
   - Contains the maze layout (walls, pellets, power pellets).
   - Responsible for loading a level layout from data (a matrix or text file).
   - Provides collision detection helpers.
4. **`entities.py`**:
   - Defines classes for `Pacman`, `Ghost`, and possibly a generic `Entity` base class.
5. **`game_states.py`** (optional):
   - Manages different states: Start, Play, Pause, Game Over, etc.
6. **`score.py`**:
   - Manages scoring logic, high score updates, UI rendering of the score.

---

## 3. Detailed Specification

### 3.1 Constants and Configuration

All critical values should be centrally defined for easy tweaking:

1. **Tile Size**: E.g., `TILE_SIZE = 16` or `TILE_SIZE = 20`.
2. **Grid Dimensions**: E.g., `GRID_WIDTH = 28`, `GRID_HEIGHT = 31`.
3. **Window Size**: e.g., `SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE`, `SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE`.
4. **Frame Rate**: e.g., `FPS = 60`.
5. **Speeds**:
   - Pac-Man speed in tiles/second (or px/sec).
   - Ghost speed, slightly less or equal to Pac-Man’s normal speed.
   - Speed modifications in frightened mode or when ghosts are returning to the ghost house.
6. **Color Definitions** (if needed for Pygame rendering):
   - Pac-Man color (yellow).
   - Ghost colors (red, pink, cyan, orange).
   - Maze wall color, text color, background color, etc.
7. **Time Durations**:
   - Scatter mode length (default ~7 seconds each cycle, though actual arcade rules vary).
   - Chase mode length.
   - Frightened mode length (power pellet effect).
   - Ghost respawn times after being eaten.

### 3.2 Maze Layout

The maze can be defined in any of the following ways:

- **Text-based file** that encodes walls (`#`), pellets (`.`), power pellets (`o`), empty paths (` `), ghost house region, etc.
- **List of strings** in Python that represent each row of the maze.
- A **2D array** with numeric codes for different tile types.

For example:
```
############################
#............##............#
#....##......##......##....#
#....##......##......##....#
#....##..............##....#
#....##......####....##....#
#............####..........#
############################
```
(Truncated for brevity; fill with the full layout.)

The **`Maze`** class should:

1. **Load Layout**:
   - Parse a 2D layout.
   - Identify walls, path tiles, pellet tiles, power pellets, ghost house, possible spawn positions.
2. **Store Pellet State**:
   - Track whether a pellet or power pellet remains at a given tile or if it’s eaten.
3. **Collision Detection**:
   - Provide a method `is_wall(x, y)` that returns `True/False` based on whether the tile is a wall.
   - Provide a method `can_move_to(x, y)` that checks if a tile is navigable (not a wall, within bounds).
4. **Pellet Consumption**:
   - If Pac-Man moves onto a tile containing a pellet or power pellet, remove it and increment the score appropriately.
5. **Render**:
   - A method to draw the maze walls, remaining pellets, and power pellets onto the screen.

#### 3.2.1 Maze Coordinates vs. Screen Coordinates

- Maze is typically in **tile coordinates** (e.g., `0 <= tile_x < 28`, `0 <= tile_y < 31`).
- Rendering uses **pixel coordinates**: `pixel_x = tile_x * TILE_SIZE`, `pixel_y = tile_y * TILE_SIZE`.
- Entities should store position in floating pixel coordinates for smooth movement, but collision checks use integer tile coordinates (by dividing the pixel position by `TILE_SIZE`).

---

### 3.3 Entity Classes

#### 3.3.1 Base Class: `Entity`
Common attributes and methods for Pac-Man and Ghosts:

1. **Attributes**:
   - `x`, `y` (float positions in pixel coordinates).
   - `direction` (current moving direction, e.g., `("left", "right", "up", "down")` or vector form).
   - `speed` (pixels per second or fraction per frame).
   - `target_tile` or `intended_direction` (the next direction to move if possible).
2. **Methods**:
   - `update(dt, maze)`: Move the entity according to current direction, handle collision with walls.
   - `move(dx, dy)`: Adjust `x` and `y` by `dx` and `dy`.
   - `get_tile_pos()`: Return `(tile_x, tile_y)` based on `(x, y)`.

#### 3.3.2 `Pacman` Class
Inherits from `Entity`, with additional logic:

1. **Attributes**:
   - `lives`: Remaining lives.
   - `power_mode`: Boolean or timer-based to indicate if Pac-Man is powered-up (after eating a power pellet).
2. **Methods**:
   - `handle_input(input_state, maze)`: Adjust intended direction if the next tile in that direction is not a wall.
   - `check_pellet_collision(maze, score_manager)`: If Pac-Man occupies a tile containing a pellet or power pellet, remove it and update score. If it’s a power pellet, set frightened mode timers for ghosts.
   - `reset_position()`: Called on new life or game start.

Movement specifics for Pac-Man:
- Only turn at tile centers. Pac-Man checks if the player’s intended direction is valid at the next tile boundary.

#### 3.3.3 `Ghost` Class
Each ghost shares a base with unique AI logic:

1. **States**:
   - `SCATTER`: Move towards a scatter corner target tile.
   - `CHASE`: Move according to the ghost’s chase logic (targeting Pac-Man’s tile or predicted tile, depending on the ghost).
   - `FRIGHTENED`: Wander randomly at reduced speed, can be eaten by Pac-Man.
   - `EATEN`: Return to ghost house for respawn.
2. **Attributes**:
   - `ghost_type`: e.g., `blinky`, `pinky`, `inky`, `clyde`.
   - `current_state`: One of the above states.
   - `state_timer`: Tracks how long a state has been active to determine transitions (scatter <-> chase).
   - `frightened_timer`: Time left in frightened mode.
3. **Methods**:
   - `update(dt, maze, pacman_position)`: 
     - Evaluate state logic (scatter, chase, etc.).
     - Move accordingly, checking for collisions with walls.
     - If frightened_time is > 0, decrement it each frame. When it hits zero, revert to chase or scatter.
     - If eaten, move towards the ghost house, then switch to scatter/chase once respawned.
   - `set_state(state)`: Switch states, reset any timers if necessary.
   - `get_target_tile(pacman_position, pacman_direction)`: 
     - For chase mode, define per-ghost logic:
       - **Blinky**: Target Pac-Man’s current tile.
       - **Pinky**: Target 4 tiles ahead of Pac-Man’s direction.
       - **Inky**: A bit more complex, uses Blinky’s position + a reflection of Pac-Man’s direction. (Implementation details vary.)
       - **Clyde**: If distance to Pac-Man is > 8 tiles, chase Pac-Man; else scatter.
     - For scatter mode, target the ghost’s corner (top-right, top-left, bottom-right, or bottom-left).
4. **Pathfinding**:
   - Use the ghost’s current tile, the target tile, and select the best next step according to a simple heuristic (like BFS or A*). For original arcade behavior, a simplified “turn priority” approach is often used (left turn, straight, right turn, etc., avoiding reversing direction unless forced).

---

### 3.4 Game State Management

At a high level, define an enum or constants for states:

- **`GameState.START`**: Show title screen, wait for input to start.
- **`GameState.PLAY`**: Normal gameplay.
- **`GameState.PAUSE`**: Pause logic if needed.
- **`GameState.GAME_OVER`**: Display final score, then back to START or exit.
- **`GameState.WIN`**: If the player eats all pellets. Possibly merges with game over or new level logic.

In each state:
- The **render** step draws relevant UI or text prompts.
- The **update** step handles logic for that state only (e.g., no entity movement in START or GAME_OVER).

---

### 3.5 Scoring and Lives

#### 3.5.1 Scoring
- **Pellet**: 10 points
- **Power Pellet**: 50 points
- **Ghost** (in frightened mode, sequential): 
  - 1st ghost eaten in a single power pellet: 200 points
  - 2nd ghost: 400
  - 3rd: 800
  - 4th: 1600
- **Bonus Fruit**: Typically 100 to 5000 points (depends on level). For simplicity, use a single value or skip if desired.

Implement a `ScoreManager` or a simple global variable:
- `current_score`
- `high_score` (read from a file or static memory)

#### 3.5.2 Lives
- Pac-Man starts with 3 (configurable).
- On collision with a non-frightened ghost:
  - Decrement a life, reset positions. If `lives == 0`, go to `GAME_OVER`.

---

### 3.6 Ghost AI Logic Details

To faithfully mimic the original style, define a cycle of **scatter** and **chase**:

1. Start the round with a short scatter period (the ghosts go to corners).
2. Then switch to chase for a specific duration.
3. Alternate between scatter and chase a few times in the early part of the level. Typically the pattern is:
   - Scatter for 7s -> Chase for 20s -> Scatter for 7s -> Chase for 20s -> Scatter for 5s -> Chase indefinite
   - Actual timings vary by level but use a simplified version if needed.

When **Frightened**:
- Ghosts move slower.
- They select random directions at each intersection.
- If Pac-Man collides with them in this state, they become “EATEN,” awarding points. 
- The ghost sprite changes (blue color or a frightened sprite). 
- The ghost’s eyes remain when “EATEN,” traveling back to the ghost house at double speed, ignoring normal collisions. 
- Once it reaches the ghost house, it returns to normal ghost mode (scatter or chase depending on the cycle).

---

### 3.7 Controls and Input Handling

Typically, we capture key events:

- **Up/Down/Left/Right** (or WASD) sets `Pacman.intended_direction`. 
- On each update, check if Pac-Man can turn in that direction at the next tile boundary.
- **ESC** might pause or quit.

---

### 3.8 Rendering

1. **Maze**: Draw walls (either tile-based images or shapes).
2. **Pellets**: Small dots. 
3. **Power Pellets**: Larger dots with possibly a blinking animation. 
4. **Entities**:
   - **Pac-Man** animation: mouth open/close. Usually 2-3 frames repeated while moving. 
   - **Ghosts**: animate using 2-frame cycles for movement, and have distinct sprites for each state (normal, frightened, eaten).
5. **Score and Lives**:
   - Display score at the top of the screen.
   - Display leftover lives near the bottom-left corner with small Pac-Man icons or a numeric representation.

---

### 3.9 Sound Effects (Optional)

1. **Waka/Waka**: Looping munch sound for pellets.
2. **Ghost Eaten**: Short sound when a ghost is eaten.
3. **Death**: Pac-Man’s death tune.
4. **Intermission**: If implementing transitions or cutscenes.

---

### 3.10 Main Game Loop

1. **Initialize**:
   - Initialize your graphics library (Pygame or other).
   - Create `Maze`, `Pacman`, `Ghost` objects, `ScoreManager`.
   - Set state to `START`.
2. **Loop**:
   1. **Event Handling**:
      - Check for keyboard events to set Pac-Man’s intended direction or handle pausing/quitting.
   2. **Update** (only if `state == PLAY`):
      - `Pacman.update(dt, maze)`
      - For each ghost: `ghost.update(dt, maze, pacman_position)`
      - Check collisions: 
        - Pac-Man with ghosts. If ghost is not frightened -> lose life. If frightened -> ghost eaten.
        - Pac-Man with pellets or power pellets -> update score, set ghost states if power pellet.
      - Check if all pellets are eaten -> transition to WIN or next level.
   3. **Render**:
      - Clear screen.
      - Draw maze (walls, remaining pellets).
      - Draw Pac-Man and ghosts.
      - Draw scores, lives.
      - Draw any additional UI (start screen or game over screen if not in PLAY).
   4. **Tick**: Delay to maintain consistent FPS.
3. **Exit** when user quits or after game over if no continue logic is present.

---

### 3.11 Edge Cases & Additional Considerations

1. **Integer rounding**: Must handle tile boundaries carefully to avoid “jitter” or misalignment in turns.
2. **Ghost House**: Some versions keep ghosts inside for a short time at round start. If implementing, track a timer for each ghost to exit the house.
3. **Wrap-around Tunnels**: Classic Pac-Man has tunnels at the left/right edges. Implement by checking if Pac-Man (or ghosts) move beyond the left boundary, they reappear at the right boundary (and vice versa).
4. **Fruit / Bonus Items**: Appear in the center, after certain numbers of pellets eaten. (Optional advanced feature.)
5. **Multiple Levels**: If implementing more levels, ghost speeds and timings can increase. Maze or color can change. (Optional.)
6. **Performance**: For BFS or A*, caching paths and employing partial recalculations can help. For a small grid, it’s usually fine to do a BFS each intersection.

---

## 4. Step-by-Step Implementation Outline

1. **Setup**:
   - Choose a library (Pygame recommended for easy 2D rendering and input).
   - Initialize constants, window, FPS clock.
2. **Maze Creation**:
   - Create a matrix from a text file or embedded layout that marks walls, pellets, power pellets.
   - Convert each tile to a `Tile` object if desired, or store them in arrays.
3. **Entity Classes**:
   - Create an `Entity` base for movement, collision checks with `Maze`.
   - Create `Pacman` with specialized input handling. 
   - Create `Ghost` with separate logic, states, and a method for choosing direction based on state.
4. **Ghost AI**:
   - Write state machine logic (scatter, chase, frightened, eaten). 
   - Timers that switch ghost states automatically.
5. **Main Loop**:
   - While `running`:
     1. Read input events, update game state (pause, exit, or control Pac-Man).
     2. Update the world if state=PLAY:
        - Move Pac-Man, handle pellet consumption, check collisions.
        - Move ghosts, handle AI states, check collisions with Pac-Man.
        - Manage score changes, lives, and game transitions.
     3. Render everything.
     4. Tick clock to maintain FPS.
6. **Polish**:
   - Add sound effects, animations, UI screens, transitions, fruit spawning, etc.
7. **Testing**:
   - Check corner cases: collisions near edges, ghost frightened timers, multiple power pellets in short time, etc.

---

## 5. Final Notes

By following this specification step by step, an LLM or developer should be able to implement a functioning Pac-Man game in Python **without additional clarifications**. All fundamental details—maze definition, entity states, collision, ghost AI, scoring, and game loop structure—have been described thoroughly. 

Adjust or extend features (multiple levels, fruit items, advanced ghost AI logic matching the exact arcade code, etc.) as desired. The core remains: tile-based movement, state machines for ghosts, pellet-based scoring, and a structured main loop that updates and renders all components.

---

**End of Specification**
