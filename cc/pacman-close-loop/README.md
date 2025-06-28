# Pacman Game

A classic Pacman game implementation in Python using Pygame.

## Features

- Classic Pacman gameplay with maze navigation
- Four ghosts with unique AI behaviors:
  - Blinky (Red): Chases Pacman directly
  - Pinky (Pink): Targets 4 tiles ahead of Pacman
  - Inky (Cyan): Complex targeting using Blinky's position
  - Clyde (Orange): Chases when far, scatters when close
- Power pellets that make ghosts vulnerable
- Score tracking and lives system
- Level progression
- Smooth movement and collision detection
- Arrow key controls with input buffering

## Installation

1. Create and activate a virtual environment using uv:
```bash
uv venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
uv pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

## Controls

- **Arrow Keys**: Move Pacman (Up, Down, Left, Right)
- **Space**: Start game / Continue after game over / Next level

## Game Rules

- Eat all pellets to complete the level
- Avoid ghosts (unless they're frightened after eating a power pellet)
- Eating a power pellet makes ghosts vulnerable for 8 seconds
- Score points:
  - Regular pellet: 10 points
  - Power pellet: 50 points
  - Frightened ghost: 200 points
- You have 3 lives

## Technical Details

- Resolution: 672x744 pixels (28x31 tile grid, 24px per tile)
- Target FPS: 60
- Built with Python 3.12 and Pygame 2.5.0