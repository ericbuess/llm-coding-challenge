import pygame
from constants import *

HIGH_SCORE_FILE = "highscore.txt"

class ScoreManager:
    def __init__(self, font_size=20):
        self.score = 0
        self.high_score = self._load_high_score()
        self.font = pygame.font.Font(None, font_size) # Use default system font
        self.ghost_eaten_streak = 0 # To track sequential ghost points

    def _load_high_score(self):
        try:
            with open(HIGH_SCORE_FILE, 'r') as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0 # Default high score if file doesn't exist or is invalid

    def _save_high_score(self):
        try:
            with open(HIGH_SCORE_FILE, 'w') as f:
                f.write(str(self.high_score))
        except IOError:
            print(f"Warning: Could not save high score to {HIGH_SCORE_FILE}")

    def add_score(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
            # Consider saving immediately or only at game over
            # self._save_high_score()

    def add_ghost_score(self):
        """Adds score for eating a ghost, considering the streak."""
        if self.ghost_eaten_streak < len(GHOST_SCORES):
            points = GHOST_SCORES[self.ghost_eaten_streak]
            self.add_score(points)
            self.ghost_eaten_streak += 1
            return points # Return points awarded for display purposes maybe
        return 0 # No points if streak limit exceeded

    def reset_ghost_streak(self):
        """Call this when power pellet mode ends."""
        self.ghost_eaten_streak = 0

    def reset_score(self):
         self.score = 0
         self.reset_ghost_streak()

    def update_high_score_on_game_over(self):
         if self.score > self.high_score:
              self.high_score = self.score
              self._save_high_score()

    def draw(self, screen, lives, pacman_icon=None):
        """Draws the current score, high score, and lives onto the screen."""
        # Score Text
        score_text = self.font.render(f"SCORE: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(topleft=(10, SCREEN_HEIGHT - 40))

        # High Score Text
        high_score_text = self.font.render(f"HIGH SCORE: {self.high_score}", True, WHITE)
        high_score_rect = high_score_text.get_rect(centerx=(SCREEN_WIDTH // 2), top=score_rect.top)

        screen.blit(score_text, score_rect)
        screen.blit(high_score_text, high_score_rect)

        # Lives Display (using icons if provided)
        lives_label_text = self.font.render("LIVES:", True, WHITE)
        lives_label_rect = lives_label_text.get_rect(left=10, top=SCREEN_HEIGHT - 20)
        screen.blit(lives_label_text, lives_label_rect)

        if pacman_icon:
             icon_rect = pacman_icon.get_rect()
             for i in range(lives -1): # Show icons for remaining lives (excluding current one)
                 icon_x = lives_label_rect.right + 10 + i * (icon_rect.width + 5)
                 icon_y = lives_label_rect.centery - icon_rect.height // 2
                 screen.blit(pacman_icon, (icon_x, icon_y))
        else:
             # Fallback to text if no icon
             lives_text = self.font.render(str(lives), True, WHITE)
             lives_rect = lives_text.get_rect(left=lives_label_rect.right + 10, centery=lives_label_rect.centery)
             screen.blit(lives_text, lives_rect) 