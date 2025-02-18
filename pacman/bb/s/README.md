# Pacman Game

A simple Pacman game implementation using Python and Pygame.

## Features

- Classic Pacman gameplay
- Four ghosts with basic chase AI
- Power pellets that make ghosts vulnerable
- Score tracking
- Win and game over states

## Requirements

- Python 3.x
- Pygame 2.5.2

## Installation

1. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

## How to Play

Run the game:

```bash
python game.py
```

### Controls

- Use arrow keys to move Pacman
- Press ESC to quit the game
- Press SPACE to restart after game over or winning

### Game Rules

- Eat all pellets to win
- Avoid ghosts unless you've eaten a power pellet
- Power pellets make ghosts vulnerable for a limited time
- Eating vulnerable ghosts gives bonus points

### Scoring

- Regular Pellet: 10 points
- Power Pellet: 50 points
- Vulnerable Ghost: 200 points
