# main.py
# Entry point for the Pac-Man game.

import pygame
from constants import *
from maze import Maze
from entities import Pacman, Ghost
from score import ScoreManager
from sound import SoundManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = START # Initial game state
        self.font = pygame.font.Font(None, 36) # Font for messages

        # Game Objects
        self.maze = Maze("layout.txt") # TODO: Ensure layout.txt exists or handle path
        self.score_manager = ScoreManager()
        self.sound_manager = SoundManager()

        # Pacman Initialization
        # TODO: Get start position from maze data
        pacman_start_x, pacman_start_y = 14, 23 # Example starting tile
        self.pacman = Pacman(pacman_start_x, pacman_start_y)

        # Ghost Initialization
        # TODO: Get start positions from maze data
        self.ghosts = pygame.sprite.Group() # Using sprite group might be useful later
        self.blinky = Ghost(13.5, 11, RED, 'blinky') # Approx start
        self.pinky = Ghost(13.5, 14, PINK, 'pinky')
        self.inky = Ghost(11.5, 14, CYAN, 'inky')
        self.clyde = Ghost(15.5, 14, ORANGE, 'clyde')
        self.ghosts.add(self.blinky, self.pinky, self.inky, self.clyde)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0 # Delta time in seconds
            self.handle_events()
            self.update(dt)
            self.render()
        self.quit_game()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.state == PLAYING:
                self.pacman.handle_input(event)
            elif self.state == START:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.start_game()
            elif self.state == GAME_OVER or self.state == WIN:
                 if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                     self.__init__() # Reset the game entirely
                     self.start_game()
                 elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                     self.running = False

    def update(self, dt):
        if self.state == PLAYING:
            # Update Pac-Man
            prev_pellets = len(self.maze.pellets) + len(self.maze.power_pellets)
            self.pacman.update(dt, self.maze, self.score_manager)
            current_pellets = len(self.maze.pellets) + len(self.maze.power_pellets)
            
            # Check if a pellet was eaten and play sound
            if current_pellets < prev_pellets:
                # Check if it was a power pellet
                if self.pacman.power_mode and self.pacman.power_timer >= FRIGHTENED_DURATION - 0.1:
                    # Just started power mode, play power pellet sound
                    self.sound_manager.play_power_pellet()
                else:
                    # Regular pellet eaten
                    self.sound_manager.play_waka()

            # Update Ghosts
            pacman_tile = self.pacman.get_tile_pos()
            pacman_dir = self.pacman.direction
            blinky_tile = self.blinky.get_tile_pos() # Inky needs Blinky's pos
            for ghost in self.ghosts:
                ghost.update(dt, self.maze, pacman_tile, pacman_dir, blinky_tile)

            # Check Collisions
            self.check_collisions()

            # Check Win Condition
            if self.maze.all_pellets_eaten():
                self.state = WIN
                self.score_manager.save_if_needed()
                print("You Win!") # Debug

            # Update Ghost power mode based on Pacman
            if self.pacman.power_mode:
                 if self.pacman.power_timer > 0:
                      # Check if any ghost is not already frightened or eaten
                      for ghost in self.ghosts:
                           if ghost.state != Ghost.FRIGHTENED and ghost.state != Ghost.EATEN:
                                ghost.set_state(Ghost.FRIGHTENED)
                 else: # Power mode timer expired
                      for ghost in self.ghosts:
                           if ghost.state == Ghost.FRIGHTENED:
                                # Revert to previous state (Scatter/Chase)
                                ghost.set_state(ghost.previous_state)

    def check_collisions(self):
         pacman_tile = self.pacman.get_tile_pos()
         for ghost in self.ghosts:
              ghost_tile = ghost.get_tile_pos()
              if pacman_tile == ghost_tile:
                   if ghost.state == Ghost.FRIGHTENED:
                        # Eat ghost
                        print(f"Ate {ghost.ghost_type}!") # Debug
                        ghost.set_state(Ghost.EATEN)
                        points = GHOST_POINTS[self.pacman.score_multiplier]
                        self.score_manager.add_score(points)
                        self.pacman.score_multiplier = min(self.pacman.score_multiplier + 1, 3) # Cap index at 3 (for 1600)
                        # Play ghost eaten sound
                        self.sound_manager.play_eat_ghost()
                   elif ghost.state != Ghost.EATEN:
                        # Pac-Man caught
                        print("Caught by ghost!") # Debug
                        # Play death sound
                        self.sound_manager.play_death()
                        game_over = self.pacman.lose_life()
                        if game_over:
                            self.state = GAME_OVER
                            self.score_manager.save_if_needed()
                            print("Game Over!") # Debug
                        else:
                            # Reset positions (Pac-Man reset in lose_life)
                            self.reset_ghost_positions()
                            self.state = START # Or a brief pause/ready state?
                            # Maybe add a small delay here

    def reset_ghost_positions(self):
         # TODO: More sophisticated reset (place in house, timers)
         self.blinky.x, self.blinky.y = 13.5 * TILE_SIZE, 11 * TILE_SIZE
         self.pinky.x, self.pinky.y = 13.5 * TILE_SIZE, 14 * TILE_SIZE
         self.inky.x, self.inky.y = 11.5 * TILE_SIZE, 14 * TILE_SIZE
         self.clyde.x, self.clyde.y = 15.5 * TILE_SIZE, 14 * TILE_SIZE
         for ghost in self.ghosts:
             ghost.direction = STOP
             ghost.set_state(Ghost.SCATTER) # Reset state on new life

    def render(self):
        self.screen.fill(BLACK)
        if self.state == START:
            self.draw_start_screen()
        elif self.state == PLAYING:
            self.maze.draw(self.screen)
            self.pacman.draw(self.screen)
            for ghost in self.ghosts:
                ghost.draw(self.screen)
            self.score_manager.draw(self.screen)
            self.draw_lives()
        elif self.state == GAME_OVER:
            self.draw_game_over_screen()
        elif self.state == WIN:
            self.draw_win_screen()

        pygame.display.flip()

    def draw_start_screen(self):
        title_text = self.font.render("Pac-Man", True, YELLOW)
        prompt_text = self.font.render("Press SPACE to Start", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(title_text, title_rect)
        self.screen.blit(prompt_text, prompt_rect)
        self.score_manager.draw(self.screen) # Show high score

    def draw_game_over_screen(self):
        go_text = self.font.render("GAME OVER", True, RED)
        prompt_text = self.font.render("Press SPACE to Restart", True, WHITE)
        esc_text = self.font.render("Press ESC to Quit", True, WHITE)
        go_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        esc_rect = esc_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(go_text, go_rect)
        self.screen.blit(prompt_text, prompt_rect)
        self.screen.blit(esc_text, esc_rect)
        self.score_manager.draw(self.screen) # Show final score

    def draw_win_screen(self):
        win_text = self.font.render("YOU WIN!", True, YELLOW)
        prompt_text = self.font.render("Press SPACE to Play Again", True, WHITE)
        win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(win_text, win_rect)
        self.screen.blit(prompt_text, prompt_rect)
        self.score_manager.draw(self.screen) # Show final score

    def draw_lives(self):
         # Draw Pac-Man icons for remaining lives
         for i in range(self.pacman.lives - 1): # Don't draw the current life
              x = 10 + i * (TILE_SIZE * 1.5)
              y = SCREEN_HEIGHT - TILE_SIZE * 1.5
              # Simple yellow circle for now
              pygame.draw.circle(self.screen, YELLOW, (int(x + TILE_SIZE/2), int(y + TILE_SIZE/2)), TILE_SIZE // 2 -1)
              # TODO: Use Pac-Man sprite later

    def start_game(self):
         self.state = PLAYING
         # Reset positions just in case
         self.pacman.reset_position()
         self.reset_ghost_positions()
         self.score_manager.reset_score() # Reset score for new game
         # Play start game sound
         self.sound_manager.play_game_start()

    def quit_game(self):
        self.score_manager.save_if_needed()
        pygame.quit()
        print("Game exited.")

if __name__ == '__main__':
    game = Game()
    game.run()
