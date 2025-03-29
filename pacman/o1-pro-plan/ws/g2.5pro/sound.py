# sound.py
# Manages sound effects for the Pac-Man game

import pygame
import os

class SoundManager:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init()
        self.sounds = {}
        self.current_waka_sound = 0  # For alternating between waka sounds
        self._load_sounds()
        
    def _load_sounds(self):
        # Create sounds directory if it doesn't exist
        if not os.path.exists('sounds'):
            os.makedirs('sounds')
            print("Created sounds directory. You'll need to add sound files.")
            return
            
        # Try to load sound files
        sound_files = {
            'waka1': 'waka1.wav',
            'waka2': 'waka2.wav',
            'power_pellet': 'power_pellet.wav',
            'eat_ghost': 'eat_ghost.wav',
            'death': 'death.wav',
            'game_start': 'game_start.wav',
            'extra_life': 'extra_life.wav'
        }
        
        for sound_name, filename in sound_files.items():
            try:
                sound_path = os.path.join('sounds', filename)
                if os.path.exists(sound_path):
                    self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
                else:
                    print(f"Missing sound file: {sound_path}")
            except pygame.error as e:
                print(f"Could not load sound {filename}: {e}")
    
    def play_sound(self, sound_name):
        """Play a sound by name"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_waka(self):
        """Play alternating waka sounds for pellet eating"""
        waka_sound = 'waka1' if self.current_waka_sound == 0 else 'waka2'
        self.current_waka_sound = 1 - self.current_waka_sound  # Toggle between 0 and 1
        
        if waka_sound in self.sounds:
            self.sounds[waka_sound].play()
    
    def play_power_pellet(self):
        """Play power pellet sound"""
        self.play_sound('power_pellet')
    
    def play_eat_ghost(self):
        """Play ghost eaten sound"""
        self.play_sound('eat_ghost')
    
    def play_death(self):
        """Play Pac-Man death sound"""
        self.play_sound('death')
    
    def play_game_start(self):
        """Play game start sound"""
        self.play_sound('game_start')
    
    def play_extra_life(self):
        """Play extra life sound"""
        self.play_sound('extra_life')
