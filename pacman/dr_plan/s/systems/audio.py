import pygame
import os
from typing import Dict

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.current_siren = None
        self.volume = 0.5
        self._load_sounds()

    def _load_sounds(self) -> None:
        """Load all sound effects."""
        sound_files = {
            "chomp": "chomp.wav",
            "death": "death.wav",
            "eat_ghost": "eat_ghost.wav",
            "power_pellet": "power_pellet.wav",
            "siren": "siren.wav",
            "frightened": "frightened.wav"
        }

        sound_dir = os.path.join("assets", "sounds")
        
        # Try to load each sound, skip if file doesn't exist
        for sound_name, filename in sound_files.items():
            try:
                path = os.path.join(sound_dir, filename)
                if os.path.exists(path):
                    self.sounds[sound_name] = pygame.mixer.Sound(path)
                    self.sounds[sound_name].set_volume(self.volume)
            except:
                print(f"Could not load sound: {filename}")

    def play_chomp(self) -> None:
        """Play pellet eating sound."""
        if "chomp" in self.sounds:
            self.sounds["chomp"].play()

    def play_death(self) -> None:
        """Play Pac-Man death sound."""
        if "death" in self.sounds:
            # Stop all other sounds first
            self.stop_all()
            self.sounds["death"].play()

    def play_eat_ghost(self) -> None:
        """Play ghost eating sound."""
        if "eat_ghost" in self.sounds:
            self.sounds["eat_ghost"].play()

    def play_power_pellet(self) -> None:
        """Play power pellet activation sound."""
        if "power_pellet" in self.sounds:
            if self.current_siren:
                self.current_siren.stop()
            self.sounds["power_pellet"].play()
            if "frightened" in self.sounds:
                self.current_siren = self.sounds["frightened"]
                self.current_siren.play(-1)  # Loop the frightened sound

    def play_siren(self) -> None:
        """Play normal gameplay siren sound."""
        if "siren" in self.sounds and not self.current_siren:
            self.current_siren = self.sounds["siren"]
            self.current_siren.play(-1)  # Loop indefinitely

    def stop_siren(self) -> None:
        """Stop the current siren sound."""
        if self.current_siren:
            self.current_siren.stop()
            self.current_siren = None

    def stop_all(self) -> None:
        """Stop all currently playing sounds."""
        pygame.mixer.stop()
        self.current_siren = None

    def set_volume(self, volume: float) -> None:
        """Set volume for all sounds (0.0 to 1.0)."""
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.volume) 