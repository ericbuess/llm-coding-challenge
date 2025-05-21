import pygame
import sys
import random
from enum import Enum
from typing import List, Tuple

class GameState(Enum):
    START = 1
    PLAYING = 2
    GAME_OVER = 3
    WIN = 4

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

CELL_SIZE = 20

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Maze:
    def __init__(self):
        self.layout = [
            "############################",
            "#............##............#",
            "#.####.#####.##.#####.####.#",
            "#o####.#####.##.#####.####o#",
            "#..........................#",
            "#.####.##.########.##.####.#",
            "#......##....##....##......#",
            "######.#####.##.#####.######",
            "     #.#####.##.#####.#     ",
            "     #.##..........##.#     ",
            "     #.##.###  ###.##.#     ",
            "######.##.#      #.##.######",
            "      ...#        #...      ",
            "######.##.#      #.##.######",
            "     #.##.########.##.#     ",
            "     #.##..........##.#     ",
            "     #.##.########.##.#     ",
            "######.##.########.##.######",
            "#............##............#",
            "#.####.#####.##.#####.####.#",
            "#o..##.......  .......##..o#",
            "###.##.##.########.##.##.###",
            "#......##....##....##......#",
            "#.##########.##.##########.#",
            "#..........................#",
            "############################"
        ]
        self.rows = len(self.layout)
        self.cols = len(self.layout[0])
        
    def get_cell(self, x: int, y: int) -> str:
        if 0 <= y < self.rows and 0 <= x < self.cols:
            return self.layout[y][x]
        return '#'
        
    def is_wall(self, x: int, y: int) -> bool:
        return self.get_cell(x, y) == '#'
        
    def is_pellet(self, x: int, y: int) -> bool:
        return self.get_cell(x, y) == '.'
        
    def is_power_pellet(self, x: int, y: int) -> bool:
        return self.get_cell(x, y) == 'o'
        
    def remove_pellet(self, x: int, y: int):
        if 0 <= y < self.rows and 0 <= x < self.cols:
            row = list(self.layout[y])
            row[x] = ' '
            self.layout[y] = ''.join(row)
            
    def draw(self, screen):
        for y in range(self.rows):
            for x in range(self.cols):
                cell = self.get_cell(x, y)
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                if cell == '#':
                    pygame.draw.rect(screen, BLUE, rect)
                elif cell == '.':
                    pygame.draw.circle(screen, WHITE, rect.center, 2)
                elif cell == 'o':
                    pygame.draw.circle(screen, WHITE, rect.center, 6)

class PacMan:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.speed = 0.1
        self.move_timer = 0
        
    def update(self, maze: Maze):
        self.move_timer += self.speed
        if self.move_timer >= 1.0:
            self.move_timer = 0
            
            next_x = self.x + self.next_direction.value[0]
            next_y = self.y + self.next_direction.value[1]
            
            if not maze.is_wall(next_x, next_y):
                self.direction = self.next_direction
                self.x = next_x
                self.y = next_y
            
            self.x = max(0, min(self.x, maze.cols - 1))
            self.y = max(0, min(self.y, maze.rows - 1))
    
    def set_direction(self, direction: Direction):
        self.next_direction = direction
        
    def draw(self, screen):
        center_x = self.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.y * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, YELLOW, (center_x, center_y), CELL_SIZE // 2 - 2)

class Ghost:
    def __init__(self, x: int, y: int, color: tuple):
        self.x = x
        self.y = y
        self.color = color
        self.direction = Direction.UP
        self.speed = 0.08
        self.move_timer = 0
        
    def update(self, maze: Maze):
        self.move_timer += self.speed
        if self.move_timer >= 1.0:
            self.move_timer = 0
            
            possible_directions = []
            for direction in Direction:
                next_x = self.x + direction.value[0]
                next_y = self.y + direction.value[1]
                if not maze.is_wall(next_x, next_y):
                    possible_directions.append(direction)
            
            if possible_directions:
                self.direction = random.choice(possible_directions)
                self.x += self.direction.value[0]
                self.y += self.direction.value[1]
            
            self.x = max(0, min(self.x, maze.cols - 1))
            self.y = max(0, min(self.y, maze.rows - 1))
    
    def draw(self, screen):
        center_x = self.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.y * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, self.color, (center_x, center_y), CELL_SIZE // 2 - 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.running = True
        self.maze = Maze()
        self.pacman = PacMan(13, 20)
        self.ghosts = [
            Ghost(13, 10, RED),
            Ghost(14, 10, PINK),
            Ghost(12, 10, CYAN),
            Ghost(15, 10, ORANGE)
        ]
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.state = GameState.START
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.state == GameState.START:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.PLAYING
                elif self.state == GameState.PLAYING:
                    if event.key == pygame.K_UP:
                        self.pacman.set_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        self.pacman.set_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.pacman.set_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.pacman.set_direction(Direction.RIGHT)
                elif self.state == GameState.GAME_OVER or self.state == GameState.WIN:
                    if event.key == pygame.K_SPACE:
                        self.__init__()
                
    def update(self):
        if self.state == GameState.PLAYING:
            self.pacman.update(self.maze)
            
            for ghost in self.ghosts:
                ghost.update(self.maze)
            
            if self.maze.is_pellet(self.pacman.x, self.pacman.y):
                self.maze.remove_pellet(self.pacman.x, self.pacman.y)
                self.score += 10
            elif self.maze.is_power_pellet(self.pacman.x, self.pacman.y):
                self.maze.remove_pellet(self.pacman.x, self.pacman.y)
                self.score += 50
                
            for ghost in self.ghosts:
                if self.pacman.x == ghost.x and self.pacman.y == ghost.y:
                    self.state = GameState.GAME_OVER
                    
            pellets_remaining = sum(row.count('.') + row.count('o') for row in self.maze.layout)
            if pellets_remaining == 0:
                self.state = GameState.WIN
        
    def render(self):
        self.screen.fill(BLACK)
        
        if self.state == GameState.START:
            title_text = self.font.render("PAC-MAN", True, YELLOW)
            start_text = self.font.render("Press SPACE to start", True, WHITE)
            title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
            start_rect = start_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
            self.screen.blit(title_text, title_rect)
            self.screen.blit(start_text, start_rect)
            
        elif self.state == GameState.PLAYING:
            self.maze.draw(self.screen)
            self.pacman.draw(self.screen)
            
            for ghost in self.ghosts:
                ghost.draw(self.screen)
            
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (10, 10))
            
        elif self.state == GameState.GAME_OVER:
            game_over_text = self.font.render("GAME OVER", True, RED)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = self.font.render("Press SPACE to restart", True, WHITE)
            
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(restart_text, restart_rect)
            
        elif self.state == GameState.WIN:
            win_text = self.font.render("YOU WIN!", True, YELLOW)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = self.font.render("Press SPACE to restart", True, WHITE)
            
            win_rect = win_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
            
            self.screen.blit(win_text, win_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()