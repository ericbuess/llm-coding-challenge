class GameLogic:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        self.ghost_value = 200  # Base points for eating a ghost
        self.ghost_multiplier = 1  # Multiplier for consecutive ghost eating
        self.frightened_duration = 7.0  # Seconds ghosts remain frightened
        self.frightened_timer = 0
        
        # Timers for ghost mode cycling
        self.scatter_duration = 7  # Seconds in scatter mode
        self.chase_duration = 20   # Seconds in chase mode
        self.mode_timer = self.scatter_duration
        self.current_mode = "SCATTER"

    def add_score(self, points):
        """Add points to the score"""
        self.score += points
        # Award extra life at 10000 points
        if self.score >= 10000 and not hasattr(self, 'extra_life_awarded'):
            self.lives += 1
            self.extra_life_awarded = True

    def add_ghost_score(self):
        """Add points for eating a ghost, with multiplier for consecutive ghosts"""
        points = self.ghost_value * self.ghost_multiplier
        self.add_score(points)
        self.ghost_multiplier *= 2  # Double points for next ghost

    def lose_life(self):
        """Handle losing a life"""
        self.lives -= 1
        self.reset_ghost_score()

    def reset_ghost_score(self):
        """Reset the ghost score multiplier"""
        self.ghost_multiplier = 1

    def activate_power_pellet(self):
        """Activate power pellet effects"""
        self.frightened_timer = self.frightened_duration
        self.reset_ghost_score()  # Reset multiplier for new power pellet

    def check_win_condition(self):
        """Check if all pellets have been eaten"""
        # This will be called with the maze's pellet count
        return len(self.maze.pellets) == 0

    def check_game_over(self):
        """Check if the game is over (no lives remaining)"""
        return self.lives <= 0

    def update_timers(self, dt):
        """Update game timers and handle mode changes"""
        # Update frightened timer
        if self.frightened_timer > 0:
            self.frightened_timer -= dt
            if self.frightened_timer <= 0:
                self.reset_ghost_score()

        # Update ghost mode timer
        self.mode_timer -= dt
        if self.mode_timer <= 0:
            if self.current_mode == "SCATTER":
                self.current_mode = "CHASE"
                self.mode_timer = self.chase_duration
            else:
                self.current_mode = "SCATTER"
                self.mode_timer = self.scatter_duration

    def next_level(self):
        """Advance to the next level"""
        self.level += 1
        # Could adjust difficulty here (ghost speed, mode timings, etc.)

    def reset(self):
        """Reset game state for new game"""
        self.score = 0
        self.lives = 3
        self.level = 1
        self.ghost_multiplier = 1
        self.frightened_timer = 0
        self.mode_timer = self.scatter_duration
        self.current_mode = "SCATTER"
        if hasattr(self, 'extra_life_awarded'):
            delattr(self, 'extra_life_awarded')
