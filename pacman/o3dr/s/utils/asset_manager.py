"""Asset manager for loading and caching game resources."""
import arcade
from pathlib import Path
from typing import Dict, Optional

class AssetManager:
    def __init__(self):
        self.root_path = Path(__file__).parent.parent
        self.textures: Dict[str, arcade.Texture] = {}
        self.sounds: Dict[str, arcade.Sound] = {}
        self.tilemaps: Dict[str, arcade.TileMap] = {}

    def get_texture(self, name: str) -> Optional[arcade.Texture]:
        """Get a cached texture or load it if not cached."""
        if name not in self.textures:
            path = self.root_path / "assets" / "images" / name
            if path.exists():
                self.textures[name] = arcade.load_texture(str(path))
            else:
                return None
        return self.textures[name]

    def get_sound(self, name: str) -> Optional[arcade.Sound]:
        """Get a cached sound or load it if not cached."""
        if name not in self.sounds:
            path = self.root_path / "assets" / "sounds" / name
            if path.exists():
                self.sounds[name] = arcade.load_sound(str(path))
            else:
                return None
        return self.sounds[name]

    def load_tilemap(self, name: str) -> Optional[arcade.TileMap]:
        """Load a tilemap from the tilemaps directory."""
        if name not in self.tilemaps:
            path = self.root_path / "assets" / "tilemaps" / name
            if path.exists():
                self.tilemaps[name] = arcade.load_tilemap(str(path), scaling=1.0)
            else:
                return None
        return self.tilemaps[name]

    def preload_assets(self):
        """Preload commonly used assets."""
        # Add preloading logic here as needed
        pass

# Global instance
assets = AssetManager() 