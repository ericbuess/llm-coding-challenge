import pygame
import sys
import random
from . import constants as C
from .maze import Maze
from .entities import Pacman, Ghost, tile_to_pixel, pixel_to_tile

class Game:
    """
    Main class to manage the Pac-Man game logic, state, and rendering.
    """
    def __init__(self):
        pygame.init()
        # Consider adding sound initialization here if needed: pygame.mixer.init()
        self.screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(C.FONT_NAME, C.FONT_SIZE)
        self.running = True
        self.game_state = "START" # Possible states: START, PLAY, PAUSE, GAME_OVER, WIN
        self.maze = None
        self.pacman = None
        self.ghosts = []
        self.score = 0
        self.high_score = self._load_high_score()
        self.lives = C.START_LIVES
        self.level = 1

        # Ghost state management timers
        self.ghost_mode_timer = 0
        self.current_ghost_mode = C.SCATTER # Start with scatter
        # Define the scatter/chase cycle pattern (time, mode)
        # Example: Scatter 7s, Chase 20s, Scatter 7s, Chase 20s, Scatter 5s, Chase indefinite
        self.ghost_mode_pattern = [
            (C.SCATTER_TIME, C.SCATTER),
            (C.CHASE_TIME, C.CHASE),
            (C.SCATTER_TIME, C.SCATTER),
            (C.CHASE_TIME, C.CHASE),
            (5, C.SCATTER), # Shorter scatter
            (C.CHASE_TIME, C.CHASE), # Another chase
            (5, C.SCATTER), # Shorter scatter
            (float('inf'), C.CHASE) # Chase indefinitely
        ]
        self.ghost_mode_index = 0

        self._initialize_level()

    def _initialize_level(self):
        """Sets up the maze, Pac-Man, and ghosts for the current level."""
        print(f"Initializing Level {self.level}...")
        maze_file = f"pacman_game/{C.MAZE_FILE}" # Assuming maze file is in pacman_game dir
        try:
            self.maze = Maze(maze_file)
        except SystemExit as e:
            print(e)
            self.running = False
            return # Stop initialization if maze file not found

        if not self.maze.pacman_spawn_point:
             print("Error: Pacman spawn point 'P' not found in maze file.")
             self.running = False
             return
        if not self.maze.ghost_spawn_points or len(self.maze.ghost_spawn_points) < 4:
             print("Error: Not enough ghost spawn points 'G' found in maze file (need 4).")
             # Decide how to handle: maybe spawn fewer ghosts or error out
             # For now, we'll proceed but might crash later if ghosts list is accessed incorrectly.


        self.pacman = Pacman(self.maze.pacman_spawn_point[0], self.maze.pacman_spawn_point[1])
        self.pacman.score = self.score # Carry over score
        self.pacman.lives = self.lives # Carry over lives

        self.ghosts = []
        ghost_types = ['blinky', 'pinky', 'inky', 'clyde']
        colors = [C.RED, C.PINK, C.CYAN, C.ORANGE]
        # Use defined spawn points if available, otherwise default or error
        spawn_points = self.maze.ghost_spawn_points
        if len(spawn_points) < 4:
             # Fallback: use the first spawn point for all if not enough found
             print("Warning: Using default spawn point for some ghosts due to lack of 'G' markers.")
             default_spawn = spawn_points[0] if spawn_points else (C.GRID_WIDTH // 2, C.GRID_HEIGHT // 2 - 2) # Arbitrary fallback
             while len(spawn_points) < 4:
                 spawn_points.append(default_spawn)


        # Assign scatter targets (can be refined based on maze)
        scatter_targets = [
            (C.GRID_WIDTH - 2, 0), # Blinky: Top right
            (1, 0),                # Pinky: Top left
            (C.GRID_WIDTH - 2, C.GRID_HEIGHT - 2), # Inky: Bottom right
            (1, C.GRID_HEIGHT - 2) # Clyde: Bottom left
        ]

        for i in range(4):
            spawn_tile = spawn_points[i]
            ghost = Ghost(spawn_tile[0], spawn_tile[1], ghost_types[i], colors[i], scatter_targets[i])
            # Set initial state/timers if needed (e.g., staggered exit from house)
            ghost.home_tile = spawn_tile # Set home for respawn
            self.ghosts.append(ghost)

        # Reset ghost mode cycle
        self.ghost_mode_timer = 0
        self.ghost_mode_index = 0
        self.current_ghost_mode = self.ghost_mode_pattern[0][1]
        self._set_ghosts_mode(self.current_ghost_mode) # Initialize ghost states

        self.game_state = "PLAY" # Start playing immediately after init for now
        # Or could go to a "READY" state first

    def _load_high_score(self):
        """Loads the high score from a file."""
        try:
            with open("pacman_game/highscore.txt", "r") as f:
                return int(f.read())
        except (FileNotFoundError, ValueError):
            return 0

    def _save_high_score(self):
        """Saves the high score to a file."""
        try:
            with open("pacman_game/highscore.txt", "w") as f:
                f.write(str(self.high_score))
        except IOError:
            print("Error: Could not save high score.")

    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(C.FPS) / 1000.0 # Delta time in seconds

            self._handle_events()
            self._update(dt)
            self._render()

        self._save_high_score()
        pygame.quit()
        sys.exit()

    def _handle_events(self):
        """Processes player input and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if self.game_state == "PLAY":
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "PAUSE" # Simple pause toggle
                    else:
                        self.pacman.handle_input(event.key)
                elif self.game_state == "START":
                    if event.key == pygame.K_RETURN:
                        self._initialize_level() # Start game
                elif self.game_state == "PAUSE":
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "PLAY" # Resume
                elif self.game_state == "GAME_OVER" or self.game_state == "WIN":
                    if event.key == pygame.K_RETURN:
                        # Reset for new game
                        self.score = 0
                        self.lives = C.START_LIVES
                        self.level = 1
                        self._initialize_level()
                        self.game_state = "START" # Go back to start screen


    def _update(self, dt):
        """Updates all game objects based on the current state."""
        if self.game_state != "PLAY":
            return # Don't update game logic if not playing

        # Update Pacman
        self.pacman.update(dt, self.maze)
        self.score = self.pacman.score # Update game score from pacman

        # Update Ghost mode (Scatter/Chase cycle)
        self._update_ghost_mode(dt)

        # Update Ghosts
        blinky = self._get_ghost('blinky') # Needed for Inky's AI
        for ghost in self.ghosts:
            # Pass pacman and blinky references for AI targeting
            ghost.update(dt, self.maze, self.pacman, blinky)

        # Check Collisions
        self._check_collisions()

        # Check Win Condition
        if self.maze.all_pellets_eaten():
            self.game_state = "WIN"
            # Play win sound/animation?
            if self.score > self.high_score:
                 self.high_score = self.score


    def _update_ghost_mode(self, dt):
        """Manages the scatter/chase mode cycles for ghosts."""
        if self.pacman.power_mode_timer > 0:
             # Frightened mode overrides scatter/chase cycle
             # Check if ghosts need to be set to FRIGHTENED (handled in collision or pacman update)
             return

        self.ghost_mode_timer += dt
        current_duration, current_mode = self.ghost_mode_pattern[self.ghost_mode_index]

        if self.ghost_mode_timer >= current_duration:
            self.ghost_mode_timer = 0 # Reset timer for the new mode
            self.ghost_mode_index += 1
            # Check if we've reached the end of the pattern (indefinite chase)
            if self.ghost_mode_index >= len(self.ghost_mode_pattern):
                self.ghost_mode_index = len(self.ghost_mode_pattern) - 1 # Stay in the last mode

            new_mode = self.ghost_mode_pattern[self.ghost_mode_index][1]
            if new_mode != self.current_ghost_mode:
                self.current_ghost_mode = new_mode
                self._set_ghosts_mode(self.current_ghost_mode)
                # print(f"Switching ghost mode to: {'SCATTER' if new_mode == C.SCATTER else 'CHASE'}") # Debug


    def _set_ghosts_mode(self, mode):
        """Sets the state for all ghosts (unless they are Frightened or Eaten)."""
        for ghost in self.ghosts:
            if ghost.current_state != C.FRIGHTENED and ghost.current_state != C.EATEN:
                ghost.set_state(mode)


    def _get_ghost(self, ghost_type):
        """Helper to find a specific ghost by type."""
        for ghost in self.ghosts:
            if ghost.ghost_type == ghost_type:
                return ghost
        return None


    def _check_collisions(self):
        """Checks for collisions between Pacman and Ghosts."""
        pacman_tile = self.pacman.get_tile_pos()
        for ghost in self.ghosts:
            ghost_tile = ghost.get_tile_pos()

            # Simple tile-based collision check
            if pacman_tile == ghost_tile:
                if ghost.current_state == C.FRIGHTENED:
                    # Eat the ghost
                    if self.pacman.eat_ghost(): # eat_ghost handles scoring
                        ghost.set_state(C.EATEN)
                        # Play ghost eaten sound
                        # Add brief pause/visual effect?
                elif ghost.current_state != C.EATEN:
                    # Pacman caught!
                    self.pacman.lose_life()
                    self.lives = self.pacman.lives
                    # Play death sound
                    if self.lives <= 0:
                        self.game_state = "GAME_OVER"
                        if self.score > self.high_score:
                            self.high_score = self.score
                    else:
                        # Reset positions for next life
                        self._reset_life()


    def _reset_life(self):
        """Resets Pacman and Ghosts to starting positions after losing a life."""
        self.pacman.reset_position()
        for ghost in self.ghosts:
            ghost.reset_position()
        # Add a brief pause or "Ready?" state before resuming?
        self.game_state = "PLAY" # Or "READY"
        # Reset ghost mode cycle? Or continue where it left off? (Arcade continues)
        self.ghost_mode_timer = 0 # Reset timer maybe?
        self.ghost_mode_index = 0 # Restart cycle?
        self.current_ghost_mode = self.ghost_mode_pattern[0][1]
        self._set_ghosts_mode(self.current_ghost_mode)


    def _render(self):
        """Draws all game elements to the screen."""
        self.screen.fill(C.BLACK) # Background

        if self.game_state == "START":
            self._draw_text("PAC-MAN", C.YELLOW, C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 4, size=36)
            self._draw_text("Press ENTER to Start", C.WHITE, C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2)
            self._draw_text(f"High Score: {self.high_score}", C.WHITE, C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT * 3 // 4)
        elif self.game_state == "GAME_OVER":
            self._draw_text("GAME OVER", C.RED, C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 4, size=36)
            self._draw_text(f"Your Score: {self.score}", C.WHITE, C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2)
            self._draw_text("Press ENTER to Play Again", C.WHITE, C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT * 3 // 4)
        elif self.game_state == "WIN":
            self._draw_text("YOU WIN!", C.YELLOW, C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 4, size=36)
            self._draw_text(f"Your Score: {self.score}", C.WHITE, C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2)
            self._draw_text("Press ENTER to Play Again", C.WHITE, C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT * 3 // 4)
        elif self.game_state == "PAUSE":
            # Optionally draw maze/entities dimmed?
            self.maze.draw(self.screen)
            self.pacman.draw(self.screen)
            for ghost in self.ghosts:
                ghost.draw(self.screen)
            self._draw_ui()
            # Draw pause message overlay
            self._draw_text("PAUSED", C.YELLOW, C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2, size=36)
            self._draw_text("Press ESC to Resume", C.WHITE, C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2 + 40)

        elif self.game_state == "PLAY":
            # Draw Maze (walls, pellets)
            self.maze.draw(self.screen)

            # Draw Entities
            self.pacman.draw(self.screen)
            for ghost in self.ghosts:
                ghost.draw(self.screen)

            # Draw UI (Score, Lives)
            self._draw_ui()

        pygame.display.flip() # Update the full screen


    def _draw_ui(self):
        """Draws the score and lives indicator."""
        # Score Text
        score_text = f"Score: {self.score}"
        self._draw_text(score_text, C.WHITE, 80, C.SCREEN_HEIGHT - 30, align="left")

        # High Score Text
        high_score_text = f"High Score: {self.high_score}"
        self._draw_text(high_score_text, C.WHITE, C.SCREEN_WIDTH - 80, C.SCREEN_HEIGHT - 30, align="right")

        # Lives Indicator (draw small Pac-Man icons)
        life_radius = C.TILE_SIZE // 2
        for i in range(self.lives):
            x = 30 + i * (life_radius * 2 + 5) # Position lives icons at bottom left
            y = C.SCREEN_HEIGHT - 25
            pygame.draw.circle(self.screen, C.YELLOW, (x, y), life_radius)


    def _draw_text(self, text, color, x, y, size=C.FONT_SIZE, align="center"):
        """Helper function to draw text on the screen."""
        font = pygame.font.SysFont(C.FONT_NAME, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "center":
            text_rect.center = (x, y)
        elif align == "left":
            text_rect.midleft = (x, y)
        elif align == "right":
            text_rect.midright = (x, y)
        self.screen.blit(text_surface, text_rect)


if __name__ == '__main__':
    game = Game()
    # Add a check for running flag in case initialization failed
    if game.running:
         game.run()