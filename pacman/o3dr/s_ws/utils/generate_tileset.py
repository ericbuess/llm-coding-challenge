"""Generate a basic tileset for Pac-Man."""
from PIL import Image, ImageDraw

TILE_SIZE = 32
TILESET_WIDTH = 3  # Number of tiles horizontally
TILESET_HEIGHT = 1  # Number of tiles vertically

def create_tileset():
    # Create a new image with a black background
    width = TILE_SIZE * TILESET_WIDTH
    height = TILE_SIZE * TILESET_HEIGHT
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw wall tile (blue rectangle)
    draw.rectangle([
        0, 0,
        TILE_SIZE - 1, TILE_SIZE - 1
    ], fill=(0, 0, 255, 255))
    
    # Draw pellet tile (small white dot)
    pellet_size = 6
    pellet_x = TILE_SIZE + (TILE_SIZE - pellet_size) // 2
    pellet_y = (TILE_SIZE - pellet_size) // 2
    draw.ellipse([
        pellet_x, pellet_y,
        pellet_x + pellet_size, pellet_y + pellet_size
    ], fill=(255, 255, 255, 255))
    
    # Draw power pellet tile (larger white dot)
    power_size = 12
    power_x = 2 * TILE_SIZE + (TILE_SIZE - power_size) // 2
    power_y = (TILE_SIZE - power_size) // 2
    draw.ellipse([
        power_x, power_y,
        power_x + power_size, power_y + power_size
    ], fill=(255, 255, 255, 255))
    
    # Save the tileset
    image.save('assets/images/tileset.png')

if __name__ == '__main__':
    create_tileset()
