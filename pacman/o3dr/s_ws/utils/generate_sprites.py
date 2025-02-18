"""Generate placeholder sprites for Pac-Man and ghosts."""
from PIL import Image, ImageDraw

def create_pacman_sprites():
    """Create basic Pac-Man sprites for all directions."""
    size = 32
    directions = ['right', 'left', 'up', 'down']
    
    for direction in directions:
        for frame in [1, 2]:
            # Create a new image with transparent background
            image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            
            # Draw yellow circle
            draw.ellipse([2, 2, size-2, size-2], fill=(255, 255, 0, 255))
            
            # For frame 2, draw a complete circle
            if frame == 1:
                # Add direction-specific mouth
                if direction == 'right':
                    draw.polygon([(size//2, size//2), (size-2, size//4), (size-2, size*3//4)], fill=(0, 0, 0, 0))
                elif direction == 'left':
                    draw.polygon([(size//2, size//2), (2, size//4), (2, size*3//4)], fill=(0, 0, 0, 0))
                elif direction == 'up':
                    draw.polygon([(size//2, size//2), (size//4, 2), (size*3//4, 2)], fill=(0, 0, 0, 0))
                elif direction == 'down':
                    draw.polygon([(size//2, size//2), (size//4, size-2), (size*3//4, size-2)], fill=(0, 0, 0, 0))
            
            # Save the sprite
            image.save(f'assets/images/pacman_{direction}_{frame}.png')

def create_ghost_sprites():
    """Create basic ghost sprites."""
    size = 32
    colors = {
        'blinky': (255, 0, 0, 255),    # Red
        'pinky': (255, 182, 255, 255),  # Pink
        'inky': (0, 255, 255, 255),     # Cyan
        'clyde': (255, 182, 85, 255)    # Orange
    }
    
    for ghost_name, color in colors.items():
        # Create a new image with transparent background
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw ghost body (semi-circle top and rectangular bottom)
        draw.ellipse([2, 2, size-2, size], fill=color)
        draw.rectangle([2, size//2, size-2, size-6], fill=color)
        
        # Draw zigzag bottom
        zigzag_points = [
            (2, size-6),
            (8, size-2),
            (14, size-6),
            (20, size-2),
            (26, size-6),
            (size-2, size-6)
        ]
        draw.line(zigzag_points, fill=color, width=2)
        
        # Draw eyes
        eye_color = (255, 255, 255, 255)
        pupil_color = (0, 0, 255, 255)
        
        # Left eye
        draw.ellipse([8, 8, 15, 15], fill=eye_color)
        draw.ellipse([10, 10, 13, 13], fill=pupil_color)
        
        # Right eye
        draw.ellipse([17, 8, 24, 15], fill=eye_color)
        draw.ellipse([19, 10, 22, 13], fill=pupil_color)
        
        # Save the ghost sprite
        image.save(f'assets/images/{ghost_name}.png')
    
    # Create frightened ghost sprite (blue)
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw ghost body in blue
    blue_color = (0, 0, 255, 255)
    draw.ellipse([2, 2, size-2, size], fill=blue_color)
    draw.rectangle([2, size//2, size-2, size-6], fill=blue_color)
    draw.line(zigzag_points, fill=blue_color, width=2)
    
    # Draw white eyes
    draw.ellipse([8, 8, 15, 15], fill=(255, 255, 255, 255))
    draw.ellipse([17, 8, 24, 15], fill=(255, 255, 255, 255))
    
    # Save frightened ghost sprite
    image.save('assets/images/ghost_frightened.png')
    
    # Create eaten ghost sprite (eyes only)
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw eyes
    draw.ellipse([8, 8, 15, 15], fill=(255, 255, 255, 255))
    draw.ellipse([10, 10, 13, 13], fill=(0, 0, 255, 255))
    draw.ellipse([17, 8, 24, 15], fill=(255, 255, 255, 255))
    draw.ellipse([19, 10, 22, 13], fill=(0, 0, 255, 255))
    
    # Save eaten ghost sprite
    image.save('assets/images/ghost_eaten.png')

if __name__ == '__main__':
    create_pacman_sprites()
    create_ghost_sprites()
