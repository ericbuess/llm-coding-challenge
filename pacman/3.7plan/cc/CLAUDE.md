# Project Setup and Guidelines

## Environment
- Use conda env `llmbattle` for all development: `conda activate llmbattle`
- Dependencies: pygame, numpy

## Build Commands
- Run game: `python main.py`
- Run tests: `pytest tests/`
- Run specific test: `pytest tests/test_file.py::test_function`
- Typecheck: `mypy .`
- Lint: `flake8 .`

## Code Style
- PEP 8 compliant
- Use 4 spaces for indentation
- Maximum line length: 88 characters
- Keep imports organized: stdlib, third-party, local
- Type annotations required for function parameters and return values
- Docstrings follow Google style

## Naming Conventions
- Classes: CamelCase (e.g., `PacMan`, `GhostEntity`)
- Functions/variables: snake_case (e.g., `update_position`, `current_score`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_SPEED`, `SCREEN_WIDTH`)

## Error Handling
- Use explicit exception handling with specific exception types
- Avoid silent failures; log errors when appropriate
- Use assertions for internal state validation

## Project Structure
Follow the modular design in the specification with separate files for:
- Main game entry point
- Entity system (Pac-Man, ghosts, pellets)
- Maze representation
- Game states management
- Rendering
- Input handling