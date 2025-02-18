"""Main menu view for Pac-Man."""
import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, TEXT_COLOR

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        
        # Create Text objects
        self.title_text = arcade.Text(
            TITLE,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.6,
            TEXT_COLOR,
            64,
            anchor_x="center",
            anchor_y="center"
        )
        
        self.start_text = arcade.Text(
            "Press ENTER to Start",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.4,
            TEXT_COLOR,
            32,
            anchor_x="center",
            anchor_y="center"
        )
        
        self.move_text = arcade.Text(
            "Arrow Keys to Move",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.3,
            TEXT_COLOR,
            24,
            anchor_x="center",
            anchor_y="center"
        )
        
        self.pause_text = arcade.Text(
            "P to Pause",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.25,
            TEXT_COLOR,
            24,
            anchor_x="center",
            anchor_y="center"
        )

    def on_show_view(self):
        """Called when switching to this view."""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """Draw the menu."""
        self.clear()
        
        # Draw all text objects
        self.title_text.draw()
        self.start_text.draw()
        self.move_text.draw()
        self.pause_text.draw()

    def on_key_press(self, key, modifiers):
        """Handle key presses."""
        if key == arcade.key.ENTER:
            # Import here to avoid circular import
            from views.game_view import GameView
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view) 