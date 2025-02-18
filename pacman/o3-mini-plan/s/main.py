import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from game import Game

def main():
    # Initialize Pygame
    pygame.init()
    
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pacman")
    
    # Create and run the game
    game = Game(screen)
    game.run()
    
    # Clean up
    pygame.quit()

if __name__ == "__main__":
    main() 