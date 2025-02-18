from pygame.math import Vector2

class CollisionManager:
    def __init__(self):
        self.collision_distance = 15  # Collision detection radius

    def check_pellet_collision(self, pacman, pellets, maze, game_logic):
        """Check and handle collisions between Pac-Man and pellets"""
        for pellet in pellets[:]:  # Use slice copy to safely remove while iterating
            if not pellet.eaten and self._check_distance(pacman.position, pellet.position):
                pellet.consume()
                game_logic.add_score(pellet.points)
                maze.remove_pellet(pellet)
                if pellet.is_power:
                    game_logic.activate_power_pellet()

    def check_ghost_collision(self, pacman, ghosts, game_logic):
        """Check and handle collisions between Pac-Man and ghosts"""
        if not pacman.alive:
            return

        for ghost in ghosts:
            if self._check_distance(pacman.position, ghost.position):
                if ghost.mode == "FRIGHTENED" and not ghost.is_eaten:
                    # Pac-Man eats the ghost
                    ghost.is_eaten = True
                    game_logic.add_ghost_score()
                elif not ghost.is_eaten and ghost.mode != "FRIGHTENED":
                    # Ghost catches Pac-Man
                    pacman.die()
                    game_logic.lose_life()
                    return  # No need to check other ghosts

    def _check_distance(self, pos1, pos2):
        """Helper method to check if two positions are close enough for collision"""
        return (pos1 - pos2).length_squared() < self.collision_distance * self.collision_distance
