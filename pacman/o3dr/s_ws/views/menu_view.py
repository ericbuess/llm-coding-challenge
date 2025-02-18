"""Menu view for Pac-Man game."""
import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FONT_SIZE

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        
    def on_show_view(self):
        """Called when switching to this view."""
        arcade.set_background_color(arcade.color.BLACK)
    
    def on_draw(self):
        """Draw the menu."""
        self.clear()
        
        # Draw title
        arcade.draw_text(
            "PAC-MAN",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 3 // 4,
            arcade.color.YELLOW,
            FONT_SIZE * 3,
            anchor_x="center",
            anchor_y="center"
        )
        
        # Draw instructions
        arcade.draw_text(
            "Use Arrow Keys to Move",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            arcade.color.WHITE,
            FONT_SIZE,
            anchor_x="center",
            anchor_y="center"
        )
        
        arcade.draw_text(
            "P to Pause",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - FONT_SIZE * 1.5,
            arcade.color.WHITE,
            FONT_SIZE,
            anchor_x="center",
            anchor_y="center"
        )
        
        arcade.draw_text(
            "Press SPACE to Start",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 4,
            arcade.color.YELLOW,
            FONT_SIZE * 1.5,
            anchor_x="center",
            anchor_y="center"
        )
    
    def on_key_press(self, key, modifiers):
        """Handle key press events."""
        if key == arcade.key.SPACE:
            # Switch to the game view
            from views.game_view import GameView
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)
