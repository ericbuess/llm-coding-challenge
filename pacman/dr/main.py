import pygame, sys
from settings import WIDTH, HEIGHT, FPS
from maze import Maze
from pacman import PacMan
from ghost import Ghost

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man")
    clock = pygame.time.Clock()

    # Create maze (walls, pellets, power pellets)
    maze = Maze()

    # Create Pac-Man at a starting position (center of screen here).
    pacman = PacMan(x=WIDTH//2, y=HEIGHT//2, speed=4)
    pacman_group = pygame.sprite.GroupSingle(pacman)

    # Create ghosts (here we add two; you can add more for variety).
    ghost_group = pygame.sprite.Group()
    ghost1 = Ghost(x=WIDTH//2 - 50, y=HEIGHT//2, speed=3, color=(255, 0, 0))  # Red ghost
    ghost2 = Ghost(x=WIDTH//2 + 50, y=HEIGHT//2, speed=3, color=(255, 105, 180))  # Pink ghost
    ghost_group.add(ghost1, ghost2)

    # Set up score and font.
    score = 0
    font = pygame.font.SysFont("arial", 24)

    # Load sound effects (ensure these files exist in your project directory).
    try:
        eat_sound = pygame.mixer.Sound("eat.wav")
        power_sound = pygame.mixer.Sound("power.wav")
        death_sound = pygame.mixer.Sound("death.wav")
        ghost_eat_sound = pygame.mixer.Sound("ghost_eat.wav")
    except Exception as e:
        print("Sound files not found or error loading sounds:", e)
        eat_sound = power_sound = death_sound = ghost_eat_sound = None

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Update intended direction based on key presses.
                if event.key == pygame.K_LEFT:
                    pacman.next_direction = pygame.math.Vector2(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    pacman.next_direction = pygame.math.Vector2(1, 0)
                elif event.key == pygame.K_UP:
                    pacman.next_direction = pygame.math.Vector2(0, -1)
                elif event.key == pygame.K_DOWN:
                    pacman.next_direction = pygame.math.Vector2(0, 1)

        # Update Pac-Man.
        pacman_group.update(maze.wall_group)

        # Check collisions with pellets.
        pellets_eaten = pygame.sprite.spritecollide(pacman, maze.pellet_group, True)
        if pellets_eaten:
            score += 10 * len(pellets_eaten)
            if eat_sound:
                eat_sound.play()

        # Check collisions with power pellets.
        power_eaten = pygame.sprite.spritecollide(pacman, maze.power_pellet_group, True)
        if power_eaten:
            score += 50 * len(power_eaten)
            # Activate power mode: make ghosts vulnerable for 10 seconds.
            power_timer = FPS * 10  # 10 seconds
            for ghost in ghost_group:
                ghost.set_vulnerable(power_timer)
            if power_sound:
                power_sound.play()

        # Update ghosts (each ghost’s AI will chase or move randomly).
        for ghost in ghost_group:
            ghost.update(maze.wall_group, pacman)

        # Check collisions between Pac-Man and any ghost.
        collided_ghost = pygame.sprite.spritecollideany(pacman, ghost_group)
        if collided_ghost:
            if collided_ghost.vulnerable:
                # Eat ghost: award points and reset ghost position.
                score += 200
                if ghost_eat_sound:
                    ghost_eat_sound.play()
                collided_ghost.rect.center = (WIDTH//2, HEIGHT//2 - 50)
                collided_ghost.vulnerable = False
            else:
                # Pac-Man dies (game over).
                if death_sound:
                    death_sound.play()
                running = False

        # Draw everything.
        screen.fill((0, 0, 0))
        maze.draw(screen)
        pacman_group.draw(screen)
        ghost_group.draw(screen)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, HEIGHT - 30))
        pygame.display.flip()

    game_over(screen, score)
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()

def game_over(screen, score):
    font_big = pygame.font.SysFont("arial", 48)
    font_small = pygame.font.SysFont("arial", 24)
    text = font_big.render("GAME OVER", True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, text_rect)
    score_text = font_small.render(f"Final Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    screen.blit(score_text, score_rect)
    pygame.display.flip()

if __name__ == "__main__":
    main()
