import pygame
from pacman import Pacman
from ghost import Ghost
from maze import Maze

class Game:
    def __init__(self):
        # Game objects - create maze first to get dimensions
        self.maze = Maze()
        
        # Screen setup - use maze dimensions for window size
        self.width, self.height = self.maze.width, self.maze.height + 50  # Extra height for score display
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pacman")
        
        # Color definitions
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        
        # Create pacman
        self.pacman = Pacman(self.maze)
        
        # Create ghosts with different colors and behaviors
        self.ghosts = [
            Ghost(self.maze, (255, 0, 0), "chase"),    # Red ghost (Blinky)
            Ghost(self.maze, (255, 192, 203), "ambush"),  # Pink ghost (Pinky)
            Ghost(self.maze, (0, 255, 255), "random"),  # Cyan ghost (Inky)
            Ghost(self.maze, (255, 165, 0), "patrol")   # Orange ghost (Clyde)
        ]
        
        # Game state
        self.score = 0
        self.lives = 3
        self.level = 1
        self.game_over = False
        self.game_won = False
        self.pause = False
        
        # Font setup
        self.font = pygame.font.SysFont('Arial', 24)
        
    def handle_key_down(self, key):
        if key == pygame.K_p:
            self.pause = not self.pause
            
        if not self.pause and not self.game_over and not self.game_won:
            if key == pygame.K_UP:
                self.pacman.change_direction("up")
            elif key == pygame.K_DOWN:
                self.pacman.change_direction("down")
            elif key == pygame.K_LEFT:
                self.pacman.change_direction("left")
            elif key == pygame.K_RIGHT:
                self.pacman.change_direction("right")
    
    def handle_key_up(self, key):
        pass
    
    def update(self):
        if self.pause or self.game_over or self.game_won:
            return
            
        # Update pacman
        self.pacman.update()
        
        # Check if pacman ate a dot
        if self.pacman.eat_dot():
            self.score += 10
            
        # Check if pacman ate a power pellet
        if self.pacman.eat_power_pellet():
            self.score += 50
            for ghost in self.ghosts:
                ghost.set_frightened()
        
        # Update ghosts
        for ghost in self.ghosts:
            ghost.update(self.pacman)
            
            # Check for collisions with ghosts
            if ghost.collides_with(self.pacman):
                if ghost.is_frightened():
                    ghost.reset_position()
                    self.score += 200
                else:
                    self.lives -= 1
                    self.pacman.reset_position()
                    for g in self.ghosts:
                        g.reset_position()
                    break
        
        # Check game over condition
        if self.lives <= 0:
            self.game_over = True
            
        # Check win condition
        if self.maze.dots_remaining() == 0:
            self.level += 1
            self.maze.reset_dots()
            self.pacman.reset_position()
            for ghost in self.ghosts:
                ghost.reset_position()
                ghost.increase_speed(self.level)
    
    def render(self):
        # Clear the screen
        self.screen.fill(self.BLACK)
        
        # Draw the maze
        self.maze.draw(self.screen)
        
        # Draw pacman
        self.pacman.draw(self.screen)
        
        # Draw ghosts
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        
        # Draw UI at the bottom of the screen
        score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (10, self.maze.height + 10))
        
        # Draw lives
        lives_text = self.font.render(f"Lives: {self.lives}", True, self.WHITE)
        self.screen.blit(lives_text, (self.width - 100, self.maze.height + 10))
        
        # Draw level
        level_text = self.font.render(f"Level: {self.level}", True, self.WHITE)
        self.screen.blit(level_text, (self.width // 2 - 40, self.maze.height + 10))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER - Press R to Restart", True, self.WHITE)
            self.screen.blit(game_over_text, (self.width // 2 - 180, self.maze.height // 2))
        
        # Draw game won message
        if self.game_won:
            game_won_text = self.font.render("YOU WIN! - Press R to Play Again", True, self.WHITE)
            self.screen.blit(game_won_text, (self.width // 2 - 180, self.maze.height // 2))
        
        # Draw pause message
        if self.pause:
            pause_text = self.font.render("PAUSED - Press P to Resume", True, self.WHITE)
            self.screen.blit(pause_text, (self.width // 2 - 150, self.maze.height // 2))
        
        # Update the display
        pygame.display.flip()