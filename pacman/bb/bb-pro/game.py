import pygame
import random
from constants import *
from sprites import Pacman, Ghost, Pellet

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 36)
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()
        self.pellets = pygame.sprite.Group()
        
        # Create Pacman
        self.pacman = Pacman(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.all_sprites.add(self.pacman)
        
        # Create Ghosts
        ghost_colors = [BLUE, (255, 0, 0), (255, 192, 203), (255, 128, 0)]  # Blue, Red, Pink, Orange
        for i, color in enumerate(ghost_colors):
            ghost = Ghost(100 + i * 100, 100, color)
            self.all_sprites.add(ghost)
            self.ghosts.add(ghost)
        
        # Create Pellets
        self.create_pellets()
        
    def create_pellets(self):
        # Create regular pellets
        for _ in range(50):
            x = random.randint(20, SCREEN_WIDTH - 20)
            y = random.randint(20, SCREEN_HEIGHT - 20)
            pellet = Pellet(x, y)
            self.all_sprites.add(pellet)
            self.pellets.add(pellet)
            
        # Create power pellets (4 corners)
        corner_positions = [
            (50, 50),
            (SCREEN_WIDTH - 50, 50),
            (50, SCREEN_HEIGHT - 50),
            (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50)
        ]
        for pos in corner_positions:
            power_pellet = Pellet(pos[0], pos[1], True)
            self.all_sprites.add(power_pellet)
            self.pellets.add(power_pellet)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    
    def update(self):
        self.all_sprites.update()
        
        # Check for pellet collisions
        pellet_collisions = pygame.sprite.spritecollide(self.pacman, self.pellets, True)
        for pellet in pellet_collisions:
            self.pacman.score += pellet.points
            
        # Check for ghost collisions
        if pygame.sprite.spritecollide(self.pacman, self.ghosts, False):
            self.running = False
            
        # Check win condition
        if not self.pellets:
            self.running = False
        
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f'Score: {self.pacman.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
