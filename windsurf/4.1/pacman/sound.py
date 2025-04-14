# sound.py
# Sound effects system for Pac-Man

import pygame
from constants import *

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.load_sounds()

    def load_sounds(self):
        for name, filename in [
            ("chomp", SOUND_CHOMP),
            ("eat_ghost", SOUND_EAT_GHOST),
            ("power_pellet", SOUND_POWER_PELLET),
            ("death", SOUND_DEATH),
            ("start", SOUND_START),
        ]:
            try:
                self.sounds[name] = pygame.mixer.Sound(filename)
            except Exception:
                self.sounds[name] = None

    def play(self, name):
        sound = self.sounds.get(name)
        if sound:
            sound.play()
