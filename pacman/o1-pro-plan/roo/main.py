"""
Pac-Man Game
Main module that initializes the game and runs the main game loop
"""

import pygame
import sys
import os
from constants import *
from maze import Maze
from entities import Pacman, Ghost
from score import ScoreManager
from game_states import GameState, GameStateManager

class PacmanGame:
    def __init__(self):
        """Initialize the game"""
        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption("Pac-Man")
        
        # Create the game window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Load game sounds
        self.load_sounds()
        
        # Initialize game objects
        self.maze = Maze()
        self.score_manager = ScoreManager()
        self.state_manager = GameStateManager(self.screen)
        
        # Initialize entities
        self.init_entities()
        
        # Game running flag
        self.running = True
        
        # Start music
        if hasattr(self, 'start_music') and self.start_music:
            self.start_music.play(-1)  # Loop indefinitely
    
    def load_sounds(self):
        """Load game sounds if available"""
        # Try to load sounds, but continue if they're unavailable
        try:
            self.munch_sound = pygame.mixer.Sound(os.path.join('sounds', 'munch.wav'))
            self.power_pellet_sound = pygame.mixer.Sound(os.path.join('sounds', 'power_pellet.wav'))
            self.eat_ghost_sound = pygame.mixer.Sound(os.path.join('sounds', 'eat_ghost.wav'))
            self.death_sound = pygame.mixer.Sound(os.path.join('sounds', 'death.wav'))
            self.start_music = pygame.mixer.Sound(os.path.join('sounds', 'start.wav'))
        except:
            # If sounds can't be loaded, just continue without them
            print("Warning: Sounds could not be loaded. Continuing without sound.")
            self.munch_sound = None
            self.power_pellet_sound = None
            self.eat_ghost_sound = None
            self.death_sound = None
            self.start_music = None
    
    def init_entities(self):
        """Initialize Pac-Man and ghost entities"""
        # Create Pac-Man
        pacman_pos = self.maze.pacman_start
        self.pacman = Pacman(pacman_pos[0], pacman_pos[1])
        
        # Create the ghosts
        self.ghosts = []
        
        # Create each ghost with its starting position and type
        ghost_types = ['BLINKY', 'PINKY', 'INKY', 'CLYDE']
        for ghost_type in ghost_types:
            if ghost_type in self.maze.ghost_starts:
                pos = self.maze.ghost_starts[ghost_type]
            else:
                # Use default positions if not found in the maze
                pos = (14, 14)  # Center of ghost house
            
            ghost = Ghost(pos[0], pos[1], ghost_type)
            self.ghosts.append(ghost)
    
    def reset_game(self):
        """Reset the game state for a new game"""
        # Reset the maze (respawn pellets)
        self.maze = Maze()
        
        # Reset the score
        self.score_manager.reset_score()
        
        # Reset entities
        self.init_entities()
    
    def reset_level(self):
        """Reset entity positions when Pac-Man loses a life"""
        # Reset Pac-Man position
        pacman_pos = self.maze.pacman_start
        self.pacman.reset_position(pacman_pos[0], pacman_pos[1])
        
        # Reset ghost positions and states
        for ghost in self.ghosts:
            ghost_type = ghost.ghost_type
            if ghost_type in self.maze.ghost_starts:
                pos = self.maze.ghost_starts[ghost_type]
            else:
                pos = (14, 14)  # Center of ghost house
            
            ghost.reset_position(pos[0], pos[1])
            ghost.reset_state()
    
    def handle_input(self):
        """Handle player input events"""
        # Collect all events in a list so we can use them for both quit checking and state management
        self.events = pygame.event.get()
        
        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False
        
        # We'll handle the rest of the input processing in update
    
    def update(self, dt):
        """Update game logic"""
        # Update game state using the events collected in handle_input
        self.state_manager.update(dt, self.events)
        
        # If the game is in the START state and was previously in GAME_OVER or WIN,
        # reset the game
        if (self.state_manager.current_state == GameState.START and
            (self.state_manager.prev_state == GameState.GAME_OVER or
             self.state_manager.prev_state == GameState.WIN)):
            self.reset_game()
        
        # Only update game logic if in PLAY state
        if not self.state_manager.is_playing():
            return
        
        # Get keyboard state for Pac-Man control
        keys = pygame.key.get_pressed()
        self.pacman.handle_input(keys)
        
        # Update Pac-Man
        self.pacman.update(dt, self.maze)
        
        # Check if Pac-Man eats a pellet
        if self.pacman.check_pellet_collision(self.maze, self.score_manager):
            # Play munching sound
            if self.maze.is_power_pellet(*self.pacman.get_tile_pos()) and self.power_pellet_sound:
                self.power_pellet_sound.play()
                # Set all ghosts to frightened mode
                for ghost in self.ghosts:
                    ghost.set_frightened()
                # Reset ghost combo
                self.score_manager.reset_ghost_combo()
            elif self.munch_sound:
                self.munch_sound.play()
        
        # Update ghosts
        blinky_position = None
        for ghost in self.ghosts:
            # Find Blinky's position for Inky's targeting
            if ghost.ghost_type == 'BLINKY':
                blinky_position = ghost.get_tile_pos()
                break
        
        for ghost in self.ghosts:
            # Update each ghost with the current state
            ghost.update(dt, self.maze, self.pacman, blinky_position)
            
            # Check for collision with Pac-Man - use a more precise pixel-based distance check
            dx = abs(self.pacman.x - ghost.x)
            dy = abs(self.pacman.y - ghost.y)
            collision_distance = TILE_SIZE * 0.7  # Slightly less than a tile
            
            if dx < collision_distance and dy < collision_distance:
                if ghost.state == Ghost.FRIGHTENED:
                    # Pac-Man eats the ghost
                    ghost.set_eaten()
                    if self.eat_ghost_sound:
                        self.eat_ghost_sound.play()
                    self.score_manager.eat_ghost()
                
                elif ghost.state != Ghost.EATEN:
                    # Ghost eats Pac-Man
                    if self.death_sound:
                        self.death_sound.play()
                    
                    # Lose a life and reset positions
                    if self.pacman.lose_life():
                        self.reset_level()
                    else:
                        # Game over
                        self.state_manager.handle_death(0)
        
        # Check if all pellets are eaten (win condition)
        if self.maze.all_pellets_eaten():
            self.state_manager.handle_win()
    
    def draw(self):
        """Draw the game elements to the screen"""
        # Clear the screen
        self.screen.fill(BLACK)
        
        # Draw the maze
        self.maze.draw(self.screen)
        
        # Draw the entities (in the correct order)
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        
        self.pacman.draw(self.screen)
        
        # Draw the score and lives
        self.score_manager.draw(self.screen, self.pacman.lives)
        
        # Draw any state-specific overlays
        self.state_manager.draw_overlay()
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            # Calculate delta time for frame-rate independent movement
            dt = self.clock.tick(FPS) / 1000.0  # Convert milliseconds to seconds
            
            # Handle input events
            self.handle_input()
            
            # Update game logic
            self.update(dt)
            
            # Draw everything
            self.draw()
        
        # Clean up when the game exits
        self.quit()
    
    def quit(self):
        """Clean up resources and quit"""
        # Save high score before exiting
        self.score_manager.save_high_score()
        
        # Quit Pygame
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    # Create and run the game
    game = PacmanGame()
    game.run()