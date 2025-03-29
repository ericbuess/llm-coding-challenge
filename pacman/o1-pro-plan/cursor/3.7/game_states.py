"""
Game state management for Pac-Man game
"""
import pygame
from constants import *

class GameStateManager:
    """
    Manages different game states and transitions between them
    """
    
    def __init__(self):
        """Initialize the game state manager"""
        self.state = START
        self.state_timer = 0
        
    def set_state(self, new_state, timer=0):
        """Set the game state and optionally a timer for the state"""
        self.state = new_state
        self.state_timer = timer
        
    def update(self):
        """Update state timer and handle automatic transitions"""
        if self.state_timer > 0:
            self.state_timer -= 1
            if self.state_timer == 0:
                # Automatic transitions when timer expires
                if self.state == "level_complete":
                    self.state = PLAYING
                    
    def is_playing(self):
        """Check if the game is in playing state"""
        return self.state == PLAYING
        
    def is_paused(self):
        """Check if the game is paused"""
        return self.state == PAUSED
        
    def toggle_pause(self):
        """Toggle between paused and playing states"""
        if self.state == PLAYING:
            self.state = PAUSED
        elif self.state == PAUSED:
            self.state = PLAYING
    
    def handle_event(self, event):
        """Handle events that affect game state"""
        if event.type == pygame.KEYDOWN:
            # Enter/return key to start game or continue after game over
            if event.key == pygame.K_RETURN:
                if self.state == START:
                    self.state = PLAYING
                elif self.state == GAME_OVER or self.state == WIN:
                    self.state = START
            
            # P key to toggle pause
            elif event.key == pygame.K_p:
                self.toggle_pause()
                
            # ESC key to quit or return to title screen
            elif event.key == pygame.K_ESCAPE:
                if self.state == PLAYING or self.state == PAUSED:
                    self.state = START
    
    def draw_overlay(self, screen, score_manager=None):
        """Draw state-specific overlays (titles, messages, etc.)"""
        font_large = pygame.font.Font(None, 64)
        font_medium = pygame.font.Font(None, 36)
        
        if self.state == START:
            # Draw title screen
            title = font_large.render("PAC-MAN", True, YELLOW)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            screen.blit(title, title_rect)
            
            # Instructions
            start_text = font_medium.render("Press ENTER to Start", True, WHITE)
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(start_text, start_rect)
            
            # Controls
            controls_text = font_medium.render("Arrow Keys or WASD to Move", True, WHITE)
            controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            screen.blit(controls_text, controls_rect)
            
            # Credits
            credits_text = font_medium.render("P to Pause, ESC to Quit", True, WHITE)
            credits_rect = credits_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
            screen.blit(credits_text, credits_rect)
            
        elif self.state == PAUSED:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # Black with 50% opacity
            screen.blit(overlay, (0, 0))
            
            # Pause text
            pause_text = font_large.render("PAUSED", True, WHITE)
            pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(pause_text, pause_rect)
            
            # Resume instructions
            resume_text = font_medium.render("Press P to Resume", True, WHITE)
            resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
            screen.blit(resume_text, resume_rect)
            
        elif self.state == GAME_OVER:
            # Game over overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 192))  # Black with 75% opacity
            screen.blit(overlay, (0, 0))
            
            # Game over text
            game_over_text = font_large.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            screen.blit(game_over_text, game_over_rect)
            
            if score_manager:
                # Final score
                score_text = font_medium.render(f"Final Score: {score_manager.score}", True, WHITE)
                score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(score_text, score_rect)
                
                # High score
                high_score_text = font_medium.render(f"High Score: {score_manager.high_score}", True, WHITE)
                high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
                screen.blit(high_score_text, high_score_rect)
            
            # Restart instructions
            restart_text = font_medium.render("Press ENTER to Play Again", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
            screen.blit(restart_text, restart_rect)
            
        elif self.state == WIN:
            # Win overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 192))  # Black with 75% opacity
            screen.blit(overlay, (0, 0))
            
            # Win text
            win_text = font_large.render("YOU WIN!", True, YELLOW)
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            screen.blit(win_text, win_rect)
            
            if score_manager:
                # Final score
                score_text = font_medium.render(f"Final Score: {score_manager.score}", True, WHITE)
                score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(score_text, score_rect)
                
                # High score
                high_score_text = font_medium.render(f"High Score: {score_manager.high_score}", True, WHITE)
                high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
                screen.blit(high_score_text, high_score_rect)
            
            # Continue instructions
            restart_text = font_medium.render("Press ENTER to Play Again", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
            screen.blit(restart_text, restart_rect)
            
        elif self.state == "level_complete":
            # Level complete overlay
            level_text = font_large.render("LEVEL COMPLETED!", True, YELLOW)
            level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(level_text, level_rect) 