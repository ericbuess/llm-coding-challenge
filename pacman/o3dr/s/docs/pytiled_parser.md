# PyTiled Parser Documentation (v2.2.0+)

PyTiled Parser is a Python Library for parsing Tiled Map Editor maps and tilesets to be used as maps and levels for 2D games.

## Features
- Parse JSON formatted Tiled Map Editor maps and tilesets
- Support for orthogonal, hexagonal, and isometric maps
- Strictly typed parsing
- Not tied to any specific graphics library

## Basic Usage
```python
from pytiled_parser import parse_map

# Load a Tiled map
tiled_map = parse_map("path/to/map.tmx")

# Access map properties
map_width = tiled_map.map_size.width
map_height = tiled_map.map_size.height

# Access layers
for layer in tiled_map.layers:
    # Process layer data
    pass
```

## Resources
- PyPI Package: https://pypi.org/project/pytiled-parser/
- Works with Python 3.6 - 3.12
