import pygame
from constants import *
from entities import Pacman, Ghost, Pellet

class Game:
    def __init__(self):
        self.state = STATE_MENU
        self.maze = [list(row) for row in MAZE]
        self.pacman = None
        self.ghosts = []
        self.pellets = []
        self.score = 0
        self.lives = LIVES
        self.level = 1
        self.font = None
        
    def start_game(self):
        self.state = STATE_PLAYING
        self.score = 0
        self.lives = LIVES
        self.level = 1
        self.init_level()
        
    def init_level(self):
        self.maze = [list(row) for row in MAZE]
        self.ghosts = []
        self.pellets = []
        
        # Find Pacman start position and create entities
        pacman_placed = False
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                cell = self.maze[y][x]
                pixel_x = x * TILE_SIZE
                pixel_y = y * TILE_SIZE
                
                if cell == ' ' and not pacman_placed and y > MAZE_HEIGHT // 2:
                    # Empty space - place Pacman here if not already placed
                    self.pacman = Pacman(pixel_x, pixel_y)
                    pacman_placed = True
                elif cell == '.':
                    # Regular pellet
                    self.pellets.append(Pellet(pixel_x, pixel_y))
                elif cell == 'o':
                    # Power pellet
                    self.pellets.append(Pellet(pixel_x, pixel_y, is_power=True))
                elif cell == 'G':
                    # Ghost house - place ghosts
                    if len(self.ghosts) == 0:
                        self.ghosts.append(Ghost(pixel_x, pixel_y, RED, "Blinky"))
                    elif len(self.ghosts) == 1:
                        self.ghosts.append(Ghost(pixel_x, pixel_y, PINK, "Pinky"))
                    elif len(self.ghosts) == 2:
                        self.ghosts.append(Ghost(pixel_x, pixel_y, CYAN, "Inky"))
                    elif len(self.ghosts) == 3:
                        self.ghosts.append(Ghost(pixel_x, pixel_y, ORANGE, "Clyde"))
                        
        # Set scatter targets for ghosts
        if len(self.ghosts) >= 4:
            self.ghosts[0].scatter_target = (MAZE_WIDTH - 1, 0)  # Blinky - top right
            self.ghosts[1].scatter_target = (0, 0)  # Pinky - top left
            self.ghosts[2].scatter_target = (MAZE_WIDTH - 1, MAZE_HEIGHT - 1)  # Inky - bottom right
            self.ghosts[3].scatter_target = (0, MAZE_HEIGHT - 1)  # Clyde - bottom left
            
        # Set Pacman lives
        if self.pacman:
            self.pacman.lives = self.lives
            
    def update(self):
        if self.state != STATE_PLAYING:
            return
            
        # Update Pacman
        if self.pacman:
            self.pacman.update(self.maze)
            
            # Check pellet collision
            for pellet in self.pellets:
                if not pellet.eaten:
                    if (abs(self.pacman.x - pellet.x) < TILE_SIZE // 2 and
                        abs(self.pacman.y - pellet.y) < TILE_SIZE // 2):
                        pellet.eaten = True
                        if pellet.is_power:
                            self.score += POWER_PELLET_SCORE
                            # Make all ghosts frightened
                            for ghost in self.ghosts:
                                ghost.make_frightened()
                        else:
                            self.score += PELLET_SCORE
                            
            # Check if all pellets eaten
            if all(pellet.eaten for pellet in self.pellets):
                self.level += 1
                self.state = STATE_LEVEL_COMPLETE
                
        # Update ghosts
        blinky = self.ghosts[0] if len(self.ghosts) > 0 else None
        for ghost in self.ghosts:
            ghost.update(self.pacman, self.maze, blinky)
            
            # Check collision with Pacman
            if self.pacman and not ghost.in_house:
                if (abs(ghost.x - self.pacman.x) < TILE_SIZE - 4 and
                    abs(ghost.y - self.pacman.y) < TILE_SIZE - 4):
                    if ghost.state == FRIGHTENED:
                        # Eat ghost
                        ghost.state = EATEN
                        ghost.speed = GHOST_SPEED * 2
                        self.score += GHOST_SCORE
                    elif ghost.state != EATEN:
                        # Pacman dies
                        self.lives -= 1
                        if self.lives <= 0:
                            self.state = STATE_GAME_OVER
                        else:
                            # Reset positions
                            self.reset_positions()
                            
    def reset_positions(self):
        # Reset Pacman position
        if self.pacman:
            for y in range(MAZE_HEIGHT):
                for x in range(MAZE_WIDTH):
                    if self.maze[y][x] == ' ':
                        self.pacman.x = x * TILE_SIZE
                        self.pacman.y = y * TILE_SIZE
                        self.pacman.direction = None
                        self.pacman.next_direction = None
                        return
                        
    def handle_input(self, key):
        if self.state == STATE_MENU:
            if key == pygame.K_SPACE:
                self.start_game()
        elif self.state == STATE_PLAYING:
            if self.pacman:
                if key == pygame.K_UP:
                    self.pacman.next_direction = UP
                elif key == pygame.K_DOWN:
                    self.pacman.next_direction = DOWN
                elif key == pygame.K_LEFT:
                    self.pacman.next_direction = LEFT
                elif key == pygame.K_RIGHT:
                    self.pacman.next_direction = RIGHT
        elif self.state == STATE_GAME_OVER:
            if key == pygame.K_SPACE:
                self.state = STATE_MENU
        elif self.state == STATE_LEVEL_COMPLETE:
            if key == pygame.K_SPACE:
                self.init_level()
                self.state = STATE_PLAYING
                
    def draw(self, screen):
        screen.fill(BLACK)
        
        if self.state == STATE_MENU:
            self.draw_menu(screen)
        elif self.state == STATE_PLAYING:
            self.draw_game(screen)
        elif self.state == STATE_GAME_OVER:
            self.draw_game_over(screen)
        elif self.state == STATE_LEVEL_COMPLETE:
            self.draw_level_complete(screen)
            
    def draw_game(self, screen):
        # Draw maze
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                cell = self.maze[y][x]
                if cell == '#':
                    pygame.draw.rect(screen, DARK_BLUE,
                                   (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif cell == '-':
                    # Ghost house door
                    pygame.draw.rect(screen, PINK,
                                   (x * TILE_SIZE, y * TILE_SIZE + TILE_SIZE // 2 - 2, TILE_SIZE, 4))
                    
        # Draw pellets
        for pellet in self.pellets:
            pellet.draw(screen)
            
        # Draw ghosts
        for ghost in self.ghosts:
            ghost.draw(screen)
            
        # Draw Pacman
        if self.pacman:
            self.pacman.draw(screen)
            
        # Draw UI
        self.draw_ui(screen)
        
    def draw_ui(self, screen):
        if self.font:
            # Score
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            screen.blit(score_text, (10, SCREEN_HEIGHT - 30))
            
            # Lives
            lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
            screen.blit(lives_text, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 30))
            
            # Level
            level_text = self.font.render(f"Level: {self.level}", True, WHITE)
            screen.blit(level_text, (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT - 30))
            
    def draw_menu(self, screen):
        if self.font:
            title = self.font.render("PACMAN", True, YELLOW)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            screen.blit(title, title_rect)
            
            start = self.font.render("Press SPACE to Start", True, WHITE)
            start_rect = start.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(start, start_rect)
            
            controls = self.font.render("Use Arrow Keys to Move", True, WHITE)
            controls_rect = controls.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
            screen.blit(controls, controls_rect)
            
    def draw_game_over(self, screen):
        self.draw_game(screen)
        
        if self.font:
            # Overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            game_over = self.font.render("GAME OVER", True, RED)
            game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over, game_over_rect)
            
            final_score = self.font.render(f"Final Score: {self.score}", True, WHITE)
            score_rect = final_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            screen.blit(final_score, score_rect)
            
            restart = self.font.render("Press SPACE to Return to Menu", True, WHITE)
            restart_rect = restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
            screen.blit(restart, restart_rect)
            
    def draw_level_complete(self, screen):
        self.draw_game(screen)
        
        if self.font:
            # Overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            complete = self.font.render(f"Level {self.level - 1} Complete!", True, YELLOW)
            complete_rect = complete.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(complete, complete_rect)
            
            next_level = self.font.render("Press SPACE to Continue", True, WHITE)
            next_rect = next_level.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            screen.blit(next_level, next_rect)