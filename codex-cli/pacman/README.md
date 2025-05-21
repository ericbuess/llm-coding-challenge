# Pac-Man Clone in Python

This project is a simple implementation of the classic Pac-Man game using Python and Pygame.

## Features
- Grid-based map loaded from a text file
- Basic movement for Pac-Man with arrow keys
- Randomly-moving ghosts
- Dot (pellet) collection and scoring

## Requirements
- Python 3.7+
- Pygame

## Setup
```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Game
```bash
python main.py
```

## Development
- Map layout is defined in `pacman/map.txt`
- Configuration (colors, tile size, FPS) in `pacman/settings.py`