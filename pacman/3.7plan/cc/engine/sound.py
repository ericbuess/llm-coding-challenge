import pygame
import os

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music = None
        
        # Initialize the mixer
        pygame.mixer.init()
        
        # Load sound effects if they exist, otherwise create placeholders
        self.load_sounds()
    
    def load_sounds(self):
        """Load all game sound effects or create placeholders if files don't exist"""
        sound_files = {
            "chomp": "assets/sounds/chomp.wav",
            "death": "assets/sounds/death.wav",
            "eat_ghost": "assets/sounds/eat_ghost.wav",
            "eat_fruit": "assets/sounds/eat_fruit.wav",
            "power_pellet": "assets/sounds/power_pellet.wav",
            "extra_life": "assets/sounds/extra_life.wav",
            "game_start": "assets/sounds/game_start.wav",
        }
        
        for name, path in sound_files.items():
            if os.path.exists(path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                    self.sounds[name].set_volume(0.5)
                except:
                    print(f"Failed to load sound: {path}")
            else:
                # No sound file, just create a placeholder
                print(f"Sound file not found: {path}")
    
    def play(self, sound_name):
        """Play a sound effect by name"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_siren(self, level):
        """Play the appropriate siren music based on level"""
        # In a real implementation, would load different siren sound files
        # Here we'll just stop any existing music
        pygame.mixer.music.stop()
        
        # For now, no music plays because we don't have the sound files
        # This would load and play a sound like:
        # pygame.mixer.music.load(f"assets/sounds/siren_{min(level, 5)}.wav")
        # pygame.mixer.music.play(-1)  # Loop indefinitely
    
    def play_frightened(self):
        """Play the frightened ghost music"""
        pygame.mixer.music.stop()
        
        # For now, no music plays because we don't have the sound files
        # pygame.mixer.music.load("assets/sounds/frightened.wav")
        # pygame.mixer.music.play(-1)  # Loop indefinitely
    
    def stop_music(self):
        """Stop any currently playing music"""
        pygame.mixer.music.stop()