import pygame
import math
from ..game.constants import *

class Display:
    def __init__(self):
        self.screen = None
        self.font = None
        self.small_font = None
        
    def initialize(self):
        """Initialize the display and create the game window"""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man")
        try:
            self.font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
        except:
            # Font initialization failed, we'll skip text rendering
            self.font = None
            self.small_font = None
        return self.screen
    
    def draw_maze(self, screen, board):
        """Draw the maze walls"""
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if board.is_wall(x, y):
                    # Draw wall as a filled rectangle
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, BLUE, rect)
                    
                    # Add some detail to walls - draw slightly smaller inner rectangle
                    inner_rect = pygame.Rect(
                        x * TILE_SIZE + 2, 
                        y * TILE_SIZE + 2, 
                        TILE_SIZE - 4, 
                        TILE_SIZE - 4
                    )
                    pygame.draw.rect(screen, (0, 0, 100), inner_rect)
    
    def draw_pellets(self, screen, board):
        """Draw all pellets and power pellets"""
        # Draw regular pellets
        for x, y in board.pellets:
            center_x = x * TILE_SIZE + TILE_SIZE // 2
            center_y = y * TILE_SIZE + TILE_SIZE // 2
            pygame.draw.circle(screen, WHITE, (center_x, center_y), 2)
        
        # Draw power pellets (larger and pulsing could be added later)
        for x, y in board.power_pellets:
            center_x = x * TILE_SIZE + TILE_SIZE // 2
            center_y = y * TILE_SIZE + TILE_SIZE // 2
            pygame.draw.circle(screen, WHITE, (center_x, center_y), 6)
    
    def draw_ghost_house(self, screen, board):
        """Draw the ghost house door"""
        # Find the door tiles (marked with '-' in the maze)
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if y < len(board.maze) and x < len(board.maze[y]):
                    if board.maze[y][x] == '-':
                        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE // 2)
                        pygame.draw.rect(screen, PINK, rect)
    
    def draw_score(self, screen, score, lives, level):
        """Draw the score, lives, and level information"""
        if self.font and self.small_font:
            # Draw score
            score_text = self.font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))
            
            # Draw level
            level_text = self.small_font.render(f"Level: {level}", True, WHITE)
            screen.blit(level_text, (SCREEN_WIDTH - 100, 10))
            
            # Draw lives text
            lives_text = self.small_font.render("Lives:", True, WHITE)
            screen.blit(lives_text, (10, SCREEN_HEIGHT - 30))
        
        # Draw lives (as small Pac-Man icons) - this works without fonts
        for i in range(lives):
            x = 70 + i * 25
            y = SCREEN_HEIGHT - 20
            pygame.draw.circle(screen, YELLOW, (x, y), 8)
            # Draw mouth (simple version)
            pygame.draw.polygon(screen, BLACK, [(x, y), (x + 8, y - 4), (x + 8, y + 4)])
    
    def draw_game_state_text(self, screen, text, subtitle=""):
        """Draw centered text for game states (game over, paused, etc.)"""
        if self.font and self.small_font:
            # Draw main text
            text_surface = self.font.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            
            # Draw background box
            padding = 20
            bg_rect = text_rect.inflate(padding * 2, padding * 2)
            pygame.draw.rect(screen, BLACK, bg_rect)
            pygame.draw.rect(screen, WHITE, bg_rect, 2)
            
            screen.blit(text_surface, text_rect)
            
            # Draw subtitle if provided
            if subtitle:
                subtitle_surface = self.small_font.render(subtitle, True, WHITE)
                subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
                screen.blit(subtitle_surface, subtitle_rect)
    
    def clear(self, screen):
        """Clear the screen"""
        screen.fill(BLACK)
    
    def update(self):
        """Update the display"""
        pygame.display.flip()
    
    def draw_pacman(self, screen, pacman):
        """Draw Pacman with animated mouth"""
        center_x = int(pacman.x + TILE_SIZE // 2)
        center_y = int(pacman.y + TILE_SIZE // 2)
        radius = TILE_SIZE // 2 - 2
        
        if pacman.is_moving and not pacman.is_dying:
            # Animate mouth based on movement
            mouth_angle = abs(pacman.animation_frame - 15) * 3  # 0-45 degrees
            
            # Determine the direction for mouth orientation
            if pacman.direction == RIGHT:
                start_angle = mouth_angle
                end_angle = 360 - mouth_angle
            elif pacman.direction == LEFT:
                start_angle = 180 + mouth_angle
                end_angle = 180 - mouth_angle
            elif pacman.direction == UP:
                start_angle = 90 + mouth_angle
                end_angle = 90 - mouth_angle
            elif pacman.direction == DOWN:
                start_angle = 270 + mouth_angle
                end_angle = 270 - mouth_angle
            else:
                start_angle = mouth_angle
                end_angle = 360 - mouth_angle
            
            # Draw Pac-Man body with mouth
            # First draw a full circle
            pygame.draw.circle(screen, YELLOW, (center_x, center_y), radius)
            
            # Then draw a triangle for the mouth
            if mouth_angle > 5:  # Only draw mouth if it's open enough
                # Calculate mouth vertices
                angle1 = math.radians(start_angle)
                angle2 = math.radians(end_angle)
                
                mouth_x1 = center_x + radius * math.cos(angle1)
                mouth_y1 = center_y - radius * math.sin(angle1)
                mouth_x2 = center_x + radius * math.cos(angle2)
                mouth_y2 = center_y - radius * math.sin(angle2)
                
                pygame.draw.polygon(screen, BLACK, [
                    (center_x, center_y),
                    (mouth_x1, mouth_y1),
                    (mouth_x2, mouth_y2)
                ])
        else:
            # Draw closed mouth Pac-Man
            pygame.draw.circle(screen, YELLOW, (center_x, center_y), radius)
    
    def draw_ghost(self, screen, ghost):
        """Draw a ghost"""
        center_x = int(ghost.x + TILE_SIZE // 2)
        center_y = int(ghost.y + TILE_SIZE // 2)
        
        # Determine ghost color based on mode
        if ghost.mode == 'frightened':
            color = BLUE
        elif ghost.mode == 'eyes':
            color = WHITE
        else:
            color = ghost.color
        
        # Draw ghost body (simple rectangle with rounded top)
        body_rect = pygame.Rect(ghost.x + 2, ghost.y + 4, TILE_SIZE - 4, TILE_SIZE - 4)
        pygame.draw.rect(screen, color, body_rect)
        pygame.draw.circle(screen, color, (center_x, center_y), TILE_SIZE // 2 - 2)
        
        # Draw eyes (simple white circles)
        if ghost.mode != 'eyes':
            eye_y = center_y - 3
            # Left eye
            pygame.draw.circle(screen, WHITE, (center_x - 5, eye_y), 3)
            pygame.draw.circle(screen, BLACK, (center_x - 5, eye_y), 1)
            # Right eye
            pygame.draw.circle(screen, WHITE, (center_x + 5, eye_y), 3)
            pygame.draw.circle(screen, BLACK, (center_x + 5, eye_y), 1)