# Python Pac-Man Clone

A simple Pac-Man clone implemented in Python using the Pygame library, based on a provided technical specification.

## Features

*   Classic Pac-Man maze layout.
*   Player-controlled Pac-Man using Arrow keys or WASD.
*   Four ghosts (Blinky, Pinky, Inky, Clyde) with distinct Scatter and Chase AI behaviors.
*   Frightened mode for ghosts after Pac-Man eats a power pellet.
*   Pellet and power pellet consumption.
*   Scoring system including points for pellets, power pellets, and eating ghosts.
*   Lives system.
*   Basic game states: Start Screen, Playing, Paused, Game Over, Win Screen.
*   High score persistence (saved in `highscore.txt`).

## Requirements

*   Python 3.x
*   Pygame (`pip install -r requirements.txt`)

## How to Run

1.  Ensure you have Python and pip installed.
2.  Clone or download the project files.
3.  Navigate to the project directory in your terminal.
4.  Install the necessary package:
    ```bash
    pip install -r requirements.txt
    ```
5.  Run the game:
    ```bash
    python main.py
    ```

## Controls

*   **Arrow Keys / WASD**: Move Pac-Man
*   **ESC**: Pause/Unpause game (during play)
*   **Enter/Space**: Start game from title screen or restart after Game Over/Win
*   **ESC**: Quit game from Game Over/Win screen

## Code Structure

*   `main.py`: Main game loop, event handling, state management.
*   `constants.py`: Game constants (colors, speeds, sizes, etc.).
*   `maze.py`: Defines the `Maze` class, handles layout, drawing, and pellet logic.
*   `entities.py`: Defines `Entity`, `Pacman`, and `Ghost` classes, handling movement and AI.
*   `score.py`: Defines the `ScoreManager` class for tracking score and high score.
*   `requirements.txt`: Lists Python package dependencies.
*   `highscore.txt`: Stores the high score between sessions. 