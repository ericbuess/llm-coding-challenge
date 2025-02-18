"""Generate basic sound effects for Pac-Man using synthesizer."""
import numpy as np
from scipy.io import wavfile

def generate_sine_wave(freq, duration, amplitude=0.5, sample_rate=44100):
    """Generate a sine wave."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    return wave

def create_chomp_sound():
    """Create a simple chomping sound."""
    duration = 0.1
    sample_rate = 44100
    
    # Create a wave that goes from high to low frequency
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    freq = np.linspace(600, 200, len(t))
    wave = 0.5 * np.sin(2 * np.pi * freq * t)
    
    # Apply envelope
    envelope = np.exp(-3 * t)
    wave = wave * envelope
    
    # Convert to 16-bit PCM
    wave = np.int16(wave * 32767)
    wavfile.write('assets/sounds/chomp.wav', sample_rate, wave)

def create_power_pellet_sound():
    """Create power pellet activation sound."""
    duration = 0.5
    sample_rate = 44100
    
    # Create alternating high and low frequencies
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave1 = 0.3 * np.sin(2 * np.pi * 800 * t)
    wave2 = 0.3 * np.sin(2 * np.pi * 1000 * t)
    wave = wave1 + wave2
    
    # Add tremolo effect
    tremolo = 0.5 + 0.5 * np.sin(2 * np.pi * 10 * t)
    wave = wave * tremolo
    
    # Convert to 16-bit PCM
    wave = np.int16(wave * 32767)
    wavfile.write('assets/sounds/power_pellet.wav', sample_rate, wave)

def create_ghost_eaten_sound():
    """Create ghost eaten sound."""
    duration = 0.3
    sample_rate = 44100
    
    # Create ascending frequency
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    freq = np.linspace(400, 1200, len(t))
    wave = 0.5 * np.sin(2 * np.pi * freq * t)
    
    # Apply envelope
    envelope = 1 - np.exp(-5 * t)
    wave = wave * envelope
    
    # Convert to 16-bit PCM
    wave = np.int16(wave * 32767)
    wavfile.write('assets/sounds/ghost_eaten.wav', sample_rate, wave)

def create_death_sound():
    """Create Pac-Man death sound."""
    duration = 1.0
    sample_rate = 44100
    
    # Create descending frequency with wobble
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    freq = np.linspace(800, 200, len(t))
    wobble = 50 * np.sin(2 * np.pi * 10 * t)
    wave = 0.5 * np.sin(2 * np.pi * (freq + wobble) * t)
    
    # Apply envelope
    envelope = np.exp(-2 * t)
    wave = wave * envelope
    
    # Convert to 16-bit PCM
    wave = np.int16(wave * 32767)
    wavfile.write('assets/sounds/death.wav', sample_rate, wave)

if __name__ == '__main__':
    create_chomp_sound()
    create_power_pellet_sound()
    create_ghost_eaten_sound()
    create_death_sound()
