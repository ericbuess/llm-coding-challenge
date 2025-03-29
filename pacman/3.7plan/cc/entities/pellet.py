import pygame
import config

class Pellet:
    def __init__(self, x, y, is_power_pellet=False):
        self.x = x
        self.y = y
        self.is_power_pellet = is_power_pellet
        self.radius = 2 if not is_power_pellet else 7
        self.color = config.WHITE  # White
        self.blink_timer = 0
        self.visible = True
    
    def update(self, dt):
        # Make power pellets blink
        if self.is_power_pellet:
            self.blink_timer += dt
            if self.blink_timer >= 0.2:
                self.blink_timer = 0
                self.visible = not self.visible
    
    def render(self, screen, offset_x=0, offset_y=0):
        if not self.visible:
            return
        
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x + offset_x), int(self.y + offset_y)),
            self.radius
        )