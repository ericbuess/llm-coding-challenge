import pygame
import sys
from constants import *
from maze import Maze
from entities import Pacman, Ghost
from score import ScoreManager
from game_states import StartState, PlayState, PauseState, GameOverState, WinState

class PacmanGame:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Create the screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 50))
        pygame.display.set_caption("Pac-Man")
        
        # Create the clock for controlling frame rate
        self.clock = pygame.time.Clock()
        
        # Create game objects
        self.maze = Maze()
        self.score_manager = ScoreManager()
        
        # Create ghosts first (so pacman can reference them)
        self.ghosts = [
            Ghost("blinky", self.maze),
            Ghost("pinky", self.maze),
            Ghost("inky", self.maze),
            Ghost("clyde", self.maze)
        ]
        
        # Create pacman with reference to ghosts (for inky targeting)
        self.pacman = Pacman(self.maze)
        self.pacman.ghosts = self.ghosts  # Add reference to ghosts
        
        # Create game states
        self.states = {
            START: StartState(self),
            PLAY: PlayState(self),
            PAUSE: PauseState(self),
            GAME_OVER: GameOverState(self),
            WIN: WinState(self)
        }
        
        # Set initial state
        self.current_state = START
        
        # Flag to track if the game is running
        self.running = True
    
    def set_state(self, state):
        """Change the current game state."""
        self.current_state = state
    
    def lose_life(self):
        """Handle Pac-Man losing a life."""
        self.pacman.lives -= 1
        
        if self.pacman.lives <= 0:
            # Game over
            self.set_state(GAME_OVER)
        else:
            # Reset positions but continue playing
            self.reset_positions()
    
    def reset_positions(self):
        """Reset Pac-Man and ghost positions."""
        self.pacman.reset_position(self.maze)
        
        # Reset ghosts to their spawn positions
        for ghost in self.ghosts:
            spawn_pos = self.maze.ghost_spawns[ghost.ghost_type]
            ghost.x = spawn_pos[0] * TILE_SIZE + TILE_SIZE // 2
            ghost.y = spawn_pos[1] * TILE_SIZE + TILE_SIZE // 2
            ghost.direction = STOP
            ghost.next_direction = STOP
            ghost.set_state(ghost.SCATTER)
    
    def reset_game(self):
        """Reset the entire game to starting state."""
        # Reset maze (recreate to restore pellets)
        self.maze = Maze()
        
        # Reset ghosts first
        self.ghosts = [
            Ghost("blinky", self.maze),
            Ghost("pinky", self.maze),
            Ghost("inky", self.maze),
            Ghost("clyde", self.maze)
        ]
        
        # Reset Pac-Man with reference to ghosts
        self.pacman = Pacman(self.maze)
        self.pacman.ghosts = self.ghosts
        
        # Reset score but keep high score
        self.score_manager.reset_score()
    
    def run(self):
        """Main game loop."""
        self.running = True
        
        # Main game loop
        while self.running:
            # Calculate delta time in milliseconds
            dt = self.clock.tick(FPS)
            
            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Pause toggle
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p and self.current_state == PLAY:
                        self.set_state(PAUSE)
                    elif event.key == pygame.K_p and self.current_state == PAUSE:
                        self.set_state(PLAY)
            
            # Pass events to current state
            if not self.states[self.current_state].handle_events(events):
                self.running = False
            
            # Update current state
            self.states[self.current_state].update(dt)
            
            # Draw current state
            self.states[self.current_state].draw(self.screen)
            
            # Update the display
            pygame.display.flip()
        
        # Quit pygame when loop exits
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = PacmanGame()
    game.run()
