import pygame
import sys
from entities.maze import Maze
from entities.pacman import PacMan
from entities.ghost import Ghost
from systems.collision import CollisionManager
from systems.rendering import Renderer
from systems.audio import AudioManager
from systems.game_logic import GameLogic, GameState

class Game:
    def __init__(self):
        pygame.init()
        
        # Initialize window
        self.tile_size = 20
        self.width = 28 * self.tile_size  # 28 tiles wide
        self.height = 31 * self.tile_size  # 31 tiles high
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pac-Man")

        # Initialize game components
        self.clock = pygame.time.Clock()
        self.maze = Maze(self.tile_size)
        self.spawn_positions = self.maze.get_spawn_positions()

        # Create entities
        self.pacman = PacMan(*self.spawn_positions["pacman"])
        self.ghosts = [
            Ghost(*self.spawn_positions["blinky"], ghost_type="blinky"),
            Ghost(*self.spawn_positions["pinky"], ghost_type="pinky"),
            Ghost(*self.spawn_positions["inky"], ghost_type="inky"),
            Ghost(*self.spawn_positions["clyde"], ghost_type="clyde")
        ]

        # Initialize systems
        self.collision_manager = CollisionManager()
        self.renderer = Renderer(self.screen)
        self.audio_manager = AudioManager()
        self.game_logic = GameLogic()

        # Start the game
        self.game_logic.start_game()

    def handle_input(self) -> bool:
        """Handle user input events. Returns False if game should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                elif event.key == pygame.K_ESCAPE:
                    self.game_logic.pause_game()
                    if self.game_logic.state == GameState.PAUSED:
                        self.audio_manager.stop_siren()
                    else:
                        self.audio_manager.play_siren()
                elif event.key == pygame.K_SPACE:
                    if self.game_logic.state in [GameState.GAME_OVER, GameState.WIN]:
                        self._reset_game()
                elif self.game_logic.state == GameState.PLAYING:
                    self.pacman.handle_input(event.key)

        return True

    def update(self, dt: float) -> None:
        """Update game state."""
        if self.game_logic.state == GameState.PLAYING:
            # Update entities
            self.pacman.update(dt, self.maze)
            for ghost in self.ghosts:
                ghost.update(dt, self.maze, self.pacman)

            # Check collisions
            pellet_eaten = self.collision_manager.check_pellet_collisions(self.pacman, self.maze)
            if isinstance(pellet_eaten, tuple):
                # Power pellet eaten
                self.audio_manager.play_power_pellet()
                self.game_logic.handle_power_pellet(self.ghosts)
            elif pellet_eaten:
                self.audio_manager.play_chomp()

            if self.collision_manager.check_ghost_collisions(self.pacman, self.ghosts):
                if not self.pacman.alive:
                    self.audio_manager.play_death()
                    self.game_logic.handle_pacman_death(self.pacman, self.ghosts)
                else:
                    self.audio_manager.play_eat_ghost()

        # Update game logic and animations
        self.game_logic.update(dt, self.pacman, self.ghosts, self.maze)
        self.maze.update(dt)

    def render(self) -> None:
        """Render the game."""
        self.renderer.clear_screen()
        self.renderer.draw_maze(self.maze)
        self.renderer.draw_pacman(self.pacman)
        self.renderer.draw_ghosts(self.ghosts)
        self.renderer.draw_score(self.pacman.score)
        self.renderer.draw_lives(self.pacman.lives)

        if self.game_logic.state == GameState.READY:
            self.renderer.draw_ready_screen()
        elif self.game_logic.state == GameState.GAME_OVER:
            self.renderer.draw_game_over(self.pacman.score)
        elif self.game_logic.state == GameState.WIN:
            self.renderer.draw_win_screen(self.pacman.score)
        elif self.game_logic.state == GameState.PAUSED:
            self.renderer.draw_pause_screen()

        pygame.display.flip()

    def _reset_game(self) -> None:
        """Reset the game to initial state."""
        self.maze.reset()
        self.pacman = PacMan(*self.spawn_positions["pacman"])
        self.ghosts = [
            Ghost(*self.spawn_positions["blinky"], ghost_type="blinky"),
            Ghost(*self.spawn_positions["pinky"], ghost_type="pinky"),
            Ghost(*self.spawn_positions["inky"], ghost_type="inky"),
            Ghost(*self.spawn_positions["clyde"], ghost_type="clyde")
        ]
        self.collision_manager.reset_ghost_multiplier()
        self.game_logic.start_game()
        self.audio_manager.stop_all()

    def run(self) -> None:
        """Main game loop."""
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0  # Convert to seconds

            running = self.handle_input()
            self.update(dt)
            self.render()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 