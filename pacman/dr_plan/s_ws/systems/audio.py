import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.load_sounds()

    def load_sounds(self):
        """Load sound files - commented out until sound files are added"""
        # These will be uncommented when sound files are added to assets/sounds/
        # self.sounds["chomp"] = pygame.mixer.Sound("assets/sounds/chomp.wav")
        # self.sounds["power_up"] = pygame.mixer.Sound("assets/sounds/power_up.wav")
        # self.sounds["eat_ghost"] = pygame.mixer.Sound("assets/sounds/eat_ghost.wav")
        # self.sounds["death"] = pygame.mixer.Sound("assets/sounds/death.wav")
        # self.sounds["siren"] = pygame.mixer.Sound("assets/sounds/siren.wav")
        pass

    def play_chomp(self):
        """Play pellet eating sound"""
        if "chomp" in self.sounds:
            self.sounds["chomp"].play()

    def play_powerup(self):
        """Play power pellet sound"""
        if "power_up" in self.sounds:
            self.sounds["power_up"].play()

    def play_eat_ghost(self):
        """Play ghost eating sound"""
        if "eat_ghost" in self.sounds:
            self.sounds["eat_ghost"].play()

    def play_death(self):
        """Play Pac-Man death sound"""
        if "death" in self.sounds:
            self.sounds["death"].play()

    def play_siren(self, loop=True):
        """Play/stop the siren sound"""
        if "siren" in self.sounds:
            if loop:
                self.sounds["siren"].play(-1)  # Loop indefinitely
            else:
                self.sounds["siren"].stop()

    def stop_all(self):
        """Stop all sounds"""
        pygame.mixer.stop()
