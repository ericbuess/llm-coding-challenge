import pygame
import os
from constants import *

class ScoreManager:
    def __init__(self):
        self.current_score = 0
        self.high_score = self.load_high_score()
        self.ghost_combo = 0  # Track consecutive ghost eaten during power mode
        self.font = None
        self.initialize_font()
    
    def initialize_font(self):
        # Initialize font for score display
        pygame.font.init()
        try:
            self.font = pygame.font.Font(None, 36)  # Default font, size 36
        except:
            self.font = pygame.font.SysFont('Arial', 36)  # Fallback font
    
    def add_score(self, points):
        # Add points to current score
        self.current_score += points
        
        # Update high score if current score exceeds it
        if self.current_score > self.high_score:
            self.high_score = self.current_score
            self.save_high_score()
    
    def add_ghost_score(self):
        # Add points for eating a ghost (score increases with combo)
        ghost_points = GHOST_POINTS[min(self.ghost_combo, len(GHOST_POINTS) - 1)]
        self.add_score(ghost_points)
        self.ghost_combo += 1
        return ghost_points
    
    def reset_ghost_combo(self):
        # Reset ghost combo counter when power mode ends
        self.ghost_combo = 0
    
    def reset_score(self):
        # Reset current score for new game
        self.current_score = 0
        self.ghost_combo = 0
    
    def load_high_score(self):
        # Load high score from file
        try:
            if os.path.exists('highscore.txt'):
                with open('highscore.txt', 'r') as file:
                    return int(file.read().strip())
        except:
            pass  # If any error occurs, return default high score
        return 0
    
    def save_high_score(self):
        # Save high score to file
        try:
            with open('highscore.txt', 'w') as file:
                file.write(str(self.high_score))
        except:
            pass  # Silently fail if unable to save high score
    
    def draw(self, screen):
        # Draw the score at the top of the screen
        if not self.font:
            self.initialize_font()
        
        # Draw current score
        score_text = self.font.render(f'Score: {self.current_score}', True, WHITE)
        screen.blit(score_text, (10, GRID_HEIGHT * TILE_SIZE + 10))
        
        # Draw high score
        high_score_text = self.font.render(f'High Score: {self.high_score}', True, WHITE)
        high_score_rect = high_score_text.get_rect()
        screen.blit(high_score_text, (SCREEN_WIDTH - high_score_rect.width - 10, GRID_HEIGHT * TILE_SIZE + 10))
