import pygame
import sys
from constants import *
from maze import Maze
from entities import Pacman, Ghost
from score import ScoreManager
from sound import SoundManager

class PacmanGame:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        
        # Create game components
        self.maze = Maze()
        self.score_manager = ScoreManager()
        self.sound_manager = SoundManager()
        
        # Create Pac-Man
        start_pos = self.maze.pacman_start_position or (GRID_WIDTH // 2, GRID_HEIGHT - 5)
        self.pacman = Pacman(*start_pos)
        
        # Create Ghosts
        self.ghosts = [
            Ghost(13, 14, BLINKY),  # Adjust positions if needed
            Ghost(14, 14, PINKY),
            Ghost(13, 15, INKY),
            Ghost(14, 15, CLYDE)
        ]
        
        # Set global entities for ghost AI reference
        global GAME_ENTITIES
        GAME_ENTITIES = [self.pacman] + self.ghosts
        
        # Game state
        self.game_state = START
        self.lives_display = self.pacman.lives
        self.level = 1
        self.ready_timer = FPS * 2  # 2 second ready screen
        
        # Load fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
    
    def handle_input(self):
        # Handle keyboard input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == PLAY:
                        self.game_state = PAUSE
                    elif self.game_state == PAUSE:
                        self.game_state = PLAY
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if self.game_state == START:
                        self.start_game()
                    elif self.game_state == GAME_OVER or self.game_state == WIN:
                        self.reset_game()
                    elif self.game_state == PAUSE:
                        self.game_state = PLAY
        
        # Handle continuous key presses for Pac-Man movement
        if self.game_state == PLAY:
            keys = pygame.key.get_pressed()
            self.pacman.handle_input(keys)
    
    def update(self):
        # Update game based on current state
        if self.game_state == PLAY:
            # Update Pac-Man
            points = self.pacman.update(1, self.maze)
            if points > 0:
                self.score_manager.add_score(points)
                if points == PELLET_POINTS:
                    self.sound_manager.play('chomp')
                elif points == POWER_PELLET_POINTS:
                    self.sound_manager.play('power_pellet')
                    # Set all ghosts to frightened mode
                    for ghost in self.ghosts:
                        ghost.set_frightened()
                    # Reset ghost combo counter
                    self.score_manager.reset_ghost_combo()
            
            # Update ghosts
            for ghost in self.ghosts:
                ghost.update(1, self.maze, self.pacman)
                
                # Check collision with Pac-Man
                if ghost.collides_with(self.pacman):
                    if ghost.current_state == FRIGHTENED and not ghost.eaten:
                        # Pac-Man eats ghost
                        ghost.set_eaten()
                        points = self.score_manager.add_ghost_score()
                        self.sound_manager.play('eat_ghost')
                    elif ghost.current_state != EATEN and not self.pacman.power_mode:
                        # Ghost catches Pac-Man
                        self.lose_life()
            
            # Check win condition
            if self.maze.pellet_count <= 0:
                self.game_state = WIN
                self.sound_manager.play('start')
        
        elif self.game_state == START and self.ready_timer > 0:
            self.ready_timer -= 1
            if self.ready_timer <= 0:
                self.sound_manager.play('start')
    
    def lose_life(self):
        # Handle Pac-Man losing a life
        self.pacman.lives -= 1
        self.sound_manager.play('death')
        
        if self.pacman.lives <= 0:
            self.game_state = GAME_OVER
        else:
            # Reset positions
            self.pacman.reset_position(self.maze)
            for ghost in self.ghosts:
                ghost.reset_position(self.maze)
            
            # Pause briefly before continuing
            self.ready_timer = FPS * 2
    
    def start_game(self):
        # Start a new game
        self.score_manager.reset_score()
        self.pacman.lives = INITIAL_LIVES
        self.reset_level()
        self.game_state = PLAY
    
    def reset_game(self):
        # Reset the game for a new start
        self.score_manager.reset_score()
        self.pacman.lives = INITIAL_LIVES
        self.level = 1
        self.reset_level()
        self.game_state = START
        self.ready_timer = FPS * 2
    
    def reset_level(self):
        # Reset level (positions, maze pellets, etc.)
        self.maze = Maze()  # Reload maze with fresh pellets
        self.pacman.reset_position(self.maze)
        for ghost in self.ghosts:
            ghost.reset_position(self.maze)
    
    def draw(self):
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw maze
        self.maze.draw(self.screen)
        
        if self.game_state == PLAY or self.game_state == PAUSE:
            # Draw entities
            self.pacman.draw(self.screen)
            for ghost in self.ghosts:
                ghost.draw(self.screen)
            
            # Draw score
            self.score_manager.draw(self.screen)
            
            # Draw lives
            self.draw_lives()
            
            # Draw pause message if paused
            if self.game_state == PAUSE:
                self.draw_centered_text("PAUSED", self.font_large, WHITE, SCREEN_HEIGHT // 2)
                self.draw_centered_text("Press SPACE to continue", self.font_small, WHITE, SCREEN_HEIGHT // 2 + 40)
        
        elif self.game_state == START:
            # Draw start screen
            self.draw_centered_text("PAC-MAN", self.font_large, YELLOW, SCREEN_HEIGHT // 3)
            if self.ready_timer <= 0:
                self.draw_centered_text("Press SPACE to start", self.font_medium, WHITE, SCREEN_HEIGHT // 2)
            else:
                self.draw_centered_text("Get Ready!", self.font_medium, WHITE, SCREEN_HEIGHT // 2)
            
            # Draw game instructions
            self.draw_centered_text("Use Arrow Keys or WASD to move", self.font_small, WHITE, SCREEN_HEIGHT * 2 // 3)
            self.draw_centered_text("Press ESC to pause", self.font_small, WHITE, SCREEN_HEIGHT * 2 // 3 + 30)
        
        elif self.game_state == GAME_OVER:
            # Draw game over screen
            self.draw_centered_text("GAME OVER", self.font_large, RED, SCREEN_HEIGHT // 3)
            self.draw_centered_text(f"Score: {self.score_manager.current_score}", self.font_medium, WHITE, SCREEN_HEIGHT // 2)
            self.draw_centered_text("Press SPACE to play again", self.font_small, WHITE, SCREEN_HEIGHT * 2 // 3)
        
        elif self.game_state == WIN:
            # Draw win screen
            self.draw_centered_text("YOU WIN!", self.font_large, YELLOW, SCREEN_HEIGHT // 3)
            self.draw_centered_text(f"Score: {self.score_manager.current_score}", self.font_medium, WHITE, SCREEN_HEIGHT // 2)
            self.draw_centered_text("Press SPACE to play again", self.font_small, WHITE, SCREEN_HEIGHT * 2 // 3)
        
        # Update display
        pygame.display.flip()
    
    def draw_centered_text(self, text, font, color, y_pos):
        # Helper to draw centered text
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
        self.screen.blit(text_surface, text_rect)
    
    def draw_lives(self):
        # Draw remaining lives as small Pac-Man icons
        for i in range(self.pacman.lives):
            # Draw small yellow circle for each life
            pygame.draw.circle(self.screen, YELLOW, 
                              (20 + i * 25, SCREEN_HEIGHT - 20), 
                              10)  # 10 pixel radius
    
    def run(self):
        # Main game loop
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
    
    def quit_game(self):
        # Save high score and exit
        self.score_manager.save_high_score()
        pygame.quit()
        sys.exit()

# This allows importing the game class without running
if __name__ == "__main__":
    game = PacmanGame()
    game.run()
