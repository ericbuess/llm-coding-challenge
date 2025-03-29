import pygame
import sys
from constants import *
from maze import Maze
from entities import Pacman, Ghost, pixel_to_tile, tile_center_pixel
from score import ScoreManager

# --- Game States ---
START = 0
PLAYING = 1
PAUSED = 2
GAME_OVER = 3
WIN = 4

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man Clone")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36) # Font for messages
        self.small_font = pygame.font.Font(None, 24)
        self.running = True
        self.state = START
        self.maze = Maze() # Uses DEFAULT_MAZE from maze.py for now
        self.score_manager = ScoreManager()

        # Find initial positions (Ensure these tiles are valid paths in DEFAULT_MAZE)
        # Pac-Man typically starts near bottom center
        self.pacman_start_pos = (13, 23) # Example: Adjust based on maze layout
        # Ghost start positions (often near or inside the house)
        self.ghost_start_positions = {
            BLINKY: (13, 11), # Outside house
            PINKY: (13, 14), # Inside house
            INKY: (11, 14),   # Inside house
            CLYDE: (15, 14)   # Inside house
        }
        self.ghost_colors = { BLINKY: RED, PINKY: PINK, INKY: CYAN, CLYDE: ORANGE }

        self.pacman = None
        self.ghosts = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        self.pacman_lives_icon = None # For score display
        self.ghost_mode_timer = 0
        self.current_ghost_mode_index = 0
        # Scatter/Chase sequence (time, mode)
        self.ghost_mode_sequence = [
            (SCATTER_TIME_1, SCATTER),
            (CHASE_TIME_1, CHASE),
            (SCATTER_TIME_2, SCATTER),
            (CHASE_TIME_2, CHASE),
            (SCATTER_TIME_3, SCATTER),
            (CHASE_TIME_3, CHASE),
            (SCATTER_TIME_4, SCATTER),
            (float('inf'), CHASE) # Chase indefinitely
        ]

        self._setup_game()

    def _setup_game(self, reset_score=True):
        """Initializes or resets game entities and state for a new game or level."""
        # Clear existing sprites
        self.all_sprites.empty()
        self.ghosts.empty()

        # Create Pac-Man
        self.pacman = Pacman(self.pacman_start_pos[0], self.pacman_start_pos[1])
        self.all_sprites.add(self.pacman)

        # Create Ghosts
        for ghost_type, start_pos in self.ghost_start_positions.items():
             ghost = Ghost(start_pos[0], start_pos[1], ghost_type, self.ghost_colors[ghost_type])
             self.ghosts.add(ghost)
             self.all_sprites.add(ghost)

        # Reset maze pellets if starting a new game (or level)
        if reset_score:
            self.maze = Maze() # Re-parse the layout to restore pellets
            self.score_manager.reset_score()
            self.pacman.lives = 3 # Reset lives only on full game reset

        # Reset ghost mode timer and state
        self.current_ghost_mode_index = 0
        self.ghost_mode_timer = 0
        self.set_ghost_mode(self.ghost_mode_sequence[0][1]) # Start with Scatter

        # Create a small icon for lives display
        self.pacman_lives_icon = pygame.Surface([TILE_SIZE // 2, TILE_SIZE // 2])
        pygame.draw.circle(self.pacman_lives_icon, YELLOW, (TILE_SIZE // 4, TILE_SIZE // 4), TILE_SIZE // 4)


    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0 # Delta time in seconds

            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if self.state == START:
                    self.state = PLAYING
                elif self.state == PLAYING:
                    if event.key == pygame.K_ESCAPE:
                        self.state = PAUSED
                    else:
                        self.pacman.handle_input(event)
                elif self.state == PAUSED:
                    if event.key == pygame.K_ESCAPE:
                        self.state = PLAYING
                elif self.state in [GAME_OVER, WIN]:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self._setup_game(reset_score=True)
                        self.state = PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
            # Pass keydown events to Pacman even if not playing (to buffer input)
            # This might be needed if player presses key during state transition
            # Consider if this is desired behavior
            if self.state != PLAYING and self.pacman: # Check if pacman exists
                self.pacman.handle_input(event)


    def update(self, dt):
        if self.state != PLAYING:
            return # Only update game logic when playing

        # --- Update Ghost Mode (Scatter/Chase Cycle) ---
        self.ghost_mode_timer += dt
        current_duration, current_mode = self.ghost_mode_sequence[self.current_ghost_mode_index]

        if self.ghost_mode_timer >= current_duration:
            self.current_ghost_mode_index += 1
            if self.current_ghost_mode_index < len(self.ghost_mode_sequence):
                next_duration, next_mode = self.ghost_mode_sequence[self.current_ghost_mode_index]
                self.set_ghost_mode(next_mode)
                self.ghost_mode_timer = 0 # Reset timer for the new mode
            else:
                # Stay in the last mode (typically indefinite chase)
                self.current_ghost_mode_index -= 1 # Keep pointing to the last mode
                self.ghost_mode_timer = 0 # Prevent it from re-triggering immediately

        # --- Update Entities ---
        power_pellet_eaten = self.pacman.update(dt, self.maze, self.score_manager)
        if power_pellet_eaten:
            self.activate_frightened_mode()
            self.score_manager.reset_ghost_streak() # Reset streak when new power pellet eaten

        # If Pacman power mode ends, reset ghost streak
        if not self.pacman.power_mode and self.score_manager.ghost_eaten_streak > 0:
            # Check if this is the exact frame power mode ended
            # Need a flag or previous state check to call reset only once
             pass # Ghost state change handles speed/color, streak reset here or on pellet eat

        # Update Ghosts (passing Pacman for targeting)
        # Need to pass Blinky's position for Inky later
        # Find Blinky (assuming only one Blinky)
        blinky = None
        for ghost in self.ghosts:
            if ghost.ghost_type == BLINKY:
                 blinky = ghost
                 break

        for ghost in self.ghosts:
            # Pass Blinky ref if implementing accurate Inky
            # ghost.update(dt, self.maze, self.pacman, blinky)
            ghost.update(dt, self.maze, self.pacman)

        # --- Check Collisions ---
        self.check_collisions()

        # --- Check Win/Loss Conditions ---
        if self.maze.get_pellet_count() == 0:
            self.state = WIN
            # Optional: Add level progression here

        if self.pacman.lives <= 0:
            self.state = GAME_OVER
            self.score_manager.update_high_score_on_game_over()


    def check_collisions(self):
        """Check for collisions between Pac-Man and Ghosts."""
        ghost_collisions = pygame.sprite.spritecollide(self.pacman, self.ghosts, False, pygame.sprite.collide_rect_ratio(0.7))

        for ghost in ghost_collisions:
            if ghost.current_state == FRIGHTENED:
                # Eat the ghost
                ghost.set_state(EATEN)
                self.score_manager.add_ghost_score()
                # Add points animation/sound later
            elif ghost.current_state != EATEN:
                # Pac-Man caught!
                self.pacman.lose_life()
                if self.pacman.lives > 0:
                    self.reset_level_after_death() # Reset positions
                # else: Game over is handled in update loop
                break # Only process one collision per frame

    def reset_level_after_death(self):
        """Resets Pac-Man and ghost positions after losing a life."""
        self.pacman.reset_position(self.pacman_start_pos[0], self.pacman_start_pos[1])
        # Reset ghosts to their starting positions and states (typically Scatter/Chase)
        for ghost in self.ghosts:
             start_pos = self.ghost_start_positions[ghost.ghost_type]
             ghost.pos = tile_center_pixel(start_pos[0], start_pos[1])
             ghost.direction = STOP # Or initial direction if they move immediately
             ghost.intended_direction = STOP
             ghost.rect.center = ghost.pos
             ghost.set_state(self.ghost_mode_sequence[self.current_ghost_mode_index][1]) # Return to current mode
             # TODO: Add logic for ghosts leaving the house one by one if needed

        # Brief pause or animation could go here
        # For now, just reset positions and continue
        self.state = PLAYING # Ensure state is playing

    def activate_frightened_mode(self):
        """Sets all non-eaten ghosts to Frightened state."""
        for ghost in self.ghosts:
            if ghost.current_state != EATEN:
                ghost.set_state(FRIGHTENED)

    def set_ghost_mode(self, mode):
        """Sets the mode for all non-frightened, non-eaten ghosts."""
        for ghost in self.ghosts:
            if ghost.current_state not in [FRIGHTENED, EATEN]:
                ghost.set_state(mode)

    def draw(self):
        self.screen.fill(BLACK)

        if self.state == START:
            self.draw_start_screen()
        elif self.state == PLAYING or self.state == PAUSED:
            self.draw_play_screen()
            if self.state == PAUSED:
                self.draw_pause_screen()
        elif self.state == GAME_OVER:
             self.draw_play_screen() # Draw final game state behind message
             self.draw_game_over_screen()
        elif self.state == WIN:
             self.draw_play_screen() # Draw final game state behind message
             self.draw_win_screen()

        pygame.display.flip()

    def draw_play_screen(self):
        # Draw Maze (walls and remaining pellets)
        self.maze.draw(self.screen)

        # Draw Entities
        self.all_sprites.draw(self.screen)
        # Custom draw for ghosts if needed (e.g., for eyes when eaten)
        for ghost in self.ghosts:
            if ghost.current_state == EATEN:
                 ghost.draw(self.screen) # Use custom draw for eyes

        # Draw Score and Lives
        self.score_manager.draw(self.screen, self.pacman.lives, self.pacman_lives_icon)

    def draw_start_screen(self):
        self.screen.fill(BLACK)
        title_text = self.font.render("PYTHON PAC-MAN", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        start_prompt = self.small_font.render("Press any key to start", True, WHITE)
        prompt_rect = start_prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self.screen.blit(title_text, title_rect)
        self.screen.blit(start_prompt, prompt_rect)

    def draw_pause_screen(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150)) # Black with alpha
        self.screen.blit(overlay, (0, 0))

        pause_text = self.font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)

    def draw_game_over_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        title_text = self.font.render("GAME OVER", True, RED)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        score_text = self.small_font.render(f"Final Score: {self.score_manager.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        restart_prompt = self.small_font.render("Press Enter/Space to Play Again, ESC to Quit", True, WHITE)
        prompt_rect = restart_prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))

        self.screen.blit(title_text, title_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_prompt, prompt_rect)

    def draw_win_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        title_text = self.font.render("YOU WIN!", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        score_text = self.small_font.render(f"Final Score: {self.score_manager.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        restart_prompt = self.small_font.render("Press Enter/Space to Play Again, ESC to Quit", True, WHITE)
        prompt_rect = restart_prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))

        self.screen.blit(title_text, title_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_prompt, prompt_rect)

if __name__ == '__main__':
    game = Game()
    game.run() 