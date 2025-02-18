"""Main gameplay view for Pac-Man."""
import arcade
from typing import List
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, Direction, GhostState,
    SCORE_PELLET, SCORE_POWER_PELLET, SCORE_GHOST,
    POWER_PELLET_DURATION, GHOST_MODE_DURATIONS,
    FONT_SIZE, SCORE_POSITION, LIVES_POSITION
)
from player import PacMan
from ghost import Ghost
from maze import Maze
from utils.asset_manager import asset_manager

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        
        # Game objects
        self.maze: Maze = None
        self.player: PacMan = None
        self.ghosts: List[Ghost] = []
        
        # Game state
        self.paused = False
        self.game_over = False
        self.power_pellet_timer = 0
        self.ghost_mode_timer = 0
        self.current_ghost_mode_index = 0
        
        # Sound effects
        self.chomp_sound = asset_manager.get_sound("chomp.wav")
        self.power_pellet_sound = asset_manager.get_sound("power_pellet.wav")
        self.ghost_eaten_sound = asset_manager.get_sound("ghost_eaten.wav")
        self.death_sound = asset_manager.get_sound("death.wav")
        
    def setup(self):
        """Set up the game."""
        # Load the maze
        self.maze = Maze("level1.tmx")
        
        # Create Pac-Man at starting position
        self.player = PacMan()
        start_x, start_y = self.maze.player_start
        self.player.reset_position(start_x, start_y)
        
        # Create ghosts at their starting positions
        ghost_types = ["blinky", "pinky", "inky", "clyde"]
        self.ghosts = []
        for ghost_type, start_pos in zip(ghost_types, self.maze.ghost_starts):
            ghost = Ghost(ghost_type)
            ghost.start_x, ghost.start_y = start_pos[0], start_pos[1]
            ghost.reset_position()
            self.ghosts.append(ghost)
        
        # Reset timers and game state
        self.power_pellet_timer = 0
        self.ghost_mode_timer = 0
        self.current_ghost_mode_index = 0
        self.paused = False
        self.game_over = False
    
    def on_update(self, delta_time: float):
        """Update game state."""
        if self.paused or self.game_over:
            return
            
        # Update Pac-Man
        self.player.update(delta_time, self.maze.wall_list)
        
        # Check for pellet collisions
        pellet = self.maze.remove_pellet(
            self.player.center_x,
            self.player.center_y
        )
        if pellet:
            if pellet in self.maze.power_pellet_list:
                self.power_pellet_timer = POWER_PELLET_DURATION
                self.player.score += SCORE_POWER_PELLET
                for ghost in self.ghosts:
                    if ghost.state != GhostState.EATEN:
                        ghost.set_state(GhostState.FRIGHTENED)
                arcade.play_sound(self.power_pellet_sound)
            else:
                self.player.score += SCORE_PELLET
                arcade.play_sound(self.chomp_sound)
        
        # Update ghost modes and states
        if self.power_pellet_timer > 0:
            self.power_pellet_timer -= delta_time
            if self.power_pellet_timer <= 0:
                for ghost in self.ghosts:
                    if ghost.state == GhostState.FRIGHTENED:
                        ghost.set_state(
                            GhostState.SCATTER
                            if self.current_ghost_mode_index % 2 == 0
                            else GhostState.CHASE
                        )
        
        # Update ghost mode timer
        self.ghost_mode_timer += delta_time
        if self.ghost_mode_timer >= GHOST_MODE_DURATIONS[self.current_ghost_mode_index]:
            self.ghost_mode_timer = 0
            self.current_ghost_mode_index += 1
            if self.current_ghost_mode_index >= len(GHOST_MODE_DURATIONS):
                self.current_ghost_mode_index = len(GHOST_MODE_DURATIONS) - 1
            
            # Update ghost states
            new_state = (
                GhostState.SCATTER
                if self.current_ghost_mode_index % 2 == 0
                else GhostState.CHASE
            )
            for ghost in self.ghosts:
                if ghost.state != GhostState.FRIGHTENED and ghost.state != GhostState.EATEN:
                    ghost.set_state(new_state)
        
        # Update ghosts
        for ghost in self.ghosts:
            ghost.update(delta_time, self.maze.wall_list, self.player)
            
            # Check for collisions with Pac-Man
            if arcade.check_for_collision(self.player, ghost):
                if ghost.state == GhostState.FRIGHTENED:
                    # Eat the ghost
                    ghost.set_state(GhostState.EATEN)
                    self.player.score += SCORE_GHOST[0]  # For now, just use first score
                    arcade.play_sound(self.ghost_eaten_sound)
                elif ghost.state != GhostState.EATEN:
                    # Pac-Man dies
                    self.player.lives -= 1
                    arcade.play_sound(self.death_sound)
                    if self.player.lives <= 0:
                        self.game_over = True
                    else:
                        self.reset_positions()
        
        # Check for level completion
        if self.maze.is_complete():
            # You could transition to a new level here
            self.game_over = True
    
    def reset_positions(self):
        """Reset Pac-Man and ghost positions after death."""
        self.player.reset_position(*self.maze.player_start)
        for ghost in self.ghosts:
            ghost.reset_position()
    
    def on_draw(self):
        """Render the game."""
        self.clear()
        
        # Draw maze and sprites
        self.maze.draw()
        self.player.draw()
        for ghost in self.ghosts:
            ghost.draw()
        
        # Draw UI
        arcade.draw_text(
            f"Score: {self.player.score}",
            *SCORE_POSITION,
            arcade.color.WHITE,
            FONT_SIZE
        )
        arcade.draw_text(
            f"Lives: {self.player.lives}",
            *LIVES_POSITION,
            arcade.color.WHITE,
            FONT_SIZE
        )
        
        # Draw pause/game over message if needed
        if self.paused:
            arcade.draw_text(
                "PAUSED",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                arcade.color.YELLOW,
                FONT_SIZE * 2,
                anchor_x="center"
            )
        elif self.game_over:
            arcade.draw_text(
                "GAME OVER" if self.player.lives <= 0 else "YOU WIN!",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                arcade.color.YELLOW,
                FONT_SIZE * 2,
                anchor_x="center"
            )
            arcade.draw_text(
                "Press SPACE to play again",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - FONT_SIZE * 2,
                arcade.color.YELLOW,
                FONT_SIZE,
                anchor_x="center"
            )
    
    def on_key_press(self, key, modifiers):
        """Handle key press events."""
        if key == arcade.key.P:
            self.paused = not self.paused
        elif key == arcade.key.SPACE and self.game_over:
            self.setup()  # Restart the game
        elif not self.paused and not self.game_over:
            # Handle movement keys
            if key == arcade.key.UP:
                self.player.set_intended_direction(Direction.UP)
            elif key == arcade.key.DOWN:
                self.player.set_intended_direction(Direction.DOWN)
            elif key == arcade.key.LEFT:
                self.player.set_intended_direction(Direction.LEFT)
            elif key == arcade.key.RIGHT:
                self.player.set_intended_direction(Direction.RIGHT)
