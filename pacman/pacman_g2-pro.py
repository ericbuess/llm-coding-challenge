import pygame
import random

# --- Constants ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
TILE_SIZE = 30
PACMAN_SPEED = 3
GHOST_SPEED = 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0,255,0)

# --- Maze Representation ---
MAZE = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#o####.#####.##.#####.####o#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.#####.##.#####.######",
    "######.#####.##.#####.######",
    "######.##..........##.######",
    "######.##.###  ###.##.######",
    "######.##.#      #.##.######",
    "      ....#      #....      ",
    "######.##.#      #.##.######",
    "######.##.########.##.######",
    "######.##..........##.######",
    "######.##.########.##.######",
    "######.##.########.##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#o####.#####.##.#####.####o#",
    "#...##................##...#",
    "###.##.##.########.##.##.###",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#..........................#",
    "############################",
]


# --- Player Class ---
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0
        self.speed_y = 0

    def update(self, walls):
        # Store the old position
        old_x = self.rect.x
        old_y = self.rect.y

        # Update position based on speed
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Check for collisions with walls
        collisions = pygame.sprite.spritecollide(self, walls, False)
        if collisions:
            # "Sticky Walls" Logic
            for wall in collisions:
                # Moving Right
                if self.speed_x > 0:
                    self.rect.right = wall.rect.left
                # Moving Left
                elif self.speed_x < 0:
                    self.rect.left = wall.rect.right
                # Moving Down
                elif self.speed_y > 0:
                    self.rect.bottom = wall.rect.top
                # Moving Up
                elif self.speed_y < 0:
                    self.rect.top = wall.rect.bottom

        # Wrap-around logic
        if self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT

    def change_speed(self, x, y):
        self.speed_x = x
        self.speed_y = y

# --- Ghost Class ---
class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, color, change_time=400):
        super().__init__()
        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0
        self.speed_y = 0
        self.change_time = change_time # how often ghost changes direction
        self.timer = 0
        self.directions = [
            (GHOST_SPEED, 0),  # Right
            (-GHOST_SPEED, 0), # Left
            (0, GHOST_SPEED),  # Down
            (0, -GHOST_SPEED), # Up
        ]
        self.current_direction = random.choice(self.directions)

    def update(self, walls):
        self.timer += 1
        if self.timer > self.change_time:
            self.timer = 0
            #find valid directions
            valid_directions = []
            for direction in self.directions:
                old_x = self.rect.x
                old_y = self.rect.y
                self.rect.x += direction[0]
                self.rect.y += direction[1]
                if not pygame.sprite.spritecollideany(self, walls):
                    valid_directions.append(direction)
                self.rect.x = old_x
                self.rect.y = old_y

            #choose one of them
            if len(valid_directions) > 0:
                # Bias against reversing direction
                reverse_direction = (-self.current_direction[0], -self.current_direction[1])
                if reverse_direction in valid_directions and len(valid_directions) > 1:
                    valid_directions.remove(reverse_direction)

                self.current_direction = random.choice(valid_directions)
            else:
                #if no valid direction, reverse
                self.current_direction = (-self.current_direction[0], -self.current_direction[1])

        # Move the ghost
        self.rect.x += self.current_direction[0]
        self.rect.y += self.current_direction[1]

        # Check for collisions
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.x -= self.current_direction[0]
            self.rect.y -= self.current_direction[1]
            self.current_direction = random.choice(self.directions)

# --- Pellet Class ---
class Pellet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([TILE_SIZE // 4, TILE_SIZE // 4])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x + TILE_SIZE // 2, y + TILE_SIZE // 2)  # Center the pellet

# --- PowerPellet Class ---
class PowerPellet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([TILE_SIZE // 2, TILE_SIZE // 2])  # Larger than regular pellets
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x + TILE_SIZE // 2, y + TILE_SIZE // 2)

# --- Wall Class ---
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# --- Game Class ---
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.pellets = pygame.sprite.Group()
        self.power_pellets = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()
        self.player = None  # Initialize player to None
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.game_state = "start" # start, playing, game_over
        self.load_maze()


    def load_maze(self):
        for row_index, row in enumerate(MAZE):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if cell == '#':
                    wall = Wall(x, y)
                    self.all_sprites.add(wall)
                    self.walls.add(wall)
                elif cell == '.':
                    pellet = Pellet(x, y)
                    self.all_sprites.add(pellet)
                    self.pellets.add(pellet)
                elif cell == 'o':
                    power_pellet = PowerPellet(x,y)
                    self.all_sprites.add(power_pellet)
                    self.power_pellets.add(power_pellet)
                elif cell == 'P':
                    self.player = Player(x, y)
                    self.all_sprites.add(self.player)
                elif cell == 'G':
                    ghost = Ghost(x, y, random.choice([RED, GREEN]))
                    self.all_sprites.add(ghost)
                    self.ghosts.add(ghost)

    def run(self):
        while self.running:
            self.handle_events()
            if self.game_state == "playing":
                self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.game_state == "start":
                    self.game_state = "playing"
                elif self.game_state == "playing":
                    if self.player is not None:
                        if event.key == pygame.K_LEFT:
                            self.player.change_speed(-PACMAN_SPEED, 0)
                        elif event.key == pygame.K_RIGHT:
                            self.player.change_speed(PACMAN_SPEED, 0)
                        elif event.key == pygame.K_UP:
                            self.player.change_speed(0, -PACMAN_SPEED)
                        elif event.key == pygame.K_DOWN:
                            self.player.change_speed(0, PACMAN_SPEED)
                elif self.game_state == "game_over":
                    if event.key == pygame.K_r:
                        self.restart()


    def update(self):
        if self.player is None:
            return

        self.all_sprites.update(self.walls)

        # Check for collisions with pellets
        pellet_hit = pygame.sprite.spritecollideany(self.player, self.pellets)
        if pellet_hit:
            pellet_hit.kill()  # Remove the pellet
            self.score += 10

        # Check for collisions with power pellets
        power_pellet_hit = pygame.sprite.spritecollideany(self.player, self.power_pellets)
        if power_pellet_hit:
            power_pellet_hit.kill()
            self.score += 50
            #TODO add ghost eating

        # Check for collisions with ghosts
        if pygame.sprite.spritecollideany(self.player, self.ghosts):
            self.game_state = "game_over"

        # Check win condition - Moved here
        if len(self.pellets) == 0 and len(self.power_pellets) == 0:
            self.game_state = "game_over" #could be a win state

    def draw(self):
        self.screen.fill(BLACK)

        if self.game_state == "start":
            text = self.font.render("Press any key to start", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
        elif self.game_state == "playing" or self.game_state == "game_over":
            self.all_sprites.draw(self.screen)

            # Display score
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (10, 10))

            if self.game_state == "game_over":
                text = self.font.render("Game Over - Press R to restart", True, WHITE)
                text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                self.screen.blit(text,text_rect)


        pygame.display.flip()

    def restart(self):
        #reset all variables
        self.all_sprites.empty()
        self.walls.empty()
        self.pellets.empty()
        self.power_pellets.empty()
        self.ghosts.empty()
        self.player = None
        self.score = 0
        self.game_state = "start"
        self.load_maze()

# --- Main ---
if __name__ == "__main__":
    game = Game()
    game.run()
