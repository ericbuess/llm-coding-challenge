import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    STATE_MENU, STATE_PLAYING, STATE_PAUSED, STATE_GAMEOVER,
    INITIAL_LIVES
)
from level import Level

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.state = STATE_PLAYING  # Start with playing state for now
        
        # Game state
        self.score = 0
        self.lives = INITIAL_LIVES
        self.level_number = 1
        
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        self.pellet_group = pygame.sprite.Group()
        self.powerpellet_group = pygame.sprite.Group()
        self.pacman_group = pygame.sprite.Group()
        self.ghost_group = pygame.sprite.Group()
        
        # Reference to pacman for ghost AI
        self.pacman = None
        
        # Load level
        self.level = Level(self)
        self.level.load()
        
        # Font for score display
        self.font = pygame.font.Font(None, 36)
        
    def run(self):
        """Main game loop."""
        while self.running:
            self.clock.tick(FPS)
            self.process_events()
            self.update()
            self.draw()
            pygame.display.flip()
            
    def process_events(self):
        """Handle game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
                
    def handle_keydown(self, key):
        """Handle keyboard input."""
        if key == pygame.K_ESCAPE:
            if self.state == STATE_PLAYING:
                self.state = STATE_PAUSED
            elif self.state == STATE_PAUSED:
                self.state = STATE_PLAYING
        elif key == pygame.K_r and self.state == STATE_GAMEOVER:
            self.reset_game()
        elif self.state == STATE_PLAYING:
            # Pass movement keys to Pacman
            if key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                if self.pacman:
                    self.pacman.handle_input(key)
                    
    def update(self):
        """Update game state."""
        if self.state != STATE_PLAYING:
            return
            
        # Update all sprites
        self.all_sprites.update()
        
        # Handle collisions
        self.handle_collisions()
        
        # Check win/lose conditions
        self.check_game_state()
        
    def handle_collisions(self):
        """Handle all game collisions."""
        if not self.pacman:
            return
            
        # Pacman collecting pellets
        pellets_hit = pygame.sprite.spritecollide(self.pacman, self.pellet_group, True)
        self.score += len(pellets_hit) * 10
        
        # Pacman collecting power pellets
        power_pellets = pygame.sprite.spritecollide(self.pacman, self.powerpellet_group, True)
        if power_pellets:
            self.score += len(power_pellets) * 50
            # Make ghosts frightened
            for ghost in self.ghost_group:
                ghost.enter_frightened_mode()
                
        # Pacman colliding with ghosts
        ghost_collisions = pygame.sprite.spritecollide(self.pacman, self.ghost_group, False)
        for ghost in ghost_collisions:
            if ghost.state == 'frightened':
                # Eat ghost
                ghost.state = 'eaten'
                self.score += 200
            elif ghost.state != 'eaten':
                # Pacman dies
                self.lives -= 1
                if self.lives > 0:
                    self.level.reset_positions()
                else:
                    self.state = STATE_GAMEOVER
                    
    def check_game_state(self):
        """Check for level completion or game over."""
        # Check if all pellets are collected
        if len(self.pellet_group) == 0 and len(self.powerpellet_group) == 0:
            self.level_number += 1
            self.reset_level()
            
    def reset_level(self):
        """Reset the current level."""
        # Clear all sprite groups
        for group in [self.all_sprites, self.wall_group, self.pellet_group,
                     self.powerpellet_group, self.pacman_group, self.ghost_group]:
            group.empty()
            
        # Reload the level
        self.level.load()
        
    def reset_game(self):
        """Reset the entire game."""
        self.score = 0
        self.lives = INITIAL_LIVES
        self.level_number = 1
        self.state = STATE_PLAYING
        self.reset_level()
        
    def draw(self):
        """Draw the game screen."""
        self.screen.fill((0, 0, 0))  # Black background
        
        # Draw all sprites
        self.all_sprites.draw(self.screen)
        
        # Draw HUD
        self.draw_hud()
        
        # Draw game over screen if needed
        if self.state == STATE_GAMEOVER:
            self.draw_game_over()
            
        # Draw pause screen if needed
        if self.state == STATE_PAUSED:
            self.draw_pause_screen()
            
    def draw_hud(self):
        """Draw heads-up display (score, lives)."""
        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        # Draw lives
        lives_text = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        self.screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))
        
    def draw_game_over(self):
        """Draw game over screen."""
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 0))
        
        game_over_text = self.font.render('GAME OVER', True, (255, 0, 0))
        restart_text = self.font.render('Press R to Restart', True, (255, 255, 255))
        
        self.screen.blit(game_over_text,
                        (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                         SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(restart_text,
                        (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                         SCREEN_HEIGHT // 2 + 50))
        
    def draw_pause_screen(self):
        """Draw pause screen."""
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 0))
        
        pause_text = self.font.render('PAUSED', True, (255, 255, 255))
        continue_text = self.font.render('Press ESC to Continue', True, (255, 255, 255))
        
        self.screen.blit(pause_text,
                        (SCREEN_WIDTH // 2 - pause_text.get_width() // 2,
                         SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(continue_text,
                        (SCREEN_WIDTH // 2 - continue_text.get_width() // 2,
                         SCREEN_HEIGHT // 2 + 50)) 