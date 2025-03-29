import pygame
import os
from constants import *

class SoundManager:
    def __init__(self):
        # Initialize sound mixer
        pygame.mixer.init()
        self.sounds = {}
        self.load_sounds()
    
    def load_sounds(self):
        # Dictionary mapping sound types to their filenames (if they exist)
        sound_files = {
            'start': 'start.wav',
            'chomp': 'chomp.wav',  # Pellet eating sound
            'power_pellet': 'power_pellet.wav',
            'eat_ghost': 'eat_ghost.wav',
            'death': 'death.wav',
            'extra_life': 'extra_life.wav',
            'fruit': 'fruit.wav',
        }
        
        # Create a sounds directory if it doesn't exist
        os.makedirs('sounds', exist_ok=True)
        
        # Load each sound if file exists, otherwise print a message
        for sound_name, filename in sound_files.items():
            full_path = os.path.join('sounds', filename)
            
            try:
                if os.path.exists(full_path):
                    self.sounds[sound_name] = pygame.mixer.Sound(full_path)
                else:
                    print(f"Sound file not found: {full_path}")
            except Exception as e:
                print(f"Error loading sound {filename}: {e}")
    
    def play(self, sound_name):
        # Play a sound by name if it exists
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Error playing sound {sound_name}: {e}")
    
    def stop_all(self):
        # Stop all sounds
        pygame.mixer.stop()
