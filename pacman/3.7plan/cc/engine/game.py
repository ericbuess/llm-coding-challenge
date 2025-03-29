import pygame
import config
import os
from engine.input_handler import InputHandler
from engine.renderer import Renderer
from engine.sound import SoundManager
from entities.pacman import Pacman
from entities.blinky import Blinky
from entities.pinky import Pinky
from entities.inky import Inky
from entities.clyde import Clyde
from entities.fruit import Fruit
from maze import Maze
from utils.collision import check_collision

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Screen setup
        self.screen_width = config.SCREEN_WIDTH
        self.screen_height = config.SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pac-Man")
        
        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        
        # Game state
        self.state = "INTRO"  # INTRO, READY, PLAYING, PACMAN_DYING, GHOST_EATEN, LEVEL_COMPLETE, GAME_OVER
        self.level = 1
        self.score = 0
        self.high_score = self.load_high_score()
        self.lives = 3
        self.ghost_score = 200  # Points for eating ghost, doubles each time
        self.next_extra_life_score = 10000
        
        # Load maze
        self.maze = Maze()
        
        # Create renderer
        self.renderer = Renderer(self.screen, self.maze)
        
        # Create input handler
        self.input_handler = InputHandler(self)
        
        # Create sound manager
        self.sound_manager = SoundManager()
        
        # Create entities
        self.pacman = None
        self.ghosts = []
        self.fruit = None
        
        # Ghost mode timing
        self.ghost_mode_timer = 0
        self.ghost_mode_schedule = [
            ("scatter", 7),    # Scatter for 7 seconds
            ("chase", 20),     # Chase for 20 seconds
            ("scatter", 7),    # Scatter for 7 seconds
            ("chase", 20),     # Chase for 20 seconds
            ("scatter", 5),    # Scatter for 5 seconds
            ("chase", 20),     # Chase for 20 seconds
            ("scatter", 5),    # Scatter for 5 seconds
            ("chase", float('inf'))  # Chase permanently
        ]
        self.current_mode_index = 0
        
        # Fruit timing
        self.fruit_timer = 0
        self.fruit_duration = 10  # 10 seconds
        self.fruit_active = False
        
        # For level restart
        self.ready_timer = 0
        self.ready_duration = 2  # 2 seconds "READY!" display
    
    def load_high_score(self):
        """Load high score from file"""
        highscore_path = "highscore.txt"
        try:
            if os.path.exists(highscore_path):
                with open(highscore_path, "r") as file:
                    return int(file.read())
            return 0
        except (FileNotFoundError, ValueError):
            return 0
    
    def save_high_score(self):
        """Save high score to file"""
        try:
            with open("highscore.txt", "w") as file:
                file.write(str(self.high_score))
        except:
            print("Failed to save high score")
    
    def init_level(self):
        """Initialize entities for current level"""
        # Create Pac-Man
        self.pacman = Pacman(14 * self.maze.tile_size, 23 * self.maze.tile_size, self.maze)
        
        # Create ghosts
        blinky = Blinky(14 * self.maze.tile_size, 11 * self.maze.tile_size, self.maze, self.pacman)
        pinky = Pinky(14 * self.maze.tile_size, 14 * self.maze.tile_size, self.maze, self.pacman)
        inky = Inky(12 * self.maze.tile_size, 14 * self.maze.tile_size, self.maze, self.pacman, blinky)
        clyde = Clyde(16 * self.maze.tile_size, 14 * self.maze.tile_size, self.maze, self.pacman)
        
        self.ghosts = [blinky, pinky, inky, clyde]
        
        # Reset ghost mode timer
        self.ghost_mode_timer = 0
        self.current_mode_index = 0
        self.update_ghost_modes()
        
        # No fruit initially
        self.fruit = None
        self.fruit_timer = 0
        self.fruit_active = False
        
        # Set ready timer
        self.ready_timer = 0
        self.state = "READY"
        
        # Play start sound
        self.sound_manager.play("game_start")
    
    def start_game(self):
        """Start a new game"""
        self.level = 1
        self.score = 0
        self.lives = 3
        self.ghost_score = 200
        self.next_extra_life_score = 10000
        
        # Reset maze (repopulate pellets)
        self.maze = Maze()
        
        # Initialize level
        self.init_level()
    
    def update(self):
        """Update game state"""
        if self.paused:
            return
        
        # Get time delta
        dt = self.clock.get_time() / 1000.0  # Convert to seconds
        
        # Handle game states
        if self.state == "INTRO":
            # Just waiting for player to start
            pass
        
        elif self.state == "READY":
            # Show "READY!" text for a moment before starting
            self.ready_timer += dt
            if self.ready_timer >= self.ready_duration:
                self.state = "PLAYING"
                self.sound_manager.play_siren(self.level)
        
        elif self.state == "PLAYING":
            # Update ghost modes
            self.update_ghost_modes(dt)
            
            # Update all entities
            self.pacman.update(dt)
            for ghost in self.ghosts:
                ghost.update(dt)
            
            # Check for collisions
            self.check_ghost_collisions()
            
            # Check for level completion
            if self.maze.pellets_remaining == 0:
                self.state = "LEVEL_COMPLETE"
                self.sound_manager.stop_music()
                # Short delay before next level
                pygame.time.set_timer(pygame.USEREVENT, 3000)  # 3 second delay
            
            # Handle fruit spawning
            self.update_fruit(dt)
            
            # Check fruit collision
            if self.fruit and self.fruit_active:
                if check_collision(self.pacman, self.fruit):
                    self.score += self.fruit.points
                    self.sound_manager.play("eat_fruit")
                    self.fruit_active = False
                    
                    # Update high score if needed
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.save_high_score()
        
        elif self.state == "PACMAN_DYING":
            # Just wait for death animation to complete
            # The pacman.update() method will handle animation and state transition
            self.pacman.update(dt)
            
            # After animation, check if game over
            if not self.pacman.is_dead:
                if self.lives <= 0:
                    self.state = "GAME_OVER"
                    pygame.time.set_timer(pygame.USEREVENT, 3000)  # 3 second delay
                else:
                    # Reset for next life
                    self.reset_level()
        
        elif self.state == "GHOST_EATEN":
            # Brief pause after ghost is eaten
            pass
        
        elif self.state == "LEVEL_COMPLETE":
            # Wait for timer to expire (handled in event processing)
            pass
        
        elif self.state == "GAME_OVER":
            # Wait for timer to expire (handled in event processing)
            pass
    
    def update_ghost_modes(self, dt=0):
        """Update ghost modes based on timer"""
        if self.state != "PLAYING":
            return
        
        self.ghost_mode_timer += dt
        current_mode, duration = self.ghost_mode_schedule[self.current_mode_index]
        
        if self.ghost_mode_timer >= duration:
            # Move to next mode
            self.ghost_mode_timer = 0
            self.current_mode_index = (self.current_mode_index + 1) % len(self.ghost_mode_schedule)
            next_mode, _ = self.ghost_mode_schedule[self.current_mode_index]
            
            # Update all ghosts
            for ghost in self.ghosts:
                if not ghost.is_eaten:
                    ghost.set_mode(next_mode)
            
            # Update music
            if next_mode == "chase" or next_mode == "scatter":
                self.sound_manager.play_siren(self.level)
    
    def frighten_ghosts(self, duration=None):
        """Set all ghosts to frightened mode"""
        # Calculate duration based on level if not provided
        if duration is None:
            index = min(self.level - 1, len(config.POWER_PELLET_DURATIONS) - 1)
            duration = config.POWER_PELLET_DURATIONS[index]
        
        self.ghost_score = 200  # Reset ghost score
        
        for ghost in self.ghosts:
            if not ghost.is_eaten:
                ghost.set_mode("frightened", duration)
        
        # Play frightened music
        self.sound_manager.play_frightened()
    
    def update_fruit(self, dt):
        """Handle fruit spawning and despawning"""
        # Spawn fruit at 70 pellets and 170 pellets remaining
        pellets_needed = [self.maze.total_pellets - 70, self.maze.total_pellets - 170]
        pellets_eaten = self.maze.total_pellets - self.maze.pellets_remaining
        
        if pellets_eaten in pellets_needed and not self.fruit_active and not self.fruit:
            # Spawn fruit
            self.fruit = Fruit(
                14 * self.maze.tile_size,
                17 * self.maze.tile_size,
                self.maze,
                self.level
            )
            self.fruit_active = True
            self.fruit_timer = 0
        
        # Update fruit timer if active
        if self.fruit_active:
            self.fruit_timer += dt
            if self.fruit_timer >= self.fruit_duration:
                self.fruit_active = False
    
    def check_ghost_collisions(self):
        """Check for collisions between Pac-Man and ghosts"""
        for ghost in self.ghosts:
            if check_collision(self.pacman, ghost):
                if ghost.mode == "frightened" and not ghost.is_eaten:
                    # Pac-Man eats ghost
                    ghost.eaten()
                    self.score += self.ghost_score
                    self.sound_manager.play("eat_ghost")
                    self.ghost_score *= 2  # Double points for next ghost
                    
                    # Update high score if needed
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.save_high_score()
                    
                    # Short pause
                    self.state = "GHOST_EATEN"
                    pygame.time.set_timer(pygame.USEREVENT, 500)  # 0.5 second pause
                
                elif not ghost.is_eaten and not self.pacman.is_dead:
                    # Ghost catches Pac-Man
                    self.pacman.die()
                    self.sound_manager.play("death")
                    self.sound_manager.stop_music()
                    self.state = "PACMAN_DYING"
    
    def reset_level(self):
        """Reset entities after Pac-Man dies"""
        # Reset Pac-Man position
        self.pacman.x = 14 * self.maze.tile_size
        self.pacman.y = 23 * self.maze.tile_size
        self.pacman.direction = (0, 0)
        self.pacman.next_direction = (0, 0)
        
        # Reset ghost positions
        blinky = self.ghosts[0]
        blinky.x = 14 * self.maze.tile_size
        blinky.y = 11 * self.maze.tile_size
        
        pinky = self.ghosts[1]
        pinky.x = 14 * self.maze.tile_size
        pinky.y = 14 * self.maze.tile_size
        
        inky = self.ghosts[2]
        inky.x = 12 * self.maze.tile_size
        inky.y = 14 * self.maze.tile_size
        
        clyde = self.ghosts[3]
        clyde.x = 16 * self.maze.tile_size
        clyde.y = 14 * self.maze.tile_size
        
        # Reset ghost modes
        for ghost in self.ghosts:
            ghost.is_eaten = False
            ghost.direction = (0, 0)
        
        self.ghost_mode_timer = 0
        self.current_mode_index = 0
        self.update_ghost_modes()
        
        # Remove fruit
        self.fruit = None
        self.fruit_active = False
        
        # Set ready state
        self.state = "READY"
        self.ready_timer = 0
    
    def next_level(self):
        """Advance to next level"""
        self.level += 1
        
        # Reset maze (repopulate pellets)
        self.maze = Maze()
        
        # Reset Pac-Man position but keep score and lives
        self.pacman.x = 14 * self.maze.tile_size
        self.pacman.y = 23 * self.maze.tile_size
        self.pacman.direction = (0, 0)
        self.pacman.next_direction = (0, 0)
        
        # Reset ghosts with increased difficulty
        for i, ghost in enumerate(self.ghosts):
            # Positions
            if i == 0:  # Blinky
                ghost.x = 14 * self.maze.tile_size
                ghost.y = 11 * self.maze.tile_size
            elif i == 1:  # Pinky
                ghost.x = 14 * self.maze.tile_size
                ghost.y = 14 * self.maze.tile_size
            elif i == 2:  # Inky
                ghost.x = 12 * self.maze.tile_size
                ghost.y = 14 * self.maze.tile_size
            elif i == 3:  # Clyde
                ghost.x = 16 * self.maze.tile_size
                ghost.y = 14 * self.maze.tile_size
            
            # Reset state
            ghost.is_eaten = False
            ghost.direction = (0, 0)
            
            # Adjust speed based on level
            # Increase ghost speed every 2 levels up to level 20
            level_factor = min(self.level, 20) / 2
            ghost.speed = config.GHOST_SPEEDS['normal'] + (level_factor * 0.05)
        
        # Reset ghost modes
        self.ghost_mode_timer = 0
        self.current_mode_index = 0
        self.update_ghost_modes()
        
        # Remove fruit
        self.fruit = None
        self.fruit_active = False
        
        # Set ready state
        self.state = "READY"
        self.ready_timer = 0
    
    def toggle_pause(self):
        """Toggle game pause state"""
        self.paused = not self.paused
    
    def render(self):
        """Render the current game state"""
        # Clear screen
        self.screen.fill(config.BLACK)
        
        if self.state == "INTRO":
            # Render intro screen
            self.renderer.render_intro_screen()
        
        elif self.state in ["READY", "PLAYING", "PACMAN_DYING", "GHOST_EATEN"]:
            # Render maze
            self.renderer.render_maze()
            
            # Render pellets
            self.renderer.render_pellets()
            
            # Render fruit if active
            if self.fruit and self.fruit_active:
                self.fruit.render(self.screen, self.renderer.offset_x, self.renderer.offset_y)
            
            # Render Pac-Man and ghosts
            self.renderer.render_entities(self.ghosts + [self.pacman])
            
            # Render score and lives
            self.renderer.render_score(self.score, self.high_score, self.level)
            self.renderer.render_lives(self.lives)
            
            # Render "READY!" text if in ready state
            if self.state == "READY":
                self.renderer.render_ready_text()
        
        elif self.state == "GAME_OVER":
            # Render maze and entities in background
            self.renderer.render_maze()
            self.renderer.render_entities(self.ghosts + [self.pacman])
            
            # Render game over screen
            self.renderer.render_game_over()
        
        # Display paused message if paused
        if self.paused:
            paused_surf = pygame.font.Font(None, 48).render("PAUSED", True, config.WHITE)
            paused_rect = paused_surf.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(paused_surf, paused_rect)
        
        # Update display
        pygame.display.flip()
    
    def handle_events(self):
        """Process input events"""
        self.input_handler.process_events()
        
        # Check for any custom events
        for event in pygame.event.get(pygame.USEREVENT):
            if self.state == "GHOST_EATEN":
                # Resume game after ghost eaten pause
                self.state = "PLAYING"
            
            elif self.state == "LEVEL_COMPLETE":
                # Advance to next level
                self.next_level()
            
            elif self.state == "GAME_OVER":
                # Return to intro screen
                self.state = "INTRO"
    
    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            self.handle_events()
            
            # Update game state
            self.update()
            
            # Render frame
            self.render()
            
            # Maintain frame rate
            self.clock.tick(config.FPS)
        
        # Save high score before quitting
        self.save_high_score()
        
        # Clean up
        pygame.quit()