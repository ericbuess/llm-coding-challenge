# Pac-Man Game in Python

A classic Pac-Man arcade game implemented in Python using Pygame.

## Features

- Classic Pac-Man maze navigation with pellets and power pellets
- Four ghosts with different AI behaviors:
  - Blinky (red): Directly targets Pac-Man
  - Pinky (pink): Targets 4 tiles ahead of Pac-Man
  - Inky (cyan): Uses a complex targeting algorithm involving Blinky
  - Clyde (orange): Targets Pac-Man when far away, scatters when close
- Ghost behavior states: Scatter, Chase, Frightened, and Eaten modes
- Authentic ghost movement and targeting algorithms
- Score tracking and high score persistence
- Lives system
- Multiple game states: Start, Playing, Paused, Game Over, Win
- Level progression when all pellets are collected

## Requirements

- Python 3.x
- Pygame

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:
   ```
   pip install pygame
   ```

## How to Play

Run the game by executing:
```
python main.py
```

### Controls

- **Arrow Keys** or **WASD**: Move Pac-Man
- **P**: Pause/Resume game
- **R**: Reset game
- **ESC**: Return to title screen
- **Enter/Return**: Start game or continue after game over

### Game Objective

- Navigate Pac-Man through the maze and eat all pellets
- Avoid ghosts unless you've eaten a power pellet
- Eat power pellets to make ghosts vulnerable for a short time
- Advance through levels by clearing all pellets

## Game Structure

The game is organized in a modular structure:

- `main.py`: Entry point and main game loop
- `constants.py`: Game constants and configurations
- `maze.py`: Maze layout and collision detection
- `entities.py`: Pac-Man and ghost entity classes
- `score.py`: Score management
- `game_states.py`: Game state management

## Customization

- Adjust game speed, difficulty, and visuals by modifying `constants.py`
- Change the maze layout by modifying the layout array in `maze.py`
- Add sound effects by placing .wav files in a "sounds" directory and uncommenting the sound loading code

## Credits

This implementation follows the specifications of the original Pac-Man arcade game, including the ghost AI behaviors and movement patterns. The code structure is designed to be modular and easy to understand.

## License

This project is available for educational purposes. 