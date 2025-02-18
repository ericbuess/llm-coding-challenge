# Pac-Man Prototype

This project is a fully-featured, single-player Pac-Man prototype built in Python 3.9+ on macOS using Arcade 3.x. It leverages modern game development practices including the use of Arcade's scene, tilemap, and view systems.

## Project Structure

The repository is organized as follows:

pacman/o3dr/s/
├── assets/ # Contains images, tilemaps (designed using Tiled), and sounds
├── constants.py # Global configurations (screen size, speeds, scoring, etc.)
├── main.py # The entry point that creates the Arcade window and shows the initial view
├── game.py # Shared game logic or Game class (if needed)
├── player.py # Defines the Pacman class (arcade.Sprite subclass)
├── ghost.py # Defines the Ghost class with simple AI logic
├── maze.py # Loads and manages the maze using Arcade's tilemap support
├── views/ # Contains different game state views (menu_view, game_view, gameover_view)
└── utils/
└── asset_manager.py # Asset loader and caching helper

## Documentation

Detailed documentation and guidance for this project can be found in the docs directory:

pacman/o3dr/s/docs/

- arcade.md: Overview and best practices for using Arcade 3.x.
- pytiled_parser.md: Information on handling Tiled maps for the maze.
- pathlib.md: Details regarding asset management and file path handling.

Please refer to these documents for more information on how the underlying libraries work and design choices made in the implementation.

## Running the Game

To run the game prototype, execute:

    python main.py

Enjoy building and extending this prototype!
