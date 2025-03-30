"""
Main module for Pac-Man game
Initializes pygame, creates all game objects, and runs the main game loop
"""
import pygame
import sys
import time
from constants import *
from maze import Maze
from entities import Pacman, Ghost
from score import ScoreManager
from game_states import GameStateManager

class PacmanGame:
    """
    Main game class that coordinates all game elements and the main loop
    """
    
    def __init__(self):
        """Initialize the game, pygame, and all game objects"""
        # Initialize pygame
        pygame.init()
        pygame.display.set_caption("Pac-Man")
        
        # Create the game window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Create game objects
        self.maze = Maze()
        self.score_manager = ScoreManager()
        self.game_state = GameStateManager()
        
        # Ensure maze has a valid Pacman spawn point
        if not self.maze.pacman_spawn:
            print("ERROR: No Pacman spawn point found")
            self.maze.pacman_spawn = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 3 * TILE_SIZE)
        else:
            print(f"Initial Pacman spawn: {self.maze.pacman_spawn}")
        
        # Create Pacman at its dedicated spawn point
        self.pacman = Pacman(*self.maze.pacman_spawn)
        
        # Create ghosts, ensuring they start in ghost area
        self.ghosts = [
            Ghost(*self.maze.ghost_spawns[BLINKY], BLINKY),
            Ghost(*self.maze.ghost_spawns[PINKY], PINKY),
            Ghost(*self.maze.ghost_spawns[INKY], INKY),
            Ghost(*self.maze.ghost_spawns[CLYDE], CLYDE)
        ]
        
        # Track timing for delta time calculation
        self.last_time = time.time()
        
        # Sound effects (optional)
        self.load_sounds()
        
    def load_sounds(self):
        """Load sound effects (if pygame.mixer is available)"""
        self.sounds = {}
        try:
            # Initialize pygame mixer
            pygame.mixer.init()
            
            # Load sound effects (these would need to be created/downloaded separately)
            # self.sounds["start"] = pygame.mixer.Sound("sounds/start.wav")
            # self.sounds["munch"] = pygame.mixer.Sound("sounds/munch.wav")
            # self.sounds["power_pellet"] = pygame.mixer.Sound("sounds/power_pellet.wav")
            # self.sounds["eat_ghost"] = pygame.mixer.Sound("sounds/eat_ghost.wav")
            # self.sounds["death"] = pygame.mixer.Sound("sounds/death.wav")
            # self.sounds["win"] = pygame.mixer.Sound("sounds/win.wav")
        except:
            print("Warning: pygame.mixer could not be initialized. Sound is disabled.")
    
    def play_sound(self, sound_name):
        """Play a sound effect if available"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def reset_game(self):
        """Reset the game state for a new game"""
        # Reset score and lives
        self.score_manager.reset()
        
        # Reset maze (regenerate pellets)
        self.maze = Maze()
        
        # Ensure maze has a valid Pacman spawn point
        if not self.maze.pacman_spawn:
            print("ERROR: No Pacman spawn point found during reset")
            self.maze.pacman_spawn = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 3 * TILE_SIZE)
        else:
            print(f"Reset Pacman spawn: {self.maze.pacman_spawn}")
            
        # Reset Pac-Man position and initialize movement
        self.pacman.reset_position(*self.maze.pacman_spawn)
        self.pacman.direction = STOP
        self.pacman.next_direction = None
        
        # Reset ghost positions and states
        for ghost in self.ghosts:
            ghost_type = ghost.ghost_type
            ghost.__init__(*self.maze.ghost_spawns[ghost_type], ghost_type)
    
    def check_collisions(self):
        """Check for collisions between Pac-Man and ghosts"""
        pacman_pos = self.pacman.get_pixel_position()
        
        for ghost in self.ghosts:
            ghost_pos = ghost.get_pixel_position()
            
            # Calculate distance between Pac-Man and ghost
            distance = ((pacman_pos[0] - ghost_pos[0]) ** 2 + 
                        (pacman_pos[1] - ghost_pos[1]) ** 2) ** 0.5
            
            # If they are close enough, handle collision
            if distance < TILE_SIZE - 2:  # Slightly less than a tile for better feel
                if ghost.is_frightened():
                    # Pac-Man eats the ghost
                    ghost.set_eaten()
                    self.score_manager.add_score(self.score_manager.get_ghost_score())
                    self.play_sound("eat_ghost")
                elif not ghost.is_eaten() and not self.pacman.invincible:
                    # Ghost catches Pac-Man
                    if self.score_manager.lose_life():
                        # Still has lives, reset positions
                        self.pacman.reset_position(*self.maze.pacman_spawn)
                        for g in self.ghosts:
                            g_type = g.ghost_type
                            g.reset_position(*self.maze.ghost_spawns[g_type])
                        self.play_sound("death")
                    else:
                        # Game over
                        self.game_state.set_state(GAME_OVER)
                        self.play_sound("death")
    
    def update(self):
        """Update all game objects based on current state"""
        # Calculate delta time
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        # Update game state
        self.game_state.update()
        
        # If not playing, don't update the game
        if not self.game_state.is_playing():
            return
            
        # Process input for Pac-Man
        keys = pygame.key.get_pressed()
        self.pacman.handle_input(keys)
        
        # Update Pac-Man
        self.pacman.update(dt, self.maze, self.score_manager)
        
        # Check if power pellet was eaten
        if self.pacman.is_power_active():
            # Set all ghosts to frightened mode
            for ghost in self.ghosts:
                if not ghost.is_frightened() and not ghost.is_eaten():
                    ghost.set_frightened()
                    self.play_sound("power_pellet")
                
        # Update ghosts
        for ghost in self.ghosts:
            ghost.update(dt, self.maze, self.pacman)
            
        # Check for collisions
        self.check_collisions()
        
        # Check if all pellets are eaten
        if self.maze.remaining_pellets == 0:
            # Level complete - advance to next level
            self.game_state.set_state("level_complete", 180)  # 3 seconds at 60 FPS
            self.score_manager.advance_level()
            self.maze = Maze()  # Reset maze with fresh pellets
            self.pacman.reset_position(*self.maze.pacman_spawn)
            # Reset ghost positions and states
            for ghost in self.ghosts:
                ghost_type = ghost.ghost_type
                ghost.__init__(*self.maze.ghost_spawns[ghost_type], ghost_type)
            self.play_sound("win")
    
    def render(self):
        """Render all game elements to the screen"""
        # Draw maze
        self.maze.draw(self.screen)
        
        # Draw Pac-Man
        self.pacman.draw(self.screen)
        
        # Draw ghosts
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        
        # Draw score
        self.score_manager.draw(self.screen)
        
        # Draw state-specific overlays
        self.game_state.draw_overlay(self.screen, self.score_manager)
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        """Run the main game loop"""
        running = True
        
        while running:
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                # Handle events that affect game state
                self.game_state.handle_event(event)
                
                # Handle key events for direct actions
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # 'R' key resets the game
                        self.reset_game()
                        self.game_state.set_state(PLAYING)
            
            # Update game state
            if self.game_state.state == START and self.game_state.state != "level_complete":
                # Reset game when at the start screen
                self.reset_game()
            
            # Update game objects
            self.update()
            
            # Render everything
            self.render()
            
            # Cap the frame rate
            self.clock.tick(FPS)
        
        # Save high score before exiting
        self.score_manager.save_high_score()
        
        # Quit pygame
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    # Create and run the game
    game = PacmanGame()
    game.run() 