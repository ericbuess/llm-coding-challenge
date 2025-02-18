# Pathlib Documentation (v1.0.1+)

Pathlib is an object-oriented interface to filesystem paths that is now part of the Python standard library.

## Key Features
- Object-oriented interface to filesystem paths
- Cross-platform path manipulation
- Path traversal and pattern matching
- File operations (read/write/create/delete)

## Basic Usage
```python
from pathlib import Path

# Create path objects
path = Path('path/to/file.txt')

# Path operations
parent_dir = path.parent
file_name = path.name
stem = path.stem  # filename without extension
suffix = path.suffix  # file extension

# File operations
path.exists()  # check if path exists
path.is_file()  # check if path is a file
path.is_dir()   # check if path is a directory

# Reading/writing files
content = path.read_text()  # read text file
path.write_text('content')  # write text file
```

## Resources
- Official Documentation: https://pathlib.readthedocs.io/
- Part of Python Standard Library (3.4+)
- Compatible with Python 2.7 and 3.x through backport
