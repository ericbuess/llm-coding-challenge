# score.py
# Score management for Pac-Man

import os
from constants import HIGH_SCORE_FILE

class ScoreManager:
    def __init__(self):
        self.score = 0
        self.high_score = self.load_high_score()

    def add(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    def reset(self):
        self.score = 0

    def load_high_score(self):
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, 'r') as f:
                return int(f.read().strip() or 0)
        return 0

    def save_high_score(self):
        with open(HIGH_SCORE_FILE, 'w') as f:
            f.write(str(self.high_score))
