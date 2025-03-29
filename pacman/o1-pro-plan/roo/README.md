# Pac-Man Game in Python

A faithful recreation of the classic Pac-Man arcade game, built in Python using Pygame.

## Features

- Classic Pac-Man maze with pellets and power pellets
- Four ghosts with distinct personalities and AI behaviors:
  - Blinky (red): Directly targets Pac-Man
  - Pinky (pink): Targets 4 tiles ahead of Pac-Man
  - Inky (cyan): Uses both Pac-Man and Blinky's positions for targeting
  - Clyde (orange): Alternates between targeting Pac-Man and running away
- Multiple game states: start screen, gameplay, pause, game over, and win
- Score tracking with high score saving
- Sound effects (if sound files are available)

## Requirements

- Python 3.6 or higher
- Pygame library

## Installation

1. Make sure you have Python installed on your system.
2. Install the Pygame library if you don't have it already:
   ```
   pip install pygame
   ```

## How to Play

Run the game by executing the main.py file:

```
python main.py
```

### Controls

- Arrow keys or WASD to move Pac-Man
- P or ESC to pause the game
- Space or Enter to start the game and navigate menus

## Sound Effects (Optional)

For sound effects, create a `sounds` directory in the game folder and add these WAV files:
- `munch.wav` - Sound when Pac-Man eats a pellet
- `power_pellet.wav` - Sound when Pac-Man eats a power pellet
- `eat_ghost.wav` - Sound when Pac-Man eats a ghost
- `death.wav` - Sound when Pac-Man dies
- `start.wav` - Music that plays at the start screen

The game will run without sound files if they are not available.

## Game Structure

- `main.py` - Main game loop and initialization
- `constants.py` - Game constants and configuration
- `maze.py` - Maze layout and collision detection
- `entities.py` - Pac-Man and Ghost classes
- `score.py` - Score management
- `game_states.py` - Game state management

## Acknowledgements

This game is based on the original Pac-Man arcade game developed by Namco in 1980.