import pygame
import sys
from constants import *
from game import Game

def main():
    pygame.init()
    
    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ready for Human Review")
    
    # Clock for FPS
    clock = pygame.time.Clock()
    
    # Initialize game
    game = Game()
    try:
        game.font = pygame.font.Font(None, 24)
    except:
        game.font = None
    
    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                game.handle_input(event.key)
                
        # Update game
        game.update()
        
        # Draw everything
        game.draw(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()