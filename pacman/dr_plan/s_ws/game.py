import pygame
import sys
from systems.rendering import Renderer
from systems.game_logic import GameLogic
from systems.collision import CollisionManager
from systems.audio import AudioManager
from entities.pacman import PacMan
from entities.ghost import Ghost
from entities.maze import Maze

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Initialize game components
        self.maze = Maze()
        self.pacman = PacMan()
        self.ghosts = [
            Ghost("Blinky", "red"),
            Ghost("Pinky", "pink"),
            Ghost("Inky", "cyan"),
            Ghost("Clyde", "orange")
        ]
        
        # Initialize systems
        self.game_logic = GameLogic()
        self.renderer = Renderer(self.screen)
        self.collision_manager = CollisionManager()
        self.audio_manager = AudioManager()
        
        self.state = "START"

    def start_game(self):
        """Initialize or reset the game state"""
        self.maze.reset()
        self.pacman.reset()
        for ghost in self.ghosts:
            ghost.reset()
        self.game_logic.reset()
        self.state = "PLAYING"

    def handle_events(self):
        """Process game events and user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                self.pacman.handle_input(event.key)
        return True

    def update(self, dt):
        """Update game state"""
        if self.state != "PLAYING":
            return

        # Update entities
        self.pacman.update(dt, self.maze)
        for ghost in self.ghosts:
            ghost.update(dt, self.pacman, self.maze)

        # Check collisions
        self.collision_manager.check_pellet_collision(self.pacman, self.maze.pellets, self.maze, self.game_logic)
        self.collision_manager.check_ghost_collision(self.pacman, self.ghosts, self.game_logic)

        # Update game logic and check win/lose conditions
        self.game_logic.update_timers(dt)
        if self.game_logic.check_win_condition():
            self.state = "WIN"
        elif self.game_logic.check_game_over():
            self.state = "GAME_OVER"

    def render(self):
        """Render the current game state"""
        self.renderer.clear_screen()
        self.renderer.draw_maze(self.maze)
        self.renderer.draw_entities(self.pacman, self.ghosts)
        self.renderer.draw_ui(self.game_logic.score, self.game_logic.lives, self.game_logic.level)
        
        if self.state == "GAME_OVER":
            self.renderer.draw_game_over()
        elif self.state == "WIN":
            self.renderer.draw_win()
        elif self.state == "START":
            self.renderer.draw_ready()
            
        pygame.display.flip()

    def run(self):
        """Main game loop"""
        running = True
        while running:
            dt = self.clock.tick(self.FPS) / 1000.0  # Convert to seconds
            
            running = self.handle_events()
            self.update(dt)
            self.render()
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
