import pygame
import math
from .board import Board
from .entities import Pacman, Ghost
from .constants import *

class GameController:
    """Main game controller that manages game state and logic"""
    def __init__(self):
        self.board = Board()
        self.pacman = None
        self.ghosts = {}
        self.score = 0
        self.lives = STARTING_LIVES
        self.level = 1
        self.game_state = 'playing'  # menu, playing, paused, game_over, level_complete, dying
        self.power_mode_timer = 0
        self.death_timer = 0
        self.initialize_level()
    
    def initialize_level(self):
        """Initialize or reset the level"""
        # Create Pacman at starting position
        self.pacman = Pacman(self.board.pacman_start[0], self.board.pacman_start[1])
        
        # Create ghosts (placeholder for now - will be implemented in Phase 3)
        self.ghosts = {
            'blinky': Ghost(self.board.ghost_starts['blinky'][0], 
                           self.board.ghost_starts['blinky'][1], 
                           'blinky', RED),
            'pinky': Ghost(self.board.ghost_starts['pinky'][0], 
                          self.board.ghost_starts['pinky'][1], 
                          'pinky', PINK),
            'inky': Ghost(self.board.ghost_starts['inky'][0], 
                         self.board.ghost_starts['inky'][1], 
                         'inky', CYAN),
            'clyde': Ghost(self.board.ghost_starts['clyde'][0], 
                          self.board.ghost_starts['clyde'][1], 
                          'clyde', ORANGE)
        }
    
    def handle_input(self, keys):
        """Handle game input"""
        if self.game_state == 'playing':
            self.pacman.handle_input(keys)
        elif self.game_state == 'game_over' or self.game_state == 'level_complete':
            # Press space to restart
            if keys[pygame.K_SPACE]:
                self.restart_game()
    
    def update(self, dt: float):
        """Update game logic"""
        # Handle death animation
        if self.game_state == 'dying':
            self.death_timer -= 1
            if self.death_timer <= 0:
                if self.lives <= 0:
                    self.game_state = 'game_over'
                else:
                    # Reset level
                    self.initialize_level()
                    self.game_state = 'playing'
            return
        
        if self.game_state != 'playing':
            return
        
        # Update Pacman
        self.pacman.update(self.board)
        
        # Check pellet collection
        collection_result = self.pacman.check_pellet_collision(self.board)
        if collection_result['points'] > 0:
            self.score += collection_result['points']
            
            # Check if power pellet was collected
            if collection_result['power_pellet']:
                self.power_mode_timer = POWER_PELLET_DURATION * FPS  # Convert seconds to frames
                # Set all ghosts to frightened mode
                for ghost in self.ghosts.values():
                    ghost.set_frightened(POWER_PELLET_DURATION * FPS)
        
        # Update power mode timer
        if self.power_mode_timer > 0:
            self.power_mode_timer -= 1
        
        # Update ghosts
        blinky = self.ghosts.get('blinky')  # Needed for Inky's AI
        for ghost in self.ghosts.values():
            ghost.update(self.board, self.pacman, blinky)
        
        # Check collisions
        self.handle_collisions()
        
        # Check win condition
        if self.check_win_condition():
            self.game_state = 'level_complete'
    
    def handle_collisions(self):
        """Handle collisions between Pacman and ghosts"""
        for ghost in self.ghosts.values():
            # Check if Pacman and ghost are colliding
            if self.check_collision(self.pacman, ghost):
                if ghost.mode == 'frightened':
                    # Pacman eats the ghost
                    ghost.mode = 'eyes'
                    ghost.speed = GHOST_SPEED * 2  # Eyes move faster
                    self.score += 200  # Points for eating a ghost
                elif ghost.mode == 'eyes':
                    # Eyes don't hurt Pacman
                    continue
                else:
                    # Ghost catches Pacman
                    self.lose_life()
                    break  # Only lose one life per frame
    
    def check_collision(self, pacman, ghost):
        """Check if Pacman and a ghost are colliding"""
        # Calculate distance between centers
        pac_center_x = pacman.x + TILE_SIZE // 2
        pac_center_y = pacman.y + TILE_SIZE // 2
        ghost_center_x = ghost.x + TILE_SIZE // 2
        ghost_center_y = ghost.y + TILE_SIZE // 2
        
        distance = math.sqrt((pac_center_x - ghost_center_x)**2 + 
                           (pac_center_y - ghost_center_y)**2)
        
        # Collision if distance is less than 75% of tile size
        return distance < TILE_SIZE * 0.75
    
    def check_win_condition(self) -> bool:
        """Check if all pellets have been collected"""
        return self.board.get_all_pellets_count() == 0
    
    def next_level(self):
        """Progress to the next level"""
        self.level += 1
        self.board.load_default_maze()  # Reset the maze
        self.initialize_level()
        self.game_state = 'playing'
    
    def restart_game(self):
        """Restart the game from level 1"""
        self.score = 0
        self.lives = STARTING_LIVES
        self.level = 1
        self.board.load_default_maze()
        self.initialize_level()
        self.game_state = 'playing'
    
    def lose_life(self):
        """Handle losing a life"""
        if self.pacman.is_dying:
            return  # Already dying, don't lose multiple lives
        
        self.pacman.is_dying = True
        self.lives -= 1
        self.game_state = 'dying'  # Pause game during death animation
        self.death_timer = 120  # 2 seconds at 60 FPS