"""Ghost AI behaviors for Pac-Man"""
import random
import math
from .constants import *

class GhostAI:
    """Static methods for ghost AI behaviors"""
    
    @staticmethod
    def get_distance(pos1, pos2):
        """Calculate Manhattan distance between two positions"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    @staticmethod
    def get_euclidean_distance(pos1, pos2):
        """Calculate Euclidean distance between two positions"""
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    @staticmethod
    def get_blinky_target(pacman_tile):
        """Blinky (red): Direct chase - targets Pacman's current tile"""
        return pacman_tile
    
    @staticmethod
    def get_pinky_target(pacman_tile, pacman_direction):
        """Pinky (pink): Ambush - targets 4 tiles ahead of Pacman"""
        target_x = pacman_tile[0] + pacman_direction[0] * 4
        target_y = pacman_tile[1] + pacman_direction[1] * 4
        return (target_x, target_y)
    
    @staticmethod
    def get_inky_target(pacman_tile, pacman_direction, blinky_tile):
        """Inky (cyan): Flanking - complex targeting using Blinky's position"""
        # Get position 2 tiles ahead of Pacman
        offset_x = pacman_tile[0] + pacman_direction[0] * 2
        offset_y = pacman_tile[1] + pacman_direction[1] * 2
        
        # Calculate vector from Blinky to offset position
        vector_x = offset_x - blinky_tile[0]
        vector_y = offset_y - blinky_tile[1]
        
        # Double the vector for final target
        target_x = blinky_tile[0] + vector_x * 2
        target_y = blinky_tile[1] + vector_y * 2
        
        return (target_x, target_y)
    
    @staticmethod
    def get_clyde_target(pacman_tile, clyde_tile, clyde_home):
        """Clyde (orange): Shy - chase when far, scatter when close"""
        distance = GhostAI.get_euclidean_distance(pacman_tile, clyde_tile)
        
        # If more than 8 tiles away, chase like Blinky
        if distance > 8:
            return pacman_tile
        else:
            # Otherwise, go to home corner
            return clyde_home
    
    @staticmethod
    def get_next_direction(current_tile, target_tile, board, current_direction):
        """Calculate best direction to reach target using simplified pathfinding"""
        x, y = current_tile
        possible_moves = []
        
        # Check all four directions
        for direction in [UP, DOWN, LEFT, RIGHT]:
            # Ghosts can't reverse direction (except in special cases)
            if direction == (-current_direction[0], -current_direction[1]):
                continue
                
            next_x = x + direction[0]
            next_y = y + direction[1]
            
            # Check if move is valid
            if not board.is_wall(next_x, next_y):
                # Calculate distance from next position to target
                distance = GhostAI.get_distance((next_x, next_y), target_tile)
                possible_moves.append((direction, distance))
        
        # If no moves available (shouldn't happen), allow reversal
        if not possible_moves:
            reverse_dir = (-current_direction[0], -current_direction[1])
            next_x = x + reverse_dir[0]
            next_y = y + reverse_dir[1]
            if not board.is_wall(next_x, next_y):
                return reverse_dir
            return (0, 0)  # Stay in place if completely stuck
        
        # Sort by distance and return best direction
        possible_moves.sort(key=lambda x: x[1])
        
        # At intersections, add some randomness to prevent predictable patterns
        if len(possible_moves) > 2 and random.random() < 0.1:
            return random.choice(possible_moves[:2])[0]
        
        return possible_moves[0][0]
    
    @staticmethod
    def get_frightened_direction(current_tile, board, current_direction):
        """Random movement when frightened"""
        x, y = current_tile
        possible_moves = []
        
        # Check all four directions
        for direction in [UP, DOWN, LEFT, RIGHT]:
            # In frightened mode, prefer not to reverse but allow it if needed
            next_x = x + direction[0]
            next_y = y + direction[1]
            
            if not board.is_wall(next_x, next_y):
                # Give non-reverse directions higher weight
                if direction != (-current_direction[0], -current_direction[1]):
                    possible_moves.extend([direction] * 3)  # Add 3 times for higher probability
                else:
                    possible_moves.append(direction)  # Add once for lower probability
        
        # If no moves available at all, return current direction
        if not possible_moves:
            return current_direction if current_direction != (0, 0) else UP
        
        # Choose randomly from weighted list
        return random.choice(possible_moves)