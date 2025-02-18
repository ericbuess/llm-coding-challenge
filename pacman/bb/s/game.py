import pygame
import sys
from maze import Maze
from sprites import Pacman, Ghost
from constants import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pacman")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.maze = Maze()
        self.all_sprites = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()
        
        # Create Pacman
        pacman_pos = self.maze.get_pacman_start()
        self.pacman = Pacman(pacman_pos[0], pacman_pos[1])
        self.all_sprites.add(self.pacman)

        # Create Ghosts
        ghost_colors = [RED, PINK, CYAN, ORANGE]
        for pos, color in zip(self.maze.get_ghost_starts(), ghost_colors):
            ghost = Ghost(pos[0], pos[1], color)
            self.ghosts.add(ghost)
            self.all_sprites.add(ghost)

        self.score = 0
        self.game_state = PLAYING
        self.power_pellet_timer = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif self.game_state == PLAYING:
                    if event.key in [UP, DOWN, LEFT, RIGHT]:
                        self.pacman.next_direction = event.key
                elif event.key == pygame.K_SPACE:
                    if self.game_state in [GAME_OVER, WIN]:
                        self.reset_game()
        return True

    def update(self):
        if self.game_state != PLAYING:
            return

        # Update Pacman
        self.pacman.update(self.maze)

        # Check pellet collisions
        pellet_collisions = pygame.sprite.spritecollide(self.pacman, self.maze.pellets, True)
        self.score += len(pellet_collisions) * PELLET_POINTS

        # Check power pellet collisions
        power_collisions = pygame.sprite.spritecollide(self.pacman, self.maze.power_pellets, True)
        if power_collisions:
            self.score += len(power_collisions) * POWER_PELLET_POINTS
            self.power_pellet_timer = pygame.time.get_ticks()
            for ghost in self.ghosts:
                ghost.make_vulnerable()

        # Update ghost vulnerability
        current_time = pygame.time.get_ticks()
        if self.power_pellet_timer > 0 and current_time - self.power_pellet_timer > 10000:  # 10 seconds
            self.power_pellet_timer = 0
            for ghost in self.ghosts:
                ghost.reset_vulnerability()

        # Update Ghosts
        for ghost in self.ghosts:
            ghost.update(self.maze, self.pacman)

        # Check ghost collisions
        ghost_collisions = pygame.sprite.spritecollide(self.pacman, self.ghosts, False)
        if ghost_collisions:
            ghost = ghost_collisions[0]
            if ghost.vulnerable:
                self.score += GHOST_POINTS
                ghost.rect.x = ghost.start_x
                ghost.rect.y = ghost.start_y
                ghost.reset_vulnerability()
            else:
                self.game_state = GAME_OVER

        # Check win condition
        if self.maze.remaining_pellets() == 0:
            self.game_state = WIN

    def draw(self):
        self.screen.fill(BLACK)
        self.maze.draw(self.screen)
        self.all_sprites.draw(self.screen)

        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Draw game over or win message
        if self.game_state == GAME_OVER:
            game_over_text = self.font.render('Game Over! Press SPACE to restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
        elif self.game_state == WIN:
            win_text = self.font.render('You Win! Press SPACE to restart', True, WHITE)
            text_rect = win_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(win_text, text_rect)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
