def check_collision(entity1, entity2, threshold=10):
    """Check if two entities are colliding"""
    # Calculate centers
    center1_x = entity1.x + entity1.maze.tile_size / 2
    center1_y = entity1.y + entity1.maze.tile_size / 2
    center2_x = entity2.x + entity2.maze.tile_size / 2
    center2_y = entity2.y + entity2.maze.tile_size / 2
    
    # Calculate distance between centers
    distance = ((center1_x - center2_x) ** 2 + (center1_y - center2_y) ** 2) ** 0.5
    
    # Return True if distance is less than threshold
    return distance < threshold