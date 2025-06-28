#!/usr/bin/env python3
"""Run the Pac-Man game"""
import subprocess
import sys
import os

# Change to the parent directory and run as module
os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run([sys.executable, "-m", "pacman.main"])