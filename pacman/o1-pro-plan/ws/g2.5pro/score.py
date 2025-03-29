# score.py
# Manages the game score, high score, and rendering the score UI.

import pygame
from constants import *

HIGH_SCORE_FILE = "highscore.txt"

class ScoreManager:
    def __init__(self):
        self.current_score = 0
        self.high_score = self._load_high_score()
        self.font = pygame.font.Font(None, 24) # Basic font for score display

    def _load_high_score(self):
        try:
            with open(HIGH_SCORE_FILE, 'r') as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def _save_high_score(self):
        try:
            with open(HIGH_SCORE_FILE, 'w') as f:
                f.write(str(self.high_score))
        except IOError:
            print(f"Warning: Could not save high score to {HIGH_SCORE_FILE}")

    def add_score(self, points):
        self.current_score += points
        if self.current_score > self.high_score:
            self.high_score = self.current_score
            # Save immediately or on game over?
            # self._save_high_score()

    def reset_score(self):
        self.current_score = 0

    def save_if_needed(self):
         # Call this on game over or exit
         self._save_high_score()

    def draw(self, screen):
        # Draw current score
        score_text = f"Score: {self.current_score}"
        score_surf = self.font.render(score_text, True, WHITE)
        score_rect = score_surf.get_rect(topleft=(10, 5))
        screen.blit(score_surf, score_rect)

        # Draw high score
        high_score_text = f"High Score: {self.high_score}"
        high_score_surf = self.font.render(high_score_text, True, WHITE)
        high_score_rect = high_score_surf.get_rect(topright=(SCREEN_WIDTH - 10, 5))
        screen.blit(high_score_surf, high_score_rect)

        # We might draw lives here too, or handle it in the main game loop/Pacman class
