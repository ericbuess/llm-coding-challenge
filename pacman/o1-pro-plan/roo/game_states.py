"""
Game states module for the Pac-Man game
Manages different game states and transitions between them
"""

import pygame
from enum import Enum, auto
from constants import *

class GameState(Enum):
    """Enum representing different game states"""
    START = auto()
    PLAY = auto()
    PAUSE = auto()
    GAME_OVER = auto()
    WIN = auto()

class GameStateManager:
    def __init__(self, screen):
        self.screen = screen
        self.current_state = GameState.START
        self.prev_state = None
        self.timer = 0
        
        # Load fonts for text rendering
        try:
            self.large_font = pygame.font.Font(None, 72)
            self.medium_font = pygame.font.Font(None, 48)
            self.small_font = pygame.font.Font(None, 36)
        except:
            self.large_font = pygame.font.SysFont('Arial', 72)
            self.medium_font = pygame.font.SysFont('Arial', 48)
            self.small_font = pygame.font.SysFont('Arial', 36)
    
    def change_state(self, new_state):
        """Change to a new game state"""
        self.prev_state = self.current_state
        self.current_state = new_state
        self.timer = 0
    
    def update(self, dt, events):
        """Update based on the current state and handle state transitions"""
        self.timer += dt
        
        # Handle keyboard events explicitly
        keys = pygame.key.get_pressed()
        
        # Handle state-specific updates and event handling
        if self.current_state == GameState.START:
            # Check for key presses both ways - through events and direct key state
            if (keys[pygame.K_SPACE] or keys[pygame.K_RETURN]):
                print("Starting game from key press")
                self.change_state(GameState.PLAY)
            
            # Also check through events for better responsiveness
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        print("Starting game from event")
                        self.change_state(GameState.PLAY)
        
        elif self.current_state == GameState.PAUSE:
            if (keys[pygame.K_p] or keys[pygame.K_ESCAPE]):
                self.change_state(GameState.PLAY)
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        self.change_state(GameState.PLAY)
        
        elif self.current_state == GameState.PLAY:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        self.change_state(GameState.PAUSE)
        
        elif self.current_state == GameState.GAME_OVER or self.current_state == GameState.WIN:
            # After a few seconds, automatically return to start screen
            if self.timer > 5.0:  # 5 seconds delay
                self.change_state(GameState.START)
            
            # Or return immediately if the player presses a key
            if (keys[pygame.K_SPACE] or keys[pygame.K_RETURN]):
                self.change_state(GameState.START)
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.change_state(GameState.START)
    
    def is_playing(self):
        """Check if the game is in the PLAY state"""
        return self.current_state == GameState.PLAY
    
    def handle_death(self, lives):
        """Handle Pac-Man's death - either go to GAME_OVER or pause briefly"""
        if lives <= 0:
            self.change_state(GameState.GAME_OVER)
        else:
            # We could add a death animation state here if desired
            pass
    
    def handle_win(self):
        """Handle winning the game (all pellets eaten)"""
        self.change_state(GameState.WIN)
    
    def draw_overlay(self):
        """Draw overlay based on the current state"""
        if self.current_state == GameState.START:
            self.draw_start_screen()
        elif self.current_state == GameState.PAUSE:
            self.draw_pause_screen()
        elif self.current_state == GameState.GAME_OVER:
            self.draw_game_over_screen()
        elif self.current_state == GameState.WIN:
            self.draw_win_screen()
    
    def draw_start_screen(self):
        """Draw the start screen"""
        # Semi-transparent black overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Title
        title_text = self.large_font.render("PAC-MAN", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        self.screen.blit(title_text, title_rect)
        
        # Instructions
        if int(self.timer * 2) % 2 == 0:  # Blinking effect
            instructions_text = self.medium_font.render("Press SPACE to Start", True, WHITE)
            instructions_rect = instructions_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(instructions_text, instructions_rect)
        
        # Controls
        controls1_text = self.small_font.render("Use Arrow Keys or WASD to move", True, WHITE)
        controls1_rect = controls1_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT*3//4 - 30))
        self.screen.blit(controls1_text, controls1_rect)
        
        controls2_text = self.small_font.render("Press P or ESC to pause", True, WHITE)
        controls2_rect = controls2_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT*3//4 + 10))
        self.screen.blit(controls2_text, controls2_rect)
    
    def draw_pause_screen(self):
        """Draw the pause screen"""
        # Semi-transparent black overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.large_font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(pause_text, pause_rect)
        
        # Resume instructions
        if int(self.timer * 2) % 2 == 0:  # Blinking effect
            resume_text = self.medium_font.render("Press P or ESC to Resume", True, WHITE)
            resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT*2//3))
            self.screen.blit(resume_text, resume_rect)
    
    def draw_game_over_screen(self):
        """Draw the game over screen"""
        # Semi-transparent black overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.large_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Continue text
        if int(self.timer * 2) % 2 == 0:  # Blinking effect
            continue_text = self.medium_font.render("Press SPACE to Continue", True, WHITE)
            continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT*2//3))
            self.screen.blit(continue_text, continue_rect)
    
    def draw_win_screen(self):
        """Draw the win screen"""
        # Semi-transparent black overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Win text
        win_text = self.large_font.render("YOU WIN!", True, YELLOW)
        win_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(win_text, win_rect)
        
        # Continue text
        if int(self.timer * 2) % 2 == 0:  # Blinking effect
            continue_text = self.medium_font.render("Press SPACE to Continue", True, WHITE)
            continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT*2//3))
            self.screen.blit(continue_text, continue_rect)