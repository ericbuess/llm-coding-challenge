# main.py
# Game loop and state management for Pac-Man

import pygame
from constants import *
from maze import Maze
from entities import PacMan, Ghost
from score import ScoreManager
from sound import SoundManager

# Game states
game_states = ['start', 'play', 'gameover', 'win']

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.state = 'start'
        self.maze = Maze()
        self.score = ScoreManager()
        self.sound = SoundManager()
        self.pacman = PacMan(13, 26)
        self.ghosts = [
            Ghost(13, 14, RED, 'blinky'),
            Ghost(13, 17, PINK, 'pinky'),
            Ghost(11, 17, CYAN, 'inky'),
            Ghost(15, 17, ORANGE, 'clyde')
        ]
        self.ghost_timers = {g.ghost_type: 0 for g in self.ghosts}
        self.ghost_exit_times = GHOST_EXIT_DELAYS.copy()
        self.lives = 3
        self.font = pygame.font.SysFont('Arial', 24)
        self.reset()

    def reset(self):
        self.pacman = PacMan(13, 26)
        self.ghosts = [
            Ghost(13, 14, RED, 'blinky'),
            Ghost(13, 17, PINK, 'pinky'),
            Ghost(11, 17, CYAN, 'inky'),
            Ghost(15, 17, ORANGE, 'clyde')
        ]
        self.lives = 3
        self.state = 'start'
        self.maze = Maze()
        self.score.reset()

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.state == 'start' and event.key == pygame.K_SPACE:
                        self.state = 'play'
                        self.sound.play('start')
                    elif self.state in ['gameover', 'win'] and event.key == pygame.K_SPACE:
                        self.reset()
                    elif self.state == 'play':
                        if event.key == pygame.K_UP:
                            self.pacman.set_direction((0, -1))
                        elif event.key == pygame.K_DOWN:
                            self.pacman.set_direction((0, 1))
                        elif event.key == pygame.K_LEFT:
                            self.pacman.set_direction((-1, 0))
                        elif event.key == pygame.K_RIGHT:
                            self.pacman.set_direction((1, 0))
            if self.state == 'play':
                self.update()
            self.draw()
        pygame.quit()

    def update(self):
        self.pacman.update(self.maze)
        for ghost in self.ghosts:
            ghost.update(self.maze, self.pacman, self.ghosts)
        # Pellet collision
        result = self.maze.eat_pellet(self.pacman.x, self.pacman.y)
        if result == 'pellet':
            self.score.add(PELLET_SCORE)
            self.sound.play('chomp')
        elif result == 'power_pellet':
            self.score.add(POWER_PELLET_SCORE)
            self.sound.play('power_pellet')
            for ghost in self.ghosts:
                ghost.frighten()
        # Ghost collision
        for ghost in self.ghosts:
            if (ghost.x, ghost.y) == (self.pacman.x, self.pacman.y):
                if ghost.state == 'frightened':
                    ghost.eaten()
                    self.score.add(GHOST_SCORE)
                    self.sound.play('eat_ghost')
                elif ghost.state != 'eaten':
                    self.lives -= 1
                    self.sound.play('death')
                    if self.lives <= 0:
                        self.state = 'gameover'
                    else:
                        self.pacman = PacMan(13, 26)
            
        if self.maze.pellets_left() == 0:
            self.state = 'win'

    def draw(self):
        self.screen.fill(BLACK)
        self.maze.draw(self.screen)
        self.pacman.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        # Draw score and lives
        score_text = self.font.render(f"Score: {self.score.score}", True, WHITE)
        high_text = self.font.render(f"High Score: {self.score.high_score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, YELLOW)
        self.screen.blit(score_text, (10, 0))
        self.screen.blit(high_text, (220, 0))
        self.screen.blit(lives_text, (10, SCREEN_HEIGHT - 30))
        # Draw state overlays
        if self.state == 'start':
            self.draw_centered("Press SPACE to Start")
        elif self.state == 'gameover':
            self.draw_centered("Game Over! Press SPACE to Restart")
        elif self.state == 'win':
            self.draw_centered("You Win! Press SPACE to Restart")
        pygame.display.flip()

    def draw_centered(self, text):
        surf = self.font.render(text, True, WHITE)
        rect = surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(surf, rect)
