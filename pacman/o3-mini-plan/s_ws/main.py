"""
Main entry point for the Pacman game.
"""
import pygame
from game import Game
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

def main():
    """Initialize pygame and start the game."""
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()  # For sound
    
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pacman")
    
    # Create clock for timing
    clock = pygame.time.Clock()
    
    # Create and start game
    game = Game(screen)
    
    # Main game loop
    while game.running:
        # Process input/events
        game.process_events()
        
        # Update game state
        game.update()
        
        # Draw everything
        game.draw()
        
        # Update the display
        pygame.display.flip()
        
        # Control the game's framerate
        clock.tick(FPS)
    
    # Clean up
    pygame.quit()

if __name__ == "__main__":
    main()
