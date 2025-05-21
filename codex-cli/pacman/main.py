#!/usr/bin/env python3
"""
Entry point for the Pac-Man game.
"""
import argparse

from pacman.game import Game


def main():
    parser = argparse.ArgumentParser(description="Pac-Man game entry point.")
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run in headless mode for testing imports and setup",
    )
    args = parser.parse_args()

    if args.headless:
        print("Headless mode: modules imported successfully.")
    else:
        game = Game()
        game.run()


if __name__ == "__main__":
    main()