"""
Pellet collectible implementation.
"""
from entities.base import BaseEntity

class Pellet(BaseEntity):
    def __init__(self, x: int, y: int):
        """Initialize pellet."""
        super().__init__(x, y, "pellet.png")
