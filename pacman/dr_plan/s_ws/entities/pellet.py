from pygame.math import Vector2

class Pellet:
    def __init__(self, position, is_power):
        self.position = Vector2(position)
        self.is_power = is_power
        self.points = 50 if is_power else 10
        self.radius = 8 if is_power else 3  # Power pellets are larger
        self.eaten = False

    def consume(self):
        """Mark the pellet as eaten"""
        self.eaten = True
