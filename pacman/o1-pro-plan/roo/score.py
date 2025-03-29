"""
Score manager for the Pac-Man game
Handles scoring logic, lives display, and high score tracking
"""

import pygame
from constants import *

class ScoreManager:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.ghost_combo = 0  # Tracks sequential ghost eats within a single power pellet
        
        # Try to load high score from a file
        try:
            with open('highscore.txt', 'r') as f:
                self.high_score = int(f.read().strip())
        except (FileNotFoundError, ValueError):
            # If file doesn't exist or contains invalid data, keep default
            self.high_score = 0
    
    def add_score(self, points):
        """Add points to the score"""
        self.score += points
        
        # Update high score if needed
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
    
    def eat_ghost(self):
        """Score points for eating a ghost, with increasing values for combos"""
        # Get the appropriate ghost score based on combo count
        ghost_score = GHOST_SCORE[min(self.ghost_combo, len(GHOST_SCORE) - 1)]
        self.add_score(ghost_score)
        
        # Increment the ghost combo (capped at the length of GHOST_SCORE)
        self.ghost_combo = min(self.ghost_combo + 1, len(GHOST_SCORE) - 1)
        
        return ghost_score
    
    def reset_ghost_combo(self):
        """Reset the ghost combo counter when power pellet effect ends"""
        self.ghost_combo = 0
    
    def reset_score(self):
        """Reset the score for a new game"""
        self.score = 0
        self.ghost_combo = 0
    
    def save_high_score(self):
        """Save the high score to a file"""
        try:
            with open('highscore.txt', 'w') as f:
                f.write(str(self.high_score))
        except IOError:
            # If there's an error saving, just continue without saving
            pass
    
    def draw(self, screen, lives):
        """Draw the score and lives information on the screen"""
        # Set up font
        try:
            font = pygame.font.Font(None, 36)
        except:
            font = pygame.font.SysFont('Arial', 36)
        
        # Draw score
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (10, SCREEN_HEIGHT - 40))
        
        # Draw high score
        high_score_text = font.render(f'High Score: {self.high_score}', True, WHITE)
        screen.blit(high_score_text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        
        # Draw lives
        for i in range(lives):
            # Draw a simple Pac-Man as a life indicator
            pygame.draw.circle(screen, YELLOW, 
                              (SCREEN_WIDTH - 30 - i * 30, SCREEN_HEIGHT - 25), 
                              10)