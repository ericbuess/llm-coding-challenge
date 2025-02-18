import pygame

class Pellet:
    def __init__(self, x: int, y: int, size: int = 4):
        self.x = x
        self.y = y
        self.size = size
        self.points = 10
        self.rect = pygame.Rect(x - size//2, y - size//2, size, size)
        self.eaten = False

    def draw(self, screen):
        """Draw the pellet on the screen."""
        if not self.eaten:
            pygame.draw.circle(screen, (255, 255, 255),
                             (self.x, self.y), self.size // 2) 