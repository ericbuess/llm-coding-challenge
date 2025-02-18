"""Main entry point for Pac-Man game."""
import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE
from views.menu_view import MenuView

def main():
    """Main function to start the game."""
    # Create the window
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    
    # Create and show the menu view
    menu_view = MenuView()
    window.show_view(menu_view)
    
    # Run the game
    arcade.run()

if __name__ == "__main__":
    main()
