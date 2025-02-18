"""
Wall entity implementation.
"""
from entities.base import BaseEntity

class Wall(BaseEntity):
    def __init__(self, x: int, y: int):
        """Initialize wall."""
        super().__init__(x, y, "wall.png")
