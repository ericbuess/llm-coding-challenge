import pygame
from pygame import Surface, Color

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)  # Default Pygame font
        
        # Colors
        self.BLACK = Color(0, 0, 0)
        self.BLUE = Color(0, 0, 255)
        self.WHITE = Color(255, 255, 255)
        self.YELLOW = Color(255, 255, 0)
        self.RED = Color(255, 0, 0)
        self.PINK = Color(255, 182, 255)
        self.CYAN = Color(0, 255, 255)
        self.ORANGE = Color(255, 182, 85)

    def clear_screen(self):
        """Clear the screen to black"""
        self.screen.fill(self.BLACK)

    def draw_maze(self, maze):
        """Draw the maze walls and background"""
        for y in range(maze.height):
            for x in range(maze.width):
                if (x, y) in maze.walls:
                    pygame.draw.rect(
                        self.screen,
                        self.BLUE,
                        (x * maze.tile_size, y * maze.tile_size,
                         maze.tile_size, maze.tile_size)
                    )

        # Draw pellets
        for pellet in maze.pellets:
            color = self.WHITE
            radius = pellet.radius
            pygame.draw.circle(
                self.screen,
                color,
                (int(pellet.position.x), int(pellet.position.y)),
                radius
            )

    def draw_entities(self, pacman, ghosts):
        """Draw Pac-Man and ghosts"""
        # Draw Pac-Man
        if pacman.alive:
            pygame.draw.circle(
                self.screen,
                self.YELLOW,
                (int(pacman.position.x), int(pacman.position.y)),
                13  # Pac-Man radius
            )
            
        # Draw ghosts
        for ghost in ghosts:
            color = self.WHITE if ghost.mode == "FRIGHTENED" else {
                "red": self.RED,
                "pink": self.PINK,
                "cyan": self.CYAN,
                "orange": self.ORANGE
            }.get(ghost.color, self.WHITE)
            
            if ghost.is_eaten:
                # Draw eyes only when eaten
                self._draw_ghost_eyes(ghost)
            else:
                # Draw full ghost
                self._draw_ghost(ghost, color)

    def _draw_ghost(self, ghost, color):
        """Helper method to draw a ghost"""
        # Draw ghost body
        pygame.draw.circle(
            self.screen,
            color,
            (int(ghost.position.x), int(ghost.position.y)),
            13  # Ghost radius
        )
        # Draw eyes
        self._draw_ghost_eyes(ghost)

    def _draw_ghost_eyes(self, ghost):
        """Helper method to draw ghost eyes"""
        eye_color = self.WHITE if not ghost.is_eaten else self.BLUE
        pupil_color = self.BLUE if not ghost.is_eaten else self.WHITE
        
        # Left eye
        pygame.draw.circle(
            self.screen,
            eye_color,
            (int(ghost.position.x - 4), int(ghost.position.y - 3)),
            3
        )
        # Right eye
        pygame.draw.circle(
            self.screen,
            eye_color,
            (int(ghost.position.x + 4), int(ghost.position.y - 3)),
            3
        )

    def draw_ui(self, score, lives, level):
        """Draw score, lives, and other UI elements"""
        # Draw score
        score_text = self.font.render(f'Score: {score}', True, self.WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw lives
        lives_text = self.font.render(f'Lives: {lives}', True, self.WHITE)
        self.screen.blit(lives_text, (10, 40))
        
        # Draw level
        level_text = self.font.render(f'Level: {level}', True, self.WHITE)
        self.screen.blit(level_text, (10, 70))

    def draw_game_over(self):
        """Draw game over screen"""
        text = self.font.render('GAME OVER', True, self.RED)
        text_rect = text.get_rect(center=(self.screen.get_width()/2,
                                        self.screen.get_height()/2))
        self.screen.blit(text, text_rect)

    def draw_win(self):
        """Draw win screen"""
        text = self.font.render('YOU WIN!', True, self.YELLOW)
        text_rect = text.get_rect(center=(self.screen.get_width()/2,
                                        self.screen.get_height()/2))
        self.screen.blit(text, text_rect)

    def draw_ready(self):
        """Draw ready screen"""
        text = self.font.render('READY!', True, self.YELLOW)
        text_rect = text.get_rect(center=(self.screen.get_width()/2,
                                        self.screen.get_height()/2))
        self.screen.blit(text, text_rect)
