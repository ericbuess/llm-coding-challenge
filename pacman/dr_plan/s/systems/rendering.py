import pygame
from typing import List, Tuple
from ..entities.pacman import PacMan
from ..entities.ghost import Ghost, GhostMode
from ..entities.maze import Maze

class Renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.font = pygame.font.Font(None, 36)  # Default Pygame font
        self.small_font = pygame.font.Font(None, 24)

    def clear_screen(self) -> None:
        """Clear the screen with black background."""
        self.screen.fill((0, 0, 0))

    def draw_maze(self, maze: Maze) -> None:
        """Draw the maze walls and pellets."""
        maze.draw(self.screen)

    def draw_pacman(self, pacman: PacMan) -> None:
        """Draw Pac-Man with basic animation."""
        if not pacman.alive:
            return

        # For now, just draw a simple circle
        pygame.draw.circle(self.screen, (255, 255, 0),
                         (int(pacman.x), int(pacman.y)),
                         pacman.size // 2)

    def draw_ghost(self, ghost: Ghost) -> None:
        """Draw a ghost with appropriate color based on state."""
        color = {
            "blinky": (255, 0, 0),    # Red
            "pinky": (255, 182, 255),  # Pink
            "inky": (0, 255, 255),     # Cyan
            "clyde": (255, 182, 85)    # Orange
        }.get(ghost.ghost_type, (255, 0, 0))

        if ghost.mode == GhostMode.FRIGHTENED:
            color = (0, 0, 255)  # Blue when frightened
        elif ghost.mode == GhostMode.EATEN:
            color = (255, 255, 255)  # White when eaten

        # Draw ghost body (simple circle for now)
        pygame.draw.circle(self.screen, color,
                         (int(ghost.x), int(ghost.y)),
                         ghost.size // 2)

    def draw_ghosts(self, ghosts: List[Ghost]) -> None:
        """Draw all ghosts."""
        for ghost in ghosts:
            self.draw_ghost(ghost)

    def draw_score(self, score: int) -> None:
        """Draw the score at the top of the screen."""
        score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def draw_lives(self, lives: int) -> None:
        """Draw remaining lives at the bottom of the screen."""
        lives_text = self.font.render(f"Lives: {lives}", True, (255, 255, 255))
        self.screen.blit(lives_text, (10, self.height - 40))

    def draw_game_over(self, score: int) -> None:
        """Draw game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))

        # Game Over text
        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        score_text = self.font.render(f"Final Score: {score}", True, (255, 255, 255))
        restart_text = self.small_font.render("Press SPACE to restart", True, (255, 255, 255))

        # Center the text
        game_over_rect = game_over_text.get_rect(center=(self.width//2, self.height//2 - 40))
        score_rect = score_text.get_rect(center=(self.width//2, self.height//2))
        restart_rect = restart_text.get_rect(center=(self.width//2, self.height//2 + 40))

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)

    def draw_win_screen(self, score: int) -> None:
        """Draw victory screen."""
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))

        win_text = self.font.render("YOU WIN!", True, (0, 255, 0))
        score_text = self.font.render(f"Final Score: {score}", True, (255, 255, 255))
        restart_text = self.small_font.render("Press SPACE to restart", True, (255, 255, 255))

        win_rect = win_text.get_rect(center=(self.width//2, self.height//2 - 40))
        score_rect = score_text.get_rect(center=(self.width//2, self.height//2))
        restart_rect = restart_text.get_rect(center=(self.width//2, self.height//2 + 40))

        self.screen.blit(win_text, win_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)

    def draw_ready_screen(self) -> None:
        """Draw 'Ready!' screen at game start."""
        ready_text = self.font.render("READY!", True, (255, 255, 0))
        ready_rect = ready_text.get_rect(center=(self.width//2, self.height//2))
        self.screen.blit(ready_text, ready_rect)

    def draw_pause_screen(self) -> None:
        """Draw pause screen overlay."""
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))

        pause_text = self.font.render("PAUSED", True, (255, 255, 255))
        continue_text = self.small_font.render("Press ESC to continue", True, (255, 255, 255))

        pause_rect = pause_text.get_rect(center=(self.width//2, self.height//2 - 20))
        continue_rect = continue_text.get_rect(center=(self.width//2, self.height//2 + 20))

        self.screen.blit(pause_text, pause_rect)
        self.screen.blit(continue_text, continue_rect) 