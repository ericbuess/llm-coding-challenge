# Pac-Man Game

A Python implementation of the classic Pac-Man arcade game using the Arcade library.

## Features

- Classic Pac-Man gameplay mechanics
- Ghost AI with different personalities
- Power pellets and ghost state changes
- Score tracking and multiple lives
- Tile-based maze layout using Tiled map editor
- Sound effects and animations

## Requirements

- Python 3.9 or higher
- Arcade library 3.x
- Pillow for image processing
- pytiled-parser for loading Tiled maps

## Installation

1. Ensure you are in the correct conda environment:
   ```bash
   conda activate operator
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

To start the game, run:
```bash
python main.py
```

## Controls

- Arrow keys to move Pac-Man
- P to pause/unpause the game
- Space to start game or restart after game over

## Project Structure

- `assets/` - Contains all game assets (images, sounds, tilemaps)
- `views/` - Contains different game views (menu, gameplay)
- `utils/` - Utility functions and asset management
- `constants.py` - Game constants and configuration
- `player.py` - Pac-Man player class
- `ghost.py` - Ghost enemy classes with AI
- `maze.py` - Maze and level management
- `main.py` - Game entry point

## Asset Requirements

The game expects the following assets in the respective directories:

### Images (`assets/images/`)
- `pacman_right_1.png`, `pacman_right_2.png` - Pac-Man animation frames
- `pacman_left_1.png`, `pacman_left_2.png`
- `pacman_up_1.png`, `pacman_up_2.png`
- `pacman_down_1.png`, `pacman_down_2.png`
- `blinky.png`, `pinky.png`, `inky.png`, `clyde.png` - Ghost sprites
- `ghost_frightened.png` - Blue ghost sprite
- `ghost_eaten.png` - Ghost eyes sprite

### Sounds (`assets/sounds/`)
- `chomp.wav` - Pellet eating sound
- `power_pellet.wav` - Power pellet activation
- `ghost_eaten.wav` - Ghost eating sound
- `death.wav` - Pac-Man death sound

### Tilemaps (`assets/tilemaps/`)
- `level1.tmx` - Main maze layout (create using Tiled map editor)

## License

This is a prototype implementation for educational purposes.
