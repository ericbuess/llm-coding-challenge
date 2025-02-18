# Pacman Game

A Python implementation of the classic Pacman arcade game using Pygame.

## Features

- Classic Pacman gameplay
- Four ghosts with different behaviors
- Power pellets that make ghosts vulnerable
- Score tracking and multiple lives
- Sound effects
- Menu, pause, and game over screens

## Requirements

- Python 3.x
- Pygame 2.5.2

## Installation

1. Make sure you have Python 3.x installed
2. Install the required package:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

1. Run the game:
   ```bash
   python main.py
   ```

2. Controls:
   - Arrow keys to move Pacman
   - ESC to pause/unpause
   - ENTER to start new game or restart after game over

## Game Rules

- Guide Pacman through the maze collecting pellets
- Each regular pellet is worth 10 points
- Power pellets are worth 50 points and make ghosts vulnerable
- Eating a vulnerable ghost is worth 200 points
- Avoid ghosts in their normal state
- Collect all pellets to complete the level

## Project Structure

- `main.py`: Entry point and game loop
- `game.py`: Main game logic
- `level.py`: Level loading and management
- `settings.py`: Game constants and configuration
- `utils.py`: Helper functions
- `entities/`: Game object classes
  - `base.py`: Base entity class
  - `pacman.py`: Pacman player class
  - `ghost.py`: Ghost enemy class
  - `pellet.py`: Regular pellet class
  - `powerpellet.py`: Power pellet class
  - `wall.py`: Wall obstacle class

## Asset Credits

The game requires the following assets in the `assets` directory:

- Images (`assets/images/`):
  - `pacman.png`
  - `ghost_red.png`
  - `ghost_blue.png`
  - `ghost_pink.png`
  - `ghost_orange.png`
  - `ghost_frightened.png`
  - `ghost_eaten.png`
  - `wall.png`
  - `pellet.png`
  - `powerpellet.png`

- Sounds (`assets/sounds/`):
  - `pacman_chomp.wav`
  - `ghost_eaten.wav`
  - `powerup.wav`

Note: Asset files are not included in this repository. You'll need to provide your own assets or create placeholder images.
