import pygame
from .pellet import Pellet

class PowerPellet(Pellet):
    def __init__(self, x: int, y: int, size: int = 8):
        super().__init__(x, y, size)
        self.points = 50
        self.flash_timer = 0
        self.flash_interval = 0.2  # seconds
        self.visible = True

    def update(self, dt: float):
        """Update power pellet animation (flashing effect)."""
        if not self.eaten:
            self.flash_timer += dt
            if self.flash_timer >= self.flash_interval:
                self.flash_timer = 0
                self.visible = not self.visible

    def draw(self, screen):
        """Draw the power pellet with flashing effect."""
        if not self.eaten and self.visible:
            pygame.draw.circle(screen, (255, 255, 255),
                             (self.x, self.y), self.size // 2) 