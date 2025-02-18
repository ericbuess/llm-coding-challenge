# Arcade Library Documentation (v3.0.0+)

The Python Arcade Library is a modern Python module for creating 2D video games that makes it easier to create 2D games and visual programs.

## Key Features
- Easy to use sprite-based game development
- Built-in physics engine
- Support for tile-based games
- Hardware accelerated graphics
- Sound support
- Controller support
- Window management

## Resources
- Official Documentation: https://api.arcade.academy/en/development/
- Examples: https://api.arcade.academy/en/development/example_code/index.html
- API Reference: https://api.arcade.academy/en/development/api_docs/index.html

## Basic Usage
```python
import arcade

# Create a window
window = arcade.Window(800, 600, "My Game")

# Create a game view
class GameView(arcade.View):
    def on_draw(self):
        self.clear()
        # Draw your game here

# Run the game
arcade.run()
```
