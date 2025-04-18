#!/usr/bin/env python3
import pygame
import sys
from game import Game

def main():
    # Initialize pygame
    pygame.init()
    
    # Create game instance
    game = Game()
    
    # Create a clock for frame rate control
    clock = pygame.time.Clock()
    
    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Add restart game functionality
                if event.key == pygame.K_r and (game.game_over or game.game_won):
                    game = Game()  # Reset the game
                else:
                    game.handle_key_down(event.key)
            elif event.type == pygame.KEYUP:
                game.handle_key_up(event.key)
        
        # Update game state
        game.update()
        
        # Render the game
        game.render()
        
        # Cap the frame rate
        clock.tick(60)

if __name__ == "__main__":
    main()