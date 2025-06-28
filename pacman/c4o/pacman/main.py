#!/usr/bin/env python3
import pygame
import sys
from .game.game import GameController
from .game.constants import FPS
from .ui.display import Display

def main():
    """Main game entry point"""
    # Initialize Pygame and display
    display = Display()
    screen = display.initialize()
    clock = pygame.time.Clock()
    
    # Initialize game controller
    game = GameController()
    
    # Game state
    running = True
    
    # Main game loop
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Get current keyboard state
        keys = pygame.key.get_pressed()
        
        # Update game logic
        game.handle_input(keys)
        game.update(dt)
        
        # Clear screen
        display.clear(screen)
        
        # Draw everything
        display.draw_maze(screen, game.board)
        display.draw_ghost_house(screen, game.board)
        display.draw_pellets(screen, game.board)
        
        # Draw Pacman (temporary simple representation)
        if game.pacman:
            display.draw_pacman(screen, game.pacman)
        
        # Draw ghosts (temporary simple representation)
        for ghost in game.ghosts.values():
            display.draw_ghost(screen, ghost)
        
        # Draw UI elements
        display.draw_score(screen, game.score, game.lives, game.level)
        
        # Draw game state messages
        if game.game_state == 'game_over':
            display.draw_game_state_text(screen, "GAME OVER", "Press SPACE to restart")
        elif game.game_state == 'level_complete':
            display.draw_game_state_text(screen, "LEVEL COMPLETE!", "Press SPACE to continue")
        
        # Update display
        display.update()
    
    # Cleanup
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()