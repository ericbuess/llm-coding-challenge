# Pac-Man Game

A complete implementation of the classic Pac-Man arcade game using Python and Pygame.

## Features

- Tile-based maze with walls, pellets, and power pellets
- Pac-Man with proper movement and animation
- Four ghosts with unique AI behaviors:
  - Blinky (red): Directly targets Pac-Man
  - Pinky (pink): Targets 4 tiles ahead of Pac-Man
  - Inky (cyan): Uses a vector from Blinky to target Pac-Man
  - Clyde (orange): Targets Pac-Man when far, switches to scatter mode when close
- Ghost states: Scatter, Chase, Frightened, and Eaten modes
- Score tracking with high score persistence
- Sound effects system (sound files need to be added)
- Game states: start, play, pause, game over, and win

## Installation

### Prerequisites

- Python 3.6 or higher

### macOS Installation

On macOS, you might encounter issues with SDL dependencies when installing pygame directly. There are two recommended approaches:

#### Option 1: Install using Homebrew (recommended)

```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install SDL2 dependencies
brew install sdl2 sdl2_gfx sdl2_image sdl2_mixer sdl2_net sdl2_ttf

# Install pygame
pip install -r requirements.txt
```

#### Option 2: Use conda

```bash
# Install Miniconda if you don't have it
# Create a conda environment
conda create -n pacman python=3.9
conda activate pacman

# Install pygame through conda
conda install -c conda-forge pygame
```

### Windows/Linux Installation

```bash
pip install -r requirements.txt
```

## How to Play

Run the game using:

```bash
python run_game.py
```

Or on macOS/Linux:

```bash
./run_game.py
```

### Controls

- Arrow keys or WASD: Move Pac-Man
- Space: Start game / Continue after game over
- ESC: Pause/Resume game

## Game Structure

- `constants.py`: Game configuration values
- `main.py`: Game loop and state management
- `entities.py`: Pac-Man and Ghost classes
- `maze.py`: Maze layout and collision detection
- `score.py`: Score management
- `sound.py`: Sound effects
- `run_game.py`: Entry point to start the game

## Adding Sound Effects

To add sound effects to the game, create a `sounds` directory and add the following WAV files:

- `start.wav`: Game start sound
- `chomp.wav`: Pellet eating sound
- `power_pellet.wav`: Power pellet sound
- `eat_ghost.wav`: Sound when eating a ghost
- `death.wav`: Pac-Man death sound
- `extra_life.wav`: Extra life sound
- `fruit.wav`: Fruit collection sound

## Troubleshooting

### Common Issues

- **SDL Error on macOS**: Follow the installation steps for macOS above.
- **Sound files not found**: The game will still run if sound files are missing; it will print a message that they weren't found.
- **Game performance issues**: If the game runs slowly, try closing other applications to free up system resources.
