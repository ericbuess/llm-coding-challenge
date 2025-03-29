import pygame
import config

class Renderer:
    def __init__(self, screen, maze):
        self.screen = screen
        self.maze = maze
        self.tile_size = maze.tile_size
        self.offset_x = (screen.get_width() - maze.width * maze.tile_size) // 2
        self.offset_y = (screen.get_height() - maze.height * maze.tile_size) // 2
        
        # Colors
        self.wall_color = (33, 33, 255)  # Blue
        self.background_color = config.BLACK
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def render_maze(self):
        """Render the maze walls"""
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.maze.is_wall(x, y):
                    pygame.draw.rect(
                        self.screen,
                        self.wall_color,
                        (
                            x * self.tile_size + self.offset_x,
                            y * self.tile_size + self.offset_y,
                            self.tile_size,
                            self.tile_size
                        )
                    )
    
    def render_pellets(self):
        """Render pellets and power pellets"""
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                tile = self.maze.get_tile(x, y)
                if tile == 2:  # Regular pellet
                    center_x = x * self.tile_size + self.tile_size // 2 + self.offset_x
                    center_y = y * self.tile_size + self.tile_size // 2 + self.offset_y
                    pygame.draw.circle(
                        self.screen,
                        config.WHITE,
                        (center_x, center_y),
                        2  # Radius
                    )
                elif tile == 3:  # Power pellet
                    center_x = x * self.tile_size + self.tile_size // 2 + self.offset_x
                    center_y = y * self.tile_size + self.tile_size // 2 + self.offset_y
                    # Make power pellets blink
                    if int(pygame.time.get_ticks() / 200) % 2 == 0:
                        pygame.draw.circle(
                            self.screen,
                            config.WHITE,
                            (center_x, center_y),
                            6  # Radius
                        )
    
    def render_entities(self, entities):
        """Render all game entities"""
        for entity in entities:
            entity.render(self.screen, self.offset_x, self.offset_y)
    
    def render_score(self, score, high_score, level):
        """Render the score and high score"""
        # Draw score
        score_surf = self.font.render(f"SCORE: {score}", True, config.WHITE)
        self.screen.blit(score_surf, (10, 10))
        
        # Draw high score
        high_score_surf = self.font.render(f"HIGH: {high_score}", True, config.WHITE)
        self.screen.blit(high_score_surf, (config.SCREEN_WIDTH - high_score_surf.get_width() - 10, 10))
        
        # Draw level
        level_surf = self.small_font.render(f"LEVEL: {level}", True, config.WHITE)
        self.screen.blit(level_surf, (10, config.SCREEN_HEIGHT - level_surf.get_height() - 10))
    
    def render_lives(self, lives):
        """Render remaining lives as small Pac-Man icons"""
        for i in range(lives):
            # Draw a simple yellow circle for each life
            pygame.draw.circle(
                self.screen,
                config.YELLOW,
                (30 + i * 25, config.SCREEN_HEIGHT - 20),
                8  # Radius
            )
    
    def render_ready_text(self):
        """Render 'READY!' text at game start"""
        ready_surf = self.font.render("READY!", True, config.YELLOW)
        ready_rect = ready_surf.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        self.screen.blit(ready_surf, ready_rect)
    
    def render_game_over(self):
        """Render 'GAME OVER' text"""
        game_over_surf = self.font.render("GAME OVER", True, config.RED)
        game_over_rect = game_over_surf.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_surf, game_over_rect)
    
    def render_intro_screen(self):
        """Render the intro/title screen"""
        # Draw title
        title_surf = pygame.font.Font(None, 72).render("PAC-MAN", True, config.YELLOW)
        title_rect = title_surf.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 4))
        self.screen.blit(title_surf, title_rect)
        
        # Draw "Press ENTER to start"
        start_surf = self.font.render("Press ENTER to start", True, config.WHITE)
        start_rect = start_surf.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT * 3 // 4))
        self.screen.blit(start_surf, start_rect)
        
        # Draw ghost characters and their names
        ghost_y = config.SCREEN_HEIGHT // 2
        ghost_colors = [config.RED, config.PINK, config.CYAN, config.ORANGE]
        ghost_names = ["BLINKY", "PINKY", "INKY", "CLYDE"]
        
        for i, (color, name) in enumerate(zip(ghost_colors, ghost_names)):
            # Draw ghost shape
            pygame.draw.rect(
                self.screen,
                color,
                (config.SCREEN_WIDTH // 4, ghost_y + i * 40, 20, 20)
            )
            
            # Draw name
            name_surf = self.small_font.render(name, True, config.WHITE)
            self.screen.blit(name_surf, (config.SCREEN_WIDTH // 4 + 30, ghost_y + i * 40))