"""Asset manager for loading and caching game resources."""
import arcade
from pathlib import Path
from typing import Dict, Optional

class AssetManager:
    def __init__(self):
        self._textures: Dict[str, arcade.Texture] = {}
        self._sounds: Dict[str, arcade.Sound] = {}
        self._tilemaps: Dict[str, arcade.TileMap] = {}
        
        # Get the absolute path to the assets directory
        self.assets_path = Path(__file__).parent.parent / 'assets'
        
    def get_texture(self, name: str) -> Optional[arcade.Texture]:
        """Get a texture from cache or load it if not cached."""
        if name not in self._textures:
            texture_path = self.assets_path / 'images' / name
            if texture_path.exists():
                self._textures[name] = arcade.load_texture(str(texture_path))
            else:
                print(f"Warning: Texture {name} not found at {texture_path}")
                return None
        return self._textures[name]
    
    def get_sound(self, name: str) -> Optional[arcade.Sound]:
        """Get a sound from cache or load it if not cached."""
        if name not in self._sounds:
            sound_path = self.assets_path / 'sounds' / name
            if sound_path.exists():
                self._sounds[name] = arcade.load_sound(str(sound_path))
            else:
                print(f"Warning: Sound {name} not found at {sound_path}")
                return None
        return self._sounds[name]
    
    def get_tilemap(self, name: str) -> Optional[arcade.TileMap]:
        """Get a tilemap from cache or load it if not cached."""
        if name not in self._tilemaps:
            tilemap_path = self.assets_path / 'tilemaps' / name
            if tilemap_path.exists():
                self._tilemaps[name] = arcade.load_tilemap(
                    str(tilemap_path),
                    scaling=1.0,
                    use_spatial_hash=True,
                    layer_options={
                        "Walls": {
                            "use_spatial_hash": True,
                        },
                    }
                )
            else:
                print(f"Warning: Tilemap {name} not found at {tilemap_path}")
                return None
        return self._tilemaps[name]
    
    def clear_cache(self):
        """Clear all cached assets."""
        self._textures.clear()
        self._sounds.clear()
        self._tilemaps.clear()

# Global instance
asset_manager = AssetManager()
