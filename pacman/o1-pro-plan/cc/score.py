import pygame
from constants import *

class ScoreManager:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.ghost_combo = 0  # Track consecutive ghosts eaten during power mode
        self.font = None
        
        # Try to load font
        try:
            self.font = pygame.font.SysFont('Arial', 24)
        except:
            # If unable to load font, continue without it
            pass
    
    def add_points(self, points):
        """Add points to the current score."""
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
    
    def reset_score(self):
        """Reset the score to 0 but preserve high score."""
        self.score = 0
        self.reset_ghost_combo()
    
    def reset_ghost_combo(self):
        """Reset the ghost combo counter."""
        self.ghost_combo = 0
    
    def eat_ghost(self):
        """Calculate and add points for eating a ghost, based on combo."""
        if self.ghost_combo < len(GHOST_POINTS):
            points = GHOST_POINTS[self.ghost_combo]
            self.add_points(points)
            self.ghost_combo += 1
            return points
        else:
            # If combo exceeds defined values, use the last value
            points = GHOST_POINTS[-1]
            self.add_points(points)
            return points
    
    def draw(self, screen, lives):
        """Draw score, high score, and remaining lives."""
        # Black background for score area
        pygame.draw.rect(screen, BLACK, 
                       (0, GRID_HEIGHT * TILE_SIZE, SCREEN_WIDTH, 50))
        
        # Draw score text if font is available
        if self.font:
            # Score text
            score_text = self.font.render(f'Score: {self.score}', True, WHITE)
            screen.blit(score_text, (10, GRID_HEIGHT * TILE_SIZE + 10))
            
            # High score text
            high_score_text = self.font.render(f'High Score: {self.high_score}', True, WHITE)
            screen.blit(high_score_text, 
                       (SCREEN_WIDTH - high_score_text.get_width() - 10, 
                        GRID_HEIGHT * TILE_SIZE + 10))
        
        # Draw lives (small Pac-Man icons)
        for i in range(lives):
            pygame.draw.circle(screen, YELLOW, 
                            (20 + i * 25, GRID_HEIGHT * TILE_SIZE + 35), 8)
