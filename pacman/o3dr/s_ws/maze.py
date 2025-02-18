"""Maze management using Arcade's TileMap system."""
import arcade
from typing import Tuple, Optional
from constants import TILE_SIZE
from utils.asset_manager import asset_manager

class Maze:
    def __init__(self, map_name: str):
        """Initialize the maze from a Tiled map file."""
        # Load the tilemap
        self.tilemap = asset_manager.get_tilemap(map_name)
        if not self.tilemap:
            raise ValueError(f"Could not load tilemap: {map_name}")
            
        # Create sprite lists for each layer
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.pellet_list = arcade.SpriteList()
        self.power_pellet_list = arcade.SpriteList()
        
        # Process wall layer
        if "Walls" in self.tilemap.sprite_lists:
            self.wall_list = self.tilemap.sprite_lists["Walls"]
        
        # Process pellet layers
        if "Pellets" in self.tilemap.sprite_lists:
            pellet_layer = self.tilemap.sprite_lists["Pellets"]
            for sprite in pellet_layer:
                self.pellet_list.append(sprite)
        
        if "PowerPellets" in self.tilemap.sprite_lists:
            power_layer = self.tilemap.sprite_lists["PowerPellets"]
            for sprite in power_layer:
                self.power_pellet_list.append(sprite)
        
        # Get the spawn points
        self.player_start = self._get_player_start()
        self.ghost_starts = self._get_ghost_starts()
        
        # Keep track of remaining pellets
        self.total_pellets = len(self.pellet_list) + len(self.power_pellet_list)
        self.remaining_pellets = self.total_pellets
    
    def _get_player_start(self) -> Tuple[float, float]:
        """Get Pac-Man's starting position from the map."""
        # Get the object layer
        spawn_layer = self.tilemap.object_lists.get("Spawn", [])
        
        # Find PlayerStart object
        for obj in spawn_layer:
            if obj.name == "PlayerStart":
                return (obj.shape[0], obj.shape[1])
        
        # Default to center if not specified
        return (14 * TILE_SIZE, 14 * TILE_SIZE)
    
    def _get_ghost_starts(self) -> list[Tuple[float, float]]:
        """Get ghost starting positions from the map."""
        ghost_starts = []
        spawn_layer = self.tilemap.object_lists.get("Spawn", [])
        
        # Find ghost start positions
        for i in range(4):
            ghost_name = f"GhostStart{i+1}"
            for obj in spawn_layer:
                if obj.name == ghost_name:
                    ghost_starts.append(
                        (obj.shape[0], obj.shape[1])
                    )
                    break
        
        # Default positions if not specified
        if not ghost_starts:
            ghost_starts = [
                (13 * TILE_SIZE, 17 * TILE_SIZE),  # Blinky
                (14 * TILE_SIZE, 17 * TILE_SIZE),  # Pinky
                (13 * TILE_SIZE, 15 * TILE_SIZE),  # Inky
                (14 * TILE_SIZE, 15 * TILE_SIZE)   # Clyde
            ]
        
        return ghost_starts
    
    def is_walkable(self, x: float, y: float) -> bool:
        """Check if a position is walkable (no wall)."""
        # Convert pixel coordinates to grid coordinates
        grid_x = int(x / TILE_SIZE)
        grid_y = int(y / TILE_SIZE)
        
        # Create a temporary sprite at the position
        temp_sprite = arcade.Sprite(
            center_x=x,
            center_y=y,
            width=TILE_SIZE - 2,  # Slightly smaller for better collision
            height=TILE_SIZE - 2
        )
        
        # Check for collision with walls
        wall_hit = arcade.check_for_collision_with_list(
            temp_sprite,
            self.wall_list
        )
        
        return not bool(wall_hit)
    
    def remove_pellet(self, x: float, y: float) -> Optional[arcade.Sprite]:
        """Remove a pellet at the given position and return it if found."""
        # Create a temporary sprite for collision checking
        temp_sprite = arcade.Sprite(
            center_x=x,
            center_y=y,
            width=TILE_SIZE / 2,  # Smaller hitbox for better pickup
            height=TILE_SIZE / 2
        )
        
        # Check regular pellets
        pellet_hits = arcade.check_for_collision_with_list(
            temp_sprite,
            self.pellet_list
        )
        
        if pellet_hits:
            pellet = pellet_hits[0]
            pellet.remove_from_sprite_lists()
            self.remaining_pellets -= 1
            return pellet
            
        # Check power pellets
        power_hits = arcade.check_for_collision_with_list(
            temp_sprite,
            self.power_pellet_list
        )
        
        if power_hits:
            power_pellet = power_hits[0]
            power_pellet.remove_from_sprite_lists()
            self.remaining_pellets -= 1
            return power_pellet
            
        return None
    
    def is_complete(self) -> bool:
        """Check if all pellets have been collected."""
        return self.remaining_pellets == 0
    
    def draw(self):
        """Draw the maze and all its elements."""
        self.wall_list.draw()
        self.pellet_list.draw()
        self.power_pellet_list.draw()
