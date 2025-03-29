import pygame
from constants import *

class GameState:
    def __init__(self, game):
        self.game = game
        self.font_large = None
        self.font_small = None
        
        # Try to initialize fonts
        try:
            self.font_large = pygame.font.SysFont('Arial', 36)
            self.font_small = pygame.font.SysFont('Arial', 24)
        except:
            # Continue without fonts if they can't be loaded
            pass
    
    def update(self, dt):
        """Update logic for the current state."""
        pass
    
    def draw(self, screen):
        """Draw the current state."""
        pass
    
    def handle_events(self, events):
        """Handle events for the current state."""
        for event in events:
            if event.type == pygame.QUIT:
                return False  # Signal to quit the game
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False  # Exit on ESC
        
        return True  # Continue the game

class StartState(GameState):
    def __init__(self, game):
        super().__init__(game)
    
    def update(self, dt):
        # Nothing to update in start state
        pass
    
    def draw(self, screen):
        # Fill screen with black
        screen.fill(BLACK)
        
        # Draw title and instructions
        if self.font_large and self.font_small:
            # Title
            title = self.font_large.render('PAC-MAN', True, YELLOW)
            screen.blit(title, 
                       (SCREEN_WIDTH//2 - title.get_width()//2, 
                        SCREEN_HEIGHT//4))
            
            # Instructions
            start_text = self.font_small.render('Press SPACE to start', True, WHITE)
            screen.blit(start_text, 
                       (SCREEN_WIDTH//2 - start_text.get_width()//2, 
                        SCREEN_HEIGHT//2))
            
            # Controls
            controls_text = self.font_small.render('Use arrow keys or WASD to move', True, WHITE)
            screen.blit(controls_text, 
                       (SCREEN_WIDTH//2 - controls_text.get_width()//2, 
                        SCREEN_HEIGHT//2 + 40))
            
            # High score
            high_score_text = self.font_small.render(f'High Score: {self.game.score_manager.high_score}', True, WHITE)
            screen.blit(high_score_text, 
                       (SCREEN_WIDTH//2 - high_score_text.get_width()//2, 
                        SCREEN_HEIGHT//2 + 80))
    
    def handle_events(self, events):
        # First check parent's event handling (for quit events)
        if not super().handle_events(events):
            return False
        
        # Check for space key to start the game
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game.set_state(PLAY)
        
        return True

class PlayState(GameState):
    def __init__(self, game):
        super().__init__(game)
    
    def update(self, dt):
        # Update Pac-Man based on current input
        keys = pygame.key.get_pressed()
        self.game.pacman.handle_input(keys)
        
        # Update Pac-Man
        power_pellet_eaten = self.game.pacman.update(dt, self.game.maze, 
                                                 self.game.score_manager)
        
        # If power pellet eaten, update ghost states
        if power_pellet_eaten:
            for ghost in self.game.ghosts:
                if ghost.current_state != ghost.EATEN:
                    ghost.set_state(ghost.FRIGHTENED)
            self.game.score_manager.reset_ghost_combo()
        
        # Update ghosts
        for ghost in self.game.ghosts:
            ghost.update(dt, self.game.maze, self.game.pacman)
            
            # Check for collision with Pac-Man
            if self.check_ghost_collision(ghost):
                if ghost.current_state == ghost.FRIGHTENED:
                    # Eat the ghost
                    ghost.set_state(ghost.EATEN)
                    self.game.score_manager.eat_ghost()
                elif ghost.current_state != ghost.EATEN:
                    # Pac-Man dies
                    self.game.lose_life()
                    return
        
        # Check if all pellets are eaten
        if self.game.maze.get_remaining_pellets() == 0:
            self.game.set_state(WIN)
    
    def check_ghost_collision(self, ghost):
        """Check if Pac-Man collides with a ghost."""
        # Calculate distance between Pac-Man and ghost
        distance = ((self.game.pacman.x - ghost.x) ** 2 + 
                   (self.game.pacman.y - ghost.y) ** 2) ** 0.5
        
        # If distance is less than sum of radii, collision occurs
        return distance < (self.game.pacman.radius + ghost.radius - 5)  # Small adjustment for better gameplay
    
    def draw(self, screen):
        # Fill screen with black
        screen.fill(BLACK)
        
        # Draw maze
        self.game.maze.draw(screen)
        
        # Draw Pac-Man
        self.game.pacman.draw(screen)
        
        # Draw ghosts
        for ghost in self.game.ghosts:
            ghost.draw(screen)
        
        # Draw score and lives
        self.game.score_manager.draw(screen, self.game.pacman.lives)

class PauseState(GameState):
    def __init__(self, game):
        super().__init__(game)
    
    def draw(self, screen):
        # First draw the play state
        self.game.states[PLAY].draw(screen)
        
        # Then overlay pause message
        if self.font_large:
            pause_text = self.font_large.render('PAUSED', True, WHITE)
            text_width = pause_text.get_width()
            
            # Draw semi-transparent background
            s = pygame.Surface((text_width + 40, 50))
            s.set_alpha(180)  # Alpha level (0-255)
            s.fill(BLACK)
            screen.blit(s, (SCREEN_WIDTH//2 - (text_width + 40)//2, SCREEN_HEIGHT//2 - 25))
            
            # Draw text
            screen.blit(pause_text, 
                       (SCREEN_WIDTH//2 - text_width//2, 
                        SCREEN_HEIGHT//2 - pause_text.get_height()//2))
    
    def handle_events(self, events):
        # First check parent's event handling
        if not super().handle_events(events):
            return False
        
        # Check for P key to unpause
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.game.set_state(PLAY)
        
        return True

class GameOverState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.timer = 0
    
    def update(self, dt):
        # Wait for a few seconds before allowing restart
        self.timer += dt
    
    def draw(self, screen):
        # Fill screen with black
        screen.fill(BLACK)
        
        if self.font_large and self.font_small:
            # Game over message
            gameover_text = self.font_large.render('GAME OVER', True, RED)
            screen.blit(gameover_text, 
                       (SCREEN_WIDTH//2 - gameover_text.get_width()//2, 
                        SCREEN_HEIGHT//3))
            
            # Final score
            score_text = self.font_small.render(f'Final Score: {self.game.score_manager.score}', True, WHITE)
            screen.blit(score_text, 
                       (SCREEN_WIDTH//2 - score_text.get_width()//2, 
                        SCREEN_HEIGHT//2))
            
            # Restart instructions (after delay)
            if self.timer > 2000:  # 2 seconds
                restart_text = self.font_small.render('Press SPACE to restart', True, WHITE)
                screen.blit(restart_text, 
                          (SCREEN_WIDTH//2 - restart_text.get_width()//2, 
                           SCREEN_HEIGHT//2 + 80))
    
    def handle_events(self, events):
        # First check parent's event handling
        if not super().handle_events(events):
            return False
        
        # Check for space key to restart (after delay)
        if self.timer > 2000:  # 2 seconds
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game.reset_game()
                        self.game.set_state(START)
        
        return True

class WinState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.timer = 0
    
    def update(self, dt):
        # Wait for a few seconds before allowing restart
        self.timer += dt
    
    def draw(self, screen):
        # Fill screen with black
        screen.fill(BLACK)
        
        if self.font_large and self.font_small:
            # Win message
            win_text = self.font_large.render('YOU WIN!', True, YELLOW)
            screen.blit(win_text, 
                      (SCREEN_WIDTH//2 - win_text.get_width()//2, 
                       SCREEN_HEIGHT//3))
            
            # Final score
            score_text = self.font_small.render(f'Final Score: {self.game.score_manager.score}', True, WHITE)
            screen.blit(score_text, 
                       (SCREEN_WIDTH//2 - score_text.get_width()//2, 
                        SCREEN_HEIGHT//2))
            
            # Restart instructions (after delay)
            if self.timer > 2000:  # 2 seconds
                restart_text = self.font_small.render('Press SPACE to restart', True, WHITE)
                screen.blit(restart_text, 
                          (SCREEN_WIDTH//2 - restart_text.get_width()//2, 
                           SCREEN_HEIGHT//2 + 80))
    
    def handle_events(self, events):
        # First check parent's event handling
        if not super().handle_events(events):
            return False
        
        # Check for space key to restart (after delay)
        if self.timer > 2000:  # 2 seconds
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game.reset_game()
                        self.game.set_state(START)
        
        return True
