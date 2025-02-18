import pygame
from game import Game

def main():
    """Main function to run the Pacman game."""
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()
