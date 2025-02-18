import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman

def load_maze(filename):
    with open(filename, 'r') as f:
        return [list(line.strip()) for line in f]

def draw_maze(screen, maze):
    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            if tile == '1':
                pygame.draw.rect(screen, BLUE, 
                               (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile == '.':
                pygame.draw.circle(screen, WHITE,
                                 (x*TILE_SIZE + TILE_SIZE//2, y*TILE_SIZE + TILE_SIZE//2), 2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pac-Man")
    clock = pygame.time.Clock()
    
    maze = load_maze(MAZE_FILE)
    pacman = Pacman(TILE_SIZE * 14, TILE_SIZE * 23)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    pacman.direction = (-1, 0)
                elif event.key == K_RIGHT:
                    pacman.direction = (1, 0)
                elif event.key == K_UP:
                    pacman.direction = (0, -1)
                elif event.key == K_DOWN:
                    pacman.direction = (0, 1)
        
        pacman.update(maze)
        screen.fill(BLACK)
        draw_maze(screen, maze)
        pacman.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main() 