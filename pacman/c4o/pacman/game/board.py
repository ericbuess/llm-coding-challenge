from .constants import TILE_SIZE, BOARD_WIDTH, BOARD_HEIGHT

class Board:
    def __init__(self):
        self.maze = []  # 2D list from maze string
        self.pellets = set()  # (x, y) tuples
        self.power_pellets = set()
        self.walls = set()
        self.ghost_house = set()
        self.pacman_start = (14, 23)
        self.ghost_starts = {
            'blinky': (14, 11),
            'pinky': (14, 14),
            'inky': (12, 14),
            'clyde': (16, 14)
        }
        self.load_default_maze()
    
    def load_default_maze(self):
        """Load the default Pac-Man maze"""
        maze_string = """############################
#............##............#
#.####.#####.##.#####.####.#
#o#  #.#   #.##.#   #.#  #o#
#.####.#####.##.#####.####.#
#..........................#
#.####.##.########.##.####.#
#.####.##.########.##.####.#
#......##....##....##......#
######.##### ## #####.######
     #.##### ## #####.#     
     #.##          ##.#     
     #.## ###--### ##.#     
######.## #GGGGGG# ##.######
      .   #GGGGGG#   .      
######.## #GGGGGG# ##.######
     #.## ######## ##.#     
     #.##          ##.#     
     #.## ######## ##.#     
######.## ######## ##.######
#............##............#
#.####.#####.##.#####.####.#
#.####.#####.##.#####.####.#
#o..##.......P........##..o#
###.##.##.########.##.##.###
###.##.##.########.##.##.###
#......##....##....##......#
#.##########.##.##########.#
#..........................#
############################"""
        self.load_maze(maze_string)
    
    def load_maze(self, maze_string: str):
        """Parse the maze string and populate data structures"""
        lines = maze_string.strip().split('\n')
        self.maze = []
        
        for y, line in enumerate(lines):
            row = []
            for x, char in enumerate(line):
                row.append(char)
                
                if char == '#':
                    self.walls.add((x, y))
                elif char == '.':
                    self.pellets.add((x, y))
                elif char == 'o':
                    self.power_pellets.add((x, y))
                elif char == 'G':
                    self.ghost_house.add((x, y))
                elif char == 'P':
                    self.pacman_start = (x, y)
                    self.pellets.add((x, y))  # Pacman starts on a pellet
                
            self.maze.append(row)
    
    def is_wall(self, x: int, y: int) -> bool:
        """Check if given tile coordinates contain a wall"""
        if 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT:
            return (x, y) in self.walls
        return True  # Out of bounds is treated as wall
    
    def is_intersection(self, x: int, y: int) -> bool:
        """Check if a tile is an intersection (3 or more non-wall neighbors)"""
        if self.is_wall(x, y):
            return False
        
        # Count non-wall neighbors
        neighbors = 0
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            if not self.is_wall(x + dx, y + dy):
                neighbors += 1
        
        return neighbors >= 3
    
    def get_neighbors(self, x: int, y: int) -> list:
        """Get all valid (non-wall) neighboring tiles"""
        neighbors = []
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy
            if not self.is_wall(nx, ny):
                neighbors.append((nx, ny))
        return neighbors
    
    def remove_pellet(self, x: int, y: int) -> dict:
        """Remove pellet at given position and return info about what was collected"""
        result = {'pellet': False, 'power_pellet': False}
        
        if (x, y) in self.pellets:
            self.pellets.remove((x, y))
            result['pellet'] = True
        elif (x, y) in self.power_pellets:
            self.power_pellets.remove((x, y))
            result['power_pellet'] = True
            
        return result
    
    def is_empty(self, x: int, y: int) -> bool:
        """Check if a tile is empty (not a wall)"""
        return not self.is_wall(x, y)
    
    def get_all_pellets_count(self) -> int:
        """Get total number of pellets and power pellets remaining"""
        return len(self.pellets) + len(self.power_pellets)