from typing import List
from ..entities.ghost import Ghost, GhostMode
from ..entities.pacman import PacMan
from ..entities.pellet import Pellet
from ..entities.powerpellet import PowerPellet

class CollisionManager:
    def __init__(self):
        self.ghost_points = 200  # Base points for eating a ghost
        self.ghost_points_multiplier = 1

    def check_pellet_collisions(self, pacman: PacMan, maze) -> None:
        """Check and handle collisions between Pac-Man and pellets."""
        pacman_rect = pacman.rect

        # Check regular pellets
        for pellet in maze.pellets[:]:  # Copy list to safely remove while iterating
            if not pellet.eaten and pacman_rect.colliderect(pellet.rect):
                pellet.eaten = True
                pacman.eat_pellet(pellet.points)
                maze.remove_pellet(pellet)
                return True  # Return True if a pellet was eaten

        # Check power pellets
        for power_pellet in maze.power_pellets[:]:
            if not power_pellet.eaten and pacman_rect.colliderect(power_pellet.rect):
                power_pellet.eaten = True
                pacman.eat_pellet(power_pellet.points)
                maze.remove_pellet(power_pellet)
                return True, True  # Second True indicates it was a power pellet

        return False  # No pellet was eaten

    def check_ghost_collisions(self, pacman: PacMan, ghosts: List[Ghost]) -> bool:
        """Check and handle collisions between Pac-Man and ghosts."""
        if not pacman.alive:
            return False

        pacman_rect = pacman.rect
        collision_occurred = False

        for ghost in ghosts:
            if ghost.rect.colliderect(pacman_rect):
                if ghost.mode == GhostMode.FRIGHTENED and not ghost.is_eaten:
                    # Pac-Man eats the ghost
                    ghost.set_mode(GhostMode.EATEN)
                    pacman.score += self.ghost_points * self.ghost_points_multiplier
                    self.ghost_points_multiplier *= 2
                    collision_occurred = True
                elif ghost.mode != GhostMode.EATEN and not ghost.is_eaten:
                    # Ghost catches Pac-Man
                    pacman.die()
                    collision_occurred = True
                    break  # No need to check other ghosts

        return collision_occurred

    def reset_ghost_multiplier(self) -> None:
        """Reset the ghost points multiplier."""
        self.ghost_points_multiplier = 1 