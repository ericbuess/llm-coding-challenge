# Pac-Man Project Development Guidelines

## Environment Setup
- Use conda env `llmbattle` for all development: `conda activate llmbattle`
- Environment includes Python 3.13.2 and Pygame 2.6.1

## Project Structure
- Follow modular design with files:
  - `main.py`: Entry point and game loop
  - `constants.py`: Game constants (screen size, speeds, colors)
  - `maze.py`: Maze layout and collision detection
  - `entities.py`: Pac-Man and ghost classes
  - `game_states.py`: Game state management
  - `score.py`: Scoring logic

## Coding Guidelines
- **Naming**: Use snake_case for variables/functions, PascalCase for classes
- **Documentation**: Add docstrings to classes and non-trivial functions
- **Type Hints**: Use Python type annotations for function parameters and returns
- **Constants**: Define game constants in UPPERCASE
- **Error Handling**: Use try/except blocks with specific exception types
- **Imports**: Group standard library, third-party, and local imports with blank lines

## Run/Test Commands
- Run game: `python main.py`
- Run specific test: `pytest tests/test_file.py::test_function -v`
- Run all tests: `pytest`
- Check code style: `flake8 .`

## Implementation Notes
- Use Pygame for rendering, input handling, and timing
- Follow the spec.md file for detailed game mechanics
- Implement proper state transitions between game phases