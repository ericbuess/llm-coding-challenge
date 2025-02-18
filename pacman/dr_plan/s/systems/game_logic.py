from enum import Enum
from typing import List
from ..entities.ghost import Ghost, GhostMode
from ..entities.pacman import PacMan

class GameState(Enum):
    MENU = 0
    READY = 1
    PLAYING = 2
    PAUSED = 3
    PACMAN_DYING = 4
    GAME_OVER = 5
    WIN = 6

class GameLogic:
    def __init__(self):
        self.state = GameState.MENU
        self.level = 1
        self.ready_timer = 2.0  # seconds to show READY! screen
        self.death_timer = 2.0  # seconds to show death animation
        self.timer = 0
        self.extra_life_score = 10000
        self.next_extra_life = self.extra_life_score

    def update(self, dt: float, pacman: PacMan, ghosts: List[Ghost], maze) -> None:
        """Update game state and handle state transitions."""
        self.timer -= dt

        if self.state == GameState.READY:
            if self.timer <= 0:
                self.state = GameState.PLAYING
                self._start_gameplay(ghosts)

        elif self.state == GameState.PACMAN_DYING:
            if self.timer <= 0:
                if pacman.lives > 0:
                    self._reset_level(pacman, ghosts)
                    self.state = GameState.READY
                    self.timer = self.ready_timer
                else:
                    self.state = GameState.GAME_OVER

        # Check for extra life
        if pacman.score >= self.next_extra_life:
            pacman.lives += 1
            self.next_extra_life += self.extra_life_score

        # Check win condition (all pellets eaten)
        if self.state == GameState.PLAYING and not maze.pellets and not maze.power_pellets:
            self.state = GameState.WIN

    def start_game(self) -> None:
        """Initialize a new game."""
        self.state = GameState.READY
        self.level = 1
        self.timer = self.ready_timer
        self.next_extra_life = self.extra_life_score

    def pause_game(self) -> None:
        """Pause or unpause the game."""
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED
        elif self.state == GameState.PAUSED:
            self.state = GameState.PLAYING

    def handle_pacman_death(self, pacman: PacMan, ghosts: List[Ghost]) -> None:
        """Handle Pac-Man's death sequence."""
        self.state = GameState.PACMAN_DYING
        self.timer = self.death_timer
        for ghost in ghosts:
            ghost.set_mode(GhostMode.SCATTER)

    def handle_power_pellet(self, ghosts: List[Ghost]) -> None:
        """Handle power pellet effects."""
        for ghost in ghosts:
            if ghost.mode != GhostMode.EATEN:
                ghost.set_mode(GhostMode.FRIGHTENED)

    def _start_gameplay(self, ghosts: List[Ghost]) -> None:
        """Start normal gameplay after READY state."""
        for ghost in ghosts:
            ghost.set_mode(GhostMode.SCATTER)

    def _reset_level(self, pacman: PacMan, ghosts: List[Ghost]) -> None:
        """Reset entities to starting positions."""
        pacman.reset()
        for ghost in ghosts:
            ghost.reset()

    def next_level(self, pacman: PacMan, ghosts: List[Ghost], maze) -> None:
        """Advance to the next level."""
        self.level += 1
        self._reset_level(pacman, ghosts)
        maze.reset()
        
        # Increase difficulty
        for ghost in ghosts:
            ghost.normal_speed *= 1.1  # 10% faster each level
            ghost.frightened_speed *= 1.1

        self.state = GameState.READY
        self.timer = self.ready_timer 