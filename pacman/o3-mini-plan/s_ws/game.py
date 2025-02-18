"""
Main game class implementation.
"""
import pygame
from settings import (
    STATE_MENU, STATE_PLAYING, STATE_PAUSED, STATE_GAMEOVER,
    PELLET_SCORE, POWERPELLET_SCORE, GHOST_SCORE
)
from level import Level

class Game:
    def __init__(self, screen: pygame.Surface):
        """Initialize game."""
        self.screen = screen
        self.running = True
        self.state = STATE_MENU
        self.score = 0
        self.lives = 3
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.pacman_group = pygame.sprite.Group()
        self.ghost_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        self.pellet_group = pygame.sprite.Group()
        self.powerpellet_group = pygame.sprite.Group()
        
        # Initialize level
        self.level = Level(self)
        self.level.load()
        
        # Initialize sounds
        self.init_sounds()
        
        # Reference to pacman (set by level loader)
        self.pacman = None
    
    def init_sounds(self):
        """Initialize game sounds."""
        try:
            self.chomp_sound = pygame.mixer.Sound("assets/sounds/pacman_chomp.wav")
            self.ghost_eaten_sound = pygame.mixer.Sound("assets/sounds/ghost_eaten.wav")
            self.powerup_sound = pygame.mixer.Sound("assets/sounds/powerup.wav")
        except pygame.error:
            print("Warning: Could not load one or more sound files")
            self.chomp_sound = None
            self.ghost_eaten_sound = None
            self.powerup_sound = None
    
    def process_events(self):
        """Process game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == STATE_PLAYING:
                        self.state = STATE_PAUSED
                    elif self.state == STATE_PAUSED:
                        self.state = STATE_PLAYING
                elif event.key == pygame.K_RETURN:
                    if self.state in [STATE_MENU, STATE_GAMEOVER]:
                        self.start_new_game()
                elif self.state == STATE_PLAYING and self.pacman:
                    self.pacman.handle_input(event.key)
    
    def update(self):
        """Update game state."""
        if self.state != STATE_PLAYING:
            return
        
        # Update all sprites
        for sprite in self.all_sprites:
            if isinstance(sprite, Ghost):
                sprite.update(self.wall_group, pygame.Vector2(self.pacman.rect.center))
            else:
                sprite.update(self.wall_group)
        
        # Handle collisions
        self.handle_collisions()
        
        # Check if level is complete
        if self.level.is_complete():
            self.state = STATE_GAMEOVER
    
    def draw(self):
        """Draw game screen."""
        self.screen.fill((0, 0, 0))
        
        # Draw all sprites
        self.all_sprites.draw(self.screen)
        
        # Draw score and lives
        self.draw_hud()
        
        # Draw state-specific overlays
        if self.state == STATE_MENU:
            self.draw_menu()
        elif self.state == STATE_PAUSED:
            self.draw_pause_screen()
        elif self.state == STATE_GAMEOVER:
            self.draw_game_over()
    
    def handle_collisions(self):
        """Handle all game collisions."""
        if not self.pacman:
            return
            
        # Pacman with pellets
        pellet_hits = pygame.sprite.spritecollide(self.pacman, self.pellet_group, True)
        if pellet_hits:
            self.score += len(pellet_hits) * PELLET_SCORE
            if self.chomp_sound:
                self.chomp_sound.play()
        
        # Pacman with power pellets
        power_hits = pygame.sprite.spritecollide(self.pacman, self.powerpellet_group, True)
        if power_hits:
            self.score += len(power_hits) * POWERPELLET_SCORE
            if self.powerup_sound:
                self.powerup_sound.play()
            for ghost in self.ghost_group:
                ghost.enter_frightened_mode()
        
        # Pacman with ghosts
        ghost_hits = pygame.sprite.spritecollide(self.pacman, self.ghost_group, False)
        for ghost in ghost_hits:
            if ghost.state == "frightened":
                ghost.get_eaten()
                self.score += GHOST_SCORE
                if self.ghost_eaten_sound:
                    self.ghost_eaten_sound.play()
            elif ghost.state != "eaten":
                self.lives -= 1
                if self.lives <= 0:
                    self.state = STATE_GAMEOVER
                else:
                    self.level.reset_positions()
    
    def draw_hud(self):
        """Draw heads-up display (score and lives)."""
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 40))
    
    def draw_menu(self):
        """Draw menu screen."""
        font = pygame.font.Font(None, 74)
        title = font.render("PACMAN", True, (255, 255, 0))
        font = pygame.font.Font(None, 36)
        start = font.render("Press ENTER to Start", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width()//2 - title.get_width()//2, 200))
        self.screen.blit(start, (self.screen.get_width()//2 - start.get_width()//2, 300))
    
    def draw_pause_screen(self):
        """Draw pause screen overlay."""
        font = pygame.font.Font(None, 74)
        text = font.render("PAUSED", True, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width()//2 - text.get_width()//2, 200))
    
    def draw_game_over(self):
        """Draw game over screen."""
        font = pygame.font.Font(None, 74)
        if self.level.is_complete():
            text = font.render("YOU WIN!", True, (255, 255, 0))
        else:
            text = font.render("GAME OVER", True, (255, 0, 0))
        score = font.render(f"Score: {self.score}", True, (255, 255, 255))
        font = pygame.font.Font(None, 36)
        restart = font.render("Press ENTER to Play Again", True, (255, 255, 255))
        
        self.screen.blit(text, (self.screen.get_width()//2 - text.get_width()//2, 200))
        self.screen.blit(score, (self.screen.get_width()//2 - score.get_width()//2, 300))
        self.screen.blit(restart, (self.screen.get_width()//2 - restart.get_width()//2, 400))
    
    def start_new_game(self):
        """Start a new game."""
        self.score = 0
        self.lives = 3
        self.state = STATE_PLAYING
        
        # Clear all sprite groups
        for group in [self.all_sprites, self.pacman_group, self.ghost_group,
                     self.wall_group, self.pellet_group, self.powerpellet_group]:
            group.empty()
        
        # Reload level
        self.level.load()
