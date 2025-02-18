"""Game over view for Pac-Man."""
import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TEXT_COLOR

class GameOverView(arcade.View):
    def __init__(self, score: int, won: bool = False):
        super().__init__()
        self.score = score
        self.won = won
        arcade.set_background_color(arcade.color.BLACK)
        
        # Create Text objects
        title = "You Won!" if won else "Game Over"
        self.title_text = arcade.Text(
            title,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.6,
            TEXT_COLOR,
            64,
            anchor_x="center",
            anchor_y="center"
        )
        
        self.score_text = arcade.Text(
            f"Final Score: {score}",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.45,
            TEXT_COLOR,
            32,
            anchor_x="center",
            anchor_y="center"
        )
        
        self.restart_text = arcade.Text(
            "Press ENTER to Play Again",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.3,
            TEXT_COLOR,
            24,
            anchor_x="center",
            anchor_y="center"
        )
        
        self.quit_text = arcade.Text(
            "Press ESC to Quit",
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
        """Draw the game over screen."""
        self.clear()
        
        # Draw all text objects
        self.title_text.draw()
        self.score_text.draw()
        self.restart_text.draw()
        self.quit_text.draw()

    def on_key_press(self, key, modifiers):
        """Handle key presses."""
        if key == arcade.key.ENTER:
            # Import here to avoid circular import
            from views.game_view import GameView
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)
        elif key == arcade.key.ESCAPE:
            from views.menu_view import MenuView
            menu_view = MenuView()
            self.window.show_view(menu_view) 