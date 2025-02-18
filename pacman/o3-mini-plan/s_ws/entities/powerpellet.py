"""
Power Pellet collectible implementation.
"""
from entities.base import BaseEntity

class PowerPellet(BaseEntity):
    def __init__(self, x: int, y: int):
        """Initialize power pellet."""
        super().__init__(x, y, "powerpellet.png")
