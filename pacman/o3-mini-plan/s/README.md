# Pacman Game

A Python implementation of the classic Pacman arcade game using Pygame.

## Features

- Classic Pacman gameplay mechanics
- Four ghosts with different behaviors
- Power pellets that make ghosts vulnerable
- Score tracking and multiple lives
- Pause functionality
- Level progression

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

Run the game:

```bash
python main.py
```

### Controls

- Arrow keys to move Pacman
- ESC to pause/unpause
- R to restart (when game over)

### Gameplay

- Guide Pacman through the maze collecting pellets
- Avoid ghosts unless you've eaten a power pellet
- Collect all pellets to advance to the next level
- Power pellets make ghosts vulnerable temporarily
- Eat frightened ghosts for bonus points

### Scoring

- Regular Pellet: 10 points
- Power Pellet: 50 points
- Ghost: 200 points

## Game Elements

- **Pacman**: The player character (yellow)
- **Ghosts**:
  - Red: Aggressive, chases directly
  - Pink: Tries to ambush
  - Blue: Unpredictable movement
  - Orange: Random behavior
- **Pellets**: Small white dots that must be collected
- **Power Pellets**: Larger white dots that make ghosts vulnerable
- **Walls**: Blue barriers that cannot be passed through

## Development

The game is structured in a modular way with separate classes for:

- Game management
- Level loading
- Entity management (Pacman, ghosts, pellets)
- Collision detection
- State management

Feel free to modify and enhance the game!
