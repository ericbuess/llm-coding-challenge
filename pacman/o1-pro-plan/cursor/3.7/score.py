"""
Score management for Pac-Man game
"""
import pygame
from constants import *

class ScoreManager:
    """
    Manages score tracking, high score persistence, and score displays
    """
    
    def __init__(self):
        """Initialize score, high score, lives, and other display elements"""
        self.score = 0
        self.high_score = self._load_high_score()
        self.lives = LIVES
        self.level = 1
        
        # Ghost score multiplier (resets after power pellet effect ends)
        self.ghost_multiplier = 0
        
    def _load_high_score(self):
        """Load high score from file or return default value"""
        try:
            with open("highscore.txt", "r") as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return 0
            
    def save_high_score(self):
        """Save high score to file if current score is higher"""
        if self.score > self.high_score:
            self.high_score = self.score
            try:
                with open("highscore.txt", "w") as file:
                    file.write(str(self.high_score))
            except IOError:
                # If file can't be written, continue silently
                pass
                
    def add_score(self, points):
        """Add points to the current score and update high score if needed"""
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
            
    def reset_ghost_multiplier(self):
        """Reset the ghost score multiplier (when power pellet effect ends)"""
        self.ghost_multiplier = 0
        
    def get_ghost_score(self):
        """Get the score for eating a ghost, and increment the multiplier"""
        if self.ghost_multiplier >= len(GHOST_SCORE):
            return GHOST_SCORE[-1]  # Use max score if beyond array bounds
            
        score = GHOST_SCORE[self.ghost_multiplier]
        self.ghost_multiplier += 1
        return score
        
    def lose_life(self):
        """Decrement the lives counter. Returns True if still alive, False if game over"""
        self.lives -= 1
        return self.lives > 0
        
    def add_life(self):
        """Add an extra life (bonus at certain score thresholds)"""
        self.lives += 1
        
    def reset(self):
        """Reset score and lives for a new game"""
        self.save_high_score()
        self.score = 0
        self.lives = LIVES
        self.level = 1
        self.ghost_multiplier = 0
        
    def advance_level(self):
        """Increment level count when player clears all pellets"""
        self.level += 1
        
    def draw(self, screen):
        """Draw score, high score, level, and lives on the screen"""
        font = pygame.font.Font(None, 36)
        
        # Draw score
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, SCREEN_HEIGHT - 40))
        
        # Draw high score
        high_score_text = font.render(f"High: {self.high_score}", True, WHITE)
        screen.blit(high_score_text, (SCREEN_WIDTH - 160, SCREEN_HEIGHT - 40))
        
        # Draw level
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        screen.blit(level_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 40))
        
        # Draw lives (Pac-Man icons)
        for i in range(self.lives):
            pygame.draw.circle(
                screen, 
                YELLOW, 
                (200 + i * 30, SCREEN_HEIGHT - 25), 
                10
            ) 