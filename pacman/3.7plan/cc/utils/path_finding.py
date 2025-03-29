def manhattan_distance(x1, y1, x2, y2):
    """Calculate Manhattan distance between two points"""
    return abs(x1 - x2) + abs(y1 - y2)

def get_possible_directions(maze, x, y, current_direction=None):
    """Get possible directions from a position, excluding reverse direction"""
    possible_dirs = []
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, Right, Down, Left
    
    # Remove reverse direction if provided
    if current_direction is not None:
        reverse_dir = (-current_direction[0], -current_direction[1])
        if reverse_dir in directions and current_direction != (0, 0):
            directions.remove(reverse_dir)
    
    # Check each direction
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if not maze.is_wall(new_x, new_y):
            possible_dirs.append((dx, dy))
    
    return possible_dirs

def get_best_direction(maze, current_pos, target_pos, current_direction=None, exclude_reverse=True):
    """
    Get the best direction to move from current position to target position.
    Uses Manhattan distance as heuristic.
    """
    x, y = current_pos
    target_x, target_y = target_pos
    
    # Get possible directions
    possible_dirs = get_possible_directions(maze, x, y, current_direction if exclude_reverse else None)
    
    # Calculate distance for each direction
    dir_distances = []
    for dx, dy in possible_dirs:
        new_x, new_y = x + dx, y + dy
        distance = manhattan_distance(new_x, new_y, target_x, target_y)
        dir_distances.append((dx, dy, distance))
    
    # Sort by distance (closest first)
    dir_distances.sort(key=lambda d: d[2])
    
    # Return the best direction or None if no directions available
    if dir_distances:
        return (dir_distances[0][0], dir_distances[0][1])
    else:
        return (0, 0)  # No movement possible